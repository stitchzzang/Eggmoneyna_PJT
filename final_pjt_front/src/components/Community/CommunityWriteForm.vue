<template>
  <div class="write-form">
    <h2>게시글 작성</h2>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="title">제목</label>
        <input 
          type="text" 
          id="title"
          v-model="title"
          required
          placeholder="제목을 입력하세요"
        >
      </div>

      <div class="form-group">
        <label for="content">내용</label>
        <textarea 
          id="content"
          v-model="content"
          required
          placeholder="내용을 입력하세요"
          rows="10"
        ></textarea>
      </div>

      <div class="button-group">
        <button type="submit" class="btn-submit">등록</button>
        <button type="button" @click="$emit('cancel')" class="btn-cancel">취소</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const emit = defineEmits(['submit', 'cancel'])

const title = ref('')
const content = ref('')

const submitForm = () => {
  emit('submit', {
    title: title.value,
    content: content.value,
    author: auth.user
  })
  title.value = ''
  content.value = ''
}
</script>

<style scoped>
.write-form {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

input, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

textarea {
  resize: vertical;
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}

button {
  padding: 10px 20px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-submit {
  background-color: #4CAF50;
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
