@echo off
REM 龙虾 Skill 合集平台 - Windows 启动脚本

echo 🦞 龙虾 Skill 合集平台
echo ======================
echo.

REM 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo ✓ Python 已安装

REM 创建虚拟环境（如果不存在）
if not exist "venv" (
    echo 📦 创建虚拟环境...
    python -m venv venv
)

REM 激活虚拟环境
echo 🔧 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖
echo 📥 安装依赖...
pip install -r requirements.txt -q

REM 创建数据目录
echo 📁 初始化数据目录...
if not exist "data" mkdir data
if not exist "data\skills" mkdir data\skills
if not exist "data\users" mkdir data\users
if not exist "data\backups" mkdir data\backups

REM 启动应用
echo.
echo 🚀 启动 Web 服务...
echo 访问地址：http://127.0.0.1:5000
echo 按 Ctrl+C 停止服务
echo.

python app.py
pause
