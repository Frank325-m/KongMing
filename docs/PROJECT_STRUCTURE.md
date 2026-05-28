
# 孔明军师 - 项目结构说明

## 📁 完整项目结构

```
KongMing/
├── kongming-backend/          # 后端 FastAPI 应用
│   ├── core/                  # 核心模块目录 ✨
│   │   ├── __init__.py
│   │   ├── config.py          # 配置模块
│   │   ├── models.py          # 数据模型
│   │   ├── session_manager.py # 会话管理器
│   │   └── llm_service.py     # LLM 服务
│   ├── main.py                # 入口文件（精简版）✨
│   ├── .env.docker            # Docker 环境配置
│   ├── Dockerfile             # 后端 Docker 镜像
│   ├── docker-compose.yml     # 后端编排
│   ├── requirements.txt       # Python 依赖
│   └── .dockerignore
│
├── kongming-vue/              # 前端 Vue3 应用
│   ├── src/
│   │   ├── components/        # Vue 组件目录 ✨
│   │   │   ├── Sidebar.vue    # 侧边栏（会话列表）
│   │   │   ├── ChatArea.vue   # 聊天区域
│   │   │   └── DeleteDialog.vue # 删除确认对话框
│   │   ├── stores/            # 状态管理 ✨
│   │   │   └── chatStore.js   # 聊天状态 Store
│   │   ├── services/          # API 服务 ✨
│   │   │   └── api.js         # 所有 API 调用
│   │   ├── App.vue            # 根组件（精简版）✨
│   │   └── main.js            # 入口文件
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── nginx.conf
│   └── package.json
│
├── docker-compose.yml         # 全项目统一部署
├── DEPLOYMENT_GUIDE.md
├── PROJECT_STRUCTURE.md       # 本文档
└── README.md
```

---

## 🏗️ 后端模块详解

### core/config.py
**职责**: 配置管理和常量定义
- `KONGMING_FULL_PERSONA`: 孔明的人格设定
- `client`: OpenAI 兼容客户端实例
- `MODEL_NAME`, `TEMP`, `TOP_P`: 模型参数
- `MAX_HISTORY_LENGTH`: 对话历史长度限制

### core/models.py
**职责**: Pydantic 数据模型定义
- `SessionInfo`: 会话信息模型
- `ChatRequest`: 聊天请求模型
- `RestoreSessionRequest`: 恢复会话请求
- `UpdateSessionTitleRequest`: 更新标题请求

### core/session_manager.py
**职责**: 会话生命周期管理
- `SessionManager` 类: 封装所有会话操作
  - `create_session()`: 创建新会话
  - `get_all_sessions()`: 获取会话列表
  - `get_session()`: 获取单个会话
  - `delete_session()`: 删除会话
  - `restore_session()`: 恢复会话
  - `add_user_message()` / `add_assistant_message()`: 添加消息
  - `get_session_history()`: 获取会话历史
- `session_manager`: 全局单例实例

### core/llm_service.py
**职责**: LLM 交互封装
- `LLMService` 类: 统一的 LLM 调用接口
  - `generate_stream_response()`: 流式响应生成
- `llm_service`: 全局单例实例

### main.py
**职责**: FastAPI 应用入口和路由定义
- CORS 中间件配置
- REST API 路由：
  - `GET /`: 健康检查
  - `POST /new-session`: 创建会话
  - `GET /sessions`: 会话列表
  - `GET /session/{id}`: 获取会话
  - `POST /update-session-title`: 更新标题
  - `DELETE /session/{id}`: 删除会话
  - `POST /restore-session`: 恢复会话
  - `POST /clear-session`: 清空会话
  - `GET/POST /chat-stream`: 流式聊天（核心）

---

## 🎨 前端模块详解

### services/api.js
**职责**: 所有后端 API 调用封装
- `createNewSession()`: 创建会话
- `fetchSessions()`: 获取列表
- `fetchSession()`: 获取单个会话
- `deleteSession()`: 删除会话
- `restoreSession()`: 恢复会话
- `updateSessionTitle()`: 更新标题
- `sendChatRequest()`: 发送流式聊天请求

