"""
龙虾 Skill 合集平台 - 数据库模型
"""
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    """用户表"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200))
    avatar = Column(String(500))
    total_points = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    uploaded_skills = relationship('Skill', back_populates='uploader', foreign_keys='Skill.uploader_id')
    downloads = relationship('DownloadHistory', back_populates='user')
    usage_records = relationship('UsageRecord', back_populates='user')
    points_history = relationship('PointsHistory', back_populates='user')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'total_points': self.total_points,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'skill_count': len(self.uploaded_skills)
        }


class Skill(Base):
    """Skill 表"""
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    version = Column(String(50), default='1.0.0')
    author = Column(String(100))
    uploader_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String(100))
    tags = Column(JSON)  # 标签列表
    file_path = Column(String(500))
    file_size = Column(Integer)
    download_count = Column(Integer, default=0)
    use_count = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    extra_data = Column(JSON)  # 额外元数据
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    uploader = relationship('User', back_populates='uploaded_skills', foreign_keys=[uploader_id])
    downloads = relationship('DownloadHistory', back_populates='skill')
    usage_records = relationship('UsageRecord', back_populates='skill')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'author': self.author,
            'uploader_id': self.uploader_id,
            'category': self.category,
            'tags': self.tags or [],
            'download_count': self.download_count,
            'use_count': self.use_count,
            'rating': round(self.rating, 2) if self.rating else 0.0,
            'file_size': self.file_size,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }


class DownloadHistory(Base):
    """下载历史表"""
    __tablename__ = 'download_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    downloaded_at = Column(DateTime, default=datetime.now)
    
    # 关系
    user = relationship('User', back_populates='downloads')
    skill = relationship('Skill', back_populates='downloads')


class UsageRecord(Base):
    """使用记录表"""
    __tablename__ = 'usage_records'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    used_at = Column(DateTime, default=datetime.now)
    duration = Column(Integer)  # 使用时长（秒）
    success = Column(Boolean, default=True)
    
    # 关系
    user = relationship('User', back_populates='usage_records')
    skill = relationship('Skill', back_populates='usage_records')


class PointsHistory(Base):
    """积分历史记录表"""
    __tablename__ = 'points_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    points = Column(Integer)
    reason = Column(String(200))
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    user = relationship('User', back_populates='points_history')
    skill = relationship('Skill')


class UserPreference(Base):
    """用户偏好表（用于推荐系统）"""
    __tablename__ = 'user_preferences'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_weights = Column(JSON)  # 类别权重
    tag_weights = Column(JSON)  # 标签权重
    recent_skills = Column(JSON)  # 最近使用的 skill IDs
    last_updated = Column(DateTime, default=datetime.now)


class Recommendation(Base):
    """推荐记录表"""
    __tablename__ = 'recommendations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    skill_ids = Column(JSON)  # 推荐的 skill IDs
    date = Column(DateTime, default=datetime.now)
    accepted_skill_id = Column(Integer, ForeignKey('skills.id'), nullable=True)


class CommunityPost(Base):
    """社区帖子表"""
    __tablename__ = 'community_posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    category = Column(String(50), default='general')  # general, share, question, discussion
    tags = Column(JSON)  # 标签列表
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)  # 是否置顶
    is_locked = Column(Boolean, default=False)  # 是否锁定
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    author = relationship('User', backref='community_posts')
    comments = relationship('CommunityComment', back_populates='post', cascade='all, delete-orphan')
    likes = relationship('CommunityLike', back_populates='post', cascade='all, delete-orphan')


class CommunityComment(Base):
    """社区评论表"""
    __tablename__ = 'community_comments'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('community_posts.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey('community_comments.id'), nullable=True)  # 回复评论
    like_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    post = relationship('CommunityPost', back_populates='comments')
    author = relationship('User', backref='community_comments')
    parent = relationship('CommunityComment', remote_side=[id], backref='replies')


class CommunityLike(Base):
    """社区点赞表"""
    __tablename__ = 'community_likes'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('community_posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    post = relationship('CommunityPost', back_populates='likes')
    user = relationship('User')


# 初始化数据库
def init_db(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
