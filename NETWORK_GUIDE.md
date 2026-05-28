# 🌐 Docker网络问题完整解决方案

## 📋 当前问题
Docker无法连接到Docker Hub或阿里云镜像源

---

## 🎯 推荐方案：本地开发模式（最快）

### ✅ 无需Docker，直接运行

#### 启动后端
```bash
cd d:\workspace\KongMing\kongming-backend
pip install -r requirements.txt
uvicorn main:app --reload --host localhost --port 8000
```

#### 启动前端（新终端）
```bash
cd d:\workspace\KongMing\kongming-vue
npm install
npm run dev
```

#### 访问应用
- 前端：http://localhost:5173
- 后端：http://localhost:8000

---

## 🐳 方案2：配置Docker镜像加速器

### 步骤1：配置Docker Desktop

1. 打开 **Docker Desktop**
2. 点击右上角齿轮 ⚙️ → **Settings**
3. 选择 **Docker Engine**
4. 粘贴以下配置（注意保持JSON格式正确）：

```json
{
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "registry-mirrors": [
    "https://docker.mirrors.ustc.edu.cn",
    "https://hub-mirror.c.163.com",
    "https://mirror.baidubce.com"
  ],
  "experimental": false
}
```

5. 点击 **Apply & Restart**
6. 等待Docker完全重启（状态栏显示绿色）

### 步骤2：测试Docker连接

```bash
# 测试镜像拉取
docker pull hello-world

# 如果成功，继续构建
cd d:\workspace\KongMing
docker-compose up -d --build
```

---

## 🌐 方案3：使用其他公共镜像源

### 可用的镜像源列表

| 镜像源 | 地址 | 说明 |
|--------|------|------|
| 中科大 | https://docker.mirrors.ustc.edu.cn | 推荐 |
| 网易 | https://hub-mirror.c.163.com | 稳定 |
| 百度 | https://mirror.baidubce.com | 快速 |
| 腾讯云 | https://mirror.ccs.tencentyun.com | 企业 |
| Docker Proxy | https://dockerproxy.com | 社区 |

### 测试各镜像源

```bash
# 测试拉取Python镜像
docker pull python:3.12-alpine

# 如果某个镜像源可以工作，更新Docker配置
```

---

## 🔧 方案4：网络代理配置

### 如果你的网络需要代理

在Docker Desktop中配置代理：

1. **Settings** → **Resources** → **Proxies**
2. 配置你的代理服务器地址
3. 点击 **Apply & Restart**

---

## 📊 Docker常用命令

### 基本操作

```bash
# 查看镜像
docker images

# 查看运行的容器
docker ps

# 查看所有容器（包括停止的）
docker ps -a

# 查看容器日志
docker-compose logs -f

# 停止容器
docker-compose down

# 删除未使用的镜像
docker image prune -f

# 清理所有未使用的资源
docker system prune -f
```

### 故障排查

```bash
# 查看Docker信息
docker info

# 查看Docker版本
docker --version

# 测试网络连接
ping registry-1.docker.io

# 查看镜像构建历史
docker history <image-id>
```

---

## 🚀 完整部署流程（成功后）

### 使用Docker部署

```bash
# 1. 确保Docker Desktop运行中
# 2. 配置好镜像加速器
# 3. 进入项目目录
cd d:\workspace\KongMing

# 4. 构建并启动服务
docker-compose up -d --build

# 5. 查看状态
docker-compose ps

# 6. 访问应用
# 前端：http://localhost:3000
# 后端：http://localhost:8000
```

---

## 💡 建议工作流

### 开发阶段
- 使用**本地开发模式**
- 快速迭代，热更新
- 调试方便

### 部署阶段
- 使用**Docker容器化**
- 环境隔离
- 易于部署

---

## ⚠️ 常见问题

### Q: Docker Desktop无法启动？
A: 检查Hyper-V或WSL2是否启用，重启电脑

### Q: 端口被占用？
A: 修改`docker-compose.yml`中的端口映射，或停止占用端口的程序

### Q: 容器启动后无法访问？
A: 检查容器日志：`docker-compose logs -f`

### Q: 如何彻底清理Docker？
A: `docker system prune -a` （慎用，会删除所有）

---

## 📞 获取帮助

如果以上方案都不行，可以：
1. 检查网络连接
2. 尝试VPN
3. 使用云服务器构建
4. 直接本地开发（推荐）
