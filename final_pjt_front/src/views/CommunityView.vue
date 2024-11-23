<template>
  <div class="community-view">
    <h1 class="page-title">📝 커뮤니티</h1>
    
    <!-- 로그인하지 않은 사용자를 위한 메시지 추가 -->
    <div v-if="!authStore.isAuthenticated" class="login-message">
      로그인 후 사용 가능합니다.
    </div>

    <!-- 로그인한 사용자에게만 커뮤니티 컨테이너 표시 -->
    <div v-else class="community-container">
      <!-- 글쓰기 버튼 (인증된 사용자만 표시) -->
      <div v-if="!isWriting && !selectedPost" class="write-button-container">
        <RouterLink :to="{ name: 'community-write' }" class="write-button">
          글쓰기
        </RouterLink>
      </div>

      <!-- 게시글 목록 -->
      <CommunityList 
        :threads="paginatedThreads"
      />

      <!-- 페이지네이션 -->
      <div class="pagination">
        <button 
          :disabled="currentPage === 1"
          @click="currentPage--"
          class="page-btn"
        >
          이전
        </button>
        
        <div class="page-numbers">
          <button 
            v-for="page in displayedPages" 
            :key="page"
            @click="currentPage = page"
            :class="['page-number', { active: currentPage === page }]"
          >
            {{ page }}
          </button>
        </div>
        
        <button 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
          class="page-btn"
        >
          다음
        </button>
      </div>

      <!-- 나머지 컴포넌트들 -->
      <CommunityWriteForm 
        v-if="isWriting"
        @submit="createPost"
        @cancel="cancelWriting"
      />

      <CommunityDetail
        v-if="selectedPost"
        :post="selectedPost"
        @close="closePostDetail"
        @delete="showDeleteConfirm"
      />

      <CommunityDeleteModal
        v-if="showDeleteModal"
        @confirm="confirmDelete"
        @cancel="cancelDelete"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import { RouterLink } from 'vue-router' 
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
const store = useCounterStore()
const currentPage = ref(1)
const itemsPerPage = 10

// 게시글 목록 조회
onMounted(() => {
  store.getThreads() 
})

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

// 페이지네이션된 게시글 목록
const paginatedThreads = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return store.threads.slice(start, end)
})

// 전체 페이지 수 계산
const totalPages = computed(() => {
  return Math.ceil(store.threads.length / itemsPerPage)
})

// 표시할 페이지 번호 계산
const displayedPages = computed(() => {
  const range = 2
  let start = Math.max(currentPage.value - range, 1)
  let end = Math.min(currentPage.value + range, totalPages.value)

  const pages = []
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
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
  text-decoration: none;
  padding: 8px 18px;
  background: linear-gradient(45deg, #86da8a, #047404) !important;
  color: white;
  border: 2px solid #1d8a0e;
  border-radius: 25px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.write-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
}

.community-view {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  margin: 20px auto;
}

.page-title {
  text-align: center;
  margin-bottom: 20px;
  color: #056800;
  font-weight: 600;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 30px 0;
  gap: 10px;
}

.page-numbers {
  display: flex;
  gap: 5px;
}

.page-btn, .page-number {
  padding: 8px 12px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  border-radius: 4px;
  min-width: 40px;
}

.page-btn:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
  color: #999;
}

.page-number.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.page-btn:not(:disabled):hover,
.page-number:not(.active):hover {
  background-color: #f0f0f0;
}

/* 로그인 메시지 스타일 추가 */
.login-message {
  text-align: center;
  padding: 20px;
  /* background-color: #f8f9fa; */
  /* border: 1px solid #ddd; */
  /* border-radius: 8px; */
  margin: 250px auto;
  color: #666;
  font-size: 1.2em;
}

</style>