<template>
  <div>
    <!-- 컬럼 헤더 -->
    <div class="column-headers" v-if="thread.id === 1">
      <div class="header-row">
        <div class="header-id">말머리</div>
        <div class="header-title">제목</div>
        <div class="header-author">작성자</div>
        <div class="header-date">작성일</div>
        <div class="header-likes">좋아요</div>
      </div>
      <hr class="header-divider">
    </div>

    <!-- 게시글 내용 -->
    <div class="post-item">
      <div class="post-id">{{ thread.id }}</div>
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
      <div class="post-author">{{ thread.username }}</div>
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
  }
})

defineEmits(['select'])

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('ko-KR')
}
</script>

<style scoped>
/* 공통 레이아웃 */
.header-row, .post-item {
  display: flex;
  align-items: center;
  padding: 10px 0;
  width: 100%;
  justify-content: center;
  margin: 0 auto;
  max-width: 900px;
}

/* 컬럼 너비 설정 */
.header-id, .post-id {
  flex: 0 0 100px;  /* 고정 너비 */
  text-align: center;
}

.header-title, .post-title {
  flex: 0 0 400px;  /* 고정 너비 */
  padding: 0 20px;
}

.header-author, .post-author {
  flex: 0 0 120px;  /* 고정 너비 */
  text-align: center;
}

.header-date, .post-date {
  flex: 0 0 120px;  /* 고정 너비 */
  text-align: center;
}

.header-likes, .post-likes {
  flex: 0 0 100px;  /* 고정 너비 */
  text-align: center;
}

/* 헤더 스타일 */
.column-headers {
  margin-bottom: 10px;
  max-width: 900px;  /* 컬럼 헤더와 동일한 너비 */
  margin: 0 auto;    /* 중앙 정렬 */
}

.header-row {
  font-weight: bold;
  color: #333;
}

.header-divider {
  border: none;
  height: 2px;
  background-color: #333;
  margin: 0 auto;    /* 중앙 정렬 */
  max-width: 900px;  /* 컬럼 헤더와 동일한 너비 */
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
  color: #ff4757;
  font-size: 0.9em;
}

.comments-count {
  color: #666;
  font-size: 0.9em;
  margin-left: 5px;
}
</style>
