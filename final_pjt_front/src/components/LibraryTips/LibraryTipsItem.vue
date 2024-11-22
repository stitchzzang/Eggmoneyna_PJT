<template>
  <li class="post-item" @click="handleClick">
    <div class="post-content">
      <h3 class="post-title">{{ post.title }}</h3>
      <p class="post-summary">{{ post.summary }}</p>
      <div class="post-meta">
        <small class="author">작성자: {{ post.author }}</small>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  props: ['post'],
  methods: {
    handleClick() {
      this.$emit('select', this.post.id);
    },
  },
};
</script>

<style scoped>
.post-item {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.post-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.post-title {
  margin: 0 0 10px 0;
  color: #333;
}

.post-summary {
  color: #666;
  margin: 0 0 15px 0;
  line-height: 1.5;
}

.post-meta {
  color: #888;
  font-size: 0.9em;
}
</style>
