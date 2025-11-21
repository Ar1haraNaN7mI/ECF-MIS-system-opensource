# 清空并重新部署指南

如果遇到部署问题，可以使用以下方法清空并重新部署。

## 方法一：使用自动化脚本（推荐）

### 步骤 1: 清空旧项目

在服务器终端执行以下命令：

```bash
# 停止所有相关进程
pkill -f "gunicorn.*app:app" 2>/dev/null || true
systemctl stop ecf-mis 2>/dev/null || true

# 删除旧项目
rm -rf /www/wwwroot/ECF-MIS-system-opensource

# 进入 wwwroot 目录
cd /www/wwwroot
```

### 步骤 2: 下载并运行部署脚本

```bash
# 克隆项目
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource

# 给脚本添加执行权限
chmod +x deploy_server.sh

# 运行部署脚本
bash deploy_server.sh
```

脚本会自动完成：
- ✅ 创建 Python 虚拟环境
- ✅ 安装所有依赖
- ✅ 创建必要的目录
- ✅ 生成 .env 配置文件
- ✅ 初始化数据库
- ✅ 设置文件权限

## 方法二：手动部署（逐步执行）

### 1. 清空旧项目

```bash
# 停止服务
pkill -f "gunicorn" || true
systemctl stop ecf-mis 2>/dev/null || true

# 删除旧项目
rm -rf /www/wwwroot/ECF-MIS-system-opensource
```

### 2. 克隆项目

```bash
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource
```

### 3. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

### 4. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

### 5. 创建必要目录

```bash
mkdir -p logs
mkdir -p instance
```

### 6. 配置环境变量

```bash
# 复制环境变量文件
cp env.example .env

# 编辑 .env 文件（可选，脚本会自动生成 SECRET_KEY）
nano .env
```

### 7. 初始化数据库

```bash
# 确保虚拟环境已激活
source venv/bin/activate

# 初始化数据库
python init_data.py
```

### 8. 设置权限

```bash
chmod -R 755 instance
chmod -R 755 static
chmod -R 755 templates
```

### 9. 测试应用

```bash
# 测试导入
python -c "from app import app; print('OK')"

# 如果成功，可以启动应用测试
python app.py
# 按 Ctrl+C 停止测试
```

## 方法三：使用宝塔 Python 项目管理器

### 1. 清空旧项目

在宝塔面板中：
- 进入 **文件** 管理
- 找到 `/www/wwwroot/ECF-MIS-system-opensource`
- 删除整个文件夹

### 2. 重新克隆项目

在宝塔面板终端中：

```bash
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
```

### 3. 使用 Python 项目管理器

1. 打开 **Python 项目管理器**
2. 点击 **添加 Python 项目**
3. 填写信息：
   - **项目名称**: ECF-MIS
   - **项目路径**: `/www/wwwroot/ECF-MIS-system-opensource`
   - **Python版本**: 选择已安装的版本（如 Python 3.8）
   - **框架**: Flask
   - **启动文件**: `app.py`
   - **端口**: `6657`
   - **项目执行文件**: `app:app`
4. 点击 **提交**

5. 在项目列表中：
   - 点击 **模块** → **安装模块**
   - 等待依赖安装完成

6. 点击 **启动** 按钮

### 4. 配置反向代理

- 网站 → 您的站点 → 设置 → 反向代理
- 添加反向代理到 `http://127.0.0.1:6657`

## 常见问题解决

### 问题 1: 虚拟环境创建失败

```bash
# 检查 Python 版本
python3 --version

# 如果没有 Python3，安装它
# CentOS/RHEL:
yum install python3 python3-pip -y

# Ubuntu/Debian:
apt-get update
apt-get install python3 python3-pip python3-venv -y
```

### 问题 2: pip 安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像源（如果网络慢）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题 3: 数据库初始化失败

```bash
# 检查 instance 目录权限
ls -la instance

# 设置权限
chmod -R 755 instance

# 重新初始化
python init_data.py
```

### 问题 4: 端口被占用

```bash
# 查看端口占用
netstat -tlnp | grep 6657

# 杀死占用进程
kill -9 <PID>

# 或修改 .env 文件中的 PORT
```

## 验证部署

部署完成后，验证步骤：

```bash
# 1. 检查虚拟环境
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate
which python  # 应该显示 venv 中的 python

# 2. 检查依赖
pip list | grep Flask  # 应该显示 Flask

# 3. 测试应用
python -c "from app import app; print('Application OK')"

# 4. 检查数据库
ls -la instance/mis_database.db  # 应该存在

# 5. 启动应用测试
python app.py
# 访问 http://服务器IP:6657 测试
```

## 生产环境启动

### 使用 Gunicorn（推荐）

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate
gunicorn --config gunicorn_config.py app:app
```

### 使用 Systemd 服务

```bash
# 复制服务文件
sudo cp ecf-mis.service /etc/systemd/system/

# 重载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start ecf-mis

# 设置开机自启
sudo systemctl enable ecf-mis

# 查看状态
sudo systemctl status ecf-mis
```

## 下一步

部署完成后：
1. ✅ 配置 Nginx 反向代理
2. ✅ 配置 SSL 证书（可选）
3. ✅ 配置防火墙规则
4. ✅ 设置定期备份

详细配置请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

