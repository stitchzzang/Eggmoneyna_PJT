<template>
  <div class="write-form">
    <h2>게시글 작성</h2>
    <form @submit.prevent="createThread">
      <div class="form-group">
        <label for="title">제목</label>
        <input 
          type="text" 
          id="title"
          v-model.trim="title"
          required
          placeholder="제목을 입력하세요"
        >
      </div>

      <div class="form-group">
        <label for="content">내용</label>
        <textarea 
          id="content"
          v-model.trim="content"
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
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const emit = defineEmits(['submit', 'cancel'])

const title = ref(null)
const content = ref(null)
const store = useCounterStore()
const router = useRouter()

const createThread = function() {
  console.log('현재 토큰:', auth.token)

  if (!auth.token) {
    alert('로그인이 필요합니다.')
    router.push('/login')
    return
  }

  axios({
    method: 'post',
    url: `${store.API_URL}/community/`,
    headers: {
      Authorization: `Token ${auth.token}`,
      'Content-Type': 'application/json',
    },
    data: {
      title: title.value,
      content: content.value
    }
  })
  .then((res) => {
    // console.log('게시글 작성 성공!')
    alert('게시글이 성공적으로 등록되었습니다!');
    router.push('/community')
  })
  .catch((err) => {
    console.log('에러 응답:', err.response?.data)
    if (err.response?.status === 401) {
      alert('로그인이 필요하거나 세션이 만료되었습니다. 다시 로그인해주세요.')
      auth.logout()
      router.push('/login')
    } else {
      alert('게시글 등록에 실패했습니다. 다시 시도해주세요.')
    }
  })
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
