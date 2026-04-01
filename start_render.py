"""
Render 云部署启动脚本
"""
import os

print("=" * 60)
print("🚀 Starting Lobster Skill Platform on Render...")
print("=" * 60)

# 检测环境
IS_RENDER = 'RENDER' in os.environ
print(f"\n🌐 Environment: {'Render Cloud' if IS_RENDER else 'Local'}")

# 导入配置
try:
    from config_render import DATABASE_URL, HOST, PORT, SECRET_KEY
    print(f"✅ Loaded config_render.py")
except ImportError as e:
    from config import DATABASE_URL, DEBUG, HOST, PORT
    SECRET_KEY = 'lobster_platform_dev_secret'
    print(f"⚠️  Using config.py: {e}")

# 初始化数据库
print(f"\n📊 Initializing database...")
from models import init_db
db_session = init_db(DATABASE_URL)
print(f"✅ Database initialized: {'PostgreSQL' if 'postgresql' in str(DATABASE_URL) else 'SQLite'}")

# 初始化服务
print(f"\n🔧 Initializing services...")
from services import UserService, SkillService, RecommendationService
user_service = UserService(db_session)
skill_service = SkillService(db_session)
recommendation_service = RecommendationService(db_session)
print(f"✅ Services initialized")

# 创建 Flask 应用
print(f"\n Creating Flask app...")
from app import app
print(f"✅ Flask app created")

# 启动服务器
print(f"\n🚀 Starting server on {HOST}:{PORT}...")
print("=" * 60)

if __name__ == '__main__':
    # Render 使用 gunicorn，但我们也支持直接运行
    app.run(host=HOST, port=PORT, debug=False)
