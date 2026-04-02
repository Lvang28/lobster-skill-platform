"""
龙虾 Skill 合集平台 - 业务逻辑服务层
"""
import os
import json
import shutil
import zipfile
import hashlib
from datetime import datetime, timedelta
from sqlalchemy import and_, or_, desc, func
from models import User, Skill, DownloadHistory, UsageRecord, PointsHistory, UserPreference, Recommendation
from config import POINTS_CONFIG, RECOMMENDATION_CONFIG, SKILLS_DIR


class UserService:
    """用户服务"""
    
    def __init__(self, session):
        self.session = session
    
    def get_or_create_user(self, username, email=None):
        user = self.session.query(User).filter_by(username=username).first()
        if not user:
            user = User(username=username, email=email)
            self.session.add(user)
            self.session.commit()
        return user
    
    def add_points(self, user_id, points, reason, skill_id=None):
        user = self.session.query(User).get(user_id)
        if user:
            user.total_points += points
            history = PointsHistory(
                user_id=user_id,
                points=points,
                reason=reason,
                skill_id=skill_id
            )
            self.session.add(history)
            self.session.commit()
            return user.total_points
        return None
    
    def get_user_stats(self, user_id):
        """获取用户详细统计信息（包含上传和下载的技能列表）"""
        user = self.session.query(User).get(user_id)
        if not user:
            return None
        
        # 下载次数
        downloaded_count = self.session.query(DownloadHistory).filter_by(user_id=user_id).count()
        # 使用次数
        used_count = self.session.query(UsageRecord).filter_by(user_id=user_id).count()
        # 上传数量
        uploaded_count = len(user.uploaded_skills)
        
        # 获取用户上传的技能列表及收益
        uploaded_skills_detail = []
        for skill in user.uploaded_skills:
            earnings = skill.download_count * POINTS_CONFIG['skill_downloaded'] + \
                      skill.use_count * POINTS_CONFIG['skill_used']
            uploaded_skills_detail.append({
                'id': skill.id,
                'name': skill.name,
                'download_count': skill.download_count,
                'use_count': skill.use_count,
                'earnings': earnings,
                'created_at': skill.created_at.isoformat() if skill.created_at else None
            })
        
        # 获取用户下载的技能列表
        download_history = self.session.query(DownloadHistory).filter_by(
            user_id=user_id
        ).order_by(desc(DownloadHistory.downloaded_at)).limit(20).all()
        
        downloaded_skills_detail = []
        for record in download_history:
            skill = self.session.query(Skill).get(record.skill_id)
            if skill:
                downloaded_skills_detail.append({
                    'id': skill.id,
                    'name': skill.name,
                    'downloaded_at': record.downloaded_at.isoformat() if record.downloaded_at else None
                })
        
        # 计算理论积分（用于验证）
        calculated_points = (
            uploaded_count * POINTS_CONFIG['upload_skill'] +
            sum(s['earnings'] for s in uploaded_skills_detail) +
            downloaded_count * POINTS_CONFIG['download_skill']
        )
        
        return {
            'user': user.to_dict(),
            'downloaded_count': downloaded_count,
            'used_count': used_count,
            'uploaded_count': uploaded_count,
            'uploaded_skills': uploaded_skills_detail,
            'downloaded_skills': downloaded_skills_detail,
            'calculated_points': calculated_points,
            'actual_points': user.total_points,
            'points_match': calculated_points == user.total_points
        }


