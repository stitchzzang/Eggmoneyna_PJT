<template>
  <div class="community-list">
    <div v-for="post in posts" 
         :key="post.id" 
         class="post-item"
         @click="$emit('select-post', post)">
      <h3>{{ post.title }}</h3>
      <div class="post-info">
        <span>작성자: {{ post.author }}</span>
        <span>작성일: {{ formatDate(post.created_at) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  posts: {
    type: Array,
    required: true
  }
})

defineEmits(['select-post'])

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ko-KR')
}
</script>

<style scoped>
.community-list {
  margin-top: 20px;
}

.post-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.post-item:hover {
  background-color: #f5f5f5;
}

.post-info {
  display: flex;
  gap: 20px;
  color: #666;
  font-size: 0.9em;
  margin-top: 8px;
}
</style>
