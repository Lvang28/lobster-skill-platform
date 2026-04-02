#!/usr/bin/env python3
"""
直接查询数据库检查技能数据
"""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://lobster_db_user:Nyt96XwP0H2k8nPkXW6SbKOtOT6ffX4G@dpg-d773676slomc73anbbp0-a/lobster_db"

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # 检查总数
    result = conn.execute(text("SELECT COUNT(*) FROM skills"))
    total = result.scalar()
    print(f"总技能数：{total}")
    
    # 检查 is_active 分布
    result = conn.execute(text("SELECT is_active, COUNT(*) FROM skills GROUP BY is_active"))
    print("\nis_active 分布:")
    for row in result:
        print(f"  is_active={row[0]}: {row[1]} 个")
    
    # 检查前 10 个技能
    result = conn.execute(text("SELECT id, name, category, is_active FROM skills ORDER BY id LIMIT 10"))
    print("\n前 10 个技能:")
    for row in result:
        print(f"  [{row[0]}] {row[1]} ({row[2]}) - is_active={row[3]}")
