"""
龙虾 Skill 合集平台 - 生产环境配置
"""
import os
from datetime import datetime

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get('DATA_DIR', os.path.join(BASE_DIR, 'data'))
SKILLS_DIR = os.path.join(DATA_DIR, 'skills')
USER_DIR = os.path.join(DATA_DIR, 'users')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')

# 数据库配置（Heroku 使用 PostgreSQL）
DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(DATA_DIR, 'lobster_platform.db')}")

# 服务器配置
HOST = os.environ.get('HOST', '0.0.0.0')
PORT = int(os.environ.get('PORT', 5000))
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

# Secret Key（生产环境必须设置）
SECRET_KEY = os.environ.get('SECRET_KEY', 'lobster_skill_platform_secret_key_2024')

# 积分规则
POINTS_CONFIG = {
    'upload_skill': 10,
    'download_skill': 2,
    'skill_downloaded': 5,
    'skill_used': 3,
    'daily_recommendation': 1
}

# 推荐系统配置
RECOMMENDATION_CONFIG = {
    'daily_count': 3,
    'update_hours': [10, 14, 17],
    'history_days': 30
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
    'type': 'webdav',
    'url': '',
    'username': '',
    'password': ''
}

# 确保目录存在
for dir_path in [DATA_DIR, SKILLS_DIR, USER_DIR, BACKUP_DIR]:
    os.makedirs(dir_path, exist_ok=True)

print(f"✓ 数据目录已初始化：{DATA_DIR}")
print(f"✓ 运行模式：{'开发' if DEBUG else '生产'}")
print(f"✓ 监听地址：{HOST}:{PORT}")
