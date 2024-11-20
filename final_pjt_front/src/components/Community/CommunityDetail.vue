<template>
  <div v-if="post" class="detail-container">
    <div class="post-header">
      <h1 class="post-title">{{ post.title }}</h1>
      <small class="post-author">작성자: {{ post.author }}</small>
    </div>
    
    <div class="post-content">
      <p>{{ post.content }}</p>
    </div>

    <div class="action-buttons">
      <button @click="goToEdit" class="edit-btn">수정</button>
      <button @click="openDeleteModal" class="delete-btn">삭제</button>
    </div>

    <CommunityDeleteModal
      v-if="showDeleteModal"
      @confirm="deletePost"
      @cancel="closeDeleteModal"
    />
  </div>
</template>

<script>
import CommunityDeleteModal from './CommunityDeleteModal.vue';

export default {
  components: { CommunityDeleteModal },
  data() {
    return {
      post: null,
      showDeleteModal: false,
    };
  },
  methods: {
    async fetchPost() {
      const response = await fetch(`/api/posts/${this.$route.params.id}`);
      this.post = await response.json();
    },
    goToEdit() {
      this.$router.push(`/community/${this.post.id}/edit`);
    },
    openDeleteModal() {
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
    },
    async deletePost() {
      await fetch(`/api/posts/${this.post.id}`, { method: 'DELETE' });
      this.$router.push('/community');
    },
  },
  mounted() {
    this.fetchPost();
  },
};
</script>

<style scoped>
.detail-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.post-header {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.post-title {
  margin: 0 0 10px 0;
  color: #333;
}

.post-author {
  color: #666;
}

.post-content {
  line-height: 1.6;
  color: #444;
  margin-bottom: 30px;
}

.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.edit-btn, .delete-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-btn {
  background-color: #007bff;
  color: white;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.edit-btn:hover {
  background-color: #0056b3;
}

.delete-btn:hover {
  background-color: #c82333;
}
</style>
