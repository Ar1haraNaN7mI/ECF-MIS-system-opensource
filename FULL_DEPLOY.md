# 完整部署指令（从重置开始）

## 在服务器终端中，直接复制以下所有命令执行

```bash
# ============================================
# ECF MIS 系统 - 完整重置并部署
# ============================================

# ========== 第一步：停止并清空旧项目 ==========
echo "=========================================="
echo "步骤 1/8: 停止所有进程并清空旧项目"
echo "=========================================="

# 停止所有相关进程
pkill -f "gunicorn.*app:app" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true
systemctl stop ecf-mis 2>/dev/null || true
sleep 2

# 删除旧项目
rm -rf /www/wwwroot/ECF-MIS-system-opensource

echo "✓ 旧项目已清空"

# ========== 第二步：克隆项目 ==========
echo ""
echo "=========================================="
echo "步骤 2/8: 克隆项目"
echo "=========================================="

cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource

echo "✓ 项目克隆完成"

# ========== 第三步：创建虚拟环境 ==========
echo ""
echo "=========================================="
echo "步骤 3/8: 创建 Python 虚拟环境"
echo "=========================================="

python3 -m venv venv
source venv/bin/activate

echo "✓ 虚拟环境创建完成"

# ========== 第四步：升级 pip ==========
echo ""
echo "=========================================="
echo "步骤 4/8: 升级 pip"
echo "=========================================="

pip install --upgrade pip --quiet

echo "✓ pip 升级完成"

# ========== 第五步：安装依赖 ==========
echo ""
echo "=========================================="
echo "步骤 5/8: 安装项目依赖（使用阿里云镜像源）"
echo "=========================================="

# 直接安装，使用阿里云镜像源中实际可用的版本
pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 验证安装
python -c "import flask; print('✓ Flask', flask.__version__, '已安装')" || {
    echo "✗ Flask 安装失败，尝试使用默认源..."
    pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0
}

echo "✓ 依赖安装完成"

# ========== 第六步：创建目录和配置文件 ==========
echo ""
echo "=========================================="
echo "步骤 6/8: 创建目录和配置文件"
echo "=========================================="

# 创建必要目录
mkdir -p logs instance

# 复制环境变量文件
cp env.example .env

# 生成 SECRET_KEY 并更新到 .env
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || openssl rand -hex 32)
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env

# 设置文件权限
chmod -R 755 instance static templates

echo "✓ 目录和配置文件创建完成"

# ========== 第七步：初始化数据库 ==========
echo ""
echo "=========================================="
echo "步骤 7/8: 初始化数据库"
echo "=========================================="

python init_data.py

echo "✓ 数据库初始化完成"

# ========== 第八步：验证应用 ==========
echo ""
echo "=========================================="
echo "步骤 8/8: 验证应用"
echo "=========================================="

python -c "from app import app; print('✓ 应用导入成功')" || {
    echo "✗ 应用验证失败！"
    exit 1
}

# ========== 完成 ==========
echo ""
echo "=========================================="
echo "✓ 部署完成！"
echo "=========================================="
echo ""
echo "项目目录: /www/wwwroot/ECF-MIS-system-opensource"
echo ""
echo "启动应用的方法："
echo ""
echo "方法 1 - 使用 Gunicorn（推荐生产环境）："
echo "  cd /www/wwwroot/ECF-MIS-system-opensource"
echo "  source venv/bin/activate"
echo "  gunicorn --config gunicorn_config.py app:app"
echo ""
echo "方法 2 - 使用宝塔 Python 项目管理器："
echo "  1. 打开宝塔面板"
echo "  2. Python 项目管理器 → 添加项目"
echo "  3. 填写信息："
echo "     - 项目路径: /www/wwwroot/ECF-MIS-system-opensource"
echo "     - 框架: Flask"
echo "     - 端口: 6657"
echo "     - 执行文件: app:app"
echo "  4. 点击启动"
echo ""
echo "方法 3 - 直接运行（测试用）："
echo "  cd /www/wwwroot/ECF-MIS-system-opensource"
echo "  source venv/bin/activate"
echo "  python app.py"
echo ""
echo "配置 Nginx 反向代理："
echo "  在宝塔面板中："
echo "  网站 → 您的站点 → 设置 → 反向代理"
echo "  添加反向代理到: http://127.0.0.1:6657"
echo ""
echo "=========================================="
```

## 一键执行脚本

如果上面的命令太长，也可以使用脚本：

```bash
# 下载并执行部署脚本
cd /www/wwwroot
rm -rf ECF-MIS-system-opensource
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource
chmod +x QUICK_DEPLOY.sh
bash QUICK_DEPLOY.sh
```

## 故障排查

### 如果步骤 5 安装失败

```bash
# 尝试使用默认 PyPI 源
pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0

# 或者不指定版本（使用最新可用版本）
pip install Flask Flask-SQLAlchemy Flask-CORS python-dotenv Werkzeug gunicorn
```

### 如果虚拟环境未激活

```bash
# 确保激活虚拟环境
source venv/bin/activate

# 检查（应该显示 venv 路径）
which python
```

### 如果数据库初始化失败

```bash
# 检查权限
chmod -R 755 instance

# 重新初始化
python init_data.py
```

### 如果应用验证失败

```bash
# 检查所有依赖是否安装
pip list | grep -i flask
pip list | grep -i sqlalchemy

# 重新安装依赖
pip install -r requirements.txt
```

