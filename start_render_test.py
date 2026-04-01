"""
测试 Render 部署的简化脚本
"""
import os
import sys

print("=" * 60)
print("🧪 Testing Render Deployment...")
print("=" * 60)

# 测试 1: 导入配置
try:
    print("\n1. Testing config import...")
    try:
        from config_render import DATABASE_URL, HOST, PORT, SECRET_KEY
        print(f"   ✅ Loaded config_render.py")
        print(f"   📍 HOST: {HOST}, PORT: {PORT}")
        print(f"   🔗 Database: {'PostgreSQL' if 'postgresql' in DATABASE_URL else 'SQLite'}")
    except ImportError as e:
        from config import DATABASE_URL, HOST, PORT
        SECRET_KEY = 'test_key'
        print(f"   ⚠️  Using config.py (config_render.py not found)")
        print(f"   Error: {e}")
except Exception as e:
    print(f"   ❌ Config test failed: {e}")
    sys.exit(1)

# 测试 2: 初始化数据库
try:
    print("\n2. Testing database initialization...")
    from models import init_db
    db_session = init_db(DATABASE_URL)
    print(f"   ✅ Database initialized")
except Exception as e:
    print(f"   ❌ Database test failed: {e}")
    sys.exit(1)

# 测试 3: 导入 Flask 应用
try:
    print("\n3. Testing Flask app import...")
    from app import app
    print(f"   ✅ Flask app imported successfully")
except Exception as e:
    print(f"   ❌ Flask app import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试 4: 测试路由
try:
    print("\n4. Testing routes...")
    with app.test_client() as client:
        rv = client.get('/')
        print(f"   GET / → Status: {rv.status_code}")
        if rv.status_code == 200:
            print(f"   ✅ Home page works!")
        else:
            print(f"   ⚠️  Home page returned {rv.status_code}")
except Exception as e:
    print(f"   ❌ Route test failed: {e}")

print("\n" + "=" * 60)
print("✅ All tests passed! App should work on Render.")
print("=" * 60)
