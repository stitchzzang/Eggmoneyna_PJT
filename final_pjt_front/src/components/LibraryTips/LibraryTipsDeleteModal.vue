<template>
  <div class="modal-overlay">
    <div class="modal">
      <p class="modal-message">정말로 삭제하시겠습니까?</p>
      <div class="modal-buttons">
        <button @click="$emit('confirm')" class="confirm-btn">확인</button>
        <button @click="$emit('cancel')" class="cancel-btn">취소</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {};
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
  align-items: center;
  justify-content: center;
}

.modal {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 300px;
}

.modal-message {
  margin-bottom: 20px;
  font-size: 1.1em;
  color: #333;
}

.modal-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.confirm-btn, .cancel-btn {
  padding: 8px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.confirm-btn {
  background-color: #dc3545;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.confirm-btn:hover {
  background-color: #c82333;
}

.cancel-btn:hover {
  background-color: #5a6268;
}
</style>
