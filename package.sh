#!/bin/bash
# 龙虾 Skill 合集平台 - 打包脚本

PACKAGE_NAME="lobster-skill-platform"
VERSION="1.0.0"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_FILE="${PACKAGE_NAME}-v${VERSION}-${TIMESTAMP}.zip"

echo "🦞 正在打包龙虾 Skill 合集平台..."
echo ""

# 排除的文件和目录
EXCLUDES=(
    "venv"
    "__pycache__"
    "*.pyc"
    ".git"
    ".DS_Store"
    "data"
    "*.db"
    "backups"
)

# 构建排除参数
EXCLUDE_ARGS=""
for item in "${EXCLUDES[@]}"; do
    EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude=$item"
done

# 打包
cd ..
zip -r "$OUTPUT_FILE" "$PACKAGE_NAME/" $EXCLUDE_ARGS

echo ""
echo "✓ 打包完成！"
echo "📦 文件：$OUTPUT_FILE"
echo ""
echo "安装说明："
echo "1. 解压 ZIP 文件"
echo "2. 运行 ./start.sh (Mac/Linux) 或 start.bat (Windows)"
echo "3. 访问 http://127.0.0.1:5000"
echo ""
