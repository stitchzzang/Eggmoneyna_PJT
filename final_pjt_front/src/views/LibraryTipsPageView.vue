<template>
  <div class="community-container">
    <!-- 게시글 목록 표시 (기본 화면) -->
    <CommunityList 
      v-if="!isWriting && !selectedPost"
      :posts="posts"
      @select-post="showPostDetail"
    />

    <!-- 글쓰기 버튼 (목록 화면에서만 표시) -->
    <div v-if="!isWriting && !selectedPost" class="write-button-container">
      <button v-if="authStore.isAuthenticated" @click="showWriteForm" class="write-button">
        글쓰기
      </button>
    </div>

    <!-- 글쓰기 폼 -->
    <CommunityWriteForm 
      v-if="isWriting"
      @submit="createPost"
      @cancel="cancelWriting"
    />

    <!-- 게시글 상세 보기 -->
    <CommunityDetail
      v-if="selectedPost"
      :post="selectedPost"
      @close="closePostDetail"
      @delete="showDeleteConfirm"
    />

    <!-- 삭제 확인 모달 -->
    <CommunityDeleteModal
      v-if="showDeleteModal"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import CommunityList from '@/components/Community/CommunityList.vue'
import CommunityWriteForm from '@/components/Community/CommunityWriteForm.vue'
import CommunityDetail from '@/components/Community/CommunityDetail.vue'
import CommunityDeleteModal from '@/components/Community/CommunityDeleteModal.vue'
import axios from 'axios'

const authStore = useAuthStore()
const router = useRouter()
const posts = ref([])
const isWriting = ref(false)
const selectedPost = ref(null)
const showDeleteModal = ref(false)
const postToDelete = ref(null)

// 게시글 목록 조회
const fetchPosts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/posts/', {
      headers: {
        'Authorization': `Token ${authStore.token}`
      }
    })
    console.log('게시글 목록:', response.data)  // 디버깅용
    posts.value = response.data
  } catch (error) {
    console.error('게시글 조회 실패:', error)
    if (error.response) {
      console.error('서버 응답:', error.response.data)
    }
  }
}

// 글쓰기 폼 표시
const showWriteForm = () => {
  if (!authStore.isAuthenticated) {
    localStorage.setItem('redirectPath', router.currentRoute.value.fullPath)
    router.push('/login')
    return
  }
  isWriting.value = true
}

// 글쓰기 취소
const cancelWriting = () => {
  isWriting.value = false
}

// 게시글 작성
const createPost = async (postData) => {
  try {
    // 인증 토큰 추가
    const config = {
      headers: {
        'Authorization': `Token ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    }
    
    console.log('전송할 데이터:', postData)  // 디버깅용
    
    const response = await axios.post(
      'http://127.0.0.1:8000/api/v1/posts/', 
      postData,
      config
    )
    
    console.log('응답:', response.data)  // 디버깅용
    
    posts.value.unshift(response.data)
    isWriting.value = false
  } catch (error) {
    console.error('게시글 작성 실패:', error.response?.data || error)
    if (error.response?.status === 401) {
      alert('로그인이 필요합니다.')
      router.push('/login')
    } else {
      alert('게시글 작성에 실패했습니다.')
    }
  }
}

// 게시글 상세 보기
const showPostDetail = (post) => {
  selectedPost.value = post
}

// 게시글 상세 닫기
const closePostDetail = () => {
  selectedPost.value = null
}

// 삭제 모달 표시
const showDeleteConfirm = (post) => {
  postToDelete.value = post
  showDeleteModal.value = true
}

// 게시글 삭제 확인
const confirmDelete = async () => {
  if (postToDelete.value) {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/v1/posts/${postToDelete.value.id}/`)
      posts.value = posts.value.filter(p => p.id !== postToDelete.value.id)
      showDeleteModal.value = false
      postToDelete.value = null
      selectedPost.value = null
    } catch (error) {
      console.error('게시글 삭제 실패:', error)
    }
  }
}

// 삭제 취소
const cancelDelete = () => {
  showDeleteModal.value = false
  postToDelete.value = null
}

onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.community-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.write-button-container {
  text-align: right;
  margin: 20px 0;
}

.write-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.write-button:hover {
  background-color: #45a049;
}
</style>