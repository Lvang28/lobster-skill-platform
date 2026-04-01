#!/bin/bash

echo "=========================================="
echo "🦞 龙虾 Skill 平台 - 公网访问模式"
echo "=========================================="
echo ""

# 停止旧的 cloudflared 进程
pkill cloudflared 2>/dev/null
sleep 1

# 检查 Flask 是否在运行
if ! lsof -i:5000 >/dev/null 2>&1; then
    echo "🚀 正在启动 Flask 服务器..."
    cd /Users/lvang/.qoderwork/workspace/mnfoi60u4zvyxkz5/lobster-skill-platform
    source venv/bin/activate
    python app.py &
    FLASK_PID=$!
    sleep 3
    
    # 检查是否启动成功
    if ! lsof -i:5000 >/dev/null 2>&1; then
        echo "❌ Flask 启动失败"
        exit 1
    fi
    echo "✅ Flask 服务器已启动 (PID: $FLASK_PID)"
else
    echo "✅ Flask 服务器已在运行"
fi

echo ""
echo "🌐 正在启动 Cloudflare Tunnel..."
echo ""

# 启动 cloudflared
cd /Users/lvang/.qoderwork/workspace/mnfoi60u4zvyxkz5/lobster-skill-platform
cloudflared tunnel --url http://localhost:5000 2>&1 | tee /tmp/cloudflared.log &
TUNNEL_PID=$!

# 等待 URL 生成
sleep 6

# 提取并显示 URL
URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' /tmp/cloudflared.log | tail -1)

if [ -n "$URL" ]; then
    echo ""
    echo "=========================================="
    echo "✅ 部署成功！"
    echo "=========================================="
    echo ""
    echo "🌐 您的公网访问地址："
    echo ""
    echo "   $URL"
    echo ""
    echo "=========================================="
    echo "📱 现在可以把这个 URL 发给任何人了！"
    echo ""
    echo "   ✅ 无需安装任何东西"
    echo "   ✅ 直接浏览器访问"
    echo "   ✅ 内网外网都能访问"
    echo "   ✅ 阿里同事也能访问"
    echo ""
    echo "=========================================="
    echo ""
    echo "💡 提示："
    echo "   - 按 Ctrl+C 停止所有服务"
    echo "   - 下次运行 ./start-public.sh 会使用同一个 URL"
    echo "   - Flask PID: $FLASK_PID"
    echo "   - Tunnel PID: $TUNNEL_PID"
    echo ""
    
    # 保持进程运行
    wait $TUNNEL_PID
else
    echo "❌ 无法获取 URL"
    echo "日志:"
    cat /tmp/cloudflared.log
fi
