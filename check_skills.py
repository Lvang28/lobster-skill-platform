#!/usr/bin/env python3
"""
检查数据库中的技能数据
"""
import requests

# 访问管理 API 查看技能
response = requests.get("https://lobster-skill-platform-v2.onrender.com/admin/init-skills?token=lobster_admin_2024_secret")
print("管理 API 响应:")
print(response.json())
print()

# 访问统计 API
response = requests.get("https://lobster-skill-platform-v2.onrender.com/api/stats")
print("平台统计:")
print(response.json())
print()

# 尝试直接访问技能列表（模拟浏览器）
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
response = requests.get("https://lobster-skill-platform-v2.onrender.com/skills", headers=headers)
print(f"技能列表页面状态码：{response.status_code}")
print(f"页面大小：{len(response.text)} 字节")

# 查找是否有技能名称
import re
skills_found = re.findall(r'Python|数据分析 |Web 开发 |机器学习|DevOps', response.text)
print(f"页面中找到的技能分类关键词：{len(skills_found)} 个")
