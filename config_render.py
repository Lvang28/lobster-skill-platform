"""
龙虾 Skill 合集平台 - Render 云部署配置
"""
import os

# 检测是否在 Render 环境
IS_RENDER = 'RENDER' in os.environ

# 基础路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if IS_RENDER:
    DATA_DIR = '/opt/render/project/src/data'
else:
    DATA_DIR = os.path.join(BASE_DIR, 'data')

SKILLS_DIR = os.path.join(DATA_DIR, 'skills')
USER_DIR = os.path.join(DATA_DIR, 'users')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')

# 数据库配置
DATABASE_URL = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(DATA_DIR, 'lobster_platform.db')}")

# 服务器配置
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 10000))
DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ.get('SECRET_KEY', 'lobster_platform_dev_secret_key_change_in_production')

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

# GitHub 配置
GITHUB_CONFIG = {'enabled': False, 'repo': '', 'token': '', 'branch': 'main'}

# 云存储配置
CLOUD_STORAGE_CONFIG = {'enabled': False, 'type': 'webdav', 'url': '', 'username': '', 'password': ''}

# 确保目录存在（关键修复！）
print("\n📁 Creating directories...")
for dir_path in [DATA_DIR, SKILLS_DIR, USER_DIR, BACKUP_DIR]:
    try:
        os.makedirs(dir_path, exist_ok=True)
        print(f"   ✓ Created: {dir_path}")
    except Exception as e:
        print(f"   ⚠️  Warning creating {dir_path}: {e}")

print(f"\n✓ 数据目录已初始化：{DATA_DIR}")
print(f"🌐 运行环境：{'Render Cloud' if IS_RENDER else 'Local'}")
print(f"🔗 数据库：{'PostgreSQL' if 'postgresql' in DATABASE_URL else 'SQLite'}")
print(f"📍 监听地址：{HOST}:{PORT}\n")
