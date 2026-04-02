"""
龙虾 Skill 合集平台 - Flask Web 应用
"""
import os
import json
import random
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session

# 自动检测环境并导入配置
try:
    from config_render import DATABASE_URL, DEBUG, HOST, PORT, SECRET_KEY
except ImportError:
    from config import DATABASE_URL, DEBUG, HOST, PORT
    SECRET_KEY = 'lobster_skill_platform_secret_key_2024'

app = Flask(__name__)
app.secret_key = SECRET_KEY

# 数据库初始化标志
_db_initialized = False

def initialize_database():
    """初始化数据库并插入默认技能数据"""
    global _db_initialized
    
    if _db_initialized:
        return
    
    try:
        from sqlalchemy import text, inspect
        
        db = get_db_session()
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        
        print("\n📋 检查数据库表...")
        if not tables:
            print("   ⚠️  表未创建，等待应用首次访问时自动创建...")
            # 表不存在，让正常流程去创建
            _db_initialized = True
            return
        
        print(f"   ✅ 找到表：{', '.join(tables)}")
        
        # 检查 skills 表是否存在且为空
        if 'skills' in tables:
            with db.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM skills"))
                count = result.scalar()
                
                if count == 0:
                    print("\n📦 检测到空数据库，开始初始化 50 个技能...")
                    run_initial_data_insert(conn)
                    conn.commit()
                    print("✅ 数据库初始化完成\n")
                else:
                    print(f"ℹ️  数据库中已有 {count} 个技能，跳过初始化\n")
        
        _db_initialized = True
        
    except Exception as e:
        print(f"⚠️  数据库初始化跳过：{e}")
        _db_initialized = True  # 即使失败也标记为已尝试

