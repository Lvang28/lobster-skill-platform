# 🦞 龙虾 Skill 合集平台

一个去中心化的技能分享与交易平台，让每个人都能上传、下载和发现优质技能，通过积分系统激励分享。

## ✨ 核心功能

### 1. **技能上传与下载**
- ✅ 支持上传各种类型的技能文件（Python 脚本、JavaScript、配置文件等）
- ✅ 分类管理、标签检索
- ✅ 一键下载，自动记录

### 2. **智能检索**
- ✅ 关键词搜索
- ✅ 分类筛选
- ✅ 按热度、评分、时间排序

### 3. **个性化推荐**
- ✅ 基于用户行为分析（浏览、下载、使用记录）
- ✅ 每日 3 次定时推送（10:30、14:00、17:00）
- ✅ 每次推荐 3 个精准匹配的技能
- ✅ 冷启动机制（新用户推荐热门技能）

### 4. **积分激励系统**
| 行为 | 积分 |
|------|------|
| 上传技能 | +10 分 |
| 下载技能 | +2 分 |
| 技能被下载 | +5 分/次 |
| 技能被使用 | +3 分/次 |
| 推荐被采纳 | +1 分 |

### 5. **数据同步与备份**
- ✅ 本地 SQLite 数据库
- ✅ 自动备份（ZIP 格式）
- ✅ 支持 GitHub 仓库同步（可选）
- ✅ 支持云存储同步（WebDAV/S3，可选）
- ✅ 定期联网更新数据和积分

## 🚀 快速开始

### 方式一：一键启动（推荐）

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

访问：http://127.0.0.1:5000

### 方式二：手动安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库（首次运行会自动创建）
python app.py

# 3. （可选）启动定时任务调度器
python scheduler.py
```

## 📁 项目结构

```
lobster-skill-platform/
├── app.py              # Flask Web 应用主程序
├── config.py           # 配置文件
├── models.py           # 数据库模型
├── services.py         # 业务逻辑层
├── sync.py             # 数据同步工具
├── scheduler.py        # 定时任务调度器
├── requirements.txt    # Python 依赖
├── start.sh            # Linux/Mac启动脚本
├── start.bat           # Windows 启动脚本
├── templates/          # HTML 模板
│   ├── base.html
│   ├── index.html
│   ├── skills.html
│   ├── skill_detail.html
│   ├── upload.html
│   └── profile.html
├── static/             # 静态资源
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── data/               # 数据目录（运行时自动创建）
    ├── lobster_platform.db  # SQLite 数据库
    ├── skills/         # 技能文件存储
    ├── users/          # 用户数据
    └── backups/        # 备份文件
```

## 🔧 配置说明

### 基础配置 (config.py)

```python
# 服务器配置
HOST = '127.0.0.1'
PORT = 5000

# 积分规则（可自定义）
POINTS_CONFIG = {
    'upload_skill': 10,
    'download_skill': 2,
    'skill_downloaded': 5,
    'skill_used': 3,
    'daily_recommendation': 1
}
```

### GitHub 同步配置（可选）

编辑 `config.py`:

```python
GITHUB_CONFIG = {
    'enabled': True,
    'repo': 'your-username/lobster-skills',
    'token': 'your-github-token',
    'branch': 'main'
}
```

### 云存储配置（可选）

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

## 📊 API 接口

### 平台统计
```
GET /api/stats
```

返回：
```json
{
  "total_skills": 100,
  "total_users": 50,
  "total_downloads": 500
}
```

### 接受推荐
```
POST /api/recommendations/accept
Content-Type: application/json

{"skill_id": 123}
```

### 记录技能使用
```
POST /skill/{id}/use
Content-Type: application/json

{"duration": 300, "success": true}
```

## ⏰ 定时任务

平台内置定时任务调度器，自动执行以下任务：

| 时间 | 任务 | 说明 |
|------|------|------|
| 10:30 | 发送推荐 | 为用户生成并推送 3 个推荐技能 |
| 14:00 | 发送推荐 | 为用户生成并推送 3 个推荐技能 |
| 17:00 | 发送推荐 | 为用户生成并推送 3 个推荐技能 |
| 02:00 | 清理维护 | 清理过期数据、优化数据库 |
| 每 6 小时 | 数据同步 | 同步到 GitHub/云存储 |

手动执行任务：
```bash
python scheduler.py recommendations  # 立即执行推荐任务
python scheduler.py cleanup          # 立即执行清理任务
python scheduler.py sync             # 立即执行同步任务
```

## 🔄 数据同步

### 导出平台数据
```python
from sync import DataSync

sync = DataSync()
backup_file = sync.export_platform_data()
# 输出：platform_export_20240401_120000.zip
```

### 导入平台数据
```python
from sync import DataSync

sync = DataSync()
sync.import_platform_data('path/to/platform_export.zip')
```

### 分享给他人
1. 导出数据：`python -c "from sync import DataSync; DataSync().export_platform_data()"`
2. 将生成的 ZIP 文件发送给其他人
3. 对方导入：`python -c "from sync import DataSync; DataSync().import_platform_data('file.zip')"`

## 🛡️ 安全建议

1. **生产环境部署**：
   - 修改 `app.secret_key` 为随机字符串
   - 设置 `DEBUG = False`
   - 使用 Gunicorn/uWSGI 运行

2. **数据备份**：
   - 定期备份 `data/` 目录
   - 启用 GitHub/云存储同步

3. **权限控制**：
   - 当前版本为单机版，适合个人或小团队使用
   - 如需公网部署，建议添加用户认证和权限管理

## 📝 使用说明

### 上传技能
1. 登录/注册账号
2. 点击"上传"按钮
3. 填写技能信息（名称、描述、分类、标签）
4. 上传技能文件
5. 提交后获得 10 积分

### 下载技能
1. 浏览技能库或搜索目标技能
2. 进入技能详情页
3. 点击下载按钮
4. 获得 2 积分，上传者获得 5 积分

### 使用技能
1. 下载技能文件
2. 在实际场景中使用
3. 返回平台点击"使用过"
4. 上传者获得 3 积分

### 查看积分
- 点击右上角用户名进入个人主页
- 查看总积分、积分历史
- 查看自己上传的技能及其收益

## 🎨 界面预览

- **首页**：展示今日推荐、热门技能、最新技能
- **技能库**：搜索、筛选、排序所有技能
- **技能详情**：查看技能详细信息、统计数据
- **上传页面**：上传新技能的表单
- **个人主页**：个人信息、积分统计、上传历史

## 🤝 贡献与反馈

欢迎提出建议和改进意见！

## 📄 许可证

MIT License

## 👥 致谢

感谢所有贡献技能的用户！

---

**🦞 让技能分享更有价值！**
