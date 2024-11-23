<template>
  <div class="comments-section">
    <!-- 댓글 작성 폼 -->
    <div class="comment-form">
      <textarea 
        v-model="newComment" 
        placeholder="댓글을 작성하세요"
        class="form-control"
      ></textarea>
      <button 
        @click="submitComment"
        class="btn btn-primary mt-2"
      >
        댓글 작성
      </button>
    </div>

    <!-- 댓글 목록 -->
    <div class="comment-list mt-4">
      <div v-for="comment in comments" :key="comment.id" class="comment-item mb-3">
        <div class="comment-content">
          <p class="mb-1">{{ comment.content }}</p>
          <div class="comment-info">
            <small class="text-muted">작성자: {{ comment.user }}</small>
          </div>
        </div>
        <div v-if="isCurrentUser(comment.user)" class="comment-actions mt-2">
          <button 
            v-if="editingCommentId !== comment.id" 
            @click="startEdit(comment)"
            class="btn btn-sm btn-outline-primary me-2"
          >
            수정
          </button>
          <button 
            @click="removeComment(comment.id)"
            class="btn btn-sm btn-outline-danger"
          >
            삭제
          </button>
        </div>
        <!-- 댓글 수정 폼 -->
        <div v-if="editingCommentId === comment.id" class="edit-form mt-2">
          <textarea 
            v-model="editContent" 
            class="form-control"
          ></textarea>
          <div class="mt-2">
            <button 
              @click="saveEdit(comment.id)"
              class="btn btn-sm btn-success me-2"
            >
              저장
            </button>
            <button 
              @click="cancelEdit"
              class="btn btn-sm btn-secondary"
            >
              취소
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useStore } from 'vuex'
import { getComments, createComment, updateComment, deleteComment } from '@/stores/community'

export default {
  name: 'CommentList',
  props: {
    threadId: {
      type: [String, Number],
      required: true
    }
  },
  setup(props) {
    const store = useStore()
    const comments = ref([])
    const newComment = ref('')
    const editingCommentId = ref(null)
    const editContent = ref('')

    const fetchComments = async () => {
      try {
        const response = await getComments(props.threadId)
        comments.value = response.data
      } catch (error) {
        console.error('댓글 불러오기 실패:', error)
      }
    }

    const submitComment = async () => {
      if (!newComment.value.trim()) return
      
      try {
        await createComment(props.threadId, newComment.value)
        newComment.value = ''
        await fetchComments()
      } catch (error) {
        console.error('댓글 작성 실패:', error)
      }
    }

    const removeComment = async (commentId) => {
      if (!confirm('정말 삭제하시겠습니까?')) return
      
      try {
        await deleteComment(props.threadId, commentId)
        await fetchComments()
      } catch (error) {
        console.error('댓글 삭제 실패:', error)
      }
    }

    const startEdit = (comment) => {
      editingCommentId.value = comment.id
      editContent.value = comment.content
    }

    const saveEdit = async (commentId) => {
      if (!editContent.value.trim()) return
      
      try {
        await updateComment(props.threadId, commentId, editContent.value)
        editingCommentId.value = null
        await fetchComments()
      } catch (error) {
        console.error('댓글 수정 실패:', error)
      }
    }

    const cancelEdit = () => {
      editingCommentId.value = null
      editContent.value = ''
    }

    const isCurrentUser = (commentUser) => {
      return store.state.user?.username === commentUser
    }

    onMounted(() => {
      fetchComments()
    })

    return {
      comments,
      newComment,
      editingCommentId,
      editContent,
      submitComment,
      removeComment,
      startEdit,
      saveEdit,
      cancelEdit,
      isCurrentUser
    }
  }
}
</script>

<style scoped>
.comments-section {
  margin-top: 2rem;
  padding: 1rem;
}

.comment-form textarea {
  width: 100%;
  min-height: 80px;
}

.comment-item {
  border-bottom: 1px solid #eee;
  padding: 1rem 0;
}

.comment-actions {
  display: flex;
  gap: 0.5rem;
}

.edit-form textarea {
  width: 100%;
  min-height: 60px;
}
</style>