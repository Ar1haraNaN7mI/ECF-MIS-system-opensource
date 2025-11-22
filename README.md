# MIS管理系统 - 老年护理基金会

这是一个完整的管理信息系统(MIS)，用于管理老年护理基金会的财务、捐赠、库存和员工数据。

## 功能特性

### 财务管理
- 财务记录管理（收入、支出、捐赠）
- 财务趋势分析
- 支出分类统计
- 财务报表生成

### 捐赠管理
- 捐赠记录管理
- 捐赠者信息管理
- 捐赠者人口统计分析（年龄组、地区分布）
- 顶级捐赠者排名

### 库存管理
- 库存物品管理
- 需求计划管理
- 供应商管理
- 采购订单管理

### 员工管理
- 员工信息管理
- 考勤记录
- 排班管理
- 绩效评估

### 数据可视化
- 财务趋势图表
- 捐赠趋势图表
- 支出分类饼图
- 捐赠者人口统计图表
- 顶级捐赠者柱状图

## 技术栈

- **后端**: Flask (Python)
- **数据库**: SQLite (可配置为其他数据库)
- **前端**: HTML5, CSS3, JavaScript
- **图表库**: Chart.js

## 安装和运行

### 方式一：一键启动脚本（最简单，推荐）

**Windows 用户：**
```bash
# 双击运行 quick_start.bat 或在命令行执行：
quick_start.bat
```

**Linux/Mac 用户：**
```bash
# 添加执行权限并运行
chmod +x quick_start.sh
./quick_start.sh
```

一键启动脚本会自动完成以下操作：
- ✅ 检查Python环境
- ✅ 创建虚拟环境（如果不存在）
- ✅ 安装/更新所有依赖包
- ✅ 创建配置文件（从env.example）
- ✅ 初始化数据库
- ✅ 启动应用服务器

启动后访问：`http://localhost:6657`

### 方式二：分步安装（适合需要自定义配置）

**Windows 用户：**
```bash
# 首次使用，配置环境
setup_env.bat

# 启动应用
run.bat
```

**Linux/Mac 用户：**
```bash
# 首次使用，配置环境
chmod +x setup_env.sh
./setup_env.sh

# 启动应用
source venv/bin/activate
python app.py
```

### 方式二：手动配置

#### 1. 创建虚拟环境

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

#### 2. 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 3. 配置环境变量

复制 `env.example` 为 `.env` 文件：
```bash
# Windows
copy env.example .env

# Linux/Mac
cp env.example .env
```

然后根据需要修改 `.env` 文件中的配置。

#### 4. 运行应用

```bash
python app.py
```

应用将在 `http://localhost:6657` 启动。

### 3. 访问系统

在浏览器中打开 `http://localhost:6657` 即可使用MIS系统。

> **注意**: 首次运行会自动创建数据库文件。

## 服务器部署

### 宝塔面板部署（推荐）

详细的宝塔面板部署指南请参考：
- [宝塔面板快速部署指南](BAOTA_QUICK_START.md) - 5分钟快速部署
- [完整部署文档](DEPLOYMENT.md) - 详细部署步骤和故障排查

### 快速部署步骤

1. **克隆项目到服务器**
   ```bash
   cd /www/wwwroot
   git clone https://github.com/Ar1haraNaN7mI/ECF-MIS-system-opensource.git
   cd ECF-MIS-system-opensource
   ```

2. **创建虚拟环境并安装依赖**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install Flask==2.0.3 Flask-SQLAlchemy==2.5.1 Flask-CORS==3.0.10 python-dotenv==0.20.0 Werkzeug==2.0.3 gunicorn==20.1.0
   ```

3. **配置环境变量**
   ```bash
   cp env.example .env
   # 编辑 .env 文件，设置 HOST=0.0.0.0 以便公网访问
   ```

4. **初始化数据库**
   ```bash
   python init_data.py
   ```

5. **启动应用**
   ```bash
   python app.py
   # 或使用 gunicorn（生产环境推荐）
   gunicorn --bind 0.0.0.0:6657 --workers 2 app:app
   ```

6. **配置 Nginx 反向代理**（在宝塔面板中）
   - 网站 → 您的站点 → 设置 → 反向代理
   - 目标URL: `http://127.0.0.1:6657`

7. **配置防火墙**
   - 开放端口 80（HTTP）和 443（HTTPS）
   - 如果直接访问应用，开放端口 6657

