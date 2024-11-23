<template>
  <div>
    <h2>게시글 작성</h2>
    <div class="community-container">
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
          <button type="submit" class="primary-btn">등록</button>
          <button type="button" @click="cancelWrite" class="secondary-btn">취소</button>
        </div>
      </form>
    </div>
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

const cancelWrite = () => {
  router.push('/community')
}

</script>

<style scoped>
h2 {
  color: #056800;
  margin: 40px 0 20px;
  margin-bottom: 40px;
  font-size: 1.8rem;
  text-align: center;
  font-weight: 600;

}

.page-title {
  margin-bottom: 20px;
}

.community-container {
  max-width: 800px;
  margin: 20px auto 60px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 600;
}

input, textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 1rem;
  background-color: #f8f9fa;
  transition: border-color 0.3s ease;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #007bff;
  background-color: #fff;
}

textarea {
  resize: vertical;
  min-height: 200px;
}

.button-group {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

.primary-btn, .secondary-btn {
  padding: 8px 18px;
  border-radius: 25px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid;
  white-space: nowrap;
  min-width: fit-content;
  font-size: 18px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.primary-btn {
  background: linear-gradient(45deg, #86da8a, #047404);
  color: white;
  border-color: #1d8a0e;
}

.secondary-btn {
  background: linear-gradient(45deg, #8a8a8a, #4a4a4a);
  color: white;
  border-color: #5a5a5a;
}

.primary-btn:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.secondary-btn:hover {
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}
</style>
