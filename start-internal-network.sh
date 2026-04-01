#!/bin/bash

echo "=========================================="
echo "🦞 龙虾 Skill 平台 - 内网访问模式"
echo "=========================================="
echo ""

# 激活虚拟环境
source venv/bin/activate

# 获取本机主要内网 IP
PRIMARY_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | grep "30\." | head -1 | awk '{print $2}')

if [ -z "$PRIMARY_IP" ]; then
    PRIMARY_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -1 | awk '{print $2}')
fi

echo "📍 检测到主要 IP: $PRIMARY_IP"
echo ""
echo "🌐 服务启动信息:"
echo "   - 本地访问：http://localhost:5000"
echo "   - 内网访问：http://$PRIMARY_IP:5000"
echo ""
echo "📋 请将以下地址发送给内网同事:"
echo "   http://$PRIMARY_IP:5000"
echo ""
echo "⚠️  如果内网同事仍无法访问，请检查:"
echo "   1. 公司防火墙是否开放 5000 端口"
echo "   2. 是否在同一个 VLAN/网段"
echo "   3. macOS 防火墙设置"
echo ""
echo "🚀 备选方案：运行 ./check-network.sh 进行诊断"
echo "=========================================="
echo ""

# 启动 Flask 应用
python app.py
