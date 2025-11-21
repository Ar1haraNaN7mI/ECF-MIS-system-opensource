# 访问应用指南

## 问题说明

您访问的是 `172.19.29.217`（内网IP），这是私有IP地址，无法从外网访问。

## 正确的访问方式

### 方式 1：通过公网 IP 访问（需要配置 Nginx 反向代理）

1. **确保应用正在运行**（绑定在 127.0.0.1:6657）

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 前台运行（可以看到输出）
gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app
```

2. **在宝塔面板中配置 Nginx 反向代理**

   - 登录宝塔面板
   - 进入 **网站** → 找到您的站点（或创建新站点）
   - 点击 **设置** → **反向代理**
   - 点击 **添加反向代理**
   - 配置：
     - **代理名称**: ECF-MIS
     - **目标URL**: `http://127.0.0.1:6657`
     - **发送域名**: `$host`
     - **缓存**: 关闭
   - 点击 **提交**

3. **访问应用**

   在浏览器中访问：
   - `http://47.242.126.44` （公网IP）
   - 或您的域名（如果已配置）

### 方式 2：直接访问端口（不推荐，仅测试用）

如果想让应用直接对外提供服务：

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 绑定到 0.0.0.0（所有网络接口）
gunicorn --bind 0.0.0.0:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app
```

然后访问：`http://47.242.126.44:6657`

**注意**：需要确保防火墙开放 6657 端口。

## 推荐配置（生产环境）

### 1. 应用绑定本地（127.0.0.1）

应用只绑定在 `127.0.0.1:6657`，不对外直接暴露。

### 2. Nginx 反向代理

通过 Nginx 反向代理到应用，对外提供 HTTP/HTTPS 服务。

### 3. 配置步骤

#### 步骤 1：启动应用

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 后台运行
nohup gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app > logs/gunicorn.log 2>&1 &

# 检查是否启动
ps aux | grep gunicorn
```

#### 步骤 2：在宝塔面板配置网站

1. **添加网站**
   - 网站 → 添加站点
   - 域名：填写您的域名或直接使用 IP `47.242.126.44`
   - 根目录：`/www/wwwroot/ECF-MIS-system-opensource`
   - PHP版本：纯静态

2. **配置反向代理**
   - 网站 → 您的站点 → 设置 → 反向代理
   - 添加反向代理：
     - 代理名称: ECF-MIS
     - 目标URL: `http://127.0.0.1:6657`
     - 发送域名: `$host`
   - 提交

3. **配置静态文件（可选优化）**
   - 网站 → 设置 → 配置文件
   - 在 `location /` 之前添加：
   ```nginx
   location /static {
       alias /www/wwwroot/ECF-MIS-system-opensource/static;
       expires 30d;
   }
   ```
   - 保存并重载

#### 步骤 3：配置防火墙

- 宝塔面板 → 安全
- 确保开放端口：**80**（HTTP）、**443**（HTTPS，如果使用SSL）
- **注意**：6657 端口不需要对外开放，仅本地访问

#### 步骤 4：访问测试

- 访问：`http://47.242.126.44`
- 如果配置了域名，访问您的域名

## 故障排查

### 问题 1：无法访问

1. **检查应用是否运行**
   ```bash
   ps aux | grep gunicorn
   netstat -tlnp | grep 6657
   ```

2. **检查 Nginx 配置**
   ```bash
   # 测试 Nginx 配置
   nginx -t
   
   # 重载 Nginx
   systemctl reload nginx
   ```

3. **检查防火墙**
   - 宝塔面板 → 安全 → 查看端口是否开放

4. **查看日志**
   ```bash
   # 应用日志
   tail -f /www/wwwroot/ECF-MIS-system-opensource/logs/error.log
   
   # Nginx 日志
   # 在宝塔面板中：网站 → 日志
   ```

### 问题 2：502 Bad Gateway

这通常表示 Nginx 无法连接到应用。

1. **检查应用是否运行**
   ```bash
   curl http://127.0.0.1:6657
   ```

2. **检查 Nginx 反向代理配置**
   - 确保目标URL是 `http://127.0.0.1:6657`

3. **重启应用**
   ```bash
   pkill -f gunicorn
   cd /www/wwwroot/ECF-MIS-system-opensource
   source venv/bin/activate
   nohup gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app > logs/gunicorn.log 2>&1 &
   ```

### 问题 3：连接超时

1. **检查服务器是否可访问**
   ```bash
   ping 47.242.126.44
   ```

2. **检查防火墙规则**
   - 确保 80/443 端口开放

3. **检查云服务器安全组**
   - 在阿里云控制台检查安全组规则

## 快速启动命令

```bash
# 1. 进入项目目录
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 2. 创建日志目录
mkdir -p logs

# 3. 启动应用（前台运行，可以看到输出）
gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app
```

## 后台运行

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate
mkdir -p logs

# 后台运行
nohup gunicorn --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log --log-level info app:app > logs/gunicorn.log 2>&1 &

# 查看进程
ps aux | grep gunicorn

# 查看日志
tail -f logs/gunicorn.log
```

