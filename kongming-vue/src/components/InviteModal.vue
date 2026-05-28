
<template>
  <div class="invite-modal-overlay" v-if="show" @click.self="$emit('close')">
    <div class="invite-modal">
      <div class="invite-header">
        <div class="invite-icon">🎋</div>
        <h2 class="invite-title">孔明恭候多时</h2>
        <p class="invite-subtitle">请出示邀请手令，方可入内</p>
      </div>

      <div class="invite-content">
        <input
          v-model="inviteCode"
          type="text"
          placeholder="请输入邀请手令..."
          @keyup.enter="handleVerify"
          class="invite-input"
          :class="{ error: errorMessage }"
        />
        <p v-if="errorMessage" class="invite-error">{{ errorMessage }}</p>
        <button class="invite-btn" @click="handleVerify" :disabled="loading">
          {{ loading ? '核验中...' : '验明正身' }}
        </button>
      </div>

      <div class="invite-footer">
        <p class="invite-hint">若无邀请手令，请联系管事</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { verifyInviteCode } from '../services/api'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['success', 'close'])

const inviteCode = ref('')
const loading = ref(false)
const errorMessage = ref('')

const handleVerify = async () => {
  if (!inviteCode.value.trim()) {
    errorMessage.value = '邀请手令不能为空'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    const result = await verifyInviteCode(inviteCode.value.trim())
    if (result.success) {
      emit('success')
      inviteCode.value = ''
    } else {
      errorMessage.value = result.message || '邀请手令有误'
    }
  } catch (error) {
    errorMessage.value = '网络不通，请稍后再试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.invite-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
}

.invite-modal {
  background: linear-gradient(180deg, #1a2744, #0f172a);
  border: 2px solid #d4b878;
  border-radius: 16px;
  width: 90%;
  max-width: 420px;
  padding: 36px 32px;
  text-align: center;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.invite-header {
  margin-bottom: 32px;
}

.invite-icon {
  font-size: 64px;
  margin-bottom: 16px;
}

.invite-title {
  font-size: 28px;
  color: #d4b878;
  margin-bottom: 8px;
}

.invite-subtitle {
  color: #94a3b8;
  font-size: 14px;
}

.invite-content {
  margin-bottom: 24px;
}

.invite-input {
  width: 100%;
  padding: 14px 20px;
  border: 2px solid #283447;
  border-radius: 10px;
  background-color: #1e293b;
  color: #e2e8f0;
  font-size: 16px;
  outline: none;
  transition: all 0.3s ease;
  box-sizing: border-box;
  text-align: center;
  letter-spacing: 2px;
}

.invite-input:focus {
  border-color: #d4b878;
  box-shadow: 0 0 0 3px rgba(212, 184, 120, 0.2);
}

.invite-input.error {
  border-color: #ef4444;
}

.invite-error {
  color: #ef4444;
  font-size: 14px;
  margin-top: 12px;
}

.invite-btn {
  width: 100%;
  padding: 14px 20px;
  margin-top: 16px;
  border: 2px solid #d4b878;
  background: linear-gradient(180deg, #3d5a4c, #2a4036);
  color: #e6c88c;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.invite-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 184, 120, 0.3);
}

.invite-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.invite-footer {
  margin-top: 24px;
}

.invite-hint {
  color: #64748b;
  font-size: 12px;
}
</style>
