#!/bin/bash
# 龙虾 Skill 平台 - ngrok 外网访问快速启动脚本

echo "🦞 龙虾 Skill 平台 - 外网访问助手"
echo "=================================="
echo ""

# 检查 ngrok 是否安装
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok 未安装，正在安装..."
    
    # macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ngrok
    # Linux
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
        tar xzf ngrok-v3-stable-linux-amd64.tgz
        sudo mv ngrok /usr/local/bin/
        rm ngrok-v3-stable-linux-amd64.tgz
    else
        echo "请手动安装 ngrok: https://ngrok.com/download"
        exit 1
    fi
fi

echo "✓ ngrok 已安装"
echo ""

# 启动 Flask 应用（后台）
echo "🚀 启动平台..."
source venv/bin/activate
python app.py &
FLASK_PID=$!

sleep 5

# 检查平台是否启动成功
if ps -p $FLASK_PID > /dev/null; then
    echo "✓ 平台已启动 (PID: $FLASK_PID)"
else
    echo "❌ 平台启动失败"
    exit 1
fi

echo ""
echo "🌐 启动 ngrok 隧道..."
echo ""

# 启动 ngrok
ngrok http 5000

# 清理
kill $FLASK_PID 2>/dev/null
