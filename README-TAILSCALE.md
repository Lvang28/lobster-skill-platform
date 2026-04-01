# Tailscale 内网穿透方案（推荐用于阿里内网访问）

## 为什么使用 Tailscale？

传统的端口开放方式在阿里内网可能会遇到：
- 公司防火墙限制
- VLAN 隔离
- 安全策略禁止开放端口

Tailscale 通过在设备上安装软件，组建一个**虚拟的私有局域网**，不受物理网络拓扑限制。

## 部署步骤

### 1. 服务器端（运行龙虾平台的机器）

```bash
# 安装 Tailscale
brew install tailscale

# 启动并登录
sudo tailscale up

# 复制输出的 URL，在浏览器中登录（支持 Google/Microsoft/GitHub 账号）

# 查看分配的 Tailscale IP
tailscale ip
```

### 2. 同事端（访问者）

每位需要访问的同事都需要：

```bash
# macOS
brew install tailscale
sudo tailscale up

# 或者 Windows/Linux
# 从 https://tailscale.com/download 下载安装包
```

登录**同一个 Tailscale 账号**（或加入同一个 Tailscale 网络）。

### 3. 访问平台

登录后，每台设备都会获得一个 `100.x.y.z` 的 Tailscale IP。

**服务器端查看自己的 Tailscale IP：**
```bash
tailscale ip
# 输出类似：100.87.45.123
```

**同事访问：**
```
http://100.87.45.123:5000
```

## 优势

✅ **无需开放防火墙端口** - Tailscale 使用打洞技术穿透 NAT  
✅ **加密传输** - 所有流量通过 WireGuard 加密  
✅ **稳定可靠** - 不依赖第三方隧道服务  
✅ **免费** - 个人使用完全免费（最多 20 台设备 +3 个用户）  
✅ **阿里内网友好** - 不受公司网络策略限制  

## 管理 Tailscale

```bash
# 查看网络状态
tailscale status

# 查看本机 IP
tailscale ip

# 停止
sudo tailscale down

# 注销
sudo tailscale logout
```

## 自动化脚本

创建 `start-with-tailscale.sh`:

```bash
#!/bin/bash

# 检查 Tailscale 是否运行
if ! tailscale status >/dev/null 2>&1; then
    echo "⚠️  Tailscale 未运行，正在启动..."
    sudo tailscale up
fi

TS_IP=$(tailscale ip | head -1)
echo "✓ Tailscale IP: $TS_IP"
echo ""
echo "🌐 访问地址:"
echo "   - Tailscale: http://$TS_IP:5000 (推荐，最稳定)"
echo ""

source venv/bin/activate
python app.py
```

## 故障排查

**问题 1: 同事看不到服务器**
```bash
# 服务器端执行
tailscale status

# 确认同事的设备在列表中
```

**问题 2: 连接超时**
```bash
# 检查防火墙
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off

# 重启 Tailscale
sudo tailscale down
sudo tailscale up
```

**问题 3: 速度较慢**
- Tailscale 会优先尝试 P2P 直连
- 如果直连失败会通过中继服务器（速度较慢）
- 确保 UDP 端口开放以改善连接质量