def run_initial_data_insert(session):
    """执行初始数据插入"""
    from datetime import datetime
    
    skills_data = [
        ('Python Excel 自动化处理工具', '自动读取、修改、合并 Excel 文件，支持批量处理，大幅提升办公效率。', 'Python', '["Python", "Excel", "自动化", "办公"]'),
        ('Python PDF 转 Word 工具', '一键批量将 PDF 转换为可编辑的 Word 文档，保持原有格式。', 'Python', '["Python", "PDF", "Word", "格式转换"]'),
        ('Python 微信机器人框架', '基于 WeChaty 的微信聊天机器人，支持自动回复、群管理等功能。', 'Python', '["Python", "微信", "机器人", "自动化"]'),
        ('Python 数据分析模板', '完整的数据分析流程模板，包括数据加载、EDA、可视化等。', 'Python', '["Python", "数据分析", "Pandas", "可视化"]'),
        ('Python 网络爬虫框架', '通用网页爬虫框架，支持反爬处理、数据清洗、自动重试。', 'Python', '["Python", "爬虫", "数据采集", "Web Scraping"]'),
        ('Python 自动化测试脚本', '基于 Selenium 的 Web 自动化测试框架，支持截图、报告生成。', 'Python', '["Python", "测试", "Selenium", "自动化"]'),
        ('Python 文件批量重命名工具', '批量重命名文件和文件夹，支持正则表达式匹配。', 'Python', '["Python", "文件管理", "批量处理", "工具"]'),
        ('Python 图片压缩工具', '批量压缩图片文件大小，保持清晰度，支持多种格式。', 'Python', '["Python", "图片处理", "压缩", "PIL"]'),
        ('Python 邮件群发助手', 'SMTP 邮件群发工具，支持 HTML 模板、附件发送、发送记录。', 'Python', '["Python", "邮件", "SMTP", "群发"]'),
        ('Python 视频下载器', '支持下载 YouTube、Bilibili 等平台视频的命令行工具。', 'Python', '["Python", "视频", "下载", "youtube-dl"]'),
        ('销售数据分析看板', '使用 Tableau/PowerBI 风格的销售数据可视化分析模板。', '数据分析', '["数据分析", "销售", "可视化", "BI"]'),
        ('用户行为分析模型', '分析用户留存率、转化率、漏斗模型的完整分析框架。', '数据分析', '["数据分析", "用户行为", "留存", "转化"]'),
        ('A/B 测试分析工具', '统计学 A/B 测试分析，包含显著性检验和功效分析。', '数据分析', '["数据分析", "A/B 测试", "统计", "假设检验"]'),
        ('时间序列预测模型', '基于 ARIMA 和 Prophet 的时间序列预测模板。', '数据分析', '["数据分析", "时间序列", "预测", "ARIMA"]'),
        ('客户分群分析', 'RFM 模型 + K-Means聚类的客户细分分析方案。', '数据分析', '["数据分析", "客户分群", "RFM", "聚类"]'),
        ('电商数据仪表盘', '完整的电商运营数据监控仪表盘，包含 GMV、转化率等指标。', '数据分析', '["数据分析", "电商", "仪表盘", "监控"]'),
        ('社交媒体分析工具', '微博、微信公众号数据统计与分析模板。', '数据分析', '["数据分析", "社交媒体", "运营", "统计"]'),
        ('财务数据分析报表', '企业财务三表分析、比率分析、趋势分析模板。', '数据分析', '["数据分析", "财务", "报表", "分析"]'),
        ('人力资源数据分析', '员工流失率、招聘效率、绩效分析的 HR 仪表盘。', '数据分析', '["数据分析", "HR", "人力资源", "绩效"]'),
        ('市场数据分析报告', '市场份额、竞品分析、价格弹性分析模板。', '数据分析', '["数据分析", "市场", "竞品", "价格"]'),
        ('Flask RESTful API 模板', '生产级 Flask RESTful API 脚手架，含 JWT 认证。', 'Web 开发', '["Flask", "API", "RESTful", "JWT"]'),
        ('Django 博客系统', '完整的 Django 博客系统，支持评论、标签、搜索。', 'Web 开发', '["Django", "博客", "CMS", "Python"]'),
        ('Vue3 后台管理模板', '基于 Vue3 + Element Plus 的后台管理系统模板。', 'Web 开发', '["Vue", "前端", "Element", "管理后台"]'),
        ('React 电商网站模板', '完整的 React 电商网站，含购物车、订单、支付。', 'Web 开发', '["React", "电商", "前端", "购物车"]'),
        ('Node.js 即时聊天室', '基于 Socket.io 的实时聊天室应用。', 'Web 开发', '["Node.js", "Socket.io", "聊天", "实时"]'),
        ('微信小程序商城模板', '完整的微信小程序商城代码，支持拼团、秒杀。', 'Web 开发', '["小程序", "微信", "商城", "电商"]'),
        ('TypeScript 工具库', '常用的 TypeScript 工具函数集合，提升开发效率。', 'Web 开发', '["TypeScript", "工具库", "JavaScript", "前端"]'),
        ('CSS 动画效果集', '50+ 种实用的 CSS 动画效果，开箱即用。', 'Web 开发', '["CSS", "动画", "前端", "UI"]'),
        ('响应式落地页模板', '营销落地页模板，适配手机和桌面端。', 'Web 开发', '["HTML", "CSS", "响应式", "落地页"]'),
        ('GraphQL API 示例', 'GraphQL API 完整示例，包含查询、变更、订阅。', 'Web 开发', '["GraphQL", "API", "后端", "查询"]'),
        ('机器学习入门教程', 'Scikit-learn 机器学习算法入门教程与代码示例。', '机器学习', '["机器学习", "Scikit-learn", "教程", "入门"]'),
        ('深度学习图像分类', '基于 PyTorch 的图像分类模型训练模板。', '机器学习', '["深度学习", "PyTorch", "图像分类", "CNN"]'),
        ('NLP 文本情感分析', '中文文本情感分析模型，支持细粒度情感打分。', '机器学习', '["NLP", "情感分析", "文本分类", "BERT"]'),
        ('推荐系统实战', '协同过滤 + 深度学习的混合推荐系统实现。', '机器学习', '["推荐系统", "协同过滤", "深度学习", "排序"]'),
        ('目标检测 YOLO 模板', 'YOLOv5 目标检测模型训练与部署模板。', '机器学习', '["目标检测", "YOLO", "计算机视觉", "深度学习"]'),
        ('语音识别工具', '基于 Whisper 的语音转文字工具，支持多语言。', '机器学习', '["语音识别", "Whisper", "ASR", "转录"]'),
        ('GAN 图像生成', '使用 GAN 生成逼真图像的完整实现代码。', '机器学习', '["GAN", "图像生成", "深度学习", "AI"]'),
        ('强化学习入门', 'Q-Learning、DQN 等强化学习算法实现。', '机器学习', '["强化学习", "Q-Learning", "DQN", "AI"]'),
        ('时间序列预测 LSTM', '基于 LSTM 神经网络的时间序列预测模型。', '机器学习', '["LSTM", "时间序列", "预测", "深度学习"]'),
        ('模型部署 Flask API', '将机器学习模型部署为 REST API 服务。', '机器学习', '["模型部署", "Flask", "API", "服务化"]'),
        ('Docker 快速入门', 'Docker 基础教程，包含常用命令和实战案例。', 'DevOps', '["Docker", "容器", "教程", "入门"]'),
        ('Kubernetes 部署模板', 'K8s Deployment、Service、Ingress 配置模板。', 'DevOps', '["Kubernetes", "K8s", "部署", "容器编排"]'),
        ('CI/CD 流水线配置', 'GitHub Actions 自动化 CI/CD 流水线配置。', 'DevOps', '["CI/CD", "GitHub Actions", "自动化", "部署"]'),
        ('Prometheus 监控配置', 'Prometheus + Grafana 监控系统搭建教程。', 'DevOps', '["监控", "Prometheus", "Grafana", "告警"]'),
        ('Ansible 自动化脚本', 'Ansible 自动化运维脚本集合。', 'DevOps', '["Ansible", "自动化", "运维", "配置管理"]'),
        ('Linux 性能优化指南', 'Linux 服务器性能分析与优化实战指南。', 'DevOps', '["Linux", "性能优化", "服务器", "调优"]'),
        ('Nginx 配置大全', '常用 Nginx 配置模板，含反向代理、负载均衡。', 'DevOps', '["Nginx", "反向代理", "负载均衡", "Web 服务器"]'),
        ('Git 工作流最佳实践', 'Git Flow、分支管理、Code Review 流程规范。', 'DevOps', '["Git", "工作流", "版本控制", "协作"]'),
        ('日志收集 ELK Stack', 'Elasticsearch + Logstash + Kibana 日志收集方案。', 'DevOps', '["ELK", "日志", "Elasticsearch", "监控"]'),
        ('云原生架构指南', '微服务、Service Mesh、云原生架构设计指南。', 'DevOps', '["云原生", "微服务", "架构", "Service Mesh"]'),
    ]
    
    insert_sql = text("""
        INSERT INTO skills 
        (name, description, category, tags, file_path, file_size, download_count, use_count, created_at)
        VALUES 
        (:name, :description, :category, :tags, :file_path, :file_size, 0, 0, :created_at)
    """)
    
    for i, (name, description, category, tags) in enumerate(skills_data, 1):
        filename = f"skill_{i:03d}_{name[:30].replace(' ', '_')}.txt"
        
        try:
            session.execute(insert_sql, {
                'name': name,
                'description': description,
                'category': category,
                'tags': tags,
                'file_path': filename,
                'file_size': 1024,
                'created_at': datetime.now()
            })
            print(f"   ✅ [{i}/50] {name}")
        except Exception as e:
            print(f"   ❌ [{i}/50] {name} - {e}")

