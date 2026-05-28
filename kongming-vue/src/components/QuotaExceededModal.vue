
<template>
  <div class="quota-overlay" v-if="show" @click.self="$emit('close')">
    <div class="quota-modal">
      <div class="quota-icon">⏳</div>
      <h3 class="quota-title">今日策论已毕</h3>
      <div class="quota-message">
        <p>今日问数已用尽</p>
        <p>请明日再临，听吾妙计</p>
      </div>
      <div class="quota-hint">
        <p>若想多问几策，不妨留下名帖</p>
      </div>
      <button class="btn-confirm" @click="$emit('close')">
        知晓，明日再来
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close'])
</script>

<style scoped>
.quota-overlay {
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

.quota-modal {
  background: linear-gradient(180deg, #1a2744, #0f172a);
  border: 2px solid #d4b878;
  border-radius: 16px;
  width: 90%;
  max-width: 420px;
  padding: 40px 32px;
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

.quota-icon {
  font-size: 72px;
  margin-bottom: 20px;
}

.quota-title {
  font-size: 26px;
  color: #e6c88c;
  margin-bottom: 20px;
}

.quota-message {
  color: #cbd5e1;
  font-size: 16px;
  line-height: 2;
  margin-bottom: 24px;
}

.quota-hint {
  color: #64748b;
  font-size: 13px;
  line-height: 1.8;
  margin-bottom: 32px;
  padding: 16px;
  background-color: rgba(212, 184, 120, 0.1);
  border-radius: 10px;
}

.btn-confirm {
  width: 100%;
  padding: 14px 20px;
  border: 2px solid #d4b878;
  background: linear-gradient(180deg, #3d5a4c, #2a4036);
  color: #e6c88c;
  border-radius: 10px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-confirm:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(212, 184, 120, 0.3);
}
</style>
