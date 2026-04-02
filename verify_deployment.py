#!/usr/bin/env python3
"""
验证部署是否成功
检查平台是否可以访问，技能数据是否正确
"""
import requests
import time

BASE_URL = "https://lobster-skill-platform-v2.onrender.com"

print("=" * 60)
print("🦞 龙虾 Skill 平台 - 部署验证")
print("=" * 60)

# 测试 1: 检查首页
print("\n📋 测试 1: 检查首页...")
try:
    response = requests.get(BASE_URL, timeout=30)
    if response.status_code == 200:
        print("✅ 首页访问成功")
    else:
        print(f"❌ 首页访问失败：{response.status_code}")
except Exception as e:
    print(f"❌ 首页访问超时或错误：{e}")

# 等待几秒让服务器响应（Render 冷启动）
time.sleep(3)

# 测试 2: 检查技能列表页
print("\n📋 测试 2: 检查技能列表页...")
try:
    response = requests.get(f"{BASE_URL}/skills", timeout=30)
    if response.status_code == 200:
        print("✅ 技能列表页访问成功")
        
        # 简单检查是否有技能数据
        if '50' in response.text or '技能' in response.text:
            print("✅ 检测到技能数据")
        else:
            print("⚠️  未检测到技能数据（可能需要手动初始化）")
    else:
        print(f"❌ 技能列表页访问失败：{response.status_code}")
except Exception as e:
    print(f"❌ 技能列表页访问超时或错误：{e}")

# 等待几秒
time.sleep(2)

# 测试 3: 检查社区页面
print("\n📋 测试 3: 检查社区页面...")
try:
    response = requests.get(f"{BASE_URL}/community", timeout=30)
    if response.status_code == 200:
        print("✅ 社区页面访问成功")
    else:
        print(f"❌ 社区页面访问失败：{response.status_code}")
except Exception as e:
    print(f"❌ 社区页面访问超时或错误：{e}")

# 测试 4: 检查 API 统计
print("\n📋 测试 4: 检查平台统计 API...")
try:
    response = requests.get(f"{BASE_URL}/api/stats", timeout=30)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ API 返回成功")
        print(f"   📊 总技能数：{data.get('total_skills', 'N/A')}")
        print(f"   👥 总用户数：{data.get('total_users', 'N/A')}")
        print(f"   ⬇️  总下载数：{data.get('total_downloads', 'N/A')}")
        
        if data.get('total_skills', 0) >= 50:
            print("\n🎉 恭喜！50 个技能已成功上传！")
        else:
            print(f"\n⚠️  技能数量不足 50，可能需要等待数据库初始化完成")
    else:
        print(f"❌ API 请求失败：{response.status_code}")
except Exception as e:
    print(f"❌ API 请求超时或错误：{e}")

print("\n" + "=" * 60)
print("✅ 验证完成！")
print("🌐 访问平台：https://lobster-skill-platform-v2.onrender.com")
print("=" * 60)
