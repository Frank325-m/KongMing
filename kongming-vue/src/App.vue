<template>
  <div class="app-container">
    <!-- 顶部标题栏 -->
    <div class="header">
      <span class="title-text">🪶 孔明军师｜专属谋断</span>
    </div>

    <!-- 聊天主体区域 -->
    <div class="chat-box" ref="chatBox">
      <div v-for="(msg, idx) in messages" :key="idx" class="msg" :class="msg.role">
        <div class="bubble">{{ msg.content }}</div>
      </div>

      <!-- 自定义羽扇加载动画 -->
      <div v-if="loading" class="msg ai">
        <div class="bubble loading-wrap">
          <span class="fan-icon">🪶</span>
          <span class="loading-text">孔明推演局势中...</span>
        </div>
      </div>
    </div>

    <!-- 底部输入栏 -->
    <div class="input-bar">
      <input
        v-model="inputText"
        @keyup.enter="sendMessage"
        placeholder="请主公吩咐，亮即刻推演..."
        :disabled="loading"
      />
      <button @click="sendMessage" :class="{disabled: loading}">献策问策</button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import axios from 'axios'

const inputText = ref('')
const messages = ref([
  { role: 'ai', content: '主公，亮已就位，天下局势、商业布局、兴业之策，皆可垂询。' }
])
const loading = ref(false)
const chatBox = ref(null)

// 流式拼接文本
const streamAnswer = ref('')

// 发送消息主逻辑
const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || loading.value) return

  // 重置状态
  inputText.value = ''
  streamAnswer.value = ''
  messages.value.push({ role: 'user', content: text })
  loading.value = true

  await nextTick()
  scrollToBottom()

  // 初始化空AI消息，用于流式填充
  messages.value.push({ role: 'ai', content: '' })
  const lastIndex = messages.value.length - 1

  // 使用Fetch API + ReadableStream替代EventSource
  const url = `http://localhost:8000/chat-stream?question=${encodeURIComponent(text)}`
  console.log('开始流式请求，URL:', url)
  
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'text/event-stream',
        'Cache-Control': 'no-cache'
      }
    })
    
    console.log('响应状态:', response.status, response.statusText)
    console.log('响应头:', Object.fromEntries(response.headers.entries()))
    
    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status} ${response.statusText}`)
    }
    
    if (!response.body) {
      throw new Error('响应没有可读流')
    }
    
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    
    // 读取流数据
    const readStream = async () => {
      try {
        while (true) {
          const { done, value } = await reader.read()
          
          if (done) {
            console.log('流读取完成')
            loading.value = false
            break
          }
          
          // 解码数据
          const chunk = decoder.decode(value, { stream: true })
          console.log('收到数据块:', chunk)
          
          // 添加到答案
          streamAnswer.value += chunk
          messages.value[lastIndex].content = streamAnswer.value
          scrollToBottom()
        }
      } catch (error) {
        console.error('读取流时出错:', error)
        
        // 检查是否已经收到了一些数据
        if (streamAnswer.value && streamAnswer.value.length > 0) {
          console.log('已收到数据长度:', streamAnswer.value.length)
          messages.value[lastIndex].content = streamAnswer.value
        } else {
          console.log('未收到任何数据')
          messages.value[lastIndex].content = '主公，推演链路受阻，请稍后再询。'
        }
        loading.value = false
      }
    }
    
    // 开始读取流
    readStream()
    
  } catch (error) {
    console.error('请求失败:', error)
    messages.value[lastIndex].content = '主公，推演链路受阻，请稍后再询。'
    loading.value = false
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (chatBox.value) {
    chatBox.value.scrollTop = chatBox.value.scrollHeight
  }
}
</script>

<style scoped>
/* 全局基础样式 */
.app-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: #070c16;
  color: #e6c88c;
  font-family: "PingFang SC", "Microsoft Yahei", sans-serif;
}

/* 顶部头部 */
.header {
  padding: 20px 16px;
  text-align: center;
  border-bottom: 1px solid #232d3f;
  background: #0a101c;
}

.title-text {
  font-size: 22px;
  font-weight: 500;
  letter-spacing: 2px;
  color: #d4b878;
}

/* 聊天容器 */
.chat-box {
  flex: 1;
  padding: 24px 16px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-sizing: border-box;
}

/* 消息基础样式 */
.msg {
  display: flex;
  width: 100%;
}

.msg.user {
  justify-content: flex-end;
}

.msg.ai {
  justify-content: flex-start;
}

.bubble {
  max-width: 85%;
  padding: 14px 18px;
  border-radius: 16px;
  line-height: 1.8;
  font-size: 15px;
  box-sizing: border-box;
  text-align: left;
}

/* 用户消息气泡 */
.user .bubble {
  background: #2a3b55;
  color: #f0e6d2;
  border-bottom-right-radius: 4px;
  text-align: right;
}

/* AI消息气泡 */
.ai .bubble {
  background: #121b2b;
  color: #e6c88c;
  border: 1px solid #283447;
  border-bottom-left-radius: 4px;
  text-align: left;
}

/* 加载动画样式 */
.loading-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  text-align: left;
}

.fan-icon {
  font-size: 18px;
  animation: fanPulse 1.5s infinite ease-in-out;
}

.loading-text {
  color: #b89f6e;
}

/* 羽扇脉冲动画 */
@keyframes fanPulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.1);
  }
}

/* 底部输入栏 */
.input-bar {
  display: flex;
  padding: 16px;
  gap: 12px;
  border-top: 1px solid #232d3f;
  background: #0a101c;
}

.input-bar input {
  flex: 1;
  padding: 14px 20px;
  border-radius: 12px;
  border: 1px solid #283447;
  background: #121b2b;
  color: #e6c88c;
  font-size: 15px;
  outline: none;
  transition: all 0.3s ease;
}

.input-bar input:focus {
  border-color: #d4b878;
  box-shadow: 0 0 8px rgba(212, 184, 120, 0.2);
}

.input-bar button {
  padding: 14px 24px;
  border-radius: 12px;
  background: linear-gradient(135deg, #c89a56, #b88948);
  color: #070c16;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
}

.input-bar button:hover:not(.disabled) {
  opacity: 0.9;
  transform: translateY(-2px);
}

.input-bar button.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* 移动端自适应 */
@media (max-width: 640px) {
  .title-text {
    font-size: 18px;
  }
  .bubble {
    max-width: 90%;
    font-size: 14px;
    padding: 12px 16px;
  }
  .input-bar {
    padding: 12px;
  }
  .input-bar button {
    padding: 12px 18px;
    font-size: 14px;
  }
}
</style>