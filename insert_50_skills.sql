-- 龙虾 Skill 平台 - 50 个技能批量插入 SQL
-- 在 Render PostgreSQL 控制台中执行此 SQL

-- 清空现有数据（可选，如果需要重置）
-- TRUNCATE TABLE skills RESTART IDENTITY CASCADE;

-- 插入 50 个技能
INSERT INTO skills (name, description, category, tags, file_path, file_size, download_count, use_count, created_at) VALUES
('Python Excel 自动化处理工具', '自动读取、修改、合并 Excel 文件，支持批量处理，大幅提升办公效率。', 'Python', '["Python", "Excel", "自动化", "办公"]', 'skill_001_Python_Excel 自动化处理工具.txt', 1024, 0, 0, NOW()),
('Python PDF 转 Word 工具', '一键批量将 PDF 转换为可编辑的 Word 文档，保持原有格式。', 'Python', '["Python", "PDF", "Word", "格式转换"]', 'skill_002_Python_PDF 转 Word 工具.txt', 1024, 0, 0, NOW()),
('Python 微信机器人框架', '基于 WeChaty 的微信聊天机器人，支持自动回复、群管理等功能。', 'Python', '["Python", "微信", "机器人", "自动化"]', 'skill_003_Python 微信机器人框架.txt', 1024, 0, 0, NOW()),
('Python 数据分析模板', '完整的数据分析流程模板，包括数据加载、EDA、可视化等。', 'Python', '["Python", "数据分析", "Pandas", "可视化"]', 'skill_004_Python 数据分析模板.txt', 1024, 0, 0, NOW()),
('Python 网络爬虫框架', '通用网页爬虫框架，支持反爬处理、数据清洗、自动重试。', 'Python', '["Python", "爬虫", "数据采集", "Web Scraping"]', 'skill_005_Python 网络爬虫框架.txt', 1024, 0, 0, NOW()),
('Python 自动化测试脚本', '基于 Selenium 的 Web 自动化测试框架，支持截图、报告生成。', 'Python', '["Python", "测试", "Selenium", "自动化"]', 'skill_006_Python 自动化测试脚本.txt', 1024, 0, 0, NOW()),
('Python 文件批量重命名工具', '批量重命名文件和文件夹，支持正则表达式匹配。', 'Python', '["Python", "文件管理", "批量处理", "工具"]', 'skill_007_Python 文件批量重命名工具.txt', 1024, 0, 0, NOW()),
('Python 图片压缩工具', '批量压缩图片文件大小，保持清晰度，支持多种格式。', 'Python', '["Python", "图片处理", "压缩", "PIL"]', 'skill_008_Python 图片压缩工具.txt', 1024, 0, 0, NOW()),
('Python 邮件群发助手', 'SMTP 邮件群发工具，支持 HTML 模板、附件发送、发送记录。', 'Python', '["Python", "邮件", "SMTP", "群发"]', 'skill_009_Python 邮件群发助手.txt', 1024, 0, 0, NOW()),
('Python 视频下载器', '支持下载 YouTube、Bilibili 等平台视频的命令行工具。', 'Python', '["Python", "视频", "下载", "youtube-dl"]', 'skill_010_Python 视频下载器.txt', 1024, 0, 0, NOW()),
('销售数据分析看板', '使用 Tableau/PowerBI 风格的销售数据可视化分析模板。', '数据分析', '["数据分析", "销售", "可视化", "BI"]', 'skill_011_销售数据分析看板.txt', 1024, 0, 0, NOW()),
('用户行为分析模型', '分析用户留存率、转化率、漏斗模型的完整分析框架。', '数据分析', '["数据分析", "用户行为", "留存", "转化"]', 'skill_012_用户行为分析模型.txt', 1024, 0, 0, NOW()),
('A/B 测试分析工具', '统计学 A/B 测试分析，包含显著性检验和功效分析。', '数据分析', '["数据分析", "A/B 测试", "统计", "假设检验"]', 'skill_013_A_B 测试分析工具.txt', 1024, 0, 0, NOW()),
('时间序列预测模型', '基于 ARIMA 和 Prophet 的时间序列预测模板。', '数据分析', '["数据分析", "时间序列", "预测", "ARIMA"]', 'skill_014_时间序列预测模型.txt', 1024, 0, 0, NOW()),
('客户分群分析', 'RFM 模型 + K-Means聚类的客户细分分析方案。', '数据分析', '["数据分析", "客户分群", "RFM", "聚类"]', 'skill_015_客户分群分析.txt', 1024, 0, 0, NOW()),
('电商数据仪表盘', '完整的电商运营数据监控仪表盘，包含 GMV、转化率等指标。', '数据分析', '["数据分析", "电商", "仪表盘", "监控"]', 'skill_016_电商数据仪表盘.txt', 1024, 0, 0, NOW()),
('社交媒体分析工具', '微博、微信公众号数据统计与分析模板。', '数据分析', '["数据分析", "社交媒体", "运营", "统计"]', 'skill_017_社交媒体分析工具.txt', 1024, 0, 0, NOW()),
('财务数据分析报表', '企业财务三表分析、比率分析、趋势分析模板。', '数据分析', '["数据分析", "财务", "报表", "分析"]', 'skill_018_财务数据分析报表.txt', 1024, 0, 0, NOW()),
('人力资源数据分析', '员工流失率、招聘效率、绩效分析的 HR 仪表盘。', '数据分析', '["数据分析", "HR", "人力资源", "绩效"]', 'skill_019_人力资源数据分析.txt', 1024, 0, 0, NOW()),
('市场数据分析报告', '市场份额、竞品分析、价格弹性分析模板。', '数据分析', '["数据分析", "市场", "竞品", "价格"]', 'skill_020_市场数据分析报告.txt', 1024, 0, 0, NOW()),
('Flask RESTful API 模板', '生产级 Flask RESTful API 脚手架，含 JWT 认证。', 'Web 开发', '["Flask", "API", "RESTful", "JWT"]', 'skill_021_Flask_RESTful_API 模板.txt', 1024, 0, 0, NOW()),
('Django 博客系统', '完整的 Django 博客系统，支持评论、标签、搜索。', 'Web 开发', '["Django", "博客", "CMS", "Python"]', 'skill_022_Django 博客系统.txt', 1024, 0, 0, NOW()),
('Vue3 后台管理模板', '基于 Vue3 + Element Plus 的后台管理系统模板。', 'Web 开发', '["Vue", "前端", "Element", "管理后台"]', 'skill_023_Vue3 后台管理模板.txt', 1024, 0, 0, NOW()),
('React 电商网站模板', '完整的 React 电商网站，含购物车、订单、支付。', 'Web 开发', '["React", "电商", "前端", "购物车"]', 'skill_024_React 电商网站模板.txt', 1024, 0, 0, NOW()),
('Node.js 即时聊天室', '基于 Socket.io 的实时聊天室应用。', 'Web 开发', '["Node.js", "Socket.io", "聊天", "实时"]', 'skill_025_Node.js 即时聊天室.txt', 1024, 0, 0, NOW()),
('微信小程序商城模板', '完整的微信小程序商城代码，支持拼团、秒杀。', 'Web 开发', '["小程序", "微信", "商城", "电商"]', 'skill_026_微信小程序商城模板.txt', 1024, 0, 0, NOW()),
('TypeScript 工具库', '常用的 TypeScript 工具函数集合，提升开发效率。', 'Web 开发', '["TypeScript", "工具库", "JavaScript", "前端"]', 'skill_027_TypeScript 工具库.txt', 1024, 0, 0, NOW()),
('CSS 动画效果集', '50+ 种实用的 CSS 动画效果，开箱即用。', 'Web 开发', '["CSS", "动画", "前端", "UI"]', 'skill_028_CSS 动画效果集.txt', 1024, 0, 0, NOW()),
('响应式落地页模板', '营销落地页模板，适配手机和桌面端。', 'Web 开发', '["HTML", "CSS", "响应式", "落地页"]', 'skill_029_响应式落地页模板.txt', 1024, 0, 0, NOW()),
('GraphQL API 示例', 'GraphQL API 完整示例，包含查询、变更、订阅。', 'Web 开发', '["GraphQL", "API", "后端", "查询"]', 'skill_030_GraphQL_API 示例.txt', 1024, 0, 0, NOW()),
('机器学习入门教程', 'Scikit-learn 机器学习算法入门教程与代码示例。', '机器学习', '["机器学习", "Scikit-learn", "教程", "入门"]', 'skill_031_机器学习入门教程.txt', 1024, 0, 0, NOW()),
('深度学习图像分类', '基于 PyTorch 的图像分类模型训练模板。', '机器学习', '["深度学习", "PyTorch", "图像分类", "CNN"]', 'skill_032_深度学习图像分类.txt', 1024, 0, 0, NOW()),
('NLP 文本情感分析', '中文文本情感分析模型，支持细粒度情感打分。', '机器学习', '["NLP", "情感分析", "文本分类", "BERT"]', 'skill_033_NLP 文本情感分析.txt', 1024, 0, 0, NOW()),
('推荐系统实战', '协同过滤 + 深度学习的混合推荐系统实现。', '机器学习', '["推荐系统", "协同过滤", "深度学习", "排序"]', 'skill_034_推荐系统实战.txt', 1024, 0, 0, NOW()),
('目标检测 YOLO 模板', 'YOLOv5 目标检测模型训练与部署模板。', '机器学习', '["目标检测", "YOLO", "计算机视觉", "深度学习"]', 'skill_035_目标检测_YOLO 模板.txt', 1024, 0, 0, NOW()),
('语音识别工具', '基于 Whisper 的语音转文字工具，支持多语言。', '机器学习', '["语音识别", "Whisper", "ASR", "转录"]', 'skill_036_语音识别工具.txt', 1024, 0, 0, NOW()),
('GAN 图像生成', '使用 GAN 生成逼真图像的完整实现代码。', '机器学习', '["GAN", "图像生成", "深度学习", "AI"]', 'skill_037_GAN 图像生成.txt', 1024, 0, 0, NOW()),
('强化学习入门', 'Q-Learning、DQN 等强化学习算法实现。', '机器学习', '["强化学习", "Q-Learning", "DQN", "AI"]', 'skill_038_强化学习入门.txt', 1024, 0, 0, NOW()),
('时间序列预测 LSTM', '基于 LSTM 神经网络的时间序列预测模型。', '机器学习', '["LSTM", "时间序列", "预测", "深度学习"]', 'skill_039_时间序列预测_LSTM.txt', 1024, 0, 0, NOW()),
('模型部署 Flask API', '将机器学习模型部署为 REST API 服务。', '机器学习', '["模型部署", "Flask", "API", "服务化"]', 'skill_040_模型部署_Flask_API.txt', 1024, 0, 0, NOW()),
('Docker 快速入门', 'Docker 基础教程，包含常用命令和实战案例。', 'DevOps', '["Docker", "容器", "教程", "入门"]', 'skill_041_Docker 快速入门.txt', 1024, 0, 0, NOW()),
('Kubernetes 部署模板', 'K8s Deployment、Service、Ingress 配置模板。', 'DevOps', '["Kubernetes", "K8s", "部署", "容器编排"]', 'skill_042_Kubernetes 部署模板.txt', 1024, 0, 0, NOW()),
('CI/CD 流水线配置', 'GitHub Actions 自动化 CI/CD 流水线配置。', 'DevOps', '["CI/CD", "GitHub Actions", "自动化", "部署"]', 'skill_043_CI_CD 流水线配置.txt', 1024, 0, 0, NOW()),
('Prometheus 监控配置', 'Prometheus + Grafana 监控系统搭建教程。', 'DevOps', '["监控", "Prometheus", "Grafana", "告警"]', 'skill_044_Prometheus 监控配置.txt', 1024, 0, 0, NOW()),
('Ansible 自动化脚本', 'Ansible 自动化运维脚本集合。', 'DevOps', '["Ansible", "自动化", "运维", "配置管理"]', 'skill_045_Ansible 自动化脚本.txt', 1024, 0, 0, NOW()),
('Linux 性能优化指南', 'Linux 服务器性能分析与优化实战指南。', 'DevOps', '["Linux", "性能优化", "服务器", "调优"]', 'skill_046_Linux 性能优化指南.txt', 1024, 0, 0, NOW()),
('Nginx 配置大全', '常用 Nginx 配置模板，含反向代理、负载均衡。', 'DevOps', '["Nginx", "反向代理", "负载均衡", "Web 服务器"]', 'skill_047_Nginx 配置大全.txt', 1024, 0, 0, NOW()),
('Git 工作流最佳实践', 'Git Flow、分支管理、Code Review 流程规范。', 'DevOps', '["Git", "工作流", "版本控制", "协作"]', 'skill_048_Git 工作流最佳实践.txt', 1024, 0, 0, NOW()),
('日志收集 ELK Stack', 'Elasticsearch + Logstash + Kibana 日志收集方案。', 'DevOps', '["ELK", "日志", "Elasticsearch", "监控"]', 'skill_049_日志收集_ELK_Stack.txt', 1024, 0, 0, NOW()),
('云原生架构指南', '微服务、Service Mesh、云原生架构设计指南。', 'DevOps', '["云原生", "微服务", "架构", "Service Mesh"]', 'skill_050_云原生架构指南.txt', 1024, 0, 0, NOW());

-- 验证插入结果
SELECT COUNT(*) as total_skills FROM skills;
SELECT category, COUNT(*) as count FROM skills GROUP BY category ORDER BY count DESC;