class SkillService:
    """Skill 服务"""
    
    def __init__(self, session):
        self.session = session
    
    def upload_skill(self, name, description, file_path, uploader_id, 
                     category=None, tags=None, author=None, metadata=None):
        # 计算文件信息
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        
        # 生成唯一文件名
        file_hash = hashlib.md5(f"{name}{datetime.now()}".encode()).hexdigest()[:8]
        dest_path = os.path.join(SKILLS_DIR, f"{file_hash}_{os.path.basename(file_path)}")
        
        # 复制文件
        if os.path.exists(file_path):
            shutil.copy2(file_path, dest_path)
        
        # 创建记录
        skill = Skill(
            name=name,
            description=description,
            file_path=dest_path,
            uploader_id=uploader_id,
            category=category,
            tags=tags or [],
            author=author,
            file_size=file_size,
            metadata=metadata
        )
        
        self.session.add(skill)
        self.session.commit()
        
        # 给上传者加分
        user_service = UserService(self.session)
        user_service.add_points(uploader_id, POINTS_CONFIG['upload_skill'], 
                               f"上传 skill: {name}", skill.id)
        
        return skill
    
    def download_skill(self, skill_id, user_id):
        skill = self.session.query(Skill).get(skill_id)
        if not skill or not skill.is_active:
            return None
        
        # 增加下载次数
        skill.download_count += 1
        
        # 记录下载历史
        history = DownloadHistory(user_id=user_id, skill_id=skill_id)
        self.session.add(history)
        
        # 给下载者加分
        user_service = UserService(self.session)
        user_service.add_points(user_id, POINTS_CONFIG['download_skill'], 
                               f"下载 skill: {skill.name}", skill_id)
        
        # 给上传者加分
        if skill.uploader_id != user_id:
            user_service.add_points(skill.uploader_id, POINTS_CONFIG['skill_downloaded'],
                                   f"skill 被下载：{skill.name}", skill_id)
        
        self.session.commit()
        return skill.file_path
    
    def record_usage(self, skill_id, user_id, duration=0, success=True):
        record = UsageRecord(
            skill_id=skill_id,
            user_id=user_id,
            duration=duration,
            success=success
        )
        self.session.add(record)
        
        # 更新使用次数
        skill = self.session.query(Skill).get(skill_id)
        if skill:
            skill.use_count += 1
            
            # 给上传者加分
            if skill.uploader_id != user_id:
                user_service = UserService(self.session)
                user_service.add_points(skill.uploader_id, POINTS_CONFIG['skill_used'],
                                       f"skill 被使用：{skill.name}", skill_id)
        
        self.session.commit()
        return record
    
    def search_skills(self, query=None, category=None, tags=None, sort_by='created_at'):
        # 不过滤 is_active，显示所有技能（包括未设置的）
        skills_query = self.session.query(Skill)
        
        if query:
            skills_query = skills_query.filter(
                or_(
                    Skill.name.contains(query),
                    Skill.description.contains(query),
                    Skill.author.contains(query)
                )
            )
        
        if category:
            skills_query = skills_query.filter_by(category=category)
        
        if tags:
            skills_query = skills_query.filter(
                Skill.tags.contains(json.dumps([tags]) if isinstance(tags, str) else tags)
            )
        
        # 排序
        sort_columns = {
            'created_at': Skill.created_at,
            'download_count': Skill.download_count,
            'use_count': Skill.use_count,
            'rating': Skill.rating,
            'name': Skill.name
        }
        
        sort_column = sort_columns.get(sort_by, Skill.created_at)
        skills_query = skills_query.order_by(desc(sort_column))
        
        return skills_query.all()
    
    def get_skill(self, skill_id):
        return self.session.query(Skill).get(skill_id)
    
    def get_categories(self):
        categories = self.session.query(Skill.category).filter(
            Skill.category.isnot(None)
        ).distinct().all()
        return [c[0] for c in categories if c[0]]