## 项目结构

```
eldercare-fundation/
├── app.py                 # Flask应用主文件
├── models.py              # 数据库模型定义
├── requirements.txt       # Python依赖包
├── quick_start.bat        # Windows一键启动脚本
├── quick_start.sh         # Linux/Mac一键启动脚本
├── setup_env.bat          # Windows环境配置脚本
├── setup_env.sh           # Linux/Mac环境配置脚本
├── run.bat                # Windows运行脚本
├── env.example            # 环境变量配置示例
├── routes/               # API路由
│   ├── __init__.py
│   ├── financial.py      # 财务管理路由
│   ├── donation.py       # 捐赠管理路由
│   ├── inventory.py      # 库存管理路由
│   ├── staff.py          # 员工管理路由
│   ├── dashboard.py      # 仪表板路由
│   └── utils.py          # 工具函数
├── templates/            # HTML模板
│   └── index.html
└── static/               # 静态文件
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## API端点

### 财务管理
- `GET /api/financial/records` - 获取财务记录
- `POST /api/financial/records` - 创建财务记录
- `GET /api/financial/summary` - 获取财务摘要
- `GET /api/financial/expenses` - 获取支出记录

### 捐赠管理
- `GET /api/donation/donations` - 获取捐赠记录
- `POST /api/donation/donations` - 创建捐赠
- `GET /api/donation/donors` - 获取捐赠者列表
- `POST /api/donation/donors` - 创建捐赠者
- `GET /api/donation/demographics` - 获取捐赠者人口统计

### 库存管理
- `GET /api/inventory/items` - 获取库存项
- `POST /api/inventory/items` - 创建库存项
- `GET /api/inventory/suppliers` - 获取供应商
- `GET /api/inventory/purchase-orders` - 获取采购订单

### 员工管理
- `GET /api/staff/staff` - 获取员工列表
- `POST /api/staff/staff` - 创建员工
- `GET /api/staff/attendance` - 获取考勤记录
- `GET /api/staff/schedules` - 获取排班表

### 仪表板
- `GET /api/dashboard/overview` - 获取仪表板概览
- `GET /api/dashboard/financial-trends` - 获取财务趋势
- `GET /api/dashboard/donation-trends` - 获取捐赠趋势
- `GET /api/dashboard/top-donors` - 获取顶级捐赠者

## 数据库模型

系统包含以下主要数据表：

- **财务管理**: FinancialRecord, Expense, PayrollRecord
- **捐赠管理**: Donation, Donor, Gift
- **库存管理**: Inventory, DemandPlan, Supplier, PurchaseOrder
- **员工管理**: Staff, Attendance, Schedule, PerformanceReview
- **用户管理**: User, Role, Permission

所有表之间的关系已在ERD图中定义，并通过外键关联。

## 使用说明

1. **仪表板**: 查看系统概览和关键统计数据
2. **财务管理**: 管理所有财务记录和支出
3. **捐赠管理**: 管理捐赠记录和捐赠者信息，查看人口统计
4. **库存管理**: 管理库存物品、供应商和采购订单
5. **员工管理**: 管理员工信息、考勤和排班

## 配置文件说明

### 环境变量 (.env)

主要配置项：
- `HOST`: 服务器绑定地址（默认: `0.0.0.0`，允许公网访问）
- `PORT`: 服务器端口（默认: `6657`）
- `SECRET_KEY`: Flask密钥（生产环境必须更改）
- `DATABASE_URL`: 数据库连接字符串（默认: SQLite）
- `FLASK_DEBUG`: 调试模式（生产环境设为 `0`）

### 生产环境配置

- `gunicorn_config.py`: Gunicorn 生产服务器配置
- `nginx.conf.example`: Nginx 反向代理配置示例
- `ecf-mis.service`: Systemd 服务文件（可选）

## 注意事项

- 首次运行时会自动创建SQLite数据库
- 可以通过环境变量 `DATABASE_URL` 配置其他数据库
- **生产环境必须修改 `SECRET_KEY` 配置**
- 生产环境建议使用 Gunicorn 而不是 Flask 开发服务器
- 建议配置 Nginx 反向代理和 SSL 证书

## 开发

系统采用模块化设计，易于扩展和维护。可以轻松添加新的功能模块或修改现有功能。

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

