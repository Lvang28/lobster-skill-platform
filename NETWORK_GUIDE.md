# 🌐 龙虾 Skill 平台 - 外网访问配置指南

## ✅ 问题已解决

已经修改配置，现在支持外网访问！

---

## 🔧 配置说明

### 1. **本地访问（原配置）**
```python
HOST = '127.0.0.1'  # 只能本机访问
```

### 2. **外网访问（新配置）**
```python
HOST = '0.0.0.0'  # 允许所有网络接口访问
```

---

## 🚀 外网访问方法

### 方法一：直接 IP 访问（同一局域网）

**步骤：**

1. **查看本机 IP 地址**
   ```bash
   # macOS/Linux
   ifconfig | grep "inet "
   
   # Windows
   ipconfig
   ```
   
   找到类似这样的 IP：`192.168.1.100` 或 `10.0.0.50`

2. **启动平台**
   ```bash
   cd lobster-skill-platform
   ./start.sh
   ```

3. **朋友访问**
   ```
   http://你的IP地址：5000
   例如：http://192.168.1.100:5000
   ```

**适用范围：**
- ✅ 同一 WiFi 下的设备
- ✅ 同一办公室/家庭的电脑
- ❌ 不能跨城市/国家

---

### 方法二：内网穿透（推荐给朋友使用）

#### 方案 A：使用 ngrok（最简单）

**安装 ngrok：**
```bash
# macOS
brew install ngrok

# 或者下载：https://ngrok.com/download
```

**使用步骤：**
1. 启动平台（保持运行）
   ```bash
   ./start.sh
   ```

2. 在另一个终端窗口运行：
   ```bash
   ngrok http 5000
   ```

3. ngrok 会生成一个公网 URL：
   ```
   Forwarding: https://abc123.ngrok.io -> http://localhost:5000
   ```

4. 把这个 URL 发给朋友即可访问！

**优点：**
- ✅ 简单快速
- ✅ 免费
- ✅ 支持 HTTPS
- ✅ 跨城市/国家都能访问

**缺点：**
- ⚠️ 每次重启 URL 会变（付费版可固定）

---

#### 方案 B：使用 Cloudflare Tunnel

**安装 cloudflared：**
```bash
# macOS
brew install cloudflared

# Linux
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared-linux-amd64
sudo mv cloudflared-linux-amd64 /usr/local/bin/cloudflared
```

**使用步骤：**
```bash
cloudflared tunnel --url http://localhost:5000
```

会生成一个 `https://xxx-xxx-xxx.cfargotunnel.com` 的永久 URL

---

#### 方案 C：使用 frp（自有服务器）

如果有云服务器，可以搭建 frp 进行反向代理。

---

### 方法三：部署到公网服务器

#### 部署到 Heroku（免费）

**步骤：**

1. 创建 `Procfile`：
   ```
   web: gunicorn app:app
   ```

2. 安装 Gunicorn：
   ```bash
   pip install gunicorn
   ```

3. 部署：
   ```bash
   heroku create lobster-skill-platform
   git push heroku main
   heroku open
   ```

会获得一个永久的 `https://xxx.herokuapp.com` 网址

---

#### 部署到 Vercel

1. 安装 Vercel CLI：
   ```bash
   npm install -g vercel
   ```

2. 部署：
   ```bash
   vercel
   ```

---

## 🔒 安全建议

### 开发环境（当前）
- ⚠️ `DEBUG = True`（仅用于开发）
- ⚠️ 无密码保护
- ⚠️ 适合内部测试

### 生产环境（如果要长期对外）
建议添加：
1. ✅ 设置 `DEBUG = False`
2. ✅ 添加用户认证系统
3. ✅ 使用 HTTPS
4. ✅ 配置防火墙
5. ✅ 限制访问频率（防 DDOS）

---

## 📊 当前配置状态

**✅ 已更新配置：**
```python
HOST = '0.0.0.0'  # 允许外网访问
PORT = 5000
DEBUG = True      # 开发模式
```

**⚠️ 注意事项：**
- 确保防火墙允许 5000 端口
- macOS 可能会提示是否允许网络连接，点击"允许"
- 路由器可能需要端口转发（5000）

---

## 🎯 快速测试

### 1. 重启平台
```bash
cd lobster-skill-platform
./start.sh
```

### 2. 查看本机 IP
```bash
# macOS
ipconfig getifaddr en0

# 或
ifconfig | grep "inet "
```

假设得到：`192.168.1.100`

### 3. 手机访问测试
- 手机连接同一 WiFi
- 浏览器打开：`http://192.168.1.100:5000`
- 应该能正常访问

### 4. 朋友远程访问
```bash
# 安装并使用 ngrok
ngrok http 5000
```

复制生成的 URL 发给朋友即可！

---

## 📞 常见问题

### Q1: 朋友访问显示"无法连接"？
**A:** 检查：
1. 平台是否正常启动
2. 防火墙是否允许 5000 端口
3. 是否在同一局域网（直接 IP 访问时）
4. 使用 ngrok 等穿透工具

### Q2: 公司网络无法访问？
**A:** 公司防火墙可能阻止，建议使用 ngrok 的 HTTPS 链接

### Q3: 如何长期稳定访问？
**A:** 
- 短期：ngrok 付费版（固定域名）
- 长期：部署到 Heroku/Vercel 等云平台

### Q4: 数据安全吗？
**A:** 
- 当前是开发模式，适合测试
- 正式使用建议部署到云端并启用 HTTPS

---

## 🎉 总结

**最简单的方案：**
1. 启动平台
2. 运行 `ngrok http 5000`
3. 发送 URL 给朋友
4. 完成！✅

**现在你的平台已经支持外网访问了！**
