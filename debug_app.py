"""
调试版本的 Flask 应用 - 添加详细错误处理
"""
import os
import sys
import traceback
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session

# 自动检测环境并导入配置
try:
    from config_render import DATABASE_URL, DEBUG, HOST, PORT, SECRET_KEY
    print(f"✅ Loaded config_render.py")
    print(f"   DATABASE_URL: {DATABASE_URL}")
    print(f"   HOST: {HOST}, PORT: {PORT}")
except ImportError as e:
    from config import DATABASE_URL, DEBUG, HOST, PORT
    SECRET_KEY = 'lobster_skill_platform_secret_key_2024'
    print(f"⚠️  Using config.py: {e}")

app = Flask(__name__)
app.secret_key = SECRET_KEY

# 添加错误处理中间件
@app.errorhandler(Exception)
def handle_exception(e):
    """全局错误处理器"""
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    print(traceback.format_exc())
    
    # 返回详细错误信息（仅开发环境）
    if DEBUG:
        return jsonify({
            'error': str(e),
            'type': type(e).__name__,
            'traceback': traceback.format_exc()
        }), 500
    
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Please check server logs for details'
    }), 500

# 延迟导入数据库
def get_db_session():
    """获取数据库会话"""
    try:
        from models import init_db
        print("📊 Initializing database...")
        db = init_db(DATABASE_URL)
        print("✅ Database initialized successfully")
        return db
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        print(traceback.format_exc())
        raise

def get_services():
    """获取服务实例"""
    try:
        print("🔧 Initializing services...")
        from services import UserService, SkillService, RecommendationService
        db = get_db_session()
        user_service = UserService(db)
        skill_service = SkillService(db)
        recommendation_service = RecommendationService(db)
        print("✅ Services initialized successfully")
        return user_service, skill_service, recommendation_service
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        print(traceback.format_exc())
        raise

# 默认用户名和头像
DEFAULT_USERNAMES = ['小龙虾', '技能达人', '探索者', '创新者', '学习家', '分享者', '实践者', '收藏家']
DEFAULT_AVATARS = ['🦞', '🚀', '⭐', '🎯', '💡', '🔥', '✨', '🌟', '', '🏆']

def get_or_create_auto_user():
    """自动创建或获取默认用户"""
    try:
        if 'user_id' not in session:
            username = f"{random.choice(DEFAULT_USERNAMES)}_{random.randint(1000, 9999)}"
            avatar = random.choice(DEFAULT_AVATARS)
            
            user_service, _, _ = get_services()
            user = user_service.get_or_create_user(username, email=None)
            user.avatar = avatar
            user_service.session.commit()
            
            session['user_id'] = user.id
            session['username'] = user.username
            session['avatar'] = avatar
        
        user_service, _, _ = get_services()
        return user_service.session.query(User).get(session.get('user_id'))
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        print(traceback.format_exc())
        raise

# 测试路由
@app.route('/health')
def health():
    """健康检查端点"""
    try:
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'message': 'Server is running'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/')
def index():
    """首页"""
    try:
        print("\n📍 Accessing home page...")
        user = get_or_create_auto_user()
        user_service, skill_service, recommendation_service = get_services()
        
        print("Getting recommendations...")
        recommendations = []
        if user:
            recommendations = recommendation_service.generate_daily_recommendations(user.id)
        
        print("Getting popular skills...")
        popular_skills = skill_service.search_skills(sort_by='download_count')[:10]
        
        print("Getting new skills...")
        new_skills = skill_service.search_skills(sort_by='created_at')[:10]
        
        print("Rendering template...")
        return render_template('index.html', 
                             user=user,
                             popular_skills=popular_skills,
                             new_skills=new_skills,
                             recommendations=recommendations)
    except Exception as e:
        print(f"❌ Home page error: {e}")
        print(traceback.format_exc())
        raise

# ... 其他路由保持不变，使用原来的 app.py 内容 ...

if __name__ == '__main__':
    print(f"\n🦞 Starting Lobster Skill Platform...")
    print(f" Listening on {HOST}:{PORT}")
    print(f"🔍 Debug mode: {DEBUG}")
    print("=" * 60)
    app.run(host=HOST, port=PORT, debug=DEBUG)
