
<template>
  <div class="sidebar" :class="{ collapsed: sidebarCollapsed }">
    <div class="sidebar-header">
      <h2>孔明军师</h2>
      <button class="new-chat-btn" @click="$emit('create-session')">+ 新对话</button>
    </div>

    <div class="session-list">
      <div v-if="sessions.length === 0" class="empty-sessions">
        暂无会话，点击“新对话”开始
      </div>

      <div
        v-for="session in sessions"
        :key="session.id"
        class="session-item"
        :class="{ active: session.id === currentSessionId }"
        @click="$emit('switch-session', session.id)"
      >
        <div class="session-info">
          <div class="session-title">{{ session.title }}</div>
          <div class="session-meta">
            <span>{{ formatDate(session.updated_at) }}</span>
            <span class="message-count">{{ session.message_count }}条</span>
          </div>
        </div>
        <button
          class="delete-session-btn"
          @click.stop="handleDelete(session.id, session.title)"
          title="删除会话"
        >
          🗑️
        </button>
      </div>
    </div>

    <div class="sidebar-footer">
      <button class="toggle-btn" @click="$emit('toggle-sidebar')">
        {{ sidebarCollapsed ? '→' : '←' }}
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  sessions: { type: Array, default: () => [] },
  currentSessionId: { type: String, default: null },
  sidebarCollapsed: { type: Boolean, default: false }
})

const emit = defineEmits(['create-session', 'switch-session', 'delete-session', 'toggle-sidebar'])

const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diff = now - date

  if (diff < 86400000) { // 24小时内
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  } else if (diff < 604800000) { // 7天内
    return date.toLocaleDateString('zh-CN', { weekday: 'short' })
  } else {
    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
  }
}

const handleDelete = (id, title) => {
  emit('delete-session', id, title)
}
</script>

<style scoped>
.sidebar {
  width: 280px;
  min-width: 280px;
  background-color: #0f172a;
  border-right: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
  transition: width 0.3s ease, min-width 0.3s ease;
}

.sidebar.collapsed {
  width: 0;
  min-width: 0;
  overflow: hidden;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid #1e293b;
}

.sidebar-header h2 {
  color: #d4b878;
  font-size: 18px;
  margin-bottom: 16px;
}

.new-chat-btn {
  width: 100%;
  padding: 12px 20px;
  border: 1px solid #3b82f6;
  background: transparent;
  color: #3b82f6;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.new-chat-btn:hover {
  background-color: #3b82f6;
  color: white;
}

.session-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  /* 自定义滚动条 - WebKit 浏览器 */
  scrollbar-width: thin;
  scrollbar-color: transparent transparent;
}

.session-list:hover {
  scrollbar-color: #475569 transparent;
}

.session-list::-webkit-scrollbar {
  width: 6px;
}

.session-list::-webkit-scrollbar-track {
  background: transparent;
}

.session-list::-webkit-scrollbar-thumb {
  background-color: transparent;
  border-radius: 3px;
  transition: background-color 0.3s ease;
}

.session-list:hover::-webkit-scrollbar-thumb {
  background-color: #475569;
}

.session-list:active::-webkit-scrollbar-thumb {
  background-color: #64748b;
}

.empty-sessions {
  text-align: center;
  color: #64748b;
  padding: 40px 20px;
  font-size: 14px;
}

.session-item {
  padding: 14px 16px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 6px;
  transition: all 0.2s ease;
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.session-item:hover {
  background-color: #1e293b;
}

.session-item.active {
  background-color: #334155;
}

.session-info {
  flex: 1;
  min-width: 0;
}

.session-title {
  color: #e2e8f0;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 6px;
}

.session-meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #64748b;
}

.delete-session-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.2s ease;
  font-size: 14px;
  padding: 2px;
}

.session-item:hover .delete-session-btn {
  opacity: 1;
}

.delete-session-btn:hover {
  transform: scale(1.2);
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #1e293b;
  text-align: center;
}

.toggle-btn {
  background: transparent;
  border: 1px solid #334155;
  color: #64748b;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.toggle-btn:hover {
  background-color: #1e293b;
  color: #e2e8f0;
}

@media (max-width: 768px) {
  .sidebar {
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 100;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3);
  }

  .sidebar.collapsed {
    transform: translateX(-100%);
    width: 280px;
    min-width: 280px;
  }
}
</style>
