"""
测试数据库连接的脚本
在 Render Shell 中执行，或本地测试
"""
import os

print("=" * 60)
print("🧪 数据库连接测试")
print("=" * 60)

# 检测环境
IS_RENDER = 'RENDER' in os.environ
print(f"\n🌐 运行环境：{'Render Cloud' if IS_RENDER else 'Local'}")

# 检查环境变量
print("\n📋 环境变量:")
print(f"   DATABASE_URL: {'✅ 已设置' if os.environ.get('DATABASE_URL') else '❌ 未设置'}")
print(f"   SECRET_KEY: {'✅ 已设置' if os.environ.get('SECRET_KEY') else '❌ 未设置'}")
print(f"   FLASK_DEBUG: {'✅ 已设置' if os.environ.get('FLASK_DEBUG') else '❌ 未设置'}")

# 获取 DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/lobster_platform.db')

if 'postgresql' in DATABASE_URL:
    print("\n🔗 数据库类型：PostgreSQL")
    
    # 尝试连接
    try:
        from sqlalchemy import create_engine, text
        print("\n 正在连接数据库...")
        
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ 数据库连接成功！")
            
            # 获取版本
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"📊 PostgreSQL 版本：{version[:50]}...")
            
    except Exception as e:
        print(f"\n❌ 数据库连接失败！")
        print(f"错误信息：{e}")
        print("\n💡 可能的原因:")
        print("   1. DATABASE_URL 格式不正确")
        print("   2. 数据库权限问题")
        print("   3. 网络连接问题")
        print("\n请检查 Render Dashboard → Environment 中的 DATABASE_URL 配置")
else:
    print("\n⚠️  使用 SQLite（数据会在重启后丢失）")
    print(f"路径：{DATABASE_URL}")

print("\n" + "=" * 60)
