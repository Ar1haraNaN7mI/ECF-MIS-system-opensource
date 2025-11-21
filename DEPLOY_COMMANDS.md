# 服务器部署命令（直接复制执行）

## 完整清空并重新部署（一键执行）

在服务器终端中，**直接复制以下所有命令并执行**：

```bash
# ============================================
# 完整清空并重新部署脚本
# ============================================

# 1. 停止所有进程
pkill -f "gunicorn" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true
systemctl stop ecf-mis 2>/dev/null || true

# 2. 删除旧项目
rm -rf /www/wwwroot/ECF-MIS-system-opensource

# 3. 克隆项目
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource

# 4. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 5. 升级 pip
pip install --upgrade pip

# 6. 配置 pip 使用国内镜像（加速下载）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 7. 安装依赖（使用阿里云镜像源，版本兼容）
pip install Flask==2.0.3 Flask-SQLAlchemy==3.0.0 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0 -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 如果上面失败，使用默认源重试：
# pip install -r requirements.txt

# 8. 验证 Flask 安装
python -c "import flask; print('Flask version:', flask.__version__)"

# 如果 Flask 未安装，手动安装：
# pip install Flask Flask-SQLAlchemy Flask-CORS python-dotenv Werkzeug gunicorn

# 9. 创建目录
mkdir -p logs instance

# 10. 配置环境变量
cp env.example .env

# 11. 生成 SECRET_KEY 并更新到 .env
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || openssl rand -hex 32)
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env

# 12. 设置权限
chmod -R 755 instance static templates

# 13. 初始化数据库
python init_data.py

# 14. 验证应用
python -c "from app import app; print('Application OK')"

echo "=========================================="
echo "部署完成！"
echo "=========================================="
echo "启动应用："
echo "  cd /www/wwwroot/ECF-MIS-system-opensource"
echo "  source venv/bin/activate"
echo "  gunicorn --config gunicorn_config.py app:app"
echo "=========================================="
```

## 分步执行（如果一键执行失败）

### 步骤 1: 清空旧项目
```bash
pkill -f "gunicorn" 2>/dev/null || true
pkill -f "python.*app.py" 2>/dev/null || true
rm -rf /www/wwwroot/ECF-MIS-system-opensource
```

### 步骤 2: 克隆项目
```bash
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource
```

### 步骤 3: 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
```

### 步骤 4: 安装依赖（使用国内镜像）
```bash
pip install --upgrade pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
pip install -r requirements.txt
```

### 步骤 5: 如果步骤 4 失败，使用默认源
```bash
pip config unset global.index-url
pip install -r requirements.txt
```

### 步骤 6: 手动安装 Flask（如果仍然失败）
```bash
pip install Flask==2.0.3 Flask-SQLAlchemy==3.0.0 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0
```

### 步骤 7: 验证 Flask 安装
```bash
python -c "import flask; print('Flask version:', flask.__version__)"
```

### 步骤 8: 设置项目
```bash
mkdir -p logs instance
cp env.example .env
SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
chmod -R 755 instance static templates
```

### 步骤 9: 初始化数据库
```bash
python init_data.py
```

### 步骤 10: 验证应用
```bash
python -c "from app import app; print('Application OK')"
```

## 启动应用

### 方法 1: 使用 Gunicorn（推荐）
```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate
gunicorn --config gunicorn_config.py app:app
```

### 方法 2: 直接运行（测试用）
```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate
python app.py
```

### 方法 3: 使用宝塔 Python 项目管理器
1. 打开宝塔面板
2. Python 项目管理器 → 添加项目
3. 填写：
   - 项目路径: `/www/wwwroot/ECF-MIS-system-opensource`
   - 框架: Flask
   - 端口: `6657`
   - 执行文件: `app:app`
4. 点击启动

## 故障排查

### 问题：Flask 安装失败
```bash
# 尝试使用具体版本（兼容阿里云镜像源）
pip install Flask==2.0.3 Flask-SQLAlchemy==3.0.0 Flask-CORS==3.0.10 python-dotenv==1.0.0 Werkzeug==2.0.3 gunicorn==20.1.0

# 或者不指定版本（使用最新可用版本）
pip install Flask Flask-SQLAlchemy Flask-CORS python-dotenv Werkzeug gunicorn
```

### 问题：pip 安装很慢
```bash
# 使用国内镜像
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
```

### 问题：虚拟环境未激活
```bash
# 确保激活虚拟环境
source venv/bin/activate

# 检查是否激活（应该显示 (venv)）
which python  # 应该显示 /www/wwwroot/ECF-MIS-system-opensource/venv/bin/python
```

### 问题：数据库初始化失败
```bash
# 检查权限
chmod -R 755 instance

# 重新初始化
python init_data.py
```

