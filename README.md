# 🪶 孔明军师

专属谋断AI军师，基于三国诸葛亮人设，专注商业、战略、管理类问题。

## 📦 项目结构

```
KongMing/
├── kongming-backend/    # 后端服务 (FastAPI + OpenAI)
│   ├── main.py         # 核心业务逻辑
│   ├── Dockerfile      # Docker构建配置
│   ├── docker-compose.yml  # 后端独立部署
│   ├── requirements.txt    # Python依赖
│   ├── .env            # 环境变量（本地开发）
│   └── .env.docker     # Docker环境变量
│
├── kongming-vue/       # 前端服务 (Vue3 + Vite)
│   ├── src/
│   │   ├── App.vue     # 主应用组件
│   │   ├── main.js     # 入口文件
│   │   └── assets/     # 静态资源
│   ├── Dockerfile      # Docker构建配置
│   ├── docker-compose.yml  # 前端独立部署
│   ├── nginx.conf      # Nginx配置
│   └── package.json    # Node依赖
│
├── docker-compose.yml  # 前后端统一部署
└── DEPLOYMENT_GUIDE.md # 完整部署文档
```

## 🚀 快速开始

### 方式1：Docker一键部署（推荐）

```bash
# 1. 进入项目根目录
cd d:\workspace\KongMing

# 2. 启动前后端服务
docker-compose up -d --build

# 3. 访问应用
# 前端: http://localhost:3000
# 后端: http://localhost:8000
```

### 方式2：本地开发

#### 后端启动
```bash
cd kongming-backend
pip install -r requirements.txt
uvicorn main:app --reload --host localhost --port 8000
```

#### 前端启动
```bash
cd kongming-vue
npm install
npm run dev
```

## ⚙️ 配置说明

### 环境变量配置

编辑根目录的 `docker-compose.yml` 或后端的 `.env.docker`：

```yaml
environment:
  - LLM_MODEL_NAME=qwen2.5:7b      # 模型名称
  - LLM_API_KEY=ollama            # API密钥
  - LLM_BASE_URL=http://host.docker.internal:11434/v1  # API地址
  - TEMPERATURE=0.45              # 温度参数（创造性）
  - TOP_P=0.7                     # Top-p参数（多样性）
```

### 使用本地Ollama

1. 确保Ollama正在运行
2. 配置环境变量指向本地服务
3. 拉取所需模型：`ollama pull qwen2.5:7b`

### 使用云端API

修改环境变量为DeepSeek等云端服务配置。

## 📝 常用命令

### Docker命令
```bash
# 启动服务
docker-compose up -d --build

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 重启服务
docker-compose restart
```

### 本地开发
```bash
# 后端开发
cd kongming-backend
uvicorn main:app --reload

# 前端开发
cd kongming-vue
npm run dev
```

## 🎯 核心特性

- **孔明人设**：专业的古代军师风格
- **流式输出**：实时响应，体验流畅
- **前后分离**：Vue3前端 + FastAPI后端
- **Docker部署**：一键启动，开箱即用
- **灵活配置**：支持本地Ollama或云端API
- **战略分析**：上中下策分层作答

## 📖 文档

- **DEPLOYMENT_GUIDE.md** - 完整部署指南
- **kongming-backend/README.md** - 后端文档
- **kongming-vue/README.md** - 前端文档

## 🔧 技术栈

### 后端
- FastAPI - Web框架
- OpenAI SDK - LLM客户端
- Python-dotenv - 环境变量管理

### 前端
- Vue3 - 前端框架
- Vite - 构建工具
- Axios - HTTP客户端
- Nginx - Web服务器

### 部署
- Docker - 容器化
- Docker Compose - 编排工具

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License
