<template>
  <h1>detail</h1>
  <div v-if="thread">
    <div v-if="!isEditing">
      <p>게시글 번호 : {{ thread.id }}</p>
      <p>게시글 제목 : {{ thread.title }}</p>
      <p>게시글 내용 : {{ thread.content }}</p>
      <p>작성자 : {{ thread.username }}</p>
      <p>작성일 : {{ formatDate(thread.created_at) }}</p> 
      <p>수정일 : {{ formatDate(thread.updated_at) }}</p> 
      
      <div v-if="isAuthor" class="button-group">
        <button @click="startEditing" class="btn-edit">수정</button>
        <button @click="deleteThread" class="btn-delete">삭제</button>
      </div>
    </div>

    <div v-else>
      <input v-model="editForm.title" type="text" class="edit-input">
      <textarea v-model="editForm.content" class="edit-textarea"></textarea>
      <div class="button-group">
        <button @click="updateThread" class="btn-edit">저장</button>
        <button @click="cancelEdit" class="btn-close">취소</button>
      </div>
    </div>
  </div>  
  <!-- <div class="community-detail">
    <div class="detail-header">
      <h2>{{ post.title }}</h2>
      <div class="post-info">
        <span>작성자: {{ post.author }}</span>
        <span>작성일: {{ formatDate(post.created_at) }}</span>
      </div>
    </div>

    <div class="post-content">
      {{ post.content }}
    </div>

    <div class="button-group">
      <button @click="$emit('close')" class="btn-close">목록으로</button>
      <div v-if="isAuthor" class="author-buttons">
        <button @click="$emit('edit', post)" class="btn-edit">수정</button>
        <button @click="$emit('delete', post)" class="btn-delete">삭제</button>
      </div>
    </div>
  </div> -->
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter' 
import { useRoute, useRouter } from 'vue-router'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const thread = ref(null)
const auth = useAuthStore()

onMounted(() => {
  getThreadDetails()
})

const getThreadDetails = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/community/${route.params.id}/`,
    headers: {
      Authorization: `Token ${auth.token}`
    }
  })
  .then((res) => {
    thread.value = res.data
  })
  .catch((err) => {
    console.log('게시글을 불러오는데 실패했습니다:', err)
  })
}

const props = defineProps({
  thread: {
    type: Object,
    required: true
  }
})

defineEmits(['close', 'edit', 'delete'])

const isEditing = ref(false)
const editForm = ref({
  title: '',
  content: ''
})

const isAuthor = computed(() => {
  return thread.value?.username === auth.username
})

const startEditing = () => {
  editForm.value = {
    title: thread.value.title,
    content: thread.value.content
  }
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
}

const updateThread = () => {
  axios({
    method: 'patch',
    url: `${store.API_URL}/community/${route.params.id}/`,
    data: editForm.value,
    headers: {
      Authorization: `Token ${auth.token}`
    }
  })
  .then((res) => {
    thread.value = res.data
    isEditing.value = false
  })
  .catch((err) => {
    console.log(err)
  })
}

const deleteThread = () => {
  if (confirm('정말로 삭제하시겠습니까?')) {
    axios({
      method: 'delete',
      url: `${store.API_URL}/community/${route.params.id}/`,
      headers: {
        Authorization: `Token ${auth.token}`
      }
    })
    .then(() => {
      alert('게시글이 삭제되었습니다.')
      router.push({ name: 'community' })
    })
    .catch((err) => {
      console.log(err)
    })
  }
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>

<style scoped>
.community-detail {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.detail-header {
  border-bottom: 1px solid #eee;
  padding-bottom: 15px;
  margin-bottom: 20px;
}

.post-info {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 0.9em;
  margin-top: 10px;
}

.post-content {
  min-height: 200px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.author-buttons {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 16px;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-close {
  background-color: #6c757d;
  color: white;
}

.btn-edit {
  background-color: #4CAF50;
  color: white;
}

.btn-delete {
  background-color: #dc3545;
  color: white;
}

button:hover {
  opacity: 0.9;
}

.edit-input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.edit-textarea {
  width: 100%;
  min-height: 200px;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
