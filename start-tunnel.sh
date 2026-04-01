#!/bin/bash
# 龙虾 Skill 平台 - 外网访问助手（使用 locatunnel，更可靠）

echo "🦞 龙虾 Skill 平台 - 外网访问助手"
echo "=================================="
echo ""

# 检查 node/npm 是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ 需要安装 Node.js/npm"
    echo ""
    echo "请先安装 Node.js:"
    echo "  macOS: brew install node"
    echo "  或访问：https://nodejs.org/"
    exit 1
fi

# 全局安装 localtunnel（如果未安装）
if ! command -v lt &> /dev/null; then
    echo "📦 正在安装 localtunnel..."
    npm install -g localtunnel --silent
fi

if command -v lt &> /dev/null; then
    echo "✅ localtunnel 已安装"
else
    echo "⚠️  安装失败，尝试直接使用 npx..."
fi

echo ""
echo "🚀 启动平台..."
cd "$(dirname "$0")"

# 检查平台是否已在运行
if lsof -i:5000 | grep -q LISTEN; then
    echo "✓ 平台已在运行"
else
    echo "📡 启动 Flask 应用..."
    source venv/bin/activate
    python app.py > /tmp/flask.log 2>&1 &
    FLASK_PID=$!
    sleep 3
    
    if ps -p $FLASK_PID > /dev/null; then
        echo "✓ 平台已启动 (PID: $FLASK_PID)"
    else
        echo "❌ 平台启动失败"
        cat /tmp/flask.log
        exit 1
    fi
fi

echo ""
echo "🌐 启动 Localtunnel..."
echo ""
echo "⏳ 正在生成公网 URL..."
echo ""

# 使用 npx 运行 localtunnel
npx localtunnel --port 5000 2>&1 | while read line; do
    echo "$line"
    
    # 提取 URL
    if [[ $line =~ https://[a-zA-Z0-9.-]+\.loca\.li\s ]]; then
        URL="${BASH_REMATCH[0]}"
        echo ""
        echo "=========================================="
        echo "✅ 成功！"
        echo "=========================================="
        echo ""
        echo "🌐 公网访问地址："
        echo "   $URL"
        echo ""
        echo "📱 把这个 URL 发给朋友即可访问！"
        echo ""
        echo "⚠️  按 Ctrl+C 停止服务"
        echo ""
        echo "💡 提示："
        echo "   - 第一次访问会显示安全警告，点击'Advanced' -> 'Proceed'"
        echo "   - URL 每次启动都会变化"
        echo ""
        
        # 保存到文件
        echo "$URL" > /tmp/loca_url.txt
        
        break
    fi
done

# 清理函数
cleanup() {
    echo ""
    echo "🛑 正在停止隧道..."
    pkill -f "localtunnel|lt" 2>/dev/null
    exit 0
}

trap cleanup SIGINT SIGTERM

# 保持运行
wait
