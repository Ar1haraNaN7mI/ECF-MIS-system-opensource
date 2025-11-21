# 宝塔面板快速部署指南

## 服务器信息
- **IP地址**: 47.242.126.44
- **系统**: 宝塔Linux面板

## 快速部署步骤（5分钟）

### 1. 上传项目到服务器

**方法一：使用 Git（推荐）**
```bash
cd /www/wwwroot
git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
cd ECF-MIS-system-opensource
```

**方法二：使用宝塔面板文件管理器**
- 登录宝塔面板 → 文件 → 进入 `/www/wwwroot/`
- 上传项目压缩包并解压

### 2. 使用宝塔 Python 项目管理器部署

1. **安装 Python 项目管理器**
   - 宝塔面板 → 软件商店 → 搜索 "Python项目管理器" → 安装

2. **添加 Python 项目**
   - 打开 Python 项目管理器
   - 点击 **添加 Python 项目**
   - 填写信息：
     ```
     项目名称: ECF-MIS
     项目路径: /www/wwwroot/ECF-MIS-system-opensource
     Python版本: Python 3.8+ (选择已安装的版本)
     框架: Flask
     启动文件: app.py
     端口: 6657
     项目执行文件: app:app
     ```
   - 点击 **提交**

3. **安装依赖**
   - 在项目列表中，找到 ECF-MIS 项目
   - 点击 **模块** → **安装模块**
   - 或使用终端：
     ```bash
     cd /www/wwwroot/ECF-MIS-system-opensource
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **配置环境变量**
   - 在项目目录下创建 `.env` 文件：
     ```bash
     cd /www/wwwroot/ECF-MIS-system-opensource
     cp env.example .env
     nano .env
     ```
   - 修改 `SECRET_KEY` 为随机字符串（重要！）
   - 保存文件

5. **初始化数据库**
   ```bash
   source venv/bin/activate
   python init_data.py
   ```

6. **启动项目**
   - 在 Python 项目管理器中，点击 **启动**

### 3. 配置网站和反向代理

1. **添加网站**
   - 宝塔面板 → 网站 → 添加站点
   - 域名：填写您的域名或直接使用 IP
   - 根目录：`/www/wwwroot/ECF-MIS-system-opensource`
   - PHP版本：纯静态

2. **配置反向代理**
   - 网站 → 找到您的站点 → 设置 → 反向代理
   - 添加反向代理：
     ```
     代理名称: ECF-MIS
     目标URL: http://127.0.0.1:6657
     发送域名: $host
     ```
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
   - 保存并重载配置

### 4. 配置防火墙

- 宝塔面板 → 安全
- 开放端口：80, 443（如果使用 HTTPS）
- **注意**：6657 端口不需要对外开放，仅本地访问

### 5. 访问测试

- 打开浏览器访问：`http://47.242.126.44` 或您的域名
- 如果看到 MIS 系统界面，说明部署成功！

## 常见问题

### Q: 502 Bad Gateway
**A:** 
1. 检查 Python 项目是否已启动（在 Python 项目管理器中查看）
2. 检查端口 6657 是否被占用
3. 查看项目日志

### Q: 静态文件无法加载
**A:** 
1. 检查 Nginx 配置中的静态文件路径
2. 检查文件权限：`chmod -R 755 static`

### Q: 数据库错误
**A:** 
1. 运行 `python init_data.py` 初始化数据库
2. 检查 `instance` 目录权限：`chmod -R 755 instance`

## 更新代码

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
# 在宝塔面板 Python 项目管理器中重启项目
```

## 详细文档

更多详细信息请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

