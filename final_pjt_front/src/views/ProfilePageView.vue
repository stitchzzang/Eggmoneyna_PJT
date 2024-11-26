<template>
  <div class="profile-container">
    <!-- 좌측 메뉴 -->
    <div class="sidebar">
      <div class="menu-item" :class="{ active: store.currentView === 'edit' }" @click="store.currentView = 'edit'">
        회원정보 조회/수정
      </div>
      <div class="financial-category">
        <div class="category-title">금융 서비스</div>
        <div class="menu-item" :class="{ active: store.currentView === 'products' }" @click="store.currentView = 'products'">
          가입한 상품 보기
        </div>
        <div class="menu-item" :class="{ active: store.currentView === 'test' }" @click="store.currentView = 'test'">
          금융 성향 테스트
        </div>
        <div class="menu-item" :class="{ active: store.currentView === 'recommend' }" @click="store.currentView = 'recommend'">
          추천 상품 보기
        </div>
      </div>
      <div class="menu-item quit" :class="{ active: store.currentView === 'quit' }" @click="store.currentView = 'quit'">
        회원 탈퇴
      </div>
    </div>

    <!-- 우측 컨텐츠 영역 -->
    <div class="content">
      <component :is="currentComponent" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProfileStore } from '@/stores/profile'
import ProfileEdit from '@/components/Profile/ProfileEdit.vue'
import ProfileProducts from '@/components/Profile/ProfileProducts.vue'
import ProfileTest from '@/components/Profile/ProfileTest.vue'
import ProfileQuit from '@/components/Profile/ProfileQuit.vue'
import ProfileRecommend from '@/components/Profile/ProfileRecommend.vue'

const route = useRoute()
const store = useProfileStore()

// URL query parameter 감지하여 view 변경
watch(() => route.query.view, (newView) => {
  if (newView) {
    store.currentView = newView
  }
}, { immediate: true })

const currentComponent = computed(() => {
  switch (store.currentView) {
    case 'edit':
      return ProfileEdit
    case 'products':
      return ProfileProducts
    case 'test':
      return ProfileTest
    case 'quit':
      return ProfileQuit
    case 'recommend':
      return ProfileRecommend
    default:
      return ProfileEdit
  }
})
</script>

<style scoped>
.profile-container {
  display: flex;
  gap: 2rem;
  padding: 2rem;
  max-width: 1300px;
  margin: 0 auto;
  min-height: 80vh;
}

.sidebar {
  width: 250px;
  min-width: 250px;
  background-color: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.financial-category {
  margin: 1.5rem 0;
  padding: 1rem 0;
  border-top: 1px solid #dee2e6;
  border-bottom: 1px solid #dee2e6;
}

.category-title {
  font-weight: bold;
  color: #495057;
  margin-bottom: 1rem;
}

.menu-item {
  padding: 0.8rem 1rem;
  margin: 0.5rem 0;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.menu-item:hover {
  background-color: #e9ecef;
}

.menu-item.active {
  background-color: #339af0;
  color: white;
}

.menu-item.quit {
  color: #dc3545;
}

.menu-item.quit:hover,
.menu-item.quit.active {
  background-color: #dc3545;
  color: white;
}

.content {
  flex: 1;
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

@media (max-width: 768px) {
  .profile-container {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    min-width: auto;
    margin-bottom: 1rem;
  }

  .menu-item {
    text-align: center;
  }
}
</style>