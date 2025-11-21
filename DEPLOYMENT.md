# 宝塔面板部署指南

本指南将帮助您将 ECF MIS 系统部署到宝塔面板服务器上。

## 服务器信息
- **服务器IP**: 47.242.126.44
- **系统**: 宝塔Linux面板 阿里云专享版 9.2.0
- **地域**: 中国香港

## 部署步骤

### 第一步：上传项目文件到服务器

#### 方法一：使用 Git 克隆（推荐）

1. 通过宝塔面板的 **终端** 功能，或使用 SSH 工具（如 PuTTY、Xshell）连接到服务器
2. 进入网站目录（通常在 `/www/wwwroot/` 下）
3. 克隆项目：

```bash
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource
```

#### 方法二：使用宝塔面板文件管理器

1. 登录宝塔面板
2. 进入 **文件** 管理
3. 进入 `/www/wwwroot/` 目录
4. 上传项目压缩包并解压，或使用 **远程下载** 功能下载 GitHub 项目

### 第二步：安装 Python 环境

1. 在宝塔面板中，进入 **软件商店**
2. 搜索并安装 **Python项目管理器**（如果未安装）
3. 或者通过终端安装 Python 3.8+：

```bash
# 检查 Python 版本
python3 --version

# 如果没有 Python 3，安装它
# CentOS/RHEL:
yum install python3 python3-pip -y

# Ubuntu/Debian:
apt-get update
apt-get install python3 python3-pip python3-venv -y
```

### 第三步：创建 Python 虚拟环境

在项目目录下创建虚拟环境：

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
python3 -m venv venv
source venv/bin/activate
```

### 第四步：安装项目依赖

```bash
# 确保在虚拟环境中
pip install --upgrade pip
pip install -r requirements.txt

# 安装 Gunicorn（生产环境 WSGI 服务器）
pip install gunicorn
```

### 第五步：配置环境变量

1. 复制环境变量示例文件：

```bash
cp env.example .env
```

2. 编辑 `.env` 文件，修改生产环境配置：

```bash
nano .env
```

或使用宝塔面板的文件编辑器编辑 `.env` 文件。

配置内容：

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=production
FLASK_DEBUG=0

# Database Configuration
DATABASE_URL=sqlite:///instance/mis_database.db

# Secret Key (必须更改！)
SECRET_KEY=your-production-secret-key-here-change-this

# Server Configuration
HOST=127.0.0.1
PORT=6657
```

**重要**: 请将 `SECRET_KEY` 更改为一个强随机字符串！

### 第六步：初始化数据库

```bash
# 确保在虚拟环境中
source venv/bin/activate
python init_data.py
```

### 第七步：使用宝塔面板 Python 项目管理器部署

#### 方法一：使用 Python 项目管理器（推荐）

1. 在宝塔面板中，进入 **软件商店** → **Python项目管理器**
2. 点击 **添加 Python 项目**
3. 填写项目信息：
   - **项目名称**: ECF-MIS
   - **项目路径**: `/www/wwwroot/ECF-MIS-system-opensource`
   - **Python 版本**: 选择已安装的 Python 3.x
   - **框架**: Flask
   - **启动文件**: `app.py`
   - **端口**: `6657`
   - **项目执行文件**: `app:app`
4. 点击 **提交**
5. 在项目列表中，找到刚创建的项目，点击 **启动**

#### 方法二：使用 Gunicorn + Systemd（手动配置）

1. 创建 Gunicorn 配置文件：

创建文件 `/www/wwwroot/ECF-MIS-system-opensource/gunicorn_config.py`：

```python
bind = "127.0.0.1:6657"
workers = 4
worker_class = "sync"
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 50
accesslog = "/www/wwwroot/ECF-MIS-system-opensource/logs/access.log"
errorlog = "/www/wwwroot/ECF-MIS-system-opensource/logs/error.log"
loglevel = "info"
```

2. 创建日志目录：

```bash
mkdir -p /www/wwwroot/ECF-MIS-system-opensource/logs
```

3. 创建 Systemd 服务文件：

创建文件 `/etc/systemd/system/ecf-mis.service`：

```ini
[Unit]
Description=ECF MIS System Gunicorn Service
After=network.target

[Service]
User=www
Group=www
WorkingDirectory=/www/wwwroot/ECF-MIS-system-opensource
Environment="PATH=/www/wwwroot/ECF-MIS-system-opensource/venv/bin"
ExecStart=/www/wwwroot/ECF-MIS-system-opensource/venv/bin/gunicorn --config gunicorn_config.py app:app

[Install]
WantedBy=multi-user.target
```

4. 启动服务：

```bash
systemctl daemon-reload
systemctl enable ecf-mis
systemctl start ecf-mis
systemctl status ecf-mis
```

### 第八步：配置 Nginx 反向代理

