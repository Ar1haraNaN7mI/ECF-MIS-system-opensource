# 完整重置并启动指南（从删除进程开始）

## 在服务器终端中，直接复制以下所有命令执行

```bash
# ============================================
# 完整重置并部署 - 从删除进程和文件开始
# ============================================

# ========== 步骤 1: 停止所有进程 ==========
echo "步骤 1/10: 停止所有进程"
pkill -f "gunicorn.*app:app" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true
pkill -f "gunicorn" 2>/dev/null || true
systemctl stop ecf-mis 2>/dev/null || true
sleep 3

# 强制杀死残留进程
if pgrep -f "gunicorn" > /dev/null; then
    echo "强制停止残留进程..."
    pkill -9 -f "gunicorn" 2>/dev/null || true
    sleep 2
fi

echo "✓ 所有进程已停止"
echo ""

# ========== 步骤 2: 删除旧项目文件 ==========
echo "步骤 2/10: 删除旧项目文件"
rm -rf /www/wwwroot/ECF-MIS-system-opensource
echo "✓ 旧项目文件已删除"
echo ""

# ========== 步骤 3: 克隆项目 ==========
echo "步骤 3/10: 克隆项目"
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource
echo "✓ 项目克隆完成"
echo ""

# ========== 步骤 4: 创建虚拟环境 ==========
echo "步骤 4/10: 创建 Python 虚拟环境"
python3 -m venv venv
source venv/bin/activate
echo "✓ 虚拟环境创建完成"
echo ""

# ========== 步骤 5: 升级 pip ==========
echo "步骤 5/10: 升级 pip"
pip install --upgrade pip --quiet
echo "✓ pip 升级完成"
echo ""

# ========== 步骤 6: 安装依赖 ==========
echo "步骤 6/10: 安装项目依赖"
pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 验证安装
python -c "import flask; print('✓ Flask', flask.__version__, '已安装')" || {
    echo "使用默认源重试..."
    pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0
}
echo "✓ 依赖安装完成"
echo ""

# ========== 步骤 7: 创建目录和配置文件 ==========
echo "步骤 7/10: 创建目录和配置文件"
mkdir -p logs instance
cp env.example .env
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || openssl rand -hex 32)
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
chmod -R 755 instance static templates
echo "✓ 目录和配置文件创建完成"
echo ""

# ========== 步骤 8: 初始化数据库 ==========
echo "步骤 8/10: 初始化数据库"
python init_data.py
echo "✓ 数据库初始化完成"
echo ""

# ========== 步骤 9: 验证应用 ==========
echo "步骤 9/10: 验证应用"
python -c "from app import app; print('✓ 应用可以导入')"
echo "✓ 应用验证完成"
echo ""

# ========== 步骤 10: 启动应用 ==========
echo "步骤 10/10: 启动应用"

# 检查端口是否被占用
if netstat -tlnp 2>/dev/null | grep -q ":6657 "; then
    echo "端口 6657 被占用，正在清理..."
    PID=$(netstat -tlnp 2>/dev/null | grep ":6657 " | awk '{print $7}' | cut -d'/' -f1)
    kill -9 $PID 2>/dev/null || true
    sleep 2
fi

# 启动应用（后台运行）
nohup gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app > logs/gunicorn.log 2>&1 &

sleep 3

# 验证启动
if ps aux | grep -q "[g]unicorn.*app:app"; then
    echo "✓ 应用启动成功！"
    echo ""
    echo "进程信息:"
    ps aux | grep "[g]unicorn.*app:app" | head -1
    echo ""
    echo "端口状态:"
    netstat -tlnp | grep 6657 || ss -tlnp | grep 6657
else
    echo "✗ 应用启动失败！"
    echo "查看日志: tail -f logs/gunicorn.log"
    exit 1
fi

echo ""
echo "=========================================="
echo "✓ 部署完成！"
echo "=========================================="
echo ""
echo "应用运行在: http://127.0.0.1:6657"
echo ""
echo "下一步："
echo "1. 在宝塔面板配置 Nginx 反向代理"
echo "   - 网站 → 您的站点 → 设置 → 反向代理"
echo "   - 目标URL: http://127.0.0.1:6657"
echo ""
echo "2. 访问应用:"
echo "   - 公网IP: http://47.242.126.44"
echo ""
echo "3. 查看日志:"
echo "   tail -f logs/error.log"
echo "   tail -f logs/gunicorn.log"
echo ""
echo "=========================================="
```

## 或者使用一键脚本

```bash
# 下载脚本
cd /www/wwwroot
rm -rf ECF-MIS-system-opensource
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource

# 给脚本添加执行权限
chmod +x COMPLETE_RESET.sh

# 执行脚本
bash COMPLETE_RESET.sh
```

## 验证部署

```bash
# 检查进程
ps aux | grep gunicorn

# 检查端口
netstat -tlnp | grep 6657

# 测试本地访问
curl http://127.0.0.1:6657

# 查看日志
tail -f /www/wwwroot/ECF-MIS-system-opensource/logs/gunicorn.log
```

## 如果启动失败

```bash
# 查看详细错误
tail -f /www/wwwroot/ECF-MIS-system-opensource/logs/error.log
tail -f /www/wwwroot/ECF-MIS-system-opensource/logs/gunicorn.log

# 前台运行查看输出
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate
gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app
```

