<template>
  <div class="community-container">
    <div class="community-content">
      <!-- 글쓰기 버튼 -->
      <div class="write-button-container" v-if="isLoggedIn">
        <button @click="showCreateForm" class="write-button">
          글쓰기
        </button>
      </div>

      <!-- 게시글 작성 폼 -->
      <div v-if="isCreating" class="create-form">
        <h3>새 글 작성</h3>
        <input 
          v-model="newPost.title" 
          type="text" 
          placeholder="제목을 입력하세요"
          class="input-title"
        >
        <textarea 
          v-model="newPost.content" 
          placeholder="내용을 입력하세요"
          class="input-content"
        ></textarea>
        <div class="button-group">
          <button @click="submitPost" class="submit-btn">등록</button>
          <button @click="cancelCreate" class="cancel-btn">취소</button>
        </div>
      </div>

      <!-- 게시글 목록 -->
      <CommunityList 
        :posts="posts" 
        @select-post="showPostDetail"
      />

      <!-- 게시글 상세 모달 -->
      <div v-if="selectedPost" class="post-modal">
        <div class="modal-content">
          <h3>{{ selectedPost.title }}</h3>
          <p>{{ selectedPost.content }}</p>
          <div class="comments-section">
            <!-- 댓글 목록 -->
            <div class="comments-list">
              <div v-for="comment in selectedPost.comments" :key="comment.id" class="comment">
                <p>{{ comment.content }}</p>
                <small>{{ comment.author }} - {{ formatDate(comment.createdAt) }}</small>
              </div>
            </div>
            <!-- 댓글 입력 -->
            <div class="comment-form" v-if="isLoggedIn">
              <textarea 
                v-model="newComment" 
                placeholder="댓글을 입력하세요"
              ></textarea>
              <button @click="submitComment">댓글 작성</button>
            </div>
          </div>
          <button @click="closePostDetail" class="close-btn">닫기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import CommunityList from '@/components/Community/CommunityList.vue'

// Vuex 대신 localStorage 사용
const isLoggedIn = computed(() => {
  return !!localStorage.getItem('token')  // 또는 실제 사용하는 토큰 키
})

// 게시글 관련 상태
const posts = ref([])
const isCreating = ref(false)
const selectedPost = ref(null)
const newPost = ref({ title: '', content: '' })
const newComment = ref('')

// 게시글 작성 관련 메서드
const showCreateForm = () => {
  isCreating.value = true
}

const cancelCreate = () => {
  isCreating.value = false
  newPost.value = { title: '', content: '' }
}

const submitPost = async () => {
  try {
    // API 호출 로직
    const response = await fetch('/api/posts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newPost.value)
    })
    const data = await response.json()
    posts.value.unshift(data)
    isCreating.value = false
    newPost.value = { title: '', content: '' }
  } catch (error) {
    console.error('게시글 작성 실패:', error)
  }
}

// 게시글 상세 관련 메서드
const showPostDetail = (post) => {
  selectedPost.value = post
}

const closePostDetail = () => {
  selectedPost.value = null
}

// 댓글 관련 메서드
const submitComment = async () => {
  try {
    // API 호출 로직
    const response = await fetch(`/api/posts/${selectedPost.value.id}/comments`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content: newComment.value })
    })
    const data = await response.json()
    selectedPost.value.comments.push(data)
    newComment.value = ''
  } catch (error) {
    console.error('댓글 작성 실패:', error)
  }
}

// 유틸리티 함수
const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ko-KR')
}
</script>

<style scoped>
.community-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;

  h1 {
    color: #056800;
    margin-bottom: 30px;
  }

  .write-button-container {
    text-align: right;
    margin-bottom: 20px;
  }

  .write-button {
    background-color: #056800;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;

    &:hover {
      background-color: darken(#056800, 10%);
    }
  }

  .create-form {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 20px;

    .input-title {
      width: 100%;
      padding: 8px;
      margin-bottom: 10px;
      border: 1px solid #ddd;
      border-radius: 4px;
    }

    .input-content {
      width: 100%;
      height: 200px;
      padding: 8px;
      margin-bottom: 10px;
      border: 1px solid #ddd;
      border-radius: 4px;
      resize: vertical;
    }

    .button-group {
      display: flex;
      gap: 10px;
      justify-content: flex-end;

      button {
        padding: 8px 16px;
        border: none;
        border-radius: 4px;
        cursor: pointer;

        &.submit-btn {
          background-color: #056800;
          color: white;
        }

        &.cancel-btn {
          background-color: #666;
          color: white;
        }
      }
    }
  }

  .post-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;

    .modal-content {
      background-color: white;
      padding: 20px;
      border-radius: 8px;
      width: 80%;
      max-width: 800px;
      max-height: 80vh;
      overflow-y: auto;

      .comments-section {
        margin-top: 20px;
        border-top: 1px solid #ddd;
        padding-top: 20px;

        .comment {
          margin-bottom: 10px;
          padding: 10px;
          background-color: #f8f9fa;
          border-radius: 4px;
        }

        .comment-form {
          margin-top: 20px;

          textarea {
            width: 100%;
            height: 100px;
            margin-bottom: 10px;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            resize: vertical;
          }

          button {
            background-color: #056800;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
          }
        }
      }
    }
  }
}
</style>