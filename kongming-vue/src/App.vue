
<template>
  <div class="app-container">
    <Sidebar
      :sessions="sessions"
      :current-session-id="sessionId"
      :sidebar-collapsed="sidebarCollapsed"
      @create-session="createNewSession"
      @switch-session="switchSession"
      @delete-session="confirmDeleteSession"
      @toggle-sidebar="toggleSidebar"
    />

    <ChatArea
      :messages="messages"
      :loading="loading"
      :sidebar-collapsed="sidebarCollapsed"
      :current-session-title="currentSessionTitle"
      @send-message="sendMessage"
      @toggle-sidebar="toggleSidebar"
    />

    <DeleteDialog
      :show="showDeleteDialog"
      :title="deleteDialogTitle"
      @cancel="cancelDelete"
      @confirm="executeDelete"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ChatArea from './components/ChatArea.vue'
import DeleteDialog from './components/DeleteDialog.vue'
import {
  createNewSession as apiCreateSession,
  fetchSessions as apiFetchSessions,
  fetchSession as apiFetchSession,
  deleteSession as apiDeleteSession,
  restoreSession as apiRestoreSession,
  sendChatRequest
} from './services/api'

// 直接在 App 中管理所有状态，更简单稳定
const messages = ref([
  { role: 'ai', content: '主公，亮已就位，天下局势、商业布局、兴业之策，皆可垂询。' }
])
const loading = ref(false)
const sessionId = ref(null)
const sessions = ref([])
const sidebarCollapsed = ref(false)

// 删除对话框状态
const showDeleteDialog = ref(false)
const deleteSessionId = ref('')
const deleteDialogTitle = ref('')

const STORAGE_KEY = 'kongming-data'

const currentSessionTitle = computed(() => {
  const session = sessions.value.find(s => s.id === sessionId.value)
  return session ? session.title : ''
})

const saveAllData = () => {
  try {
    const data = {
      currentSessionId: sessionId.value,
      sessions: sessions.value,
      messages: {}
    }
    if (sessionId.value) {
      data.messages[sessionId.value] = messages.value
    }
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch (e) {
    console.error('保存数据失败:', e)
  }
}

const restoreAllData = () => {
  try {
    const savedData = localStorage.getItem(STORAGE_KEY)
    if (savedData) {
      const data = JSON.parse(savedData)

      if (data.sessions) {
        sessions.value = data.sessions
      }

      if (data.currentSessionId) {
        sessionId.value = data.currentSessionId
      }

      if (data.messages && data.messages[sessionId.value]) {
        messages.value = data.messages[sessionId.value]
      }
    }
  } catch (e) {
    console.error('恢复数据失败:', e)
  }
}

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

const createNewSession = async () => {
  if (loading.value) return

  try {
    const result = await apiCreateSession()
    sessionId.value = result.session_id
    messages.value = [
      { role: 'ai', content: '主公，新的推演已开始，请吩咐。' }
    ]
    await refreshSessionList()
    saveAllData()
  } catch (error) {
    sessionId.value = null
    messages.value = [
      { role: 'ai', content: '主公，新的推演已开始，请吩咐。' }
    ]
  }
}

const refreshSessionList = async () => {
  try {
    const result = await apiFetchSessions()
    sessions.value = result.sessions || []
    saveAllData()
  } catch (error) {
    console.error('刷新会话列表失败:', error)
  }
}

const switchSession = async (id) => {
  if (loading.value || id === sessionId.value) return

  try {
    const result = await apiFetchSession(id)
    if (result.error) {
      throw new Error(result.error)
    }
    sessionId.value = id
    messages.value = result.messages
    saveAllData()
  } catch (error) {
    try {
      const savedData = localStorage.getItem(STORAGE_KEY)
      if (savedData) {
        const data = JSON.parse(savedData)
        if (data.messages && data.messages[id]) {
          sessionId.value = id
          messages.value = data.messages[id]
        }
      }
    } catch (e) {
      console.error('本地恢复会话失败:', e)
    }
  }
}

const confirmDeleteSession = (id, title) => {
  deleteSessionId.value = id
  deleteDialogTitle.value = title
  showDeleteDialog.value = true
}

const cancelDelete = () => {
  showDeleteDialog.value = false
  deleteSessionId.value = ''
  deleteDialogTitle.value = ''
}

const executeDelete = async () => {
  try {
    await apiDeleteSession(deleteSessionId.value)

    if (deleteSessionId.value === sessionId.value) {
      if (sessions.value.length > 1) {
        const otherSessions = sessions.value.filter(s => s.id !== deleteSessionId.value)
        if (otherSessions.length > 0) {
          await switchSession(otherSessions[0].id)
        }
      } else {
        sessionId.value = null
        messages.value = [
          { role: 'ai', content: '主公，亮已就位，天下局势、商业布局、兴业之策，皆可垂询。' }
        ]
      }
    }

    await refreshSessionList()
    cancelDelete()
  } catch (error) {
    console.error('删除会话失败:', error)
  }
}

const sendMessage = async (text) => {
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  loading.value = true
  messages.value.push({ role: 'ai', content: '' })

  sendChatRequest(
    text,
    sessionId.value,
    (chunk) => {
      const lastIndex = messages.value.length - 1
      if (lastIndex >= 0) {
        messages.value[lastIndex].content += chunk
      }
    },
    (error) => {
      console.error('请求失败:', error)
      const lastIndex = messages.value.length - 1
      if (lastIndex >= 0) {
        if (messages.value[lastIndex].content && messages.value[lastIndex].content.length > 0) {
        } else {
          messages.value[lastIndex].content = '主公，推演链路受阻，请稍后再询。'
        }
      }
      loading.value = false
    },
    async (receivedSessionId) => {
      if (receivedSessionId) {
        sessionId.value = receivedSessionId
      }
      loading.value = false
      await refreshSessionList()
      saveAllData()
    }
  )
}

const restoreBackendSession = async () => {
  if (!sessionId.value || !Array.isArray(messages.value) || messages.value.length === 0) {
    return
  }

  try {
    const historyForBackend = messages.value.filter(msg => msg.role !== 'system')
      .map(msg => {
        return {
          role: msg.role === 'ai' ? 'assistant' : msg.role,
          content: msg.content
        }
      })

    const result = await apiRestoreSession(sessionId.value, historyForBackend)
    if (result.session_id) {
      sessionId.value = result.session_id
      console.log('后端会话恢复成功:', result.session_id)
    }
  } catch (error) {
    console.error('恢复后端会话失败:', error)
  }
}

onMounted(async () => {
  showDeleteDialog.value = false
  deleteSessionId.value = ''
  deleteDialogTitle.value = ''
  
  restoreAllData()
  await refreshSessionList()
  await restoreBackendSession()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Microsoft YaHei', sans-serif;
  background-color: #0f172a;
  color: #e2e8f0;
  height: 100vh;
  overflow: hidden;
}

.app-container {
  display: flex;
  height: 100vh;
  width: 100%;
}
</style>
