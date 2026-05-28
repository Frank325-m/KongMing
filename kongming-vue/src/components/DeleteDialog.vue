
<template>
  <div v-if="show" class="modal-overlay" @click="$emit('cancel')">
    <div class="modal-content" @click.stop>
      <h3>确认删除会话</h3>
      <p>确定要删除会话"{{ title }}"吗？</p>
      <p class="warning">此操作无法撤销！</p>
      <div class="modal-buttons">
        <button class="btn-cancel" @click="$emit('cancel')">取消</button>
        <button class="btn-delete" @click="$emit('confirm')">删除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: { type: Boolean, default: false },
  title: { type: String, default: '' }
})

defineEmits(['cancel', 'confirm'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #1e293b;
  padding: 32px;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
  border: 1px solid #334155;
}

.modal-content h3 {
  color: #e2e8f0;
  margin-bottom: 16px;
  font-size: 18px;
}

.modal-content p {
  color: #94a3b8;
  margin-bottom: 8px;
  line-height: 1.6;
}

.modal-content .warning {
  color: #ef4444;
  font-weight: 500;
}

.modal-buttons {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  justify-content: flex-end;
}

.btn-cancel {
  padding: 10px 20px;
  border: 1px solid #334155;
  background: transparent;
  color: #94a3b8;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background-color: #334155;
  color: #e2e8f0;
}

.btn-delete {
  padding: 10px 20px;
  border: none;
  background-color: #ef4444;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-delete:hover {
  background-color: #dc2626;
}
</style>
