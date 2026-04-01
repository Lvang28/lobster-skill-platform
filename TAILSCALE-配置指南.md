# 🦞 龙虾 Skill 平台 - Tailscale 配置指南

## ✅ Tailscale 已安装成功！

现在只需要 3 步就能完成配置：

---

## 🚀 第一步：启动 Tailscale（需要您手动执行）

在终端中运行：

```bash
sudo tailscale up
```

**说明：**
- 系统会提示输入密码（您的 Mac 登录密码）
- 或者使用 Touch ID 验证

---

## 🔐 第二步：浏览器登录

运行命令后，终端会输出一个 URL，类似这样：

```
https://login.tailscale.com/a/abc123def456...
```

**操作：**
1. 复制这个 URL
2. 粘贴到浏览器打开
3. 使用以下任一账号登录：
   - Google 账号
   - Microsoft 账号
   - GitHub 账号
   - Apple 账号

**重要：** 记住您使用的登录账号，同事需要用同一个账号！

---

## 📍 第三步：查看您的 Tailscale IP

登录后，回到终端运行：

```bash
tailscale ip
```

会输出类似这样的 IP：
```
100.87.45.123
```

这就是您的 **虚拟局域网 IP**！

---

## 🌐 访问地址

### 您自己访问：
```
http://localhost:5000
```

### 同事访问（通过 Tailscale）：
```
http://[您的 Tailscale IP]:5000
例如：http://100.87.45.123:5000
```

---

## 👥 给同事的访问说明

把以下内容发给需要访问的同事：

---

### 📋 同事安装指南

**Step 1: 安装 Tailscale**

macOS：
```bash
brew install tailscale
sudo tailscale up
```

Windows：
1. 下载安装包：https://tailscale.com/download
2. 安装并运行
3. 登录账号

Linux：
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

**Step 2: 登录同一账号**

使用与您**相同的 Tailscale 账号**登录。

**Step 3: 访问平台**

打开浏览器访问：
```
http://[您的 Tailscale IP]:5000
```

---

## 🎯 快速启动脚本

我已经创建了自动化脚本，以后只需运行：

```bash
cd /Users/lvang/.qoderwork/workspace/mnfoi60u4zvyxkz5/lobster-skill-platform
./start-tailscale.sh
```

这个脚本会：
- ✅ 自动检查 Tailscale 状态
- ✅ 显示您的 Tailscale IP
- ✅ 显示所有访问地址
- ✅ 提供同事访问说明
- ✅ 自动启动龙虾平台

---

## 📱 管理 Tailscale 设备

### 查看已连接设备：
```bash
tailscale status
```

### 查看本机 IP：
```bash
tailscale ip
```

### 注销账号：
```bash
sudo tailscale logout
```

### 停止服务：
```bash
sudo tailscale down
```

---

## 💡 常见问题

### Q: 可以几个人同时使用？
A: Tailscale 免费版支持：
- 最多 20 台设备
- 最多 3 个用户
- 完全够用！

### Q: 安全吗？
A: 非常安全：
- WireGuard 协议端到端加密
- 只有登录同一账号的人才能访问
- 不经过第三方服务器中转数据

### Q: 会影响公司网络安全策略吗？
A: 不会：
- Tailscale 使用出站连接
- 不违反任何入站防火墙规则
- 不需要开放任何端口

### Q: 如果同事不在同一个账号怎么办？
A: 有两种方式：
1. **共享账号**（简单）：所有人用同一个 Google/GitHub 账号登录
2. **创建团队**（正规）：在 tailscale.com 创建团队，邀请同事加入

### Q: Tailscale IP 会变吗？
A: 基本不变：
- 只要不注销账号，IP 是固定的
- 即使重启电脑、重装系统，只要登录同一账号就是同一 IP

---

## 🔧 故障排查

### 问题 1: 看不到其他设备

```bash
# 检查自己是否在线
tailscale status

# 确认同事也在线且使用同一账号
```

### 问题 2: 连接超时

```bash
# 重启 Tailscale
sudo tailscale down
sudo tailscale up

# 检查防火墙
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off
```

### 问题 3: 速度慢

Tailscale 会优先尝试 P2P 直连，如果失败会通过中继服务器。

改善方法：
- 确保 UDP 端口开放
- 尽量在同一城市/地区

---

## 🎉 完成！

配置完成后，您就可以：

1. **自己访问**：http://localhost:5000
2. **告诉同事 Tailscale IP**：让他们访问 `http://[您的 IP]:5000`
3. **享受稳定的内网访问**！

---

## 📞 现在需要做什么？

**立即执行：**

```bash
# 1. 启动 Tailscale
sudo tailscale up

# 2. 复制输出的 URL 到浏览器登录

# 3. 登录后查看 IP
tailscale ip

# 4. 运行智能启动脚本
./start-tailscale.sh
```

然后把显示的访问地址发给同事即可！

有任何问题随时告诉我！🦞