1. 在宝塔面板中，进入 **网站** → **添加站点**
2. 填写站点信息：
   - **域名**: 您的域名（如 `mis.yourdomain.com`）或直接使用 IP
   - **根目录**: `/www/wwwroot/ECF-MIS-system-opensource`
   - **PHP版本**: 纯静态（不需要 PHP）
3. 点击 **提交**

4. 配置 Nginx 反向代理：
   - 进入 **网站** → 找到刚创建的站点 → **设置**
   - 进入 **反向代理** 标签
   - 点击 **添加反向代理**
   - 配置如下：
     - **代理名称**: ECF-MIS
     - **目标URL**: `http://127.0.0.1:6657`
     - **发送域名**: `$host`
     - **缓存**: 关闭
   - 点击 **提交**

5. 或者手动编辑 Nginx 配置：

在站点配置文件中添加：

```nginx
location / {
    proxy_pass http://127.0.0.1:6657;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_connect_timeout 60s;
    proxy_send_timeout 60s;
    proxy_read_timeout 60s;
}

# 静态文件直接服务
location /static {
    alias /www/wwwroot/ECF-MIS-system-opensource/static;
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### 第九步：配置防火墙

1. 在宝塔面板中，进入 **安全**
2. 确保以下端口已开放：
   - **80** (HTTP)
   - **443** (HTTPS，如果使用 SSL)
   - **6657** (仅本地访问，不需要对外开放)

### 第十步：配置 SSL 证书（可选但推荐）

1. 在宝塔面板中，进入 **网站** → 找到您的站点 → **设置**
2. 进入 **SSL** 标签
3. 选择 **Let's Encrypt** 免费证书
4. 填写域名，点击 **申请**
5. 开启 **强制 HTTPS**

### 第十一步：测试部署

1. 访问您的域名或 IP 地址
2. 检查应用是否正常运行
3. 查看日志文件确认没有错误：
   - 应用日志: `/www/wwwroot/ECF-MIS-system-opensource/logs/error.log`
   - Nginx 日志: 在宝塔面板的 **网站** → **日志** 中查看

## 常用管理命令

### 启动/停止/重启应用

如果使用 Python 项目管理器：
- 在宝塔面板中操作即可

如果使用 Systemd：
```bash
systemctl start ecf-mis      # 启动
systemctl stop ecf-mis       # 停止
systemctl restart ecf-mis    # 重启
systemctl status ecf-mis     # 查看状态
```

### 查看日志

```bash
# 应用日志
tail -f /www/wwwroot/ECF-MIS-system-opensource/logs/error.log

# Nginx 访问日志
tail -f /www/wwwroot/ECF-MIS-system-opensource/logs/access.log
```

### 更新代码

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
systemctl restart ecf-mis  # 或通过宝塔面板重启
```

## 故障排查

### 问题1: 应用无法启动

- 检查 Python 版本和虚拟环境是否正确
- 检查依赖是否全部安装
- 查看日志文件中的错误信息

### 问题2: 502 Bad Gateway

- 检查应用是否在运行: `systemctl status ecf-mis`
- 检查端口 6657 是否被占用: `netstat -tlnp | grep 6657`
- 检查 Nginx 反向代理配置是否正确

### 问题3: 数据库错误

- 检查 `instance` 目录权限: `chmod -R 755 instance`
- 检查数据库文件是否存在
- 重新初始化数据库: `python init_data.py`

### 问题4: 静态文件无法加载

- 检查 Nginx 配置中的静态文件路径
- 检查文件权限: `chmod -R 755 static`

## 性能优化建议

1. **使用 Gunicorn**: 生产环境不要使用 Flask 自带的开发服务器
2. **配置 Worker 数量**: 根据服务器 CPU 核心数调整 `workers` 参数
3. **启用缓存**: 对静态文件启用浏览器缓存
4. **使用 CDN**: 将静态资源放到 CDN 上
5. **数据库优化**: 如果数据量大，考虑迁移到 PostgreSQL 或 MySQL

## 安全建议

1. **更改 SECRET_KEY**: 使用强随机字符串
2. **关闭调试模式**: 生产环境设置 `FLASK_DEBUG=0`
3. **配置防火墙**: 只开放必要端口
4. **使用 HTTPS**: 配置 SSL 证书
5. **定期备份**: 备份数据库和重要文件
6. **更新依赖**: 定期更新 Python 包以修复安全漏洞

## 备份策略

```bash
# 备份数据库
cp /www/wwwroot/ECF-MIS-system-opensource/instance/mis_database.db /backup/mis_database_$(date +%Y%m%d).db

# 备份整个项目
tar -czf /backup/ecf-mis-$(date +%Y%m%d).tar.gz /www/wwwroot/ECF-MIS-system-opensource
```

## 联系支持

如遇到问题，请查看：
- 项目 README.md
- 日志文件
- GitHub Issues

