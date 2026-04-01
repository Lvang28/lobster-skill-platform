#!/bin/bash

echo "=========================================="
echo "龙虾 Skill 平台 - 内网访问诊断工具"
echo "=========================================="
echo ""

# 获取本机 IP 地址
echo "📍 本机 IP 地址:"
ifconfig | grep "inet " | grep -v 127.0.0.1 | while read line; do
    echo "   $line"
done
echo ""

# 检查端口占用
echo "🔌 端口 5000 状态:"
lsof -i :5000 | head -5
if [ $? -ne 0 ]; then
    echo "   端口 5000 未被占用"
fi
echo ""

# 检查防火墙状态
echo "🔥 防火墙状态:"
if command -v ufw &> /dev/null; then
    ufw status 2>/dev/null || echo "   无法获取防火墙状态"
elif command -v firewall-cmd &> /dev/null; then
    firewall-cmd --state 2>/dev/null || echo "   无法获取防火墙状态"
else
    echo "   macOS (ipfw 或 pf)"
    sudo pfctl -s info 2>/dev/null | head -3 || echo "   无法获取防火墙状态"
fi
echo ""

# 测试本地访问
echo "🧪 测试本地访问:"
curl -s -o /dev/null -w "   HTTP 状态码：%{http_code}\n   响应时间：%{time_total}s\n" http://localhost:5000 || echo "   无法访问 localhost:5000"
echo ""

# 生成访问 URL 列表
echo "📋 请尝试以下 URL 访问（从其他内网机器）:"
echo ""
ifconfig | grep "inet " | grep -v 127.0.0.1 | grep -v "inet6" | while read -r line; do
    ip=$(echo $line | awk '{print $2}')
    echo "   http://$ip:5000"
done
echo ""

echo "=========================================="
echo "💡 内网访问故障排查建议:"
echo "=========================================="
echo "1. 确保服务器和访问者在同一内网网段"
echo "2. 检查公司防火墙是否开放 5000 端口"
echo "3. 尝试关闭 macOS 防火墙："
echo "   sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off"
echo ""
echo "4. 如果以上都不行，使用内网穿透方案（见下方）"
echo "=========================================="
echo ""

# 提供内网穿透备选方案
echo "🚀 备选方案：使用 frp 内网穿透（推荐用于阿里内网）"
echo ""
echo "方案 A: 使用阿里云 FRP 服务（最稳定）"
echo "   1. 在阿里云 ECS 上部署 frps (frp server)"
echo "   2. 本地运行 frpc 连接到阿里云"
echo "   3. 同事通过阿里云公网 IP 访问"
echo ""
echo "方案 B: 使用 Tailscale 组建虚拟局域网"
echo "   1. brew install tailscale"
echo "   2. sudo tailscale up"
echo "   3. 同事也安装 tailscale 并登录同一账号"
echo "   4. 通过 tailscale IP 访问（不受物理网络限制）"
echo ""
echo "方案 C: 使用 ngrok 企业版"
echo "   1. 注册 ngrok 账号"
echo "   2. ./ngrok http 5000 -region=ap"
echo ""
