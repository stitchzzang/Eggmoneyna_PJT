<template>
  <div class="comments-section">
    <!-- 댓글 목록 -->
    <div v-for="comment in comments" :key="comment.id" class="comment">
      <p>{{ comment.content }}</p>
      <small>작성자: {{ comment.user }}</small>
      <div class="comment-actions" v-if="isCurrentUser(comment.user)">
        <button @click="editComment(comment)">수정</button>
        <button @click="deleteComment(comment.id)">삭제</button>
      </div>
    </div>
    
    <!-- 댓글 작성 폼 -->
    <div class="comment-form">
      <textarea v-model="newComment" placeholder="댓글을 작성하세요"></textarea>
      <button @click="submitComment">댓글 작성</button>
    </div>
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>