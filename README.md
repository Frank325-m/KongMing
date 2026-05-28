# 🪶 孔明军师

专属谋断AI军师，基于三国诸葛亮人设，专注商业、战略、管理类问题。

## ✨ 核心特性

- **孔明人设**：专业的古代军师风格，使用"主公"等称呼
- **多会话管理**：支持创建、切换、删除多个独立会话
- **上下文记忆**：AI能记住之前的对话，保持连贯性
- **流式输出**：实时响应，体验流畅
- **自动生成标题**：自动用第一个问题作为会话标题
- **本地持久化**：使用 localStorage 存储会话历史
- **前后分离**：Vue3 前端 + FastAPI 后端
- **Docker部署**：一键启动，开箱即用
- **灵活配置**：支持本地 Ollama 或云端 API
- **战略分析**：上中下策分层作答
- **优雅UI**：响应式设计，支持移动端
- **自动隐藏滚动条**：清爽的视觉体验

## 📦 项目结构

```
KongMing/
├── kongming-backend/    # 后端服务 (FastAPI + OpenAI)
│   ├── core/           # 核心模块
│   │   ├── config.py       # 配置管理
│   │   ├── models.py       # 数据模型
│   │   ├── session_manager.py  # 会话管理器
│   │   └── llm_service.py  # LLM服务
│   ├── main.py         # 入口文件
│   ├── Dockerfile      # Docker构建配置
│   ├── docker-compose.yml  # 后端独立部署
│   ├── requirements.txt    # Python依赖
│   ├── .env            # 环境变量（本地开发）
│   └── .env.docker     # Docker环境变量
│
├── kongming-vue/       # 前端服务 (Vue3 + Vite)
│   ├── src/
│   │   ├── components/     # Vue组件
│   │   │   ├── Sidebar.vue     # 侧边栏
│   │   │   ├── ChatArea.vue    # 聊天区域
│   │   │   └── DeleteDialog.vue # 删除对话框
│   │   ├── stores/       # 状态管理
│   │   │   └── chatStore.js
│   │   ├── services/     # API服务
│   │   │   └── api.js
│   │   ├── App.vue     # 主应用组件
│   │   └── main.js     # 入口文件
│   ├── Dockerfile      # Docker构建配置
│   ├── docker-compose.yml  # 前端独立部署
│   ├── nginx.conf      # Nginx配置
│   └── package.json    # Node依赖
│
├── docker-compose.yml  # 前后端统一部署
├── docs/              # 文档目录
│   └── PROJECT_STRUCTURE.md  # 项目结构详细说明
└── README.md          # 本文件
```

## 🚀 快速开始

### 方式1：本地开发（推荐，最快）

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

### 方式2：Docker一键部署

```bash
# 1. 进入项目根目录
cd d:\workspace\KongMing

# 2. 启动前后端服务
docker-compose up -d --build

# 3. 访问应用
# 前端: http://localhost:3000
# 后端: http://localhost:8000
```

## ⚙️ 配置说明

### 环境变量配置

编辑后端的 `.env`（本地开发）或 `.env.docker`（Docker部署）：

```env
# LLM Configuration
LLM_MODEL_NAME=qwen2.5:7b      # 模型名称
LLM_API_KEY=ollama            # API密钥
LLM_BASE_URL=http://localhost:11434/v1  # API地址

# Model Parameters
TEMPERATURE=0.45              # 温度参数（创造性）
TOP_P=0.7                     # Top-p参数（多样性）
```

### 使用本地 Ollama

1. 确保 Ollama 正在运行
2. 配置环境变量指向本地服务
3. 拉取所需模型：`ollama pull qwen2.5:7b`

### 使用云端 API

修改环境变量为 DeepSeek 等云端服务配置。

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
uvicorn main:app --reload --host localhost --port 8000

# 前端开发
cd kongming-vue
npm run dev
```

## 🎯 使用指南

### 基本使用
1. 打开应用，孔明会主动问候
2. 在输入框输入问题，点击"献策问策"或按回车
3. 孔明会以军师的身份，给出专业的回答

### 多会话管理
1. **创建新会话**：点击左侧边栏的"+ 新对话"按钮
2. **切换会话**：在左侧边栏点击想要的会话
3. **删除会话**：悬停在会话上，点击 🗑️ 删除按钮

### 会话记忆
- 孔明会记住当前会话的所有对话
- 切换会话后，会自动恢复该会话的上下文
- 刷新页面后，会话记忆依然完整保留

### 界面操作
- **折叠侧边栏**：点击侧边栏底部的按钮
- **移动端菜单**：点击顶部的☰按钮展开侧边栏

## 📖 文档

- **docs/PROJECT_STRUCTURE.md** - 项目结构详细说明

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

## 🗄️ 数据存储

### 前端存储
- **位置**：浏览器 `localStorage`
- **键名**：`kongming-data`
- **内容**：会话列表、当前会话ID、各会话的消息历史

### 后端存储
- **位置**：服务器内存
- **说明**：会话数据临时存储，重启会清空
- **同步机制**：页面加载时，前端会自动将 localStorage 数据恢复到后端

## 🧹 清除会话

### 方法1：界面删除（推荐）
- 悬停会话 → 点击 🗑️ → 确认删除

### 方法2：清除浏览器存储
1. 按 F12 打开开发者工具
2. 进入 Application → Local Storage
3. 删除 `kongming-data` 项
4. 刷新页面

### 方法3：完全清除
- 清除浏览器 localStorage
- 重启后端服务

## 🎯 核心API

### 会话管理
- `GET /sessions` - 获取所有会话列表
- `GET /session/{session_id}` - 获取单个会话详情
- `POST /new-session` - 创建新会话
- `POST /restore-session` - 恢复会话（用于重启后同步）
- `POST /update-session-title` - 更新会话标题
- `DELETE /session/{session_id}` - 删除会话

### 对话
- `GET /chat-stream` - 流式对话接口
- `POST /chat-stream` - 流式对话接口（POST方式）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
