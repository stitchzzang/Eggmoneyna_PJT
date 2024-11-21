<template>
  <div class="post-item" @click="$emit('select')">
    <h3 class="post-title">{{ post.title }}</h3>
    <div class="post-info">
      <span class="author">{{ post.author }}</span>
      <span class="date">{{ formatDate(post.created_at) }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  post: {
    type: Object,
    required: true
  }
})

defineEmits(['select'])

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ko-KR')
}
</script>

<style scoped>
.post-item {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.post-item:hover {
  background-color: #f8f9fa;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.post-title {
  margin: 0 0 8px 0;
  font-size: 1.1em;
}

.post-info {
  display: flex;
  gap: 15px;
  font-size: 0.9em;
  color: #666;
}

.author {
  font-weight: 500;
}

.date {
  color: #888;
}
</style>
