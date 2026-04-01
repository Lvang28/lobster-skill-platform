#!/bin/bash
# 龙虾 Skill 合集平台 - 快速启动脚本

echo "🦞 龙虾 Skill 合集平台"
echo "======================"
echo ""

# 检查 Python 环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

echo "✓ Python 版本：$(python3 --version)"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -r requirements.txt -q

# 创建数据目录
echo "📁 初始化数据目录..."
mkdir -p data/skills data/users data/backups

# 启动应用
echo ""
echo "🚀 启动 Web 服务..."
echo "访问地址：http://127.0.0.1:5000"
echo "按 Ctrl+C 停止服务"
echo ""

python app.py
