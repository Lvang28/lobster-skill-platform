"""
龙虾 Skill 合集平台 - 网络热门技能自动抓取器
每天自动从 GitHub、Gitee 等平台抓取热门技能
"""
import os
import json
import requests
from datetime import datetime, timedelta
from models import init_db, User, Skill
from config import DATABASE_URL, SKILLS_DIR
from services import SkillService
import tempfile


class HotSkillCrawler:
    """热门技能抓取器"""
    
    def __init__(self):
        self.session = init_db(DATABASE_URL)
        self.skill_service = SkillService(self.session)
        
        # 获取系统用户（用于归属抓取的技能）
        system_user = self.session.query(User).filter_by(username='系统自动').first()
        if not system_user:
            system_user = User(username='系统自动', email='system@lobster.com')
            self.session.add(system_user)
            self.session.commit()
        self.system_user = system_user
    
    def fetch_github_trending(self, language='Python', since='daily'):
        """从 GitHub Trending 抓取热门项目"""
        url = f"https://api.github.com/search/repositories"
        params = {
            'q': f'language:{language} stars:>100',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            skills = []
            for repo in data.get('items', [])[:5]:
                skill_data = {
                    'name': repo['name'].replace('-', ' ').title(),
                    'description': repo['description'] or 'GitHub 热门项目',
                    'category': '开发工具',
                    'tags': [language.lower(), 'github', 'trending'],
                    'author': repo['owner']['login'],
                    'source_url': repo['html_url'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count']
                }
                skills.append(skill_data)
            
            return skills
        except Exception as e:
            print(f"❌ GitHub 抓取失败：{e}")
            return []
    
    def fetch_gitee_recommend(self):
        """从 Gitee 推荐项目抓取"""
        url = "https://gitee.com/api/v5/repos"
        params = {
            'sort': 'stars_count',
            'order': 'desc',
            'page': 1,
            'per_page': 5
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            skills = []
            for repo in data:
                skill_data = {
                    'name': repo['name'].replace('-', ' ').title(),
                    'description': repo['description'] or 'Gitee 推荐项目',
                    'category': '开发工具',
                    'tags': ['gitee', 'recommend'],
                    'author': repo.get('owner', {}).get('login', 'Unknown'),
                    'source_url': repo['html_url'],
                    'stars': repo.get('stargazers_count', 0)
                }
                skills.append(skill_data)
            
            return skills
        except Exception as e:
            print(f"❌ Gitee 抓取失败：{e}")
            return []
    
    def fetch_awesome_skills(self):
        """从 Awesome 系列仓库抓取优质技能"""
        awesome_repos = [
            'awesome-python-applications',
            'awesome-python',
            'awesome-autoit',
            'awesome-scripts'
        ]
        
        skills = []
        for repo_name in awesome_repos:
            try:
                # 这里简化处理，实际应该解析 README
                skills.append({
                    'name': f'Awesome {repo_name.replace("awesome-", "").title()}',
                    'description': f'来自 GitHub Awesome 系列的优质资源 - {repo_name}',
                    'category': '其他',
                    'tags': ['awesome', 'resources', 'collection'],
                    'author': 'community',
                    'source_type': 'awesome'
                })
            except:
                continue
        
        return skills
    
    def create_skill_from_crawl(self, skill_data):
        """将抓取的数据转换为技能并保存"""
        # 检查是否已存在
        existing = self.session.query(Skill).filter(
            Skill.name == skill_data['name']
        ).first()
        
        if existing:
            print(f"⚠️  技能已存在：{skill_data['name']}")
            return None
        
        # 创建临时文件
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
        temp_file.write(f"# {skill_data['name']}\n\n")
        temp_file.write(f"{skill_data['description']}\n\n")
        temp_file.write(f"## 来源\n\n")
        if 'source_url' in skill_data:
            temp_file.write(f"- 原始地址：{skill_data['source_url']}\n")
        temp_file.write(f"- 作者：{skill_data['author']}\n")
        temp_file.write(f"- 抓取时间：{datetime.now().isoformat()}\n")
        temp_file.close()
        
        # 上传技能
        skill = self.skill_service.upload_skill(
            name=skill_data['name'],
            description=skill_data['description'],
            file_path=temp_file.name,
            uploader_id=self.system_user.id,
            category=skill_data.get('category', '其他'),
            tags=skill_data.get('tags', []),
            author=skill_data.get('author', 'Unknown'),
            metadata={
                'source_url': skill_data.get('source_url'),
                'stars': skill_data.get('stars', 0),
                'crawl_time': datetime.now().isoformat(),
                'is_auto_crawled': True
            }
        )
        
        # 清理临时文件
        os.unlink(temp_file.name)
        
        print(f"✅ 成功添加技能：{skill.name}")
        return skill
    
    def crawl_all(self):
        """执行全部抓取任务"""
        print(f"\n🕷️ 开始抓取热门技能 - {datetime.now()}")
        
        total_added = 0
        
        # 1. 抓取 GitHub Trending (Python)
        print("\n📦 抓取 GitHub Trending (Python)...")
        github_skills = self.fetch_github_trending('Python', 'daily')
        for skill_data in github_skills:
            if self.create_skill_from_crawl(skill_data):
                total_added += 1
        
        # 2. 抓取 GitHub Trending (JavaScript)
        print("\n📦 抓取 GitHub Trending (JavaScript)...")
        js_skills = self.fetch_github_trending('JavaScript', 'daily')
        for skill_data in js_skills:
            if self.create_skill_from_crawl(skill_data):
                total_added += 1
        
        # 3. 抓取 Gitee 推荐
        print("\n📦 抓取 Gitee 推荐...")
        gitee_skills = self.fetch_gitee_recommend()
        for skill_data in gitee_skills:
            if self.create_skill_from_crawl(skill_data):
                total_added += 1
        
        # 4. 抓取 Awesome 系列
        print("\n📦 抓取 Awesome 系列...")
        awesome_skills = self.fetch_awesome_skills()
        for skill_data in awesome_skills:
            if self.create_skill_from_crawl(skill_data):
                total_added += 1
        
        print(f"\n✅ 抓取完成！新增技能：{total_added} 个\n")
        return total_added
    
    def cleanup_old_crawled(self, keep_days=7):
        """清理旧的自动抓取技能"""
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        old_skills = self.session.query(Skill).filter(
            Skill.uploader_id == self.system_user.id,
            Skill.created_at < cutoff_date
        ).all()
        
        deleted_count = 0
        for skill in old_skills:
            # 删除文件
            if skill.file_path and os.path.exists(skill.file_path):
                os.remove(skill.file_path)
            
            # 删除记录
            self.session.delete(skill)
            deleted_count += 1
        
        self.session.commit()
        print(f"🧹 清理了 {deleted_count} 个旧的自动抓取技能")
        return deleted_count


def daily_crawl_task():
    """每日自动抓取任务"""
    crawler = HotSkillCrawler()
    
    # 执行抓取
    added_count = crawler.crawl_all()
    
    # 清理旧数据
    crawler.cleanup_old_crawled(keep_days=7)
    
    return added_count


if __name__ == '__main__':
    daily_crawl_task()
