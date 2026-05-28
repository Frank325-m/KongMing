# 孔明项目Docker部署完整指南

## 项目结构
```
KongMing/
├── kongming-backend/    # 后端服务
├── kongming-vue/        # 前端服务
└── docker-compose.yml   # 根目录统一部署配置
```

## 快速开始

### 前置条件
1. Docker Desktop已安装并运行
2. 已配置Docker镜像加速器（见NETWORK_GUIDE.md）
3. 端口3000和8000未被占用

### 一键启动（推荐）

在项目根目录运行：

```bash
cd d:\workspace\KongMing
docker-compose up -d --build
```

### 单独启动

#### 仅启动前端
```bash
cd d:\workspace\KongMing\kongming-vue
docker-compose up -d --build
```

#### 仅启动后端
```bash
cd d:\workspace\KongMing\kongming-backend
docker-compose up -d --build
```

## 访问地址

- **前端界面**: http://localhost:3000
- **后端API**: http://localhost:8000
- **API根路径**: http://localhost:8000/
- **流式对话**: http://localhost:8000/chat-stream

## 常用命令

### 查看状态
```bash
docker-compose ps
```

### 查看日志
```bash
# 查看所有服务日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f kongming-vue
docker-compose logs -f kongming-backend
```

### 停止服务
```bash
# 停止并删除容器
docker-compose down

# 停止并删除容器、镜像、卷
docker-compose down --rmi all --volumes
```

### 重启服务
```bash
docker-compose restart
```

### 进入容器
```bash
# 进入前端容器
docker exec -it kongming-vue sh

# 进入后端容器
docker exec -it kongming-backend sh
```

## 配置说明

### 环境变量配置

编辑根目录的docker-compose.yml中的environment：

```yaml
environment:
  - LLM_MODEL_NAME=qwen2.5:7b      # 模型名称
  - LLM_API_KEY=ollama            # API密钥
  - LLM_BASE_URL=http://host.docker.internal:11434/v1  # API地址
  - TEMPERATURE=0.45              # 温度参数
  - TOP_P=0.7                     # Top-p参数
```

### 使用本地Ollama
确保Ollama正在运行，配置如下：
```yaml
LLM_BASE_URL=http://host.docker.internal:11434/v1
```

### 使用云端API（如DeepSeek）
修改环境变量：
```yaml
LLM_MODEL_NAME=deepseek-v4-flash
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

## 开发模式

### 前端开发
```bash
cd d:\workspace\KongMing\kongming-vue
npm install
npm run dev
```

### 后端开发
```bash
cd d:\workspace\KongMing\kongming-backend
pip install -r requirements.txt
uvicorn main:app --reload --host localhost --port 8000
```

## 网络问题

参考NETWORK_GUIDE.md配置Docker镜像加速器。

## 故障排除

### 端口冲突
```bash
# 查看端口占用
netstat -ano | findstr :3000
netstat -ano | findstr :8000
```

### 容器启动失败
```bash
# 查看详细日志
docker-compose logs kongming-vue
docker-compose logs kongming-backend
```

### 清除所有数据
```bash
docker-compose down --rmi all --volumes
```

## 验证部署

1. **检查容器状态**
   ```bash
   docker-compose ps
   ```

2. **测试后端API**
   ```bash
   curl http://localhost:8000/
   ```

3. **访问前端界面**
   打开浏览器访问 http://localhost:3000

## 下一步

- 配置Ollama模型
- 测试前后端通信
- 自定义前端样式
- 优化后端参数

祝你使用愉快！