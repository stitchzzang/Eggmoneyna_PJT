<template>
  <div class="community-detail">
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
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
})

defineEmits(['close', 'edit', 'delete'])

const auth = useAuthStore()
const isAuthor = computed(() => auth.user === props.post.author)

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ko-KR')
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
</style>
