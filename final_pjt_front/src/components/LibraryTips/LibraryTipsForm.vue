<template>
  <div class="form-container">
    <h1 class="form-title">{{ isEdit ? '게시글 수정' : '새 게시글 작성' }}</h1>
    <form @submit.prevent="handleSubmit" class="post-form">
      <div class="form-group">
        <input 
          v-model="form.title" 
          placeholder="제목" 
          required 
          class="form-input"
        />
      </div>
      <div class="form-group">
        <textarea 
          v-model="form.content" 
          placeholder="내용" 
          required 
          class="form-textarea"
        ></textarea>
      </div>
      <button type="submit" class="submit-btn">저장</button>
    </form>
  </div>
</template>

<script>
export default {
  props: ['initialData'],
  data() {
    return {
      form: this.initialData || { title: '', content: '' },
    };
  },
  computed: {
    isEdit() {
      return !!this.initialData;
    },
  },
  methods: {
    async handleSubmit() {
      if (this.isEdit) {
        // 수정
        await fetch(`/api/posts/${this.initialData.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.form),
        });
      } else {
        // 새 글 작성
        await fetch('/api/posts', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(this.form),
        });
      }
      this.$router.push('/community');
    },
  },
};
</script>

<style scoped>
.form-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.form-title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.post-form {
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-textarea {
  min-height: 200px;
  resize: vertical;
}

.submit-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #218838;
}
</style>