class RecommendationService:
    """推荐服务"""
    
    def __init__(self, session):
        self.session = session
    
    def analyze_user_preference(self, user_id):
        """分析用户偏好"""
        user = self.session.query(User).get(user_id)
        if not user:
            return None
        
        # 获取最近的使用记录
        days_ago = datetime.now() - timedelta(days=RECOMMENDATION_CONFIG['history_days'])
        recent_usage = self.session.query(UsageRecord).filter(
            and_(
                UsageRecord.user_id == user_id,
                UsageRecord.used_at >= days_ago
            )
        ).all()
        
        # 统计类别和标签权重
        category_weights = {}
        tag_weights = {}
        recent_skill_ids = []
        
        for record in recent_usage:
            skill = self.session.query(Skill).get(record.skill_id)
            if skill:
                recent_skill_ids.append(skill.id)
                
                # 类别权重
                if skill.category:
                    category_weights[skill.category] = category_weights.get(skill.category, 0) + 1
                
                # 标签权重
                if skill.tags:
                    for tag in skill.tags:
                        tag_weights[tag] = tag_weights.get(tag, 0) + 1
        
        # 归一化权重
        total = sum(category_weights.values()) or 1
        category_weights = {k: v/total for k, v in category_weights.items()}
        
        total = sum(tag_weights.values()) or 1
        tag_weights = {k: v/total for k, v in tag_weights.items()}
        
        # 保存或更新偏好
        preference = self.session.query(UserPreference).filter_by(user_id=user_id).first()
        if preference:
            preference.category_weights = category_weights
            preference.tag_weights = tag_weights
            preference.recent_skills = recent_skill_ids[-20:]  # 保留最近 20 个
            preference.last_updated = datetime.now()
        else:
            preference = UserPreference(
                user_id=user_id,
                category_weights=category_weights,
                tag_weights=tag_weights,
                recent_skills=recent_skill_ids[-20:]
            )
            self.session.add(preference)
        
        self.session.commit()
        return preference
    
    def generate_daily_recommendations(self, user_id):
        """生成每日推荐"""
        # 先分析用户偏好
        preference = self.analyze_user_preference(user_id)
        
        if not preference or not (preference.category_weights or preference.tag_weights):
            # 冷启动：推荐热门技能
            skills = self.session.query(Skill).filter_by(is_active=True).order_by(
                desc(Skill.download_count)
            ).limit(RECOMMENDATION_CONFIG['daily_count'] * 2).all()
        else:
            # 基于偏好推荐
            skills = self.session.query(Skill).filter_by(is_active=True).all()
            
            # 计算每个技能的匹配度
            scored_skills = []
            for skill in skills:
                score = 0
                
                # 排除已使用的技能
                if preference.recent_skills and skill.id in preference.recent_skills:
                    continue
                
                # 类别匹配
                if skill.category and preference.category_weights:
                    score += preference.category_weights.get(skill.category, 0) * 10
                
                # 标签匹配
                if skill.tags and preference.tag_weights:
                    for tag in skill.tags:
                        score += preference.tag_weights.get(tag, 0) * 5
                
                # 热度加成
                score += min(skill.download_count / 100, 2)
                
                scored_skills.append((score, skill))
            
            # 按分数排序
            scored_skills.sort(key=lambda x: x[0], reverse=True)
            skills = [s[1] for s in scored_skills]
        
        # 选择推荐数量
        recommended = skills[:RECOMMENDATION_CONFIG['daily_count']]
        
        # 保存推荐记录
        if recommended:
            rec = Recommendation(
                user_id=user_id,
                skill_ids=[s.id for s in recommended]
            )
            self.session.add(rec)
            self.session.commit()
        
        return recommended
    
    def accept_recommendation(self, user_id, skill_id):
        """用户接受了推荐"""
        rec = self.session.query(Recommendation).filter_by(
            user_id=user_id,
            accepted_skill_id=None
        ).order_by(desc(Recommendation.date)).first()
        
        if rec and skill_id in rec.skill_ids:
            rec.accepted_skill_id = skill_id
            self.session.commit()
            
            # 给上传者加分
            skill = self.session.query(Skill).get(skill_id)
            if skill:
                user_service = UserService(self.session)
                user_service.add_points(skill.uploader_id, 
                                       POINTS_CONFIG['daily_recommendation'],
                                       f"推荐被采纳：{skill.name}", skill_id)
