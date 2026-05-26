# KongMing 项目

这是一个全栈项目，包含前端和后端组件。

## 项目结构

```
kongming/
├── .gitignore                    # 根目录通用忽略规则
├── README.md                     # 项目说明文档
├── kongming-backend/             # Python FastAPI 后端
│   ├── .gitignore               # Python 特定忽略规则
│   ├── main.py                  # 后端主程序
│   └── venv/                    # Python 虚拟环境（已忽略）
└── kongming-vue/                # Vue.js 前端
    ├── .gitignore               # Vue/Node.js 特定忽略规则
    ├── package.json             # 前端依赖配置
    ├── src/                     # 前端源代码
    └── public/                  # 静态资源
```

## .gitignore 配置说明

### 根目录 (.gitignore)
- 通用操作系统文件（.DS_Store, Thumbs.db等）
- IDE配置文件（.vscode/, .idea/等）
- 临时文件和日志
- 环境变量文件（.env）

### 后端 (kongming-backend/.gitignore)
- Python编译文件（__pycache__/, *.pyc等）
- 虚拟环境（venv/, .venv/等）
- 构建输出（dist/, build/等）
- 测试和覆盖率报告
- 包管理文件（根据使用的工具）

### 前端 (kongming-vue/.gitignore)
- Node.js依赖（node_modules/）
- 构建输出（dist/, .next/等）
- 日志和缓存文件
- 环境变量文件
- IDE配置文件

## 开发环境设置

### 后端开发
1. 进入后端目录：
   ```bash
   cd kongming-backend
   ```

2. 创建并激活虚拟环境：
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install fastapi uvicorn openai python-dotenv
   ```

4. 运行开发服务器：
   ```bash
   uvicorn main:app --reload --host localhost --port 8000
   ```

### 前端开发
1. 进入前端目录：
   ```bash
   cd kongming-vue
   ```

2. 安装依赖：
   ```bash
   npm install
   ```

3. 运行开发服务器：
   ```bash
   npm run dev
   ```

## 注意事项

1. **环境变量**：所有 `.env` 文件已被忽略，请创建 `.env.example` 文件作为模板
2. **虚拟环境**：Python虚拟环境不应提交到版本控制
3. **依赖管理**：确保提交 `requirements.txt`（后端）和 `package.json`（前端）
4. **构建输出**：所有构建产物（如 `dist/`, `build/`）不应提交

## 版本控制最佳实践

1. 提交前运行相关测试
2. 确保没有提交敏感信息（API密钥、密码等）
3. 使用有意义的提交信息
4. 定期更新依赖包