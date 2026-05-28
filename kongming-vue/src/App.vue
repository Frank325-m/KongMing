
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
      :remaining-quota="remainingQuota"
      :user-type="userData.userType"
      :user-email="userData.email"
      :today-limit="todayLimit"
      @send-message="handleSendMessage"
      @toggle-sidebar="toggleSidebar"
      @open-wisdom-bag="openWisdomBag"
      @collect-wisdom="collectWisdom"
      @logout="handleLogout"
      @open-login-modal="showLoginModal = true"
    />

    <DeleteDialog
      :show="showDeleteDialog"
      :title="deleteDialogTitle"
      @cancel="cancelDelete"
      @confirm="executeDelete"
    />

    <WisdomBag
      v-if="showWisdomBag"
      ref="wisdomBagRef"
      @close="closeWisdomBag"
    />

    <LoginModal
      :show="showLoginModal"
      :guest-limit="guestLimit"
      :user-limit="userLimit"
      @login="handleLogin"
      @close="closeLoginModal"
    />

    <QuotaExceededModal
      :show="showQuotaExceededModal"
      @close="showQuotaExceededModal = false"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import Sidebar from './components/Sidebar.vue'
import ChatArea from './components/ChatArea.vue'
import DeleteDialog from './components/DeleteDialog.vue'
import WisdomBag from './components/WisdomBag.vue'
import LoginModal from './components/LoginModal.vue'
import QuotaExceededModal from './components/QuotaExceededModal.vue'
import {
  createNewSession as apiCreateSession,
  fetchSessions as apiFetchSessions,
  fetchSession as apiFetchSession,
  deleteSession as apiDeleteSession,
  restoreSession as apiRestoreSession,
  sendChatRequest
} from './services/api'
import {
  getUserData,
  saveUserData,
  login as apiLogin,
  logout as apiLogout,
  checkQuotaExceeded,
  useOneQuota,
  getRemainingQuota,
  getQuotaConfig,
  loadQuotaConfig
} from './utils/quota'
import { getQuotaConfig as fetchQuotaConfig } from './services/api'

const messages = ref([
  { role: 'ai', content: '主公，亮已就位，天下局势、商业布局、兴业之策，皆可垂询。' }
])
const loading = ref(false)
const sessionId = ref(null)
const sessions = ref([])
const sidebarCollapsed = ref(false)
const showDeleteDialog = ref(false)
const deleteSessionId = ref('')
const deleteDialogTitle = ref('')
const showWisdomBag = ref(false)
const showLoginModal = ref(false)
const showQuotaExceededModal = ref(false)
const wisdomBagRef = ref(null)
const userData = ref(getUserData())
const quotaConfig = ref({
  guest: { dailyLimit: 5, displayName: '访客' },
  user: { dailyLimit: 30, displayName: '登录用户' }
})
const isQuotaConfigLoaded = ref(false)

const STORAGE_KEY_PREFIX = 'kongming-data'

// 计算属性 - 直接从 quotaConfig 获取值
const guestLimit = computed(() => {
  return quotaConfig.value?.guest?.dailyLimit || 5
})

const userLimit = computed(() => {
  return quotaConfig.value?.user?.dailyLimit || 30
})

const todayLimit = computed(() => {
  return userData.value.userType === 'user' ? userLimit.value : guestLimit.value
})

// 根据用户类型获取存储键名
const getStorageKey = () => {
  if (userData.value.userType === 'user' && userData.value.email) {
    return `${STORAGE_KEY_PREFIX}-${userData.value.email}`
  }
  return `${STORAGE_KEY_PREFIX}-guest`
}

// 获取锦囊的存储键名
const getWisdomStorageKey = () => {
  if (userData.value.userType === 'user' && userData.value.email) {
    return `kongming-wisdom-bag-${userData.value.email}`
  }
  return `kongming-wisdom-bag`
}

const currentSessionTitle = computed(() => {
  const session = sessions.value.find(s => s.id === sessionId.value)
  return session ? session.title : ''
})

const remainingQuota = computed(() => {
  // 使用当前的 quotaConfig 来计算
  const userQuota = quotaConfig.value[userData.value.userType]?.dailyLimit || 5
  return Math.max(0, userQuota - userData.value.todayCount)
})

const saveAllData = () => {
  try {
    const storageKey = getStorageKey()
    const data = {
      currentSessionId: sessionId.value,
      sessions: sessions.value,
      messages: {}
    }
    if (sessionId.value) {
      data.messages[sessionId.value] = messages.value
    }
    localStorage.setItem(storageKey, JSON.stringify(data))
    console.log('💾 数据已保存到:', storageKey)
  } catch (e) {
    console.error('保存数据失败:', e)
  }
}

