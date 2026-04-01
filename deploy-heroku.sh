#!/bin/bash
# 龙虾 Skill 平台 - Heroku 一键部署脚本

echo "🦞 龙虾 Skill 平台 - Heroku 云部署"
echo "===================================="
echo ""

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ 需要安装 Git"
    echo "请运行：brew install git"
    exit 1
fi

# 检查 Heroku CLI
if ! command -v heroku &> /dev/null; then
    echo "📦 正在安装 Heroku CLI..."
    brew tap heroku/brew && brew install heroku
fi

echo "✅ 环境检查通过"
echo ""

# 登录 Heroku
echo "🔐 登录 Heroku..."
heroku login

# 创建应用名称
APP_NAME="lobster-skill-$(date +%s)"
echo ""
echo "📝 应用名称：$APP_NAME"
echo ""

# 初始化 Git（如果还没有）
if [ ! -d ".git" ]; then
    echo "📂 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit - Lobster Skill Platform"
fi

# 创建 Heroku 应用
echo "🚀 创建 Heroku 应用..."
heroku create $APP_NAME

# 设置环境变量
echo "⚙️  配置环境变量..."
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set FLASK_DEBUG=False
heroku config:set PYTHONUNBUFFERED=1

# 添加 PostgreSQL 数据库
echo "📊 添加 PostgreSQL 数据库..."
heroku addons:create heroku-postgresql:mini

# 等待数据库就绪
sleep 5

# 获取数据库 URL
DATABASE_URL=$(heroku config:get DATABASE_URL)

# 更新本地配置（可选）
echo "💾 保存数据库配置..."
export DATABASE_URL=$DATABASE_URL

# 推送代码
echo "📤 推送到 Heroku..."
git push heroku main

# 初始化数据库
echo "🗄️  初始化数据库..."
heroku run "python -c \"from models import init_db; from config_prod import DATABASE_URL; init_db(DATABASE_URL); print('✅ 数据库初始化成功')\""

# 打开应用
echo ""
echo "🎉 部署完成！"
echo ""
echo "🌐 访问地址："
heroku open

echo ""
echo "📱 分享链接："
heroku apps:info --shell | grep web_url

echo ""
echo "💡 提示："
echo "   - 查看日志：heroku logs --tail"
echo "   - 重启应用：heroku restart"
echo "   - 查看配置：heroku config"
echo "   - 删除应用：heroku apps:destroy --app $APP_NAME --confirm $APP_NAME"
echo ""
