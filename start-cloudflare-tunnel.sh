#!/bin/bash

echo "=========================================="
echo "🦞 龙虾 Skill 平台 - Cloudflare Tunnel"
echo "=========================================="
echo ""
echo "正在启动 Cloudflare Tunnel..."
echo ""
echo "⏳ 请稍等，正在获取公网 URL..."
echo ""

# 启动 cloudflared 并捕获输出
cloudflared tunnel --url http://localhost:5000 2>&1 | tee /tmp/cloudflared.log &
TUNNEL_PID=$!

# 等待 URL 生成
sleep 5

# 提取 URL
URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' /tmp/cloudflared.log | head -1)

if [ -n "$URL" ]; then
    echo ""
    echo "=========================================="
    echo "✅ Tunnel 启动成功！"
    echo "=========================================="
    echo ""
    echo "🌐 您的公网访问地址："
    echo ""
    echo "   $URL"
    echo ""
    echo "=========================================="
    echo "📱 现在可以把这个 URL 发给任何人了！"
    echo "   - 无需安装任何东西"
    echo "   - 直接浏览器访问"
    echo "   - 内网外网都能访问"
    echo "=========================================="
    echo ""
    echo "💡 提示："
    echo "   - 按 Ctrl+C 停止隧道"
    echo "   - 每次启动 URL 相同（只要不删除 ~/.cloudflared）"
    echo ""
    
    # 保持进程运行
    wait $TUNNEL_PID
else
    echo "❌ 无法获取 URL，请检查日志"
    cat /tmp/cloudflared.log
fi
