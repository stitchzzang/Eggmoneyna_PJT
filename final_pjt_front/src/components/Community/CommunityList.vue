<template>
  <div class="container">
    <div class="list-wrapper">
      <div class="column-headers">
        <div class="list-row">
          <div class="column id">말머리</div>
          <div class="column title">제목</div>
          <div class="column author">작성자</div>
          <div class="column date">작성일</div>
          <div class="column likes">좋아요</div>
        </div>
        <hr class="header-divider">
      </div>

      <!-- 게시글 목록 -->
      <CommunityItem
        v-for="thread in threads"
        :key="thread.id"
        :thread="thread"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CommunityItem from './CommunityItem.vue'

// props만 정의
const props = defineProps({
  threads: {
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
.container {
  width: 100%;
  margin: 0 auto;
}

.list-wrapper {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 20px;
}

.list-row {
  display: flex;
  align-items: center;
  padding: 10px 0;
  font-weight: bold;
}

.column {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.id {
  flex: 0 0 100px;
  text-align: center;
  margin-left: 8px;
}

.title {
  flex: 0 0 400px;
  text-align: center;
  padding: 0 20px;
}

.author {
  flex: 0 0 120px;
  text-align: center;
}

.date {
  flex: 0 0 120px;
  text-align: center;
}

.likes {
  flex: 0 0 100px;
  text-align: center;
}

.header-divider {
  border: none;
  height: 1px;
  background-color: #ddd;
  margin: 0;
}
</style>
