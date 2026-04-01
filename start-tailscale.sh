#!/bin/bash

echo "=========================================="
echo "🦞 龙虾 Skill 平台 - Tailscale 启动"
echo "=========================================="
echo ""

# 检查 Tailscale 状态
if ! tailscale status >/dev/null 2>&1; then
    echo "⚠️  Tailscale 尚未运行！"
    echo ""
    echo "请执行以下命令启动 Tailscale："
    echo ""
    echo "   sudo tailscale up"
    echo ""
    echo "然后复制输出的 URL 到浏览器登录（支持 Google/微软/GitHub 账号）"
    echo ""
    echo "登录后，再次运行此脚本查看您的 Tailscale IP"
    echo "=========================================="
    exit 1
fi

# 获取 Tailscale IP
TS_IP=$(tailscale ip | head -1)

if [ -z "$TS_IP" ]; then
    echo "⚠️  Tailscale 未连接或尚未分配 IP"
    echo ""
    echo "请运行：sudo tailscale up"
    echo "然后在浏览器中完成登录"
    exit 1
fi

echo "✅ Tailscale 已连接！"
echo ""
echo "📍 您的 Tailscale IP: $TS_IP"
echo ""
echo "🌐 访问地址："
echo ""
echo "   您自己访问："
echo "   http://localhost:5000"
echo ""
echo "   同事通过 Tailscale 访问（推荐，最稳定）："
echo "   http://$TS_IP:5000"
echo ""
echo "=========================================="
echo "📋 给同事的访问说明："
echo "=========================================="
echo ""
echo "1. 安装 Tailscale："
echo "   brew install tailscale"
echo "   sudo tailscale up"
echo ""
echo "2. 使用同一个账号登录"
echo ""
echo "3. 访问地址："
echo "   http://$TS_IP:5000"
echo ""
echo "=========================================="
echo "🚀 正在启动龙虾 Skill 平台..."
echo "=========================================="
echo ""

# 激活虚拟环境并启动
source venv/bin/activate
python app.py
