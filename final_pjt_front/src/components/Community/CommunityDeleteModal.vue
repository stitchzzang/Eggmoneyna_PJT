<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h3>게시글 삭제</h3>
      <p>정말로 이 게시글을 삭제하시겠습니까?</p>
      <div class="button-group">
        <button @click="$emit('confirm')" class="btn-delete">삭제</button>
        <button @click="$emit('cancel')" class="btn-cancel">취소</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineEmits(['confirm', 'cancel'])
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 400px;
  text-align: center;
}

h3 {
  margin-bottom: 15px;
}

p {
  margin-bottom: 20px;
  color: #666;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: center;
}

button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}

.btn-cancel {
  background-color: #6c757d;
  color: white;
}

button:hover {
  opacity: 0.9;
}
</style>
