<template>
  <div class="list-container">
    <div class="list-header">
      <h1 class="list-title">알쓸금잡</h1>
      <button 
        v-if="isLoggedIn" 
        @click="$router.push('/news/create')" 
        class="create-btn"
      >
        글쓰기
      </button>
      <button 
        v-else 
        @click="handleUnauthorized" 
        class="login-required-btn"
      >
        글쓰기
      </button>
    </div>

    <ul class="post-list" v-if="posts.length">
      <NewsTipsItem
        v-for="post in posts"
        :key="post.id"
        :post="post"
        @select="goToDetail"
      />
    </ul>
    
    <div v-else class="no-posts">
      게시글이 없습니다.
    </div>
  </div>
</template>

<script>
import NewsTipsItem from './LibraryTipsItem.vue'

export default {
  components: {
    NewsTipsItem
  },
  data() {
    return {
      posts: [],
      isLoggedIn: false // Vuex store에서 관리하는 것이 좋습니다
    }
  },
  methods: {
    async fetchPosts() {
      try {
        const response = await fetch('/api/posts')
        this.posts = await response.json()
      } catch (error) {
        console.error('게시글을 불러오는데 실패했습니다:', error)
      }
    },
    goToDetail(postId) {
      this.$router.push(`/news/detail/${postId}`)
    },
    handleUnauthorized() {
      alert('로그인이 필요한 서비스입니다.')
      this.$router.push('/login')
    }
  },
  mounted() {
    this.fetchPosts()
    // Vuex store에서 로그인 상태를 가져오는 것이 좋습니다
    this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
  }
}
</script>

<style scoped>
.list-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.list-title {
  margin: 0;
  color: #333;
}

.create-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.create-btn:hover {
  background-color: #218838;
}

.login-required-btn {
  background-color: #0d6d00;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-required-btn:hover {
  background-color: #145202;
}

.post-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.no-posts {
  text-align: center;
  color: #666;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
