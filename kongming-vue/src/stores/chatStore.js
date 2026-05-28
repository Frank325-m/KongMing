
import { ref, watch, computed } from 'vue'

const STORAGE_KEY = 'kongming-data'

const inputText = ref('')
const messages = ref([
  { role: 'ai', content: '主公，亮已就位，天下局势、商业布局、兴业之策，皆可垂询。' }
])
const loading = ref(false)
const sessionId = ref(null)
const sessions = ref([])
const sidebarCollapsed = ref(false)

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

watch(messages, saveAllData, { deep: true })
watch(sessions, saveAllData, { deep: true })
watch(sessionId, saveAllData)

const setInputText = (text) => {
  inputText.value = text
}

const addMessage = (role, content) => {
  messages.value.push({ role: role, content: content })
}

const updateLastMessage = (content) => {
  const lastIndex = messages.value.length - 1
  if (lastIndex >= 0) {
    messages.value[lastIndex].content = content
  }
}

const setLoading = (status) => {
  loading.value = status
}

const setSessionId = (id) => {
  sessionId.value = id
}

const setSessions = (list) => {
  sessions.value = list
}

const setMessages = (msgs) => {
  messages.value = msgs
}

const toggleSidebar = () => {
  sidebarCollapsed.value = !sidebarCollapsed.value
}

export default {
  inputText,
  messages,
  loading,
  sessionId,
  sessions,
  sidebarCollapsed,
  currentSessionTitle,

  setInputText,
  addMessage,
  updateLastMessage,
  setLoading,
  setSessionId,
  setSessions,
  setMessages,
  toggleSidebar,
  saveAllData,
  restoreAllData
}