const restoreAllData = () => {
  try {
    const storageKey = getStorageKey()
    const savedData = localStorage.getItem(storageKey)
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
      } else {
        messages.value = [
          { role: 'ai', content: '主公，亮已就位，天下局势、商业布局、兴业之策，皆可垂询。' }
        ]
      }
      console.log('📂 数据已从', storageKey, '恢复')
    } else {
      // 没有保存的数据，重置为默认
      sessions.value = []
      sessionId.value = null
      messages.value = [
        { role: 'ai', content: '主公，亮已就位，天下局势、商业布局、兴业之策，皆可垂询。' }
      ]
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
    sessionId.value = result.sessionId
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
      const storageKey = getStorageKey()
      const savedData = localStorage.getItem(storageKey)
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

const handleSendMessage = async (text) => {
  if (!text || loading.value) return
  
  // 检查配额
  if (checkQuotaExceeded(userData.value)) {
    showQuotaExceededModal.value = true
    return
  }

  messages.value.push({ role: 'user', content: text })
  loading.value = true
  messages.value.push({ role: 'ai', content: '' })
  
  // 使用一次配额
  userData.value = useOneQuota(userData.value)

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
    if (result.sessionId) {
      sessionId.value = result.sessionId
      console.log('后端会话恢复成功:', result.sessionId)
    }
  } catch (error) {
    console.error('恢复后端会话失败:', error)
  }
}

const openWisdomBag = () => {
  console.log('📜 openWisdomBag called')
  showWisdomBag.value = true
  // 打开时刷新锦囊数据，确保使用正确的用户存储
  setTimeout(() => {
    if (wisdomBagRef.value && wisdomBagRef.value.refreshUserData) {
      wisdomBagRef.value.refreshUserData()
    }
  }, 0)
}

const closeWisdomBag = () => {
  console.log('📜 closeWisdomBag called')
  showWisdomBag.value = false
}

const collectWisdom = (title, content) => {
  console.log('📥 App.vue collectWisdom called - title:', title, 'content length:', content.length)
  
  if (wisdomBagRef.value) {
    const success = wisdomBagRef.value.addWisdom(title, content)
    if (success) {
      openWisdomBag()
    }
  } else {
    console.log('📥 wisdomBagRef not ready, opening panel first...')
    openWisdomBag()
    
    setTimeout(() => {
      if (wisdomBagRef.value) {
        console.log('📥 Now adding wisdom via delayed call')
        wisdomBagRef.value.addWisdom(title, content)
      }
    }, 100)
  }
}

const handleLogin = (loginData) => {
  if (loginData.userType === 'guest') {
    userData.value = {
      ...getUserData(),
      userType: 'guest',
      email: null
    }
  } else {
    userData.value = apiLogin(loginData.email)
  }
  
  showLoginModal.value = false
  
  // 登录后切换到对应账号的数据
  console.log('🔐 切换到用户:', userData.value.userType, userData.value.email)
  restoreAllData()
}

const closeLoginModal = () => {
  showLoginModal.value = false
}

const handleLogout = () => {
  console.log('👋 退出登录')
  userData.value = apiLogout()
  showLoginModal.value = true
  // 切换到访客数据
  restoreAllData()
}

// 从后端加载配额配置的函数
const loadQuotaConfigFromBackend = async () => {
  try {
    console.log('📡 从后端加载配额配置...')
    const apiConfig = await fetchQuotaConfig()
    console.log('📡 后端返回的配额配置:', apiConfig)
    
    // 更新 quotaConfig 对象，触发响应式
    if (apiConfig) {
      quotaConfig.value = {
        guest: { dailyLimit: apiConfig.guest_daily_limit || 5, displayName: '访客' },
        user: { dailyLimit: apiConfig.user_daily_limit || 30, displayName: '登录用户' }
      }
      console.log('✅ quotaConfig 已更新:', quotaConfig.value)
    }
    
    isQuotaConfigLoaded.value = true
  } catch (error) {
    console.error('加载配额配置失败，使用默认值:', error)
  }
}

onMounted(async () => {
  showDeleteDialog.value = false
  deleteSessionId.value = ''
  deleteDialogTitle.value = ''

  // 先从后端加载配额配置
  await loadQuotaConfigFromBackend()

  // 检查是否需要登录（只在第一次使用时显示）
  const savedData = localStorage.getItem(getStorageKey())
  if (!savedData && !userData.value.email && userData.value.userType === 'guest') {
    console.log('💡 新用户，显示登录弹窗')
    showLoginModal.value = true
  }

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
