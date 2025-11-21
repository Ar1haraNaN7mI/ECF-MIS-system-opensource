# 快速启动指南

## 环境配置已完成 ✅

虚拟环境已创建，依赖已安装。现在可以启动应用了。

## 启动方式

### 方式一：使用 run.bat（Windows）

直接双击 `run.bat` 文件，或在命令行运行：
```bash
run.bat
```

### 方式二：手动启动

1. **激活虚拟环境**：
   ```bash
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows CMD
   venv\Scripts\activate.bat
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **启动应用**：
   ```bash
   python app.py
   ```

## 访问应用

应用启动后，在浏览器中打开：
```
http://localhost:5000
```

## 环境配置说明

- ✅ 虚拟环境：`venv/`
- ✅ 依赖包：已安装到虚拟环境
- ✅ 环境变量：`.env` 文件（如果不存在会自动使用默认配置）
- ✅ 数据库：首次运行会自动创建 `instance/mis_database.db`

## 常见问题

### 问题：PowerShell 执行策略限制

如果遇到 PowerShell 执行策略错误，运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 问题：端口被占用

如果 5000 端口被占用，可以：
1. 修改 `.env` 文件中的 `PORT=5000` 为其他端口
2. 或修改 `app.py` 最后一行的端口号

### 问题：模块导入错误

确保已激活虚拟环境：
```bash
# 检查虚拟环境是否激活（应该显示 (venv)）
# 如果没有，重新激活
.\venv\Scripts\Activate.ps1
```

## 下一步

1. 启动应用
2. 访问 http://localhost:5000
3. 开始使用 MIS 系统！




