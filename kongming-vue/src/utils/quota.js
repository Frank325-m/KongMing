
// 配额配置 - 用 let 以便从后端动态更新
let QUOTA_CONFIG = {
  guest: {
    dailyLimit: 5,
    displayName: '访客'
  },
  user: {
    dailyLimit: 30,
    displayName: '登录用户'
  }
}

let CONFIG_LOADED = false

export const loadQuotaConfig = async (apiConfig) => {
  if (apiConfig) {
    // 直接更新配置对象
    if (apiConfig.guest_daily_limit !== undefined) {
      QUOTA_CONFIG.guest.dailyLimit = apiConfig.guest_daily_limit
    }
    if (apiConfig.user_daily_limit !== undefined) {
      QUOTA_CONFIG.user.dailyLimit = apiConfig.user_daily_limit
    }
    CONFIG_LOADED = true
    console.log('✅ 配额配置已从后端加载:', QUOTA_CONFIG)
  }
}

export const getQuotaConfig = () => {
  // 返回一个新对象，确保 Vue 的响应式能触发
  return {
    guest: { ...QUOTA_CONFIG.guest },
    user: { ...QUOTA_CONFIG.user }
  }
}

const STORAGE_KEY = 'kongming-user-data'

export const getUserData = () => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (!saved) {
      return {
        userType: 'guest',
        email: null,
        lastLoginDate: null,
        todayCount: 0
      }
    }
    const data = JSON.parse(saved)
    
    // 每日0点自动重置配额计数
    const today = new Date().toDateString()
    if (data.lastLoginDate !== today) {
      return {
        ...data,
        lastLoginDate: today,
        todayCount: 0
      }
    }
    
    return data
  } catch (e) {
    console.error('加载用户数据失败:', e)
    return {
      userType: 'guest',
      email: null,
      lastLoginDate: null,
      todayCount: 0
    }
  }
}

export const saveUserData = (data) => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
  } catch (e) {
    console.error('保存用户数据失败:', e)
  }
}

export const getTodayQuota = (userType) => {
  return QUOTA_CONFIG[userType]?.dailyLimit || 5
}

export const getRemainingQuota = (userType, todayCount) => {
  return Math.max(0, getTodayQuota(userType) - todayCount)
}

// 消耗一次配额，每日自动重置
export const useOneQuota = (userData) => {
  const today = new Date().toDateString()
  
  if (userData.lastLoginDate !== today) {
    userData = {
      ...userData,
      lastLoginDate: today,
      todayCount: 1
    }
  } else {
    userData = {
      ...userData,
      todayCount: userData.todayCount + 1
    }
  }
  
  saveUserData(userData)
  return userData
}

// 检查当前配额是否已用尽
export const checkQuotaExceeded = (userData) => {
  const today = new Date().toDateString()
  let currentData = userData
  
  if (userData.lastLoginDate !== today) {
    currentData = {
      ...userData,
      lastLoginDate: today,
      todayCount: 0
    }
  }
  
  const remaining = getRemainingQuota(currentData.userType, currentData.todayCount)
  return remaining <= 0
}

export const login = (email) => {
  const today = new Date().toDateString()
  const data = {
    userType: 'user',
    email,
    lastLoginDate: today,
    todayCount: 0
  }
  saveUserData(data)
  return data
}

export const logout = () => {
  const today = new Date().toDateString()
  const data = {
    userType: 'guest',
    email: null,
    lastLoginDate: today,
    todayCount: 0
  }
  saveUserData(data)
  return data
}
