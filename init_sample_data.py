"""
龙虾 Skill 合集平台 - 数据初始化脚本
用于创建示例数据，方便测试和演示
"""
from models import init_db, User, Skill
from config import DATABASE_URL
from services import UserService, SkillService
import os


def init_sample_data():
    """初始化示例数据"""
    print("🦞 正在初始化龙虾 Skill 平台示例数据...")
    
    # 初始化数据库
    session = init_db(DATABASE_URL)
    user_service = UserService(session)
    skill_service = SkillService(session)
    
    # 创建示例用户
    print("\n📝 创建示例用户...")
    users_data = [
        {'username': '张三', 'email': 'zhangsan@example.com'},
        {'username': '李四', 'email': 'lisi@example.com'},
        {'username': '王五', 'email': 'wangwu@example.com'},
        {'username': '数据分析大师', 'email': 'data@example.com'},
        {'username': 'AI 爱好者', 'email': 'ai@example.com'},
    ]
    
    users = []
    for user_data in users_data:
        user = user_service.get_or_create_user(**user_data)
        users.append(user)
        print(f"  ✓ 用户：{user.username} (初始积分：{user.total_points})")
    
    # 创建示例技能
    print("\n📦 创建示例技能...")
    
    skills_data = [
        {
            'name': 'Excel 数据自动处理工具',
            'description': '自动读取 Excel 文件，进行数据清洗、格式转换、统计分析，并生成可视化报表。支持批量处理，大幅提升办公效率。',
            'category': '办公效率',
            'tags': ['python', 'excel', '数据处理', '自动化'],
            'author': '张三'
        },
        {
            'name': '智能周报生成器',
            'description': '基于 AI 的周报自动生成工具，输入本周工作内容，自动生成结构清晰、内容丰富的周报文档。支持多种模板选择。',
            'category': 'AI 工具',
            'tags': ['AI', '周报', '文档生成', '办公'],
            'author': '李四'
        },
        {
            'name': '网站数据爬虫框架',
            'description': '轻量级网页爬虫框架，支持动态页面渲染、反爬突破、数据提取、定时任务等功能。内置多个网站爬虫模板。',
            'category': '数据处理',
            'tags': ['爬虫', '数据采集', 'python', '自动化'],
            'author': '王五'
        },
        {
            'name': '销售数据可视化大屏',
            'description': '实时展示销售数据的可视化大屏，包含销售额、订单量、客户分布、产品排行等核心指标。支持自定义数据源。',
            'category': '数据处理',
            'tags': ['可视化', '数据分析', 'dashboard', '销售'],
            'author': '数据分析大师'
        },
        {
            'name': 'Python 代码质量检查工具',
            'description': '自动检查 Python 代码质量，包括代码规范、性能问题、潜在 bug、安全漏洞等。集成 flake8、pylint、bandit 等工具。',
            'category': '开发工具',
            'tags': ['python', '代码质量', '静态分析', '开发工具'],
            'author': 'AI 爱好者'
        },
        {
            'name': '社交媒体自动发布助手',
            'description': '一键发布内容到多个社交媒体平台（微博、微信公众号、知乎等）。支持定时发布、内容排版、数据统计。',
            'category': '自动化',
            'tags': ['社交媒体', '自动化', '营销', '定时任务'],
            'author': '张三'
        },
        {
            'name': '机器学习模型训练模板',
            'description': '标准化的机器学习模型训练模板，包含数据预处理、特征工程、模型选择、超参数调优、结果评估等完整流程。',
            'category': 'AI 工具',
            'tags': ['机器学习', '深度学习', 'python', '模板'],
            'author': 'AI 爱好者'
        },
        {
            'name': '财务报表自动生成系统',
            'description': '从财务软件导出数据，自动生成标准财务报表（资产负债表、利润表、现金流量表）。支持自定义报表格式。',
            'category': '办公效率',
            'tags': ['财务', '报表', '自动化', 'excel'],
            'author': '李四'
        },
    ]
    
    # 创建临时文件并上传技能
    for i, skill_data in enumerate(skills_data):
        # 创建示例文件
        temp_file = f'/tmp/skill_{i}.py'
        with open(temp_file, 'w') as f:
            f.write(f'# {skill_data["name"]}\n')
            f.write(f'# Author: {skill_data["author"]}\n\n')
            f.write('print("这是一个示例技能文件")\n')
        
        # 找到对应的用户
        uploader = next((u for u in users if u.username == skill_data['author']), users[0])
        
        # 上传技能
        skill = skill_service.upload_skill(
            name=skill_data['name'],
            description=skill_data['description'],
            file_path=temp_file,
            uploader_id=uploader.id,
            category=skill_data['category'],
            tags=skill_data['tags'],
            author=skill_data['author']
        )
        
        print(f"  ✓ 技能：{skill.name} (分类：{skill.category}, 积分：+10)")
        
        # 清理临时文件
        os.remove(temp_file)
    
    # 模拟一些下载和使用记录
    print("\n🔄 模拟用户行为...")
    for user in users:
        # 每个用户下载 2-3 个技能
        from random import choice
        all_skills = session.query(Skill).all()
        downloaded = choice(all_skills) if all_skills else None
        
        if downloaded:
            skill_service.download_skill(downloaded.id, user.id)
            print(f"  ✓ {user.username} 下载了 {downloaded.name}")
    
    print("\n✅ 示例数据初始化完成！")
    print("\n📊 统计信息:")
    total_users = session.query(User).count()
    total_skills = session.query(Skill).count()
    print(f"  - 用户数：{total_users}")
    print(f"  - 技能数：{total_skills}")
    
    print("\n💡 提示：现在可以启动平台查看示例数据")
    print("   运行：python app.py")


if __name__ == '__main__':
    init_sample_data()