# 延迟导入和初始化（避免 gunicorn 启动时的问题）
def get_db_session():
    """获取数据库会话"""
    from models import init_db
    return init_db(DATABASE_URL)

def get_services():
    """获取服务实例"""
    from services import UserService, SkillService, RecommendationService
    db = get_db_session()
    return UserService(db), SkillService(db), RecommendationService(db)

# 默认用户名和头像列表
DEFAULT_USERNAMES = ['小龙虾', '技能达人', '探索者', '创新者', '学习家', '分享者', '实践者', '收藏家']
DEFAULT_AVATARS = [
    '🦞', '🚀', '⭐', '🎯', '💡', '🔥', '✨', '🌟', '🎨', ''
]

def get_or_create_auto_user():
    """自动创建或获取默认用户"""
    from models import User  # 导入 User 模型
    
    try:
        if 'user_id' not in session:
            username = f"{random.choice(DEFAULT_USERNAMES)}_{random.randint(1000, 9999)}"
            avatar = random.choice(DEFAULT_AVATARS)
            
            user_service, _, _ = get_services()
            user = user_service.get_or_create_user(username, email=None)
            user.avatar = avatar
            user_service.session.commit()
            
            # 存入 session
            session['user_id'] = user.id
            session['username'] = user.username
            session['avatar'] = avatar
        
        user_service, _, _ = get_services()
        return user_service.session.query(User).get(session.get('user_id'))
    except Exception as e:
        print(f"❌ User creation failed: {e}")
        raise


