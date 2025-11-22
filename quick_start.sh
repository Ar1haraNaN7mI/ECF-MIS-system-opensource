#!/bin/bash

echo "===================================="
echo "MIS系统 - 一键启动脚本"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到Python3，请先安装Python 3.7或更高版本"
    echo "安装命令: sudo apt-get install python3 python3-pip python3-venv"
    exit 1
fi

echo "[✓] Python已安装"
python3 --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[1/5] 创建虚拟环境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[错误] 虚拟环境创建失败"
        exit 1
    fi
    echo "[✓] 虚拟环境创建成功"
else
    echo "[✓] 虚拟环境已存在"
fi
echo ""

# Activate virtual environment
echo "[2/5] 激活虚拟环境..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[错误] 虚拟环境激活失败"
    exit 1
fi
echo "[✓] 虚拟环境已激活"
echo ""

# Upgrade pip
echo "[3/5] 更新pip..."
python -m pip install --upgrade pip --quiet
echo "[✓] pip已更新"
echo ""

# Install dependencies
echo "[4/5] 安装依赖包..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[错误] 依赖包安装失败"
    exit 1
fi
echo "[✓] 依赖包安装完成"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[5/5] 创建配置文件..."
    if [ -f "env.example" ]; then
        cp env.example .env
        echo "[✓] 已从env.example创建.env配置文件"
    else
        echo "[警告] env.example文件不存在，将使用默认配置"
    fi
else
    echo "[✓] 配置文件已存在"
fi
echo ""

# Create instance directory if not exists
if [ ! -d "instance" ]; then
    mkdir -p instance
    echo "[✓] 已创建instance目录"
fi

# Initialize database
echo "[初始化] 初始化数据库..."
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('[✓] 数据库初始化完成')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[警告] 数据库初始化可能失败，将在启动时自动创建"
fi
echo ""

echo "===================================="
echo "环境配置完成！"
echo "===================================="
echo ""
echo "正在启动MIS系统..."
echo "访问地址: http://localhost:6657"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "===================================="
echo ""

# Start the application
python app.py

