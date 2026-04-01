@echo off
REM 龙虾 Skill 合集平台 - Windows 打包脚本

set PACKAGE_NAME=lobster-skill-platform
set VERSION=1.0.0
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%
set OUTPUT_FILE=%PACKAGE_NAME%-v%VERSION%-%TIMESTAMP%.zip

echo 🦞 正在打包龙虾 Skill 合集平台...
echo.

cd ..

REM 使用 PowerShell 压缩
powershell -Command "Compress-Archive -Path '%PACKAGE_NAME%' -DestinationPath '%OUTPUT_FILE%' -Force"

echo.
echo ✓ 打包完成！
echo 📦 文件：%OUTPUT_FILE%
echo.
echo 安装说明：
echo 1. 解压 ZIP 文件
echo 2. 运行 start.bat
echo 3. 访问 http://127.0.0.1:5000
echo.

pause