@app.route('/')
def index():
    """首页"""
    # 确保数据库已初始化
    initialize_database()
    
    # 自动登录
    user = get_or_create_auto_user()
    user_service, skill_service, recommendation_service = get_services()
    
    recommendations = []
    if user:
        # 获取今日推荐
        recommendations = recommendation_service.generate_daily_recommendations(user.id)
    
    # 获取热门技能
    popular_skills = skill_service.search_skills(sort_by='download_count')[:10]
    
    # 获取最新技能
    new_skills = skill_service.search_skills(sort_by='created_at')[:10]
    
    return render_template('index.html', 
                         user=user,
                         popular_skills=popular_skills,
                         new_skills=new_skills,
                         recommendations=recommendations)


@app.route('/logout')
def logout():
    """登出（重新分配新用户）"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/skills')
def skills():
    """技能列表页"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    sort_by = request.args.get('sort', 'created_at')
    
    # 自动登录
    user = get_or_create_auto_user()
    _, skill_service, _ = get_services()
    
    skills = skill_service.search_skills(
        query=query,
        category=category,
        sort_by=sort_by
    )
    
    categories = skill_service.get_categories()
    
    return render_template('skills.html',
                         skills=skills,
                         categories=categories,
                         current_category=category,
                         current_sort=sort_by,
                         query=query,
                         user=user)


@app.route('/skill/<int:skill_id>')
def skill_detail(skill_id):
    """技能详情页"""
    # 自动登录
    user = get_or_create_auto_user()
    _, skill_service, _ = get_services()
    
    skill = skill_service.get_skill(skill_id)
    if not skill:
        return "Skill not found", 404
    
    from models import User
    uploader = get_db_session().query(User).get(skill.uploader_id)
    
    return render_template('skill_detail.html',
                         skill=skill,
                         uploader=uploader,
                         user=user)


@app.route('/skill/<int:skill_id>/download')
def download_skill(skill_id):
    """下载技能"""
    # 自动登录
    user = get_or_create_auto_user()
    _, skill_service, _ = get_services()
    
    file_path = skill_service.download_skill(skill_id, user.id)
    if not file_path:
        return jsonify({'error': 'Skill not found'}), 404
    
    return send_file(file_path, as_attachment=True)


@app.route('/skill/<int:skill_id>/use', methods=['POST'])
def use_skill(skill_id):
    """记录技能使用"""
    # 自动登录
    user = get_or_create_auto_user()
    _, skill_service, _ = get_services()
    
    data = request.get_json()
    duration = data.get('duration', 0)
    success = data.get('success', True)
    
    skill_service.record_usage(skill_id, user.id, duration, success)
    return jsonify({'success': True})


