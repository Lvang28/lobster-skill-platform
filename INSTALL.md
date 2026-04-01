# 🦞 龙虾 Skill 合集平台 - 快速安装指南

## 📦 方式一：使用 ZIP 包（推荐）

### 步骤 1：下载 ZIP 包
从分享者处获取 `lobster-skill-platform-v1.0.0-*.zip` 文件

### 步骤 2：解压文件
```bash
# macOS/Linux
unzip lobster-skill-platform-v1.0.0-*.zip

# Windows
右键 -> 解压到当前文件夹
```

### 步骤 3：运行程序

**macOS/Linux:**
```bash
cd lobster-skill-platform
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
cd lobster-skill-platform
start.bat
```

### 步骤 4：访问平台
打开浏览器访问：**http://127.0.0.1:5000**

---

## 🔧 方式二：从 GitHub 克隆

```bash
# 克隆仓库
git clone https://github.com/your-repo/lobster-skill-platform.git

# 进入目录
cd lobster-skill-platform

# 运行启动脚本
./start.sh  # Mac/Linux
# 或
start.bat   # Windows
```

---

## 🎯 首次使用

### 1. 注册/登录
- 打开首页
- 点击右上角"登录/注册"
- 输入用户名（必填）和邮箱（可选）
- 点击"进入平台"

### 2. 上传第一个技能
- 点击导航栏"上传"
- 填写技能信息：
  - 名称：例如"数据分析助手"
  - 作者：你的昵称
  - 分类：选择合适分类
  - 标签：用逗号分隔，如"python,数据分析，可视化"
  - 描述：详细说明功能和使用方法
  - 文件：选择技能文件（.py/.zip/.js 等）
- 点击"上传技能"
- ✅ 获得 **10 积分** 奖励！

### 3. 下载技能
- 浏览技能库或搜索感兴趣的技能
- 进入技能详情页
- 点击"下载此技能"
- ✅ 获得 **2 积分**，上传者获得 **5 积分**

### 4. 使用技能并反馈
- 下载后在实际场景中使用
- 返回技能详情页
- 点击"使用过"按钮
- ✅ 上传者获得 **3 积分**

### 5. 查看个人主页
- 点击右上角用户名
- 查看：
  - 总积分
  - 上传的技能数量
  - 下载记录
  - 积分历史明细

---

## ⚙️ 高级配置（可选）

### 启用 GitHub 同步

1. 编辑 `config.py` 文件
2. 修改以下配置：

```python
GITHUB_CONFIG = {
    'enabled': True,           # 改为 True
    'repo': 'your-username/lobster-skills',  # 你的 GitHub 仓库
    'token': 'ghp_xxxxxxxxxxxx',  # GitHub Personal Access Token
    'branch': 'main'
}
```

3. 获取 GitHub Token：
   - 访问 https://github.com/settings/tokens
   - 生成新 Token（勾选 `repo` 权限）
   - 复制到配置中

### 启用云存储同步

1. 编辑 `config.py`
2. 配置 WebDAV（以阿里云盘为例）：

```python
CLOUD_STORAGE_CONFIG = {
    'enabled': True,
    'type': 'webdav',
    'url': 'https://dav.aliyundrive.com',
    'username': 'your-username',
    'password': 'your-password'
}
```

---

## 🔄 数据备份与恢复

### 手动备份
```bash
# 在平台目录下执行
python -c "from sync import DataSync; DataSync().create_backup()"
```

备份文件位置：`data/backups/backup_YYYYMMDD_HHMMSS.zip`

### 导出平台数据（用于分享）
```bash
python -c "from sync import DataSync; DataSync().export_platform_data()"
```

导出的 ZIP 文件可以分享给其他人导入使用。

### 导入他人分享的数据
```bash
python -c "from sync import DataSync; DataSync().import_platform_data('path/to/file.zip')"
```

---

## 🛠️ 常见问题

### Q1: 启动失败，提示端口被占用
**解决方案：** 修改 `config.py` 中的端口号
```python
PORT = 5001  # 改为其他端口
```

### Q2: 依赖安装失败
**解决方案：** 
```bash
# 手动安装依赖
pip install flask sqlalchemy requests python-dateutil
```

### Q3: 数据库权限问题
**解决方案：** 确保 `data/` 目录有写权限
```bash
chmod -R 755 data/
```

### Q4: 如何重置平台？
**解决方案：** 删除数据库文件重新开始
```bash
rm data/lobster_platform.db
# 重启平台会自动创建新数据库
```

---

## 📊 系统要求

- **Python**: 3.8+
- **操作系统**: macOS / Linux / Windows
- **内存**: 最低 512MB
- **磁盘**: 至少 100MB 可用空间

---

## 🎉 开始使用

一切准备就绪！现在你可以：

1. ✅ 上传你的第一个技能
2. ✅ 探索他人分享的优质技能
3. ✅ 通过积分系统获得激励
4. ✅ 每日接收个性化推荐

**🦞 让技能分享更有价值！**

---

## 📞 技术支持

如有问题，请：
1. 查看 README.md 完整文档
2. 检查 data/目录权限
3. 查看控制台错误信息

祝使用愉快！
