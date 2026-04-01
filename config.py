"""
龙虾 Skill 合集平台 - 配置文件
"""
import os
from datetime import datetime

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SKILLS_DIR = os.path.join(DATA_DIR, 'skills')
USER_DIR = os.path.join(DATA_DIR, 'users')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')

# 数据库配置
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'lobster_platform.db')}"

# 服务器配置
HOST = '0.0.0.0'  # 允许外网访问（改为 0.0.0.0）
PORT = 5000
DEBUG = True

# 积分规则
POINTS_CONFIG = {
    'upload_skill': 10,      # 上传 skill 获得积分
    'download_skill': 2,     # 下载 skill 获得积分（下载者）
    'skill_downloaded': 5,   # skill 被下载获得积分（上传者）
    'skill_used': 3,         # skill 被使用获得积分（上传者）
    'daily_recommendation': 1  # 每日推荐技能被采纳获得积分
}

# 推荐系统配置
RECOMMENDATION_CONFIG = {
    'daily_count': 3,        # 每日推荐数量
    'update_hours': [10, 14, 17],  # 每日更新时间
    'history_days': 30       # 分析最近多少天的用户行为
}

# GitHub 配置（可选）
GITHUB_CONFIG = {
    'enabled': False,
    'repo': '',
    'token': '',
    'branch': 'main'
}

# 云存储配置（可选）
CLOUD_STORAGE_CONFIG = {
    'enabled': False,
    'type': 'webdav',  # webdav, s3, etc.
    'url': '',
    'username': '',
    'password': ''
}

# 确保目录存在
for dir_path in [DATA_DIR, SKILLS_DIR, USER_DIR, BACKUP_DIR]:
    os.makedirs(dir_path, exist_ok=True)

print(f"✓ 数据目录已初始化：{DATA_DIR}")
