# 🌐 外网访问 - 3 种可靠方案

## ⚠️ Cloudflare Tunnel 问题说明

如果你发现 `trycloudflare.com` 的 URL 打不开，可能是：
- 隧道已关闭
- 网络问题
- 服务暂时不可用

**不用担心！还有更可靠的方案！**

---

## ✅ 方案一：Localtunnel（推荐！最可靠）

### 一键启动

```bash
cd lobster-skill-platform
./start-tunnel.sh
```

### 手动步骤

```bash
# 1. 安装 localtunnel
npm install -g localtunnel

# 2. 确保平台在运行
./start.sh

# 3. 启动隧道（新终端窗口）
lt --port 5000

# 4. 复制生成的 URL
# 格式：https://xxx.loca.li
```

### 首次访问提示

第一次打开 loca.li 的链接会显示：
```
Potential Security Risk Ahead
```

**解决方法：**
1. 点击 "Advanced"（高级）
2. 点击 "Proceed to xxx.loca.li"（继续访问）
3. 即可正常访问

### 优点
- ✅ 非常稳定
- ✅ 免费
- ✅ 全球可访问
- ✅ 支持 HTTPS

---

## ✅ 方案二：局域网 IP 访问（最简单）

### 适用场景
- 朋友在同一 WiFi
- 同一办公室/家庭

### 步骤

```bash
# 1. 查看本机 IP
ipconfig getifaddr en0
# 输出：192.168.1.100

# 2. 手机/电脑访问
http://192.168.1.100:5000
```

### 如果无法访问

**检查防火墙：**
```bash
# macOS
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate off

# 或系统偏好设置 -> 安全性与隐私 -> 防火墙 -> 关闭
```

**允许 Python 联网：**
- 系统偏好设置 -> 安全性与隐私
- 找到 Python，允许入站连接

---

## ✅ 方案三：Ngrok（备选）

### 安装使用

```bash
# 1. 官网下载
https://ngrok.com/download

# 2. 解压后放到 /usr/local/bin
sudo mv ~/Downloads/ngrok /usr/local/bin/

# 3. 启动
ngrok http 5000

# 4. 复制生成的 ngrok.io URL
```

### Ngrok 免费版限制
- URL 每次重启会变
- 有流量限制
- 但很稳定

---

## 🎯 快速对比

| 方案 | 稳定性 | 难度 | 适用场景 |
|------|--------|------|---------|
| Localtunnel | ⭐⭐⭐⭐⭐ | 简单 | 远程访问（首选） |
| 局域网 IP | ⭐⭐⭐⭐⭐ | 最简单 | 同一 WiFi |
| Ngrok | ⭐⭐⭐⭐ | 中等 | 备选方案 |
| Cloudflare | ⭐⭐⭐ | 简单 | 备用 |

---

## 🚀 立即体验

### 最快方案（局域网）

```bash
# 1. 查看 IP（5 秒）
ipconfig getifaddr en0

# 2. 访问
http://你的IP:5000
```

### 远程方案（Localtunnel）

```bash
# 一键启动（2 分钟）
./start-tunnel.sh

# 复制 URL 发给朋友
```

---

## 💡 常见问题

### Q: loca.li 网址打不开？
**A:** 
1. 检查是否安装了 Node.js
2. 运行 `npm install -g localtunnel`
3. 重新运行 `./start-tunnel.sh`

### Q: 局域网 IP 访问不了？
**A:**
1. 确认手机和电脑在同一 WiFi
2. 关闭防火墙试试
3. 检查 IP 是否正确

### Q: 需要长期稳定的网址？
**A:** 
建议部署到：
- Heroku（免费）
- Vercel（免费）
- Railway（免费额度）

---

## 📝 工具清单

**已准备的脚本：**
- ✅ `start-tunnel.sh` - Localtunnel 一键启动
- ✅ `start-public.sh` - Cloudflare 启动（备用）
- ✅ `start.sh` - 本地启动

**文档：**
- ✅ `QUICK_NETWORK.md` - 快速指南
- ✅ `NETWORK_GUIDE.md` - 详细指南
- ✅ `本文件` - 故障排除

---

## 🎉 推荐流程

**第一步：** 试试局域网访问
```bash
ipconfig getifaddr en0
# 手机访问 http://你的IP:5000
```

**第二步：** 如果不行，用 Localtunnel
```bash
./start-tunnel.sh
# 复制 URL
```

**第三步：** 如果还不行，检查网络和防火墙

---

**现在就试试吧！总有一种方法适合你！**
