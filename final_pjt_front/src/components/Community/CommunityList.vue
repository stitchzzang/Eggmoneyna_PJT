<template>
  <div class="community-list">
    <CommunityItem 
      v-for="thread in store.threads" 
      :key="thread.id" 
      :thread="thread"
    />
</div>
</template>

<script setup>
import CommunityItem from '@/components/Community/CommunityItem.vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()

defineProps({
  thread: {
    type: Object,
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
