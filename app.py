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


if __name__ == '__main__':
    print(f"🦞 龙虾 Skill 合集平台启动中...")
    print(f"访问地址：http://{HOST}:{PORT}")
    # Render 使用 gunicorn，本地开发使用 Flask 内置服务器
    app.run(host=HOST, port=PORT, debug=DEBUG)