### stores/chatStore.js
**职责**: 全局状态管理（类似 Pinia/Vuex）
- **State**:
  - `inputText`: 输入框内容
  - `messages`: 消息列表
  - `loading`: 加载状态
  - `sessionId`: 当前会话ID
  - `sessions`: 会话列表
  - `sidebarCollapsed`: 侧边栏状态
  - `showDeleteDialog`: 删除对话框状态
- **Actions**:
  - `saveAllData()`: 持久化到 localStorage
  - `restoreAllData()`: 从 localStorage 恢复
  - 各种 set/update 方法

### components/Sidebar.vue
**职责**: 侧边栏会话列表
- 会话列表展示
- 新会话按钮
- 删除会话按钮
- 侧边栏折叠
- 响应式布局（移动端悬浮）

### components/ChatArea.vue
**职责**: 主聊天区域
- 消息气泡展示
- 输入框和发送按钮
- 加载动画
- 自动滚动到底部
- 响应式布局

### components/DeleteDialog.vue
**职责**: 删除确认对话框
- 模态对话框组件
- 确认/取消按钮

### App.vue
**职责**: 根组件
- 组件组合
- 业务逻辑协调
- 生命周期管理

---

## 🎯 模块化设计原则

### 1. 单一职责原则 (SRP)
每个模块只做一件事：
- `config.py`: 只管理配置
- `session_manager.py`: 只管理会话
- `api.js`: 只做 API 调用
- `chatStore.js`: 只管理状态

### 2. 高内聚低耦合
- 模块内部紧密相关
- 模块之间通过清晰的接口通信
- 减少相互依赖

### 3. 可维护性
- 代码结构清晰，易于理解
- 修改一个功能只需要动少量文件
- 添加新功能更容易

### 4. 可测试性
- 每个模块可以独立测试
- 依赖可以轻松 Mock

---

## 🚀 快速启动

### 本地开发模式（推荐）

```bash
# 终端 1 - 后端
cd kongming-backend
pip install -r requirements.txt
uvicorn main:app --reload --host localhost --port 8000

# 终端 2 - 前端
cd kongming-vue
npm install
npm run dev
```

### Docker 部署模式

```bash
# 全项目统一部署
docker-compose up -d --build

# 分别部署
cd kongming-backend && docker-compose up -d
cd kongming-vue && docker-compose up -d
```

---

## 📚 开发指南

### 添加新的后端 API

1. 在 `core/session_manager.py` 中添加业务逻辑
2. 在 `main.py` 中添加路由
3. 在 `kongming-vue/src/services/api.js` 中添加调用
4. 在组件中使用新 API

### 添加新的前端组件

1. 在 `kongming-vue/src/components/` 创建新组件
2. 在 `App.vue` 或父组件中引入
3. 通过 Props/Emit 进行通信

### 修改孔明人格

只需修改 `core/config.py` 中的 `KONGMING_FULL_PERSONA` 常量即可！

---

## ✨ 重构前后对比

### 重构前
- ❌ 所有代码在一个文件里
- ❌ 难以维护和扩展
- ❌ 组件耦合度高
- ❌ 测试困难

### 重构后
- ✅ 清晰的模块划分
- ✅ 易于维护和扩展
- ✅ 组件低耦合
- ✅ 每个模块可独立测试
- ✅ 代码可复用性提高
- ✅ 更容易定位和修复问题

---

## 🔮 未来扩展建议

### 后端扩展
- 🔄 添加 Redis 持久化存储会话
- 🔄 添加用户认证 (JWT/OAuth)
- 🔄 添加数据库持久化 (SQLite/PostgreSQL)
- 🔄 添加限流和错误处理中间件
- 🔄 添加日志系统

### 前端扩展
- 🔄 使用 Pinia 替代自定义 Store
- 🔄 添加路由 Vue Router
- 🔄 添加单元测试 (Vitest)
- 🔄 添加国际化 i18n
- 🔄 添加更多主题

---

## 📝 总结

本次重构成功实现了：

1. ✅ **后端模块化**: 拆分为 4 个核心模块
2. ✅ **前端组件化**: 拆分为 3 个主要组件 + 服务层 + 状态层
3. ✅ **职责清晰**: 每个模块有明确的单一职责
4. ✅ **易维护**: 代码结构清晰，易于修改和扩展
5. ✅ **向后兼容**: 所有功能保持不变，API 完全兼容

项目现在具备了专业应用的架构基础！
