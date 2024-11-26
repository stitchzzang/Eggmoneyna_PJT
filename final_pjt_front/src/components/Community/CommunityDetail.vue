<template>
  <div class="community-detail">
    <!-- 게시글 상세 정보 -->
    <div v-if="thread" class="detail-container">
      <div v-if="!isEditing" class="detail-content">
        <div class="detail-header">
          <h2>{{ thread.title }}</h2>
          <div class="post-info">
            <span>
              {{ thread.member_type === 'regular' ? '🐣 ' : '☑️ ' }}
              {{ thread.name }}
            </span>
            <span>작성일: {{ formatDate(thread.created_at) }}</span>
            <span>수정일: {{ formatDate(thread.updated_at) }}</span>
          </div>
        </div>
        
        <div class="post-content">
          {{ thread.content }}
        </div>
        
        <div class="action-row">
          <div class="like-section">
            <div class="like-container">
              <input type="checkbox" id="checkbox" v-model="thread.is_liked" @change="toggleLike" />
              <label for="checkbox" class="heart-label">
                <svg id="heart-svg" viewBox="467 392 58 57" xmlns="http://www.w3.org/2000/svg">
                  <g id="Group" fill="none" fill-rule="evenodd" transform="translate(467 392)">
                    <path d="M29.144 20.773c-.063-.13-4.227-8.67-11.44-2.59C7.63 28.795 28.94 43.256 29.143 43.394c.204-.138 21.513-14.6 11.44-25.213-7.214-6.08-11.377 2.46-11.44 2.59z" 
                          id="heart" fill="#AAB8C2"/>
                    <circle id="main-circ" fill="#E2264D" opacity="0" cx="29.5" cy="29.5" r="1.5"/>
                    <g id="grp7" opacity="0" transform="translate(7 6)">
                      <circle id="oval1" fill="#9CD8C3" cx="2" cy="6" r="2"/>
                      <circle id="oval2" fill="#8CE8C3" cx="5" cy="2" r="2"/>
                    </g>
                    <!-- grp2~grp6도 동일한 패턴으로 추가 -->
                  </g>
                </svg>
              </label>
              <span class="like-text">{{ thread.like_count }}</span>
            </div>
          </div>
          
          <div v-if="isAuthor" class="author-buttons">
            <button @click="startEditing" class="btn-edit">수정</button>
            <button @click="deleteThread" class="btn-delete">삭제</button>
          </div>
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
              <span class="comment-author">
                {{ comment.member_type === 'regular' ? '🐣 ' : '☑️ ' }}
                {{ comment.name }}
                <span v-if="comment.username === thread.username" class="author-tag">(작성자)</span>
              </span>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
            <div class="comment-date">{{ formatDate(comment.created_at) }}</div>
            <!-- <div>{{ comment.username }} - {{ auth.userInfo.username }}</div> -->
            <div v-if="comment.username === auth.userInfo.username" class="comment-buttons">
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
    console.log(res.data)
    thread.value = {
      ...res.data,
      is_liked: res.data.is_liked || false,
      like_count: res.data.like_count || 0
    }
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
  return thread.value?.username === auth.userInfo.username
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

const toggleLike = async () => {
  try {
    const response = await axios({
      method: 'post',
      url: `${store.API_URL}/community/${route.params.id}/like/`,
      headers: {
        Authorization: `Token ${auth.token}`
      }
    })
    
    // 스레드 정보 업데이트
    thread.value = {
      ...thread.value,
      is_liked: response.data.is_liked,
      like_count: response.data.like_count
    }
  } catch (err) {
    console.log('좋아요 처리 중 오가 발생했습니다:', err)
  }
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
  background-color: rgba(255, 255, 255, 0.4);
  border-radius: 15px;
  padding: 20px;
  margin: 20px;
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
}

.author-tag {
  color: #047404;
  font-size: 0.9em;
  margin-left: 5px;
}

.like-section {
  margin: 0;
}

.like-container {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #f8f9fab6;
  border-radius: 10px;
  padding: 8px 16px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.like-text {
  font-size: 18px;
  margin-right: 10px;
}

.heart-label {
  display: flex;
  align-items: center;
}

#checkbox {
  display: none;
}

svg {
  cursor: pointer;
  overflow: visible;
  width: 45px;
  height: 45px;
  vertical-align: middle;
}

svg #heart {
  transform-origin: center;
  animation: animateHeartOut .3s linear forwards;
}

svg #main-circ {
  transform-origin: 29.5px 29.5px;
}

#checkbox:checked + label svg #heart {
  transform: scale(.2);
  fill: #E2264D;
  animation: animateHeart .3s linear forwards .25s;
}

#checkbox:checked + label svg #main-circ {
  transition: all 2s;
  animation: animateCircle .3s linear forwards;
  opacity: 1;
}

/* 애니메이션 키프레임 추가 */
@keyframes animateCircle {
  40% {
    transform: scale(10);
    opacity: 1;
    fill: #DD4688;
  }
  55% {
    transform: scale(11);
    opacity: 1;
    fill: #D46ABF;
  }
  65% {
    transform: scale(12);
    opacity: 1;
    fill: #CC8EF5;
  }
  75% {
    transform: scale(13);
    opacity: 1;
    fill: transparent;
    stroke: #CC8EF5;
    stroke-width: .5;
  }
  85% {
    transform: scale(17);
    opacity: 1;
    fill: transparent;
    stroke: #CC8EF5;
    stroke-width: .2;
  }
  95% {
    transform: scale(18);
    opacity: 1;
    fill: transparent;
    stroke: #CC8EF5;
    stroke-width: .1;
  }
  100% {
    transform: scale(19);
    opacity: 1;
    fill: transparent;
    stroke: #CC8EF5;
    stroke-width: 0;
  }
}

@keyframes animateHeart {
  0% {
    transform: scale(.2);
  }
  40% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes animateHeartOut {
  0% {
    transform: scale(1.4);
  }
  100% {
    transform: scale(1);
  }
}

.edit-form {
  width: 100%;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.4);
  border-radius: 8px;
}

.edit-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1.2em;
  background-color: rgba(255, 255, 255, 0.8);
}

.edit-textarea {
  width: 100%;
  min-height: 300px;
  padding: 15px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-size: 1em;
  line-height: 1.6;
  background-color: rgba(255, 255, 255, 0.8);
}

.button-group {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* 저장, 취소 버튼 완전히 동일한 스타일 */
.button-group .btn-edit,
.button-group .btn-close {
  width: 100px !important;
  height: 40px !important;
  padding: 0 !important;
  margin: 0 !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  font-size: 16px !important;
  font-weight: bold !important;
  border-radius: 5px !important;
  cursor: pointer !important;
  transition: all 0.3s ease !important;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
  border: none !important;
  color: white !important;
}

/* 저장 버튼 색상 */
.button-group .btn-edit {
  background: linear-gradient(45deg, #86da8a, #047404) !important;
  border: 2px solid #128004 !important;
}

/* 취소 버튼 색상 - 회색 계열 */
.button-group .btn-close {
  background: linear-gradient(45deg, #8f9296, #495057) !important;
  border: px solid #495057 !important;
}

/* 호버 효과 */
.button-group .btn-edit:hover,
.button-group .btn-close:hover {
  transform: translateY(-2px) !important;
  opacity: 0.9 !important;
}

.like-text {
  font-size: 16px;
  color: #495057;
  font-weight: 500;
  line-height: 1;
  vertical-align: middle;
}

.action-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
}

</style>
