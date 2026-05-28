
<template>
  <div class="wisdom-bag-overlay" @click="$emit('close')">
    <div class="wisdom-bag-panel" @click.stop>
      <div class="wisdom-bag-header">
        <h3 class="wisdom-bag-title">
          <span class="wisdom-bag-icon">📜</span> 孔明锦囊
          <span v-if="wisdomList.length > 0" class="wisdom-count">({{ wisdomList.length }})</span>
        </h3>
        <button class="wisdom-bag-close" @click="$emit('close')">×</button>
      </div>

      <div class="wisdom-bag-content">
        <div v-if="wisdomList.length === 0" class="wisdom-bag-empty">
          <div class="empty-icon">🪶</div>
          <div class="empty-text">主公，暂无锦囊妙计</div>
          <div class="empty-hint">收藏精彩回答，收入锦囊</div>
        </div>

        <div v-else class="wisdom-bag-list">
          <div v-for="item in wisdomList" :key="item.id" class="wisdom-bag-item">
            <div class="wisdom-bag-item-header">
              <div class="wisdom-bag-item-title">{{ item.title }}</div>
              <button class="wisdom-bag-item-delete" @click="deleteWisdom(item.id)">×</button>
            </div>
            <div class="wisdom-bag-item-content">{{ item.content }}</div>
            <div class="wisdom-bag-item-time">
              收入锦囊于：{{ formatTime(item.createTime) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const STORAGE_KEY = 'kongming-wisdom-bag'

const emit = defineEmits(['close'])

const wisdomList = ref([])
const wisdomHashSet = ref(new Set())

const hashCode = (str) => {
  let hash = 0
  if (str.length === 0) return hash
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash // Convert to 32bit integer
  }
  return hash.toString()
}

const buildHashSet = () => {
  wisdomHashSet.value = new Set(wisdomList.value.map(item => item.contentHash))
  console.log('📚 HashSet built with', wisdomHashSet.value.size, 'items')
}

const loadWisdomList = () => {
  try {
    console.log('📚 Loading wisdom list...')
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      wisdomList.value = JSON.parse(saved)
      buildHashSet()
      console.log('📚 Loaded wisdom list:', wisdomList.value.length, 'items')
    } else {
      console.log('📚 No wisdom list found, starting fresh')
    }
  } catch (e) {
    console.error('加载锦囊失败:', e)
  }
}

const saveWisdomList = () => {
  try {
    console.log('📚 Saving wisdom list:', wisdomList.value.length, 'items')
    localStorage.setItem(STORAGE_KEY, JSON.stringify(wisdomList.value))
  } catch (e) {
    console.error('保存锦囊失败:', e)
  }
}

const checkWisdomExists = (content) => {
  const contentHash = hashCode(content)
  return wisdomHashSet.value.has(contentHash)
}

const addWisdom = (title, content) => {
  console.log('📚 Adding wisdom to list - title:', title, 'content length:', content.length)
  
  const contentHash = hashCode(content)
  if (wisdomHashSet.value.has(contentHash)) {
    console.log('📚 Wisdom already exists (hash match), skipping addition')
    alert('此锦囊妙计已在囊中！')
    return false
  }
  
  const newWisdom = {
    id: Date.now().toString(),
    title,
    content,
    contentHash: contentHash,
    createTime: new Date().toISOString()
  }
  
  wisdomList.value.unshift(newWisdom)
  wisdomHashSet.value.add(contentHash)
  saveWisdomList()
  
  console.log('📚 Wisdom added successfully, total now:', wisdomList.value.length)
  return true
}

const deleteWisdom = (id) => {
  console.log('📚 Deleting wisdom with id:', id)
  const item = wisdomList.value.find(item => item.id === id)
  if (item && item.contentHash) {
    wisdomHashSet.value.delete(item.contentHash)
  }
  wisdomList.value = wisdomList.value.filter(item => item.id !== id)
  saveWisdomList()
}

const formatTime = (timeStr) => {
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) {
    return '刚刚'
  } else if (diff < 3600000) {
    return Math.floor(diff / 60000) + '分钟前'
  } else if (diff < 86400000) {
    return Math.floor(diff / 3600000) + '小时前'
  } else if (diff < 604800000) {
    return Math.floor(diff / 86400000) + '天前'
  } else {
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
}

onMounted(() => {
  console.log('📚 WisdomBag component mounted')
  loadWisdomList()
})

defineExpose({
  addWisdom
})
</script>

<style scoped>
.wisdom-bag-overlay {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0; left: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: flex-end;
  z-index: 1000;
}

.wisdom-bag-panel {
  width: 400px;
  height: 100%;
  background: linear-gradient(180deg, #1a2744, #0f172a);
  border-left: 2px solid #d4b878;
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.wisdom-bag-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #283447;
  background-color: #121b2b;
}

.wisdom-bag-title {
  font-size: 20px;
  font-weight: 600;
  color: #d4b878;
  display: flex;
  align-items: center;
  gap: 10px;
}

.wisdom-count {
  font-size: 14px;
  font-weight: 400;
  color: #94a3b8;
}

.wisdom-bag-icon {
  font-size: 24px;
}

.wisdom-bag-close {
  width: 36px;
  height: 36px;
  border: 1px solid #334155;
  background: transparent;
  color: #94a3b8;
  font-size: 20px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.wisdom-bag-close:hover {
  border-color: #d4b878;
  color: #d4b878;
}

.wisdom-bag-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scrollbar-width: thin;
  scrollbar-color: #475569 transparent;
}

.wisdom-bag-content::-webkit-scrollbar {
  width: 6px;
}

.wisdom-bag-content::-webkit-scrollbar-track {
  background: transparent;
}

.wisdom-bag-content::-webkit-scrollbar-thumb {
  background-color: #475569;
  border-radius: 3px;
}

.wisdom-bag-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 16px;
  color: #64748b;
}

.empty-icon {
  font-size: 64px;
  opacity: 0.5;
}

.empty-text {
  font-size: 16px;
  color: #94a3b8;
}

.empty-hint {
  font-size: 14px;
  color: #475569;
}

.wisdom-bag-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.wisdom-bag-item {
  background-color: #121b2b;
  border: 1px solid #283447;
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
}

.wisdom-bag-item:hover {
  border-color: #d4b878;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 184, 120, 0.2);
}

.wisdom-bag-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.wisdom-bag-item-title {
  font-size: 14px;
  font-weight: 600;
  color: #e6c88c;
  max-width: 280px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.wisdom-bag-item-delete {
  width: 28px;
  height: 28px;
  border: none;
  background: transparent;
  color: #94a3b8;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.wisdom-bag-item-delete:hover {
  color: #ef4444;
  background-color: rgba(239, 68, 68, 0.1);
}

.wisdom-bag-item-content {
  color: #cbd5e1;
  font-size: 14px;
  line-height: 1.8;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.wisdom-bag-item-time {
  color: #64748b;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

@media (max-width: 768px) {
  .wisdom-bag-panel {
    width: 100%;
  }
}
</style>
