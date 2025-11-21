# 启动应用和故障排查指南

## 问题：Gunicorn 没有反馈

如果 gunicorn 命令执行后没有任何输出，可能是：
1. 应用启动失败但没有显示错误
2. 日志文件路径问题
3. 需要前台运行查看输出

## 方法 1：前台运行 Gunicorn（推荐，可以看到输出）

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 前台运行，直接看到输出
gunicorn --bind 127.0.0.1:6657 --workers 2 app:app
```

或者使用配置文件但前台运行：

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 确保 logs 目录存在
mkdir -p logs

# 前台运行（不使用 daemon 模式）
gunicorn --config gunicorn_config.py --daemon=False app:app
```

## 方法 2：检查 Gunicorn 是否在运行

```bash
# 检查进程
ps aux | grep gunicorn

# 检查端口是否被占用
netstat -tlnp | grep 6657

# 或者使用 ss 命令
ss -tlnp | grep 6657
```

## 方法 3：查看日志文件

```bash
cd /www/wwwroot/ECF-MIS-system-opensource

# 查看错误日志
tail -f logs/error.log

# 查看访问日志
tail -f logs/access.log

# 如果日志文件不存在，检查是否有权限问题
ls -la logs/
```

## 方法 4：测试应用是否能正常导入

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 测试导入
python -c "from app import app; print('App imported successfully')"

# 测试数据库连接
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database OK')"
```

## 方法 5：使用 Python 直接运行（测试用）

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 直接运行 Flask 开发服务器
python app.py
```

如果这个能运行，说明应用本身没问题，问题在 gunicorn 配置。

## 方法 6：简化 Gunicorn 启动

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 最简单的启动方式
gunicorn app:app --bind 127.0.0.1:6657 --workers 2 --access-logfile logs/access.log --error-logfile logs/error.log
```

## 常见问题排查

### 问题 1：logs 目录不存在

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
mkdir -p logs
chmod 755 logs
```

### 问题 2：应用导入失败

```bash
# 检查所有依赖是否安装
pip list | grep -i flask
pip list | grep -i sqlalchemy

# 重新安装依赖
pip install -r requirements.txt
```

### 问题 3：数据库初始化问题

```bash
# 检查 instance 目录
ls -la instance/

# 重新初始化数据库
python init_data.py
```

### 问题 4：端口被占用

```bash
# 查看占用端口的进程
lsof -i:6657
# 或
netstat -tlnp | grep 6657

# 杀死占用进程
kill -9 <PID>
```

### 问题 5：权限问题

```bash
# 检查文件权限
ls -la /www/wwwroot/ECF-MIS-system-opensource/

# 设置正确权限
chmod -R 755 /www/wwwroot/ECF-MIS-system-opensource
chown -R www:www /www/wwwroot/ECF-MIS-system-opensource  # 如果使用 www 用户
```

## 推荐的启动方式（生产环境）

### 方式 1：使用 Systemd 服务

```bash
# 复制服务文件
sudo cp /www/wwwroot/ECF-MIS-system-opensource/ecf-mis.service /etc/systemd/system/

# 修改服务文件中的路径（如果需要）
sudo nano /etc/systemd/system/ecf-mis.service

# 重载并启动
sudo systemctl daemon-reload
sudo systemctl start ecf-mis
sudo systemctl enable ecf-mis

# 查看状态
sudo systemctl status ecf-mis

# 查看日志
sudo journalctl -u ecf-mis -f
```

### 方式 2：使用宝塔 Python 项目管理器

1. 打开宝塔面板
2. Python 项目管理器 → 添加项目
3. 填写：
   - 项目路径: `/www/wwwroot/ECF-MIS-system-opensource`
   - 框架: Flask
   - 端口: `6657`
   - 执行文件: `app:app`
4. 点击启动
5. 查看日志

### 方式 3：后台运行 Gunicorn

```bash
cd /www/wwwroot/ECF-MIS-system-opensource
source venv/bin/activate

# 确保 logs 目录存在
mkdir -p logs

# 后台运行
nohup gunicorn --config gunicorn_config.py app:app > logs/gunicorn.log 2>&1 &

# 查看进程
ps aux | grep gunicorn

# 查看日志
tail -f logs/gunicorn.log
```

## 验证应用是否运行

```bash
# 测试本地访问
curl http://127.0.0.1:6657

# 或者使用 wget
wget http://127.0.0.1:6657 -O /dev/null

# 如果返回 HTML 内容，说明应用正常运行
```

