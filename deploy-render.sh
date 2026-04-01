#!/bin/bash

echo "=========================================="
echo "🦞 龙虾 Skill 平台 - Render 云部署"
echo "=========================================="
echo ""
echo "📱 Render.com 优势："
echo "   ✅ 完全免费（无需信用卡）"
echo "   ✅ 自动 HTTPS"
echo "   ✅ 永久公网 URL"
echo "   ✅ 自动部署"
echo "   ✅ 内置数据库存储"
echo ""
echo "=========================================="
echo ""

# 检查 Git
if ! command -v git &> /dev/null; then
    echo "❌ 需要安装 Git"
    echo "请运行：brew install git"
    exit 1
fi

# 初始化 Git 仓库（如果还没有）
if [ ! -d ".git" ]; then
    echo "📂 初始化 Git 仓库..."
    git init
    git add .
    git commit -m "Initial commit - Lobster Skill Platform"
    echo "✅ Git 仓库已初始化"
else
    echo "✅ Git 仓库已存在"
fi

echo ""
echo "=========================================="
echo "🚀 部署步骤："
echo "=========================================="
echo ""
echo "Step 1: 访问 https://render.com 并注册账号（支持 GitHub 登录）"
echo ""
echo "Step 2: 点击 'New +' → 'Blueprint'"
echo ""
echo "Step 3: 连接您的 GitHub 仓库"
echo "        （或者将代码上传到 GitHub 后连接）"
echo ""
echo "Step 4: Render 会自动识别 render.yaml 并部署！"
echo ""
echo "=========================================="
echo ""
echo "💡 快速上传到 GitHub 的方法："
echo ""
echo "   # 创建 GitHub 仓库（在 github.com 上）"
echo "   # 然后执行："
echo "   git remote add origin https://github.com/YOUR_USERNAME/lobster-skill-platform.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "   # 然后在 Render 连接这个仓库即可"
echo ""
echo "=========================================="
echo ""
echo "🎯 部署完成后您会获得："
echo "   - 永久公网 URL: https://lobster-skill-xxxx.onrender.com"
echo "   - 直接分享给任何人，无需安装任何东西！"
echo ""
