<template>
  <div>
    <!-- 게시글 내용 -->
    <div class="post-item">
      <div class="post-id">{{ index }}</div>
      <div class="post-title">
        <RouterLink 
          :to="{ name: 'community-detail', params: { id: thread.id } }"
          class="title-link">
          {{ thread.title }} 
          <span class="comments-count">
            ({{ thread.comment_count || 0 }})
          </span>
        </RouterLink>
      </div>
      <div class="post-author">
        {{ thread.member_type === 'regular' ? '🐣 ' : '☑️ ' }}
        {{ thread.name }}
      </div>
      <div class="post-date">{{ formatDate(thread.created_at) }}</div>
      <div class="post-likes">
        <i class="fas fa-heart"></i> {{ thread.likes_count }}
      </div>
      <hr>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({
  thread: {  
    type: Object,
    required: true
  },
  index: {    // 새로운 prop 추가
    type: Number,
    required: true
  }
})

defineEmits(['select'])

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ko-KR')
}
</script>
<style scoped>
/* 공통 레이아웃 */
.post-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  width: 100%;
  justify-content: center;
  margin: 0 auto;
  max-width: 900px;
}

/* 컬럼 너비 설정 */
.post-id {
  flex: 0 0 100px;  /* 고정 너비 */
  text-align: center;
}

.post-title {
  flex: 0 0 400px;  /* 고정 너비 */
  padding: 0 20px;
}

.post-author {
  flex: 0 0 120px;  /* 고정 너비 */
  text-align: center;
}

.post-date {
  flex: 0 0 120px;  /* 고정 너비 */
  text-align: center;
}

.post-likes {
  flex: 0 0 100px;  /* 고정 너비 */
  text-align: center;
}

/* 게시글 스타일 */
.post-item {
  border-bottom: 1px solid #e0e0e0;
}

.title-link {
  text-decoration: none;
  color: #333;
}

.title-link:hover {
  color: #007bff;
  text-decoration: underline;
}

.post-id {
  color: #666;
  font-size: 0.9em;
}

.post-author {
  color: #555;
  font-size: 0.9em;
}

.post-date {
  color: #888;
  font-size: 0.9em;
}

.post-likes {
  color: #888;
  font-size: 0.9em;
}

.comments-count {
  color: #666;
  font-size: 0.9em;
  margin-left: 5px;
}
</style>

