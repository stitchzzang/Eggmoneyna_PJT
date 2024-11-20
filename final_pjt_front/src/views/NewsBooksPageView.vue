<template>
  <div class="books-container">
    <h1 class="page-title">도서 추천</h1>
    <div class="books-grid">
      <div v-for="book in books" :key="book.id" class="book-card">
        <img :src="book.image" :alt="book.title" class="book-image">
        <div class="book-info">
          <h3 class="book-title">{{ book.title }}</h3>
          <p class="book-author">{{ book.author }}</p>
          <p class="book-description">{{ book.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 임시 데이터 - 나중에 API로 대체하세요
const books = ref([
  {
    id: 1,
    title: 'EBS 다큐프라임 자본주의',
    author: '저자 1',
    description: '책 설명이 들어갑니다.',
    image: new URL('@/assets/books1.png', import.meta.url).href
  },
  {
    id: 2,
    title: '보도섀퍼의 돈',
    author: '저자 1',
    description: '책 설명이 들어갑니다.',
    image: new URL('@/assets/books2.png', import.meta.url).href
  },
  {
    id: 3,
    title: '돈은 좋지만 재테크는 겁나는 너에게',
    author: '저자 1',
    description: '책 설명이 들어갑니다.',
    image: new URL('@/assets/books3.png', import.meta.url).href
  },
  {
    id: 4,
    title: '바빌론 부자들의 돈 버는 지혜',
    author: '저자 1',
    description: '책 설명이 들어갑니다.',
    image: new URL('@/assets/books4.png', import.meta.url).href
  },
  {
    id: 5,
    title: '1일 1단어 1분으로 끝내는 경제공부',
    author: '저자 1',
    description: '책 설명이 들어갑니다.',
    image: new URL('@/assets/books5.png', import.meta.url).href
  },
  {
    id: 6,
    title: '난처한 경제 이야기 1 : 기본 편',
    author: '저자 1',
    description: '책 설명이 들어갑니다.',
    image: new URL('@/assets/books6.png', import.meta.url).href
  },
  {
    id: 7,
    title: '부의 시나리오',
    author: '저자 1',
    description: '책 설명이 들어갑니다.',
    image: new URL('@/assets/books7.png', import.meta.url).href
  },
  {
    id: 8,
    title: '최진기의 경제상식',
    author: '저자 1',
    description: '책 설명이 들어갑니다.',
    image: new URL('@/assets/books8.png', import.meta.url).href
  },
])
</script>

<style scoped>
.books-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  margin: 20px auto;
}

.page-title {
  text-align: center;
  margin-bottom: 20px;
  color: #056800;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 30px;
  padding: 20px;
}

.book-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
  overflow: hidden;
}

.book-card:hover {
  transform: translateY(-5px);
}

.book-image {
  width: 100%;
  height: 300px;
  object-fit: contain;
  background-color: #f5f5f5;
  padding: 10px;
}

.book-info {
  padding: 15px;
}

.book-title {
  font-size: 1.2rem;
  margin: 0 0 10px 0;
  color: #333;
}

.book-author {
  color: #666;
  margin: 5px 0;
}

.book-description {
  font-size: 0.9rem;
  color: #777;
  margin: 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .books-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 480px) {
  .books-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .book-image {
    height: 250px;
  }
}
</style>