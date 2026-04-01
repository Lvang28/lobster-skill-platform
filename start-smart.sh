#!/bin/bash

echo "=========================================="
echo "🦞 龙虾 Skill 平台 - 智能启动"
echo "=========================================="
echo ""

# 激活虚拟环境
source venv/bin/activate

# 获取各种 IP 地址
LOCALHOST="localhost"
IP_30=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | grep "30\." | head -1 | awk '{print $2}')
IP_192=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | grep "192\." | head -1 | awk '{print $2}')
OTHER_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | grep -v "30\." | grep -v "192\." | head -1 | awk '{print $2}')

echo "📍 网络接口检测:"
[ -n "$IP_30" ] && echo "   阿里内网 IP: $IP_30"
[ -n "$IP_192" ] && echo "   私有网络 IP: $IP_192"
[ -n "$OTHER_IP" ] && echo "   其他 IP: $OTHER_IP"
echo ""

# 检查 Tailscale
TS_IP=""
if command -v tailscale &> /dev/null; then
    if tailscale status >/dev/null 2>&1; then
        TS_IP=$(tailscale ip | head -1)
        echo "✅ Tailscale 已连接：$TS_IP (最稳定)"
    else
        echo "⚠️  Tailscale 已安装但未连接"
        echo "   运行 'sudo tailscale up' 启用虚拟局域网"
    fi
else
    echo "ℹ️  未检测到 Tailscale（推荐安装以获得最佳内网访问体验）"
fi
echo ""

# 显示所有可用访问地址
echo "🌐 访问地址列表:"
echo ""
echo "   1. 本地访问:"
echo "      http://localhost:5000"
echo ""
if [ -n "$TS_IP" ]; then
    echo "   2. Tailscale 虚拟局域网 (推荐):"
    echo "      http://$TS_IP:5000"
    echo ""
fi
if [ -n "$IP_30" ]; then
    echo "   3. 阿里内网直连:"
    echo "      http://$IP_30:5000"
    echo ""
fi
if [ -n "$IP_192" ]; then
    echo "   4. 私有网络:"
    echo "      http://$IP_192:5000"
    echo ""
fi
if [ -n "$OTHER_IP" ]; then
    echo "   5. 其他网络:"
    echo "      http://$OTHER_IP:5000"
    echo ""
fi

echo "=========================================="
echo "💡 访问建议:"
echo "=========================================="
echo ""
echo "场景 A: 只有您自己使用"
echo "   → 访问 http://localhost:5000"
echo ""
echo "场景 B: 阿里内网同事访问（同一办公网）"
echo "   → 优先尝试 http://$IP_30:5000"
echo "   → 如失败，安装 Tailscale 后使用其 IP"
echo ""
echo "场景 C: 外网朋友访问"
echo "   → 使用 Tailscale（所有人都安装）"
echo "   → 或使用 ngrok/云部署"
echo ""
echo "场景 D: 大规模部署（多人长期访问）"
echo "   → 建议使用 Heroku/阿里云等云平台"
echo "   → 参考 deploy-heroku.sh"
echo ""
echo "=========================================="
echo ""

# 故障诊断提示
echo "🔧 如果内网访问失败，运行:"
echo "   ./check-network.sh"
echo ""
echo "📖 查看 Tailscale 详细配置:"
echo "   cat README-TAILSCALE.md"
echo ""
echo "=========================================="
echo "🚀 正在启动服务..."
echo "=========================================="
echo ""

# 启动 Flask 应用
python app.py
