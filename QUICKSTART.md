# 🎉 龙虾 Skill 合集平台 - 快速开始指南

## ⚡ 3 分钟快速启动

### 第一步：解压文件
```bash
# macOS/Linux
unzip lobster-skill-platform-v1.0.0.zip

# Windows
右键点击 ZIP 文件 -> 解压到当前文件夹
```

### 第二步：运行程序

**macOS/Linux:**
```bash
cd lobster-skill-platform
chmod +x start.sh
./start.sh
```

**Windows:**
双击 `start.bat` 或在命令行运行：
```bash
cd lobster-skill-platform
start.bat
```

### 第三步：访问平台
打开浏览器访问：**http://127.0.0.1:5000**

---

## 🚀 可选：初始化示例数据

如果你想看到一些示例技能和用户，可以运行：

```bash
cd lobster-skill-platform
python init_sample_data.py
```

这会创建：
- 5 个示例用户
- 8 个示例技能（办公效率、AI 工具、数据处理等分类）
- 模拟的下载和使用记录

然后重启平台：
```bash
./start.sh  # 或 start.bat
```

---

## 📱 功能概览

### ✅ 已实现的核心功能

1. **技能上传与下载**
   - 支持多种文件格式（.py, .zip, .js, .json, .md）
   - 分类管理和标签系统
   - 一键下载，自动统计

2. **智能检索系统**
   - 关键词搜索（支持标题、描述、作者）
   - 分类筛选
   - 多维度排序（最新、最热、最多使用、最高评分）

3. **个性化推荐引擎**
   - 基于用户行为分析（下载、使用记录）
   - 每日 3 次定时推送（10:30、14:00、17:00）
   - 每次推荐 3 个精准匹配的技能
   - 冷启动机制（新用户推荐热门技能）

4. **积分激励系统**
   ```
   上传技能          +10 分
   下载技能          +2 分
   技能被下载        +5 分/次
   技能被使用        +3 分/次
   推荐被采纳        +1 分
   ```

5. **数据同步与备份**
   - 本地 SQLite 数据库（无需额外配置）
   - 自动备份（ZIP 格式）
   - 支持导出/导入平台数据
   - GitHub 同步（可选配置）
   - 云存储同步（可选配置）

6. **定时任务调度**
   - 每日推荐任务（10:30、14:00、17:00）
   - 数据库清理维护（02:00）
   - 数据同步（每 6 小时）

---

## 🎯 使用流程

### 作为技能上传者：
1. 注册/登录账号
2. 点击"上传"按钮
3. 填写技能信息并上传文件
4. 获得 10 积分奖励
5. 每次有人下载你的技能，获得 5 积分
6. 每次有人使用你的技能，获得 3 积分

### 作为技能使用者：
1. 浏览技能库或搜索所需技能
2. 下载技能文件（获得 2 积分）
3. 在实际场景中使用
4. 返回平台标记"使用过"（帮助上传者获得 3 积分）
5. 在个人主页查看积分历史

---

## 📂 文件结构说明

```
lobster-skill-platform/
├── app.py                    # 主程序（Web 服务）
├── scheduler.py              # 定时任务调度器
├── sync.py                   # 数据同步工具
├── init_sample_data.py       # 示例数据初始化脚本
├── config.py                 # 配置文件
├── models.py                 # 数据库模型
├── services.py               # 业务逻辑层
├── requirements.txt          # Python 依赖列表
├── start.sh                  # Linux/Mac启动脚本
├── start.bat                 # Windows 启动脚本
├── package.sh                # Linux/Mac打包脚本
├── package.bat               # Windows 打包脚本
├── README.md                 # 完整文档
├── INSTALL.md                # 安装指南
├── templates/                # HTML 模板目录
├── static/                   # CSS/JS静态资源
└── data/                     # 数据目录（运行时自动创建）
    ├── lobster_platform.db   # SQLite 数据库
    ├── skills/               # 技能文件存储
    └── backups/              # 备份文件
```

---

## 🔧 常用操作

### 查看平台状态
启动后访问首页，底部会显示：
- 📦 技能总数
- 👥 用户总数
- ⬇️ 下载总次数

### 手动备份数据
```bash
python -c "from sync import DataSync; DataSync().create_backup()"
```

### 导出数据分享给他人
```bash
python -c "from sync import DataSync; DataSync().export_platform_data()"
```

### 导入他人分享的数据
```bash
python -c "from sync import DataSync; DataSync().import_platform_data('path/to/file.zip')"
```

### 立即执行推荐任务
```bash
python scheduler.py recommendations
```

---

## 🌐 高级配置

### 修改端口号
编辑 `config.py`:
```python
PORT = 5001  # 改为其他端口
```

### 启用 GitHub 同步
编辑 `config.py`:
```python
GITHUB_CONFIG = {
    'enabled': True,
    'repo': 'your-username/lobster-skills',
    'token': 'ghp_xxxxxxxxxxxx',
    'branch': 'main'
}
```

### 启用云存储同步
编辑 `config.py`:
```python
CLOUD_STORAGE_CONFIG = {
    'enabled': True,
    'type': 'webdav',
    'url': 'https://your-webdav.com',
    'username': 'your-username',
    'password': 'your-password'
}
```

---

## ❓ 常见问题

### Q: 如何停止服务？
A: 在运行终端按 `Ctrl+C`

### Q: 数据存在哪里？
A: `data/` 目录下，最重要的是 `lobster_platform.db` 数据库文件

### Q: 如何重置所有数据？
A: 删除 `data/lobster_platform.db` 文件，重启平台会自动创建新数据库

### Q: 可以在公网上部署吗？
A: 可以，但建议：
   - 修改 `config.py` 中的 `SECRET_KEY`
   - 设置 `DEBUG = False`
   - 使用 Gunicorn 运行：`gunicorn app:app`
   - 添加 HTTPS 支持

---

## 📞 需要帮助？

1. 查看 `README.md` - 完整功能文档
2. 查看 `INSTALL.md` - 详细安装指南
3. 检查控制台错误信息
4. 确保 `data/` 目录有写权限

---

## 🎉 开始享受技能分享的乐趣！

现在你已经准备好了，打开浏览器访问 **http://127.0.0.1:5000** 开始使用吧！

**🦞 让技能分享更有价值！**
