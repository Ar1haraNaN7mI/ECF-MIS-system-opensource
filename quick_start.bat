@echo off
chcp 65001 >nul
echo ====================================
echo MIS系统 - 一键启动脚本
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python已安装
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [1/5] 创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo [✓] 虚拟环境创建成功
) else (
    echo [✓] 虚拟环境已存在
)
echo.

REM Activate virtual environment
echo [2/5] 激活虚拟环境...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [错误] 虚拟环境激活失败
    pause
    exit /b 1
)
echo [✓] 虚拟环境已激活
echo.

REM Upgrade pip
echo [3/5] 更新pip...
python -m pip install --upgrade pip --quiet
echo [✓] pip已更新
echo.

REM Install dependencies
echo [4/5] 安装依赖包...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [错误] 依赖包安装失败
    pause
    exit /b 1
)
echo [✓] 依赖包安装完成
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [5/5] 创建配置文件...
    if exist "env.example" (
        copy env.example .env >nul
        echo [✓] 已从env.example创建.env配置文件
    ) else (
        echo [警告] env.example文件不存在，将使用默认配置
    )
) else (
    echo [✓] 配置文件已存在
)
echo.

REM Create instance directory if not exists
if not exist "instance" (
    mkdir instance
    echo [✓] 已创建instance目录
)

REM Initialize database
echo [初始化] 初始化数据库...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('[✓] 数据库初始化完成')" 2>nul
if %errorlevel% neq 0 (
    echo [警告] 数据库初始化可能失败，将在启动时自动创建
)
echo.

echo ====================================
echo 环境配置完成！
echo ====================================
echo.
echo 正在启动MIS系统...
echo 访问地址: http://localhost:6657
echo.
echo 按 Ctrl+C 停止服务器
echo ====================================
echo.

REM Start the application
python app.py

