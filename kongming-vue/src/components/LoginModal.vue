
<template>
  <div class="login-overlay" v-if="show" @click.self="$emit('close')">
    <div class="login-modal">
      <div class="login-header">
        <h3>孔明军师</h3>
        <p class="login-subtitle">三分天下，尽在掌中</p>
      </div>

      <div class="login-content">
        <div class="login-options">
          <button class="btn-guest" @click="handleGuestLogin">
            <span class="btn-icon">🚶</span>
            <span>访客模式</span>
            <span class="btn-info">每日可询 {{ guestLimit }} 次</span>
          </button>

          <div class="divider">
            <span>或</span>
          </div>

          <div class="email-login">
            <label class="email-label">主公请留名（邮箱）</label>
            <input
              v-model="email"
              type="email"
              placeholder="请输入邮箱"
              @keyup.enter="handleEmailLogin"
              class="email-input"
            />
            <button
              class="btn-login"
              @click="handleEmailLogin"
              :disabled="!validateEmail()"
            >
              <span class="btn-icon">🔐</span>
              登录咨询
            </button>
            <p class="login-hint">登录用户每日可询 {{ userLimit }} 次</p>
          </div>
        </div>
      </div>

      <p class="login-footer">卧龙在此，恭候多时</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  guestLimit: {
    type: Number,
    default: 5
  },
  userLimit: {
    type: Number,
    default: 30
  }
})

const emit = defineEmits(['login', 'close'])

const email = ref('')

const validateEmail = () => {
  const re = /\S+@\S+\.\S+/
  return re.test(email.value)
}

const handleGuestLogin = () => {
  emit('login', { userType: 'guest' })
}

const handleEmailLogin = () => {
  if (validateEmail()) {
    emit('login', { userType: 'user', email: email.value })
  }
}
</script>

<style scoped>
.login-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.login-modal {
  background: linear-gradient(180deg, #1a2744, #0f172a);
  border: 2px solid #d4b878;
  border-radius: 16px;
  width: 90%;
  max-width: 420px;
  padding: 32px;
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

.login-header {
  text-align: center;
  margin-bottom: 28px;
}

.login-header h3 {
  font-size: 28px;
  color: #d4b878;
  margin-bottom: 8px;
}

.login-subtitle {
  color: #94a3b8;
  font-size: 14px;
}

.login-content {
  margin-bottom: 20px;
}

.login-options {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.btn-guest,
.btn-login {
  width: 100%;
  padding: 14px 20px;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.btn-guest {
  background: linear-gradient(180deg, #283447, #1e293b);
  color: #cbd5e1;
  border-color: #334155;
}

.btn-guest:hover {
  border-color: #d4b878;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 184, 120, 0.2);
}

.btn-login {
  background: linear-gradient(180deg, #3d5a4c, #2a4036);
  color: #e6c88c;
  border-color: #4a6b5a;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(61, 90, 76, 0.4);
}

.btn-login:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-icon {
  font-size: 22px;
}

.btn-info {
  font-size: 12px;
  opacity: 0.8;
}

.divider {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  color: #475569;
  font-size: 14px;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background-color: #283447;
}

.email-login {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.email-label {
  color: #94a3b8;
  font-size: 14px;
}

.email-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #283447;
  border-radius: 8px;
  background-color: #1e293b;
  color: #e2e8f0;
  font-size: 15px;
  outline: none;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.email-input:focus {
  border-color: #4a6b5a;
}

.login-hint {
  color: #64748b;
  font-size: 12px;
  text-align: center;
}

.login-footer {
  color: #64748b;
  font-size: 12px;
  text-align: center;
}
</style>
