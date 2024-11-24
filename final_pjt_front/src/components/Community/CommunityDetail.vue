<template>
  <div class="community-detail">
    <!-- 게시글 상세 정보 -->
    <div v-if="thread" class="detail-container">
      <div v-if="!isEditing" class="detail-content">
        <div class="detail-header">
          <h2>{{ thread.title }}</h2>
          <div class="post-info">
            <span>작성자: {{ thread.username }}</span>
            <span>작성일: {{ formatDate(thread.created_at) }}</span>
            <span>수정일: {{ formatDate(thread.updated_at) }}</span>
          </div>
        </div>

        <div class="post-content">
          {{ thread.content }}
        </div>
        
        <div v-if="isAuthor" class="author-buttons">
          <button @click="startEditing" class="btn-edit">수정</button>
          <button @click="deleteThread" class="btn-delete">삭제</button>
        </div>
      </div>

      <!-- 수정 폼 -->
      <div v-else class="edit-form">
        <input v-model="editForm.title" type="text" class="edit-input" placeholder="제목">
        <textarea v-model="editForm.content" class="edit-textarea" placeholder="내용"></textarea>
        <div class="button-group">
          <button @click="updateThread" class="btn-edit">저장</button>
          <button @click="cancelEdit" class="btn-close">취소</button>
        </div>
      </div>
    </div>  

    <!-- 댓글 섹션 -->
    <div class="comments-section">
      <h3>💬 댓글</h3>
      <div class="comment-form">
        <textarea 
          v-model="newComment" 
          placeholder="댓글을 작성하세요"
          class="comment-textarea"
        ></textarea>
        <button 
          @click="submitComment" 
          class="btn-submit"
        >
          댓글 작성
        </button>
      </div>

      <!-- 댓글 목록 -->
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div v-if="editingCommentId !== comment.id">
            <div class="comment-info">
              <span class="comment-author">{{ comment.username }}</span>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
            <div class="comment-date">{{ formatDate(comment.created_at) }}</div>
            <div v-if="comment.username === auth.username" class="comment-buttons">
              <button @click="startEditComment(comment)" class="btn-edit-sm">수정</button>
              <button @click="deleteComment(comment.id)" class="btn-delete-sm">삭제</button>
            </div>
          </div>
          <!-- 댓글 수정 폼 -->
          <div v-else class="comment-edit-form">
            <textarea 
              v-model="editCommentContent" 
              class="comment-textarea"
            ></textarea>
            <div class="button-group">
              <button @click="updateComment(comment.id)" class="btn-edit-sm">저장</button>
              <button @click="cancelEditComment" class="btn-close-sm">취소</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
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
  getComments()
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

const comments = ref([])
const newComment = ref('')
const editingCommentId = ref(null)
const editCommentContent = ref('')

const getComments = () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/community/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${auth.token}`
    }
  })
  .then((res) => {
    comments.value = res.data
  })
  .catch((err) => {
    console.log('댓글을 불러오는데 실패했습니다:', err)
  })
}

const submitComment = () => {
  if (!newComment.value.trim()) return

  axios({
    method: 'post',
    url: `${store.API_URL}/community/${route.params.id}/comments/create/`,
    data: { content: newComment.value },
    headers: {
      Authorization: `Token ${auth.token}`
    }
  })
  .then(() => {
    newComment.value = ''
    getComments()
  })
  .catch((err) => {
    console.log('댓글 작성에 실패했습니다:', err)
  })
}

const startEditComment = (comment) => {
  editingCommentId.value = comment.id
  editCommentContent.value = comment.content
}

const cancelEditComment = () => {
  editingCommentId.value = null
  editCommentContent.value = ''
}

const updateComment = (commentId) => {
  if (!editCommentContent.value.trim()) return

  axios({
    method: 'put',
    url: `${store.API_URL}/community/${route.params.id}/comments/${commentId}/`,
    data: { content: editCommentContent.value },
    headers: {
      Authorization: `Token ${auth.token}`
    }
  })
  .then(() => {
    editingCommentId.value = null
    getComments()
  })
  .catch((err) => {
    console.log('댓글 수정에 실패했습니다:', err)
  })
}

const deleteComment = (commentId) => {
  if (!confirm('정말로 삭제하시겠습니까?')) return

  axios({
    method: 'delete',
    url: `${store.API_URL}/community/${route.params.id}/comments/${commentId}/`,
    headers: {
      Authorization: `Token ${auth.token}`
    }
  })
  .then(() => {
    getComments()
  })
  .catch((err) => {
    console.log('댓글 삭제에 실패했습니다:', err)
  })
}
</script>

<style scoped>
.community-detail {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  margin-top: 40px;
}

.detail-container {
  background-color: rgba(255, 255, 255, 0.4);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 30px;
}

.detail-header {
  border-bottom: 2px solid #eee;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.detail-header h2 {
  color: #333;
  margin-bottom: 15px;
}

.post-info {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 0.9em;
}

.post-content {
  min-height: 200px;
  line-height: 1.8;
  color: #444;
  white-space: pre-wrap;
  margin-bottom: 30px;
}

/* 버튼 스타일 업데이트 */
.btn-edit, .btn-delete, .btn-close, .btn-submit {
  padding: 10px 20px;
  border-radius: 25px;
  border: none;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s ease;
}

.btn-edit {
  background: linear-gradient(45deg, #86da8a, #047404) !important;
  border: 2px solid #128004;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  letter-spacing: 1.3px;
  color: white;
  opacity: 0.8;
  padding: 8px 20px;
  border-radius: 5px;
}

.btn-edit:hover {
  opacity: 1;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(64, 192, 87, 0.4);
}

.btn-delete {
  background: linear-gradient(45deg, #fa8b8b, #eb1c1c);
  border: 2px solid #b5221a;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  letter-spacing: 1.3px;
  color: white;
  opacity: 0.8;
  padding: 8px 20px;
  border-radius: 5px;
}

.btn-delete:hover {
  opacity: 1;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(250, 82, 82, 0.4);
}

.btn-close {
  background: linear-gradient(45deg, #6c757d, #495057);
  color: white;
}

.btn-submit {
  padding: 10px 20px;
  background: linear-gradient(45deg, #47e0cc, #049b8c) !important;
  color: white;
  border: 2px solid #00897B;
  border-radius: 25px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  font-size: 18px;
  width: 100%;
  margin-top: 10px;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.btn-submit:hover {
  opacity: 1;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(134, 218, 138, 0.4);
}

/* 댓글 섹션 스타일 업데이트 */
.comments-section {
  background: none;
  padding: 30px;
}

.comments-section h3 {
  color: #056800;
  margin-bottom: 20px;
}

.comment-textarea {
  width: 100%;
  min-height: 100px;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
  resize: vertical;
  background-color: rgba(255, 255, 255, 0.4);

}

.comment-item {
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.comment-info {
  margin-bottom: 10px;
}

.comment-author {
  font-weight: bold;
  color: #056800;
}

.comment-content {
  margin: 10px 0;
  line-height: 1.6;
}

.comment-date {
  color: #666;
  font-size: 0.9em;
  margin-bottom: 10px;
}

/* 작은 버튼 스타일 */
.btn-edit-sm, .btn-delete-sm, .btn-close-sm {
  padding: 6px 12px;
  border-radius: 15px;
  font-size: 0.9em;
}

.comment-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.author-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>