@app.route('/upload', methods=['GET', 'POST'])
def upload_skill():
    """上传技能"""
    # 自动登录
    user = get_or_create_auto_user()
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        tags = request.form.get('tags', '').split(',')
        author = request.form.get('author')
        
        if 'file' not in request.files:
            return jsonify({'error': '请选择文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '请选择文件'}), 400
        
        # 保存临时文件
        temp_path = os.path.join('/tmp', file.filename)
        file.save(temp_path)
        
        # 上传技能
        _, skill_service, _ = get_services()
        skill = skill_service.upload_skill(
            name=name,
            description=description,
            file_path=temp_path,
            uploader_id=user.id,
            category=category,
            tags=[t.strip() for t in tags if t.strip()],
            author=author
        )
        
        return redirect(url_for('skill_detail', skill_id=skill.id))
    
    return render_template('upload.html', user=user)


@app.route('/profile')
def profile():
    """个人主页"""
    from models import PointsHistory
    from sqlalchemy import desc
    
    # 自动登录
    user = get_or_create_auto_user()
    user_service, _, _ = get_services()
    
    stats = user_service.get_user_stats(user.id)
    
    # 获取积分历史
    points_history = user_service.session.query(PointsHistory).filter_by(
        user_id=user.id
    ).order_by(desc(PointsHistory.created_at)).limit(20).all()
    
    return render_template('profile.html',
                         stats=stats,
                         user=user,
                         points_history=points_history)


# ==================== 社区功能路由 ====================

@app.route('/community')
def community():
    """社区首页"""
    from models import CommunityPost
    from sqlalchemy import desc, func
    
    # 自动登录
    user = get_or_create_auto_user()
    user_service, _, _ = get_services()
    
    # 获取分类参数
    category = request.args.get('category', 'all')
    page = int(request.args.get('page', 1))
    per_page = 20
    
    # 查询帖子
    query = user_service.session.query(CommunityPost)
    
    if category != 'all':
        query = query.filter(CommunityPost.category == category)
    
    # 排序：置顶优先，然后按时间
    posts = query.order_by(
        desc(CommunityPost.is_pinned),
        desc(CommunityPost.created_at)
    ).offset((page - 1) * per_page).limit(per_page).all()
    
    # 统计总数
    total_posts = query.count()
    
    # 统计各分类帖子数
    category_stats = user_service.session.query(
        CommunityPost.category,
        func.count(CommunityPost.id)
    ).group_by(CommunityPost.category).all()
    
    return render_template('community.html',
                         posts=posts,
                         user=user,
                         current_category=category,
                         category_stats=dict(category_stats),
                         total_posts=total_posts,
                         page=page,
                         per_page=per_page)


@app.route('/community/post/<int:post_id>')
def view_post(post_id):
    """查看帖子详情"""
    from models import CommunityPost, CommunityComment, CommunityLike
    
    # 自动登录
    user = get_or_create_auto_user()
    user_service, _, _ = get_services()
    
    post = user_service.session.query(CommunityPost).get(post_id)
    if not post:
        return "帖子不存在", 404
    
    # 增加浏览数
    post.view_count += 1
    user_service.session.commit()
    
    # 获取评论（只获取顶级评论）
    comments = user_service.session.query(CommunityComment).filter_by(
        post_id=post_id,
        parent_id=None
    ).order_by(desc(CommunityComment.created_at)).all()
    
    # 检查当前用户是否已点赞
    has_liked = False
    if user:
        has_liked = user_service.session.query(CommunityLike).filter_by(
            post_id=post_id,
            user_id=user.id
        ).first() is not None
    
    return render_template('post_detail.html',
                         post=post,
                         comments=comments,
                         user=user,
                         has_liked=has_liked)


@app.route('/community/create', methods=['GET', 'POST'])
def create_post():
    """创建新帖子"""
    from models import CommunityPost
    
    # 自动登录
    user = get_or_create_auto_user()
    user_service, _, _ = get_services()
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        category = request.form.get('category', 'general')
        tags = request.form.get('tags', '').split(',')
        
        if not title or not content:
            return jsonify({'error': '标题和内容不能为空'}), 400
        
        # 创建帖子
        post = CommunityPost(
            title=title,
            content=content,
            author_id=user.id,
            category=category,
            tags=[t.strip() for t in tags if t.strip()]
        )
        
        user_service.session.add(post)
        user_service.session.commit()
        
        return redirect(url_for('view_post', post_id=post.id))
    
    return render_template('create_post.html', user=user)


@app.route('/api/community/post/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    """点赞帖子"""
    from models import CommunityPost, CommunityLike
    
    # 自动登录
    user = get_or_create_auto_user()
    user_service, _, _ = get_services()
    
    # 检查是否已点赞
    existing_like = user_service.session.query(CommunityLike).filter_by(
        post_id=post_id,
        user_id=user.id
    ).first()
    
    if existing_like:
        # 取消点赞
        user_service.session.delete(existing_like)
        post = user_service.session.query(CommunityPost).get(post_id)
        post.like_count -= 1
        liked = False
    else:
        # 添加点赞
        like = CommunityLike(post_id=post_id, user_id=user.id)
        user_service.session.add(like)
        post = user_service.session.query(CommunityPost).get(post_id)
        post.like_count += 1
        liked = True
    
    user_service.session.commit()
    
    return jsonify({
        'success': True,
        'liked': liked,
        'like_count': post.like_count
    })


@app.route('/api/community/comment', methods=['POST'])
def add_comment():
    """添加评论"""
    from models import CommunityComment, CommunityPost
    
    # 自动登录
    user = get_or_create_auto_user()
    user_service, _, _ = get_services()
    
    data = request.get_json()
    post_id = data.get('post_id')
    content = data.get('content')
    parent_id = data.get('parent_id')
    
    if not content:
        return jsonify({'error': '评论内容不能为空'}), 400
    
    # 检查帖子是否存在且未锁定
    post = user_service.session.query(CommunityPost).get(post_id)
    if not post or post.is_locked:
        return jsonify({'error': '帖子不存在或已锁定'}), 404
    
    # 创建评论
    comment = CommunityComment(
        post_id=post_id,
        author_id=user.id,
        content=content,
        parent_id=parent_id
    )
    
    user_service.session.add(comment)
    
    # 增加帖子的评论数
    post.comment_count += 1
    user_service.session.commit()
    
    return jsonify({
        'success': True,
        'comment_id': comment.id,
        'content': comment.content,
        'author': user.username,
        'avatar': user.avatar,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
    })


@app.route('/api/recommendations/accept', methods=['POST'])
def accept_recommendation():
    """接受推荐"""
    # 自动登录
    user = get_or_create_auto_user()
    _, _, recommendation_service = get_services()
    
    data = request.get_json()
    skill_id = data.get('skill_id')
    
    recommendation_service.accept_recommendation(user.id, skill_id)
    return jsonify({'success': True})


@app.route('/api/stats')
def get_stats():
    """获取平台统计"""
    from sqlalchemy import func
    from models import User, Skill, DownloadHistory
    
    db = get_db_session()
    total_skills = db.query(func.count(Skill.id)).scalar()
    total_users = db.query(func.count(User.id)).scalar()
    total_downloads = db.query(func.count(DownloadHistory.id)).scalar()
    
    return jsonify({
        'total_skills': total_skills,
        'total_users': total_users,
        'total_downloads': total_downloads
    })


@app.route('/admin/init-skills', methods=['GET'])
def admin_init_skills():
    """管理员初始化技能数据（临时路由）"""
    from sqlalchemy import text, inspect
    
    # 简单权限检查（生产环境应该用更好的认证）
    token = request.args.get('token', '')
    if token != 'lobster_admin_2024_secret':
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        db = get_db_session()
        
        # 检查表是否存在
        inspector = inspect(db.bind)
        tables = inspector.get_table_names()
        
        if 'skills' not in tables:
            return jsonify({'error': 'Skills table not found'}), 404
        
        # 检查是否已有数据
        result = db.execute(text("SELECT COUNT(*) FROM skills"))
        count = result.scalar()
        
        if count > 0:
            return jsonify({
                'message': f'Database already has {count} skills',
                'action': 'skipped'
            })
        
        # 执行插入
        print("\n📦 Admin API: Inserting 50 skills...")
        run_initial_data_insert(db)
        db.commit()
        
        # 验证结果
        result = db.execute(text("SELECT COUNT(*) FROM skills"))
        new_count = result.scalar()
        
        return jsonify({
            'message': f'Successfully inserted {new_count} skills',
            'action': 'inserted',
            'count': new_count
        })
        
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500


if __name__ == '__main__':
    print(f"🦞 龙虾 Skill 合集平台启动中...")
    print(f"访问地址：http://{HOST}:{PORT}")
    # Render 使用 gunicorn，本地开发使用 Flask 内置服务器
    app.run(host=HOST, port=PORT, debug=DEBUG)
