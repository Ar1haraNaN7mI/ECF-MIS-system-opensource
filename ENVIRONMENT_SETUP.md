# 环境配置指南

## 快速开始

### Windows 用户

1. **运行环境配置脚本**（首次使用）：
   ```bash
   setup_env.bat
   ```
   这个脚本会自动：
   - 创建虚拟环境
   - 安装所有依赖包
   - 配置环境变量

2. **启动应用**：
   ```bash
   run.bat
   ```
   或者手动激活环境后运行：
   ```bash
   venv\Scripts\activate.bat
   python app.py
   ```

### Linux/Mac 用户

1. **运行环境配置脚本**（首次使用）：
   ```bash
   chmod +x setup_env.sh
   ./setup_env.sh
   ```

2. **启动应用**：
   ```bash
   source venv/bin/activate
   python app.py
   ```

## 手动配置步骤

### 1. 创建虚拟环境

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件（如果不存在）：

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

# Database Configuration
DATABASE_URL=sqlite:///instance/mis_database.db

# Secret Key (Change this in production!)
SECRET_KEY=dev-secret-key-change-in-production-2024

# Server Configuration
HOST=0.0.0.0
PORT=5000
```

### 4. 启动应用

```bash
python app.py
```

应用将在 `http://localhost:5000` 启动。

## 环境变量说明

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | 数据库连接字符串 | `sqlite:///instance/mis_database.db` |
| `SECRET_KEY` | Flask密钥（生产环境必须更改） | `dev-secret-key-change-in-production` |
| `FLASK_ENV` | Flask环境（development/production） | `development` |
| `FLASK_DEBUG` | 是否启用调试模式 | `1` |
| `HOST` | 服务器主机 | `0.0.0.0` |
| `PORT` | 服务器端口 | `5000` |

## 数据库配置

### SQLite (默认)
```env
DATABASE_URL=sqlite:///instance/mis_database.db
```

### PostgreSQL
```env
DATABASE_URL=postgresql://user:password@localhost/mis_database
```

### MySQL
```env
DATABASE_URL=mysql://user:password@localhost/mis_database
```

## 故障排除

### 问题1: 虚拟环境创建失败
- 确保已安装 Python 3.8 或更高版本
- 检查 Python 是否在系统 PATH 中

### 问题2: 依赖安装失败
- 升级 pip: `python -m pip install --upgrade pip`
- 使用国内镜像源（如需要）:
  ```bash
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

### 问题3: 端口被占用
- 更改 `.env` 文件中的 `PORT` 值
- 或修改 `app.py` 中的端口号

### 问题4: 数据库连接失败
- 检查 `DATABASE_URL` 配置是否正确
- 确保数据库服务正在运行（如使用 PostgreSQL/MySQL）
- 检查数据库文件权限（如使用 SQLite）

## 生产环境部署

1. **更改 SECRET_KEY**:
   ```env
   SECRET_KEY=your-very-secure-random-key-here
   ```

2. **设置 FLASK_ENV**:
   ```env
   FLASK_ENV=production
   FLASK_DEBUG=0
   ```

3. **使用生产级数据库**:
   - 推荐使用 PostgreSQL 或 MySQL
   - 配置数据库连接池

4. **使用 WSGI 服务器**:
   - 推荐使用 Gunicorn (Linux) 或 Waitress (Windows)




