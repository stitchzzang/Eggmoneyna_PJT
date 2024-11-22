<template>
  <div class="books-container">
    <h1 class="page-title">✏️ 도서 추천</h1>
    <div class="books-grid">
      <div v-for="book in books" :key="book.id" class="book-card">
        <div class="book-thumbnail" @click="goToBookSite(book.link)">
          <img :src="book.image" :alt="book.title" class="book-image">
          <div class="link-button">
            <i class="fas fa-external-link-alt"></i>
          </div>
        </div>
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

const goToBookSite = (link) => {
  window.open(link, '_blank')
}

const books = ref([
  {
    id: 1,
    title: 'EBS 다큐프라임 자본주의',
    author: 'EBS 자본주의 제작팀',
    description: '우리가 반드시 알아야 할 자본주의의 진실! 『자본주의』는 자본주의를 쉽게 풀어낸 방송, "EBS 다큐프라임 《자본주의》 5부작"을 책으로 엮은 것이다. 지갑 속 돈과 통장, 매달 갚아야 할 대출금과 이자, 살고 있는 집의 가격 등 이 모든 것이 자본주의 시스템에서 자유롭지 못한 오늘날, 세계 최고의 석학들을 만나 돈에 관한 진실과 자본주의의 비밀을 밝혀낸다. 그리고 무의식중에 우리를 나락으로 빠뜨리는 자본주의의 유혹과 위협 속에서 어떻게 살아남을 것인지도 알려준다. 이 책에서 독자들은 자신이 돈을 알맞게 쓰고 있는지 체크해 볼 수 있고, 자신을 지키며 행복하게 소비할 수 있는 방법을 찾아볼 수 있을 것이다.',
    image: new URL('@/assets/books1.png', import.meta.url).href,
    link: 'https://search.shopping.naver.com/book/catalog/32490330444?query=%EB%8B%A4%ED%81%90%ED%94%84%EB%9D%BC%EC%9E%84%20%EC%9E%90%EB%B3%B8%EC%A3%BC%EC%9D%98&NaPm=ct%3Dm3re2ay8%7Cci%3D7819d1db63fbb0ffa7c7507dba5654f39d66be89%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3Db56dc0ffe3d6a2b69b9c66a0d91fe4f86d07b170'
  },
  {
    id: 2,
    title: '보도섀퍼의 돈',
    author: '보도 섀퍼',
    description: '재테크의 기본 개념을 갖게 해주는 책 경제를 넘어 인생까지 폭넓게 생각하게 하는 책 부자가 되는 것은 결코 기적이 아니다!',
    image: new URL('@/assets/books2.png', import.meta.url).href,
    link: 'https://search.shopping.naver.com/book/catalog/32445148668?query=%EB%8F%88&NaPm=ct%3Dm3re47mg%7Cci%3Db7f54ea7c1ba0fb0ae5b339fde8c16ba18967831%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D3f40ea840a18724e0f8c7055301756dc319f5bd5'
  },
  {
    id: 3,
    title: '돈은 좋지만 재테크는 겁나는 너에게',
    author: '뿅글이',
    description: '주변 사람들과 지금의 나를 비교할 필요는 없어요. 여러분의 재테크 여정에 함께 할게요. 16만 구독자가 닮고 싶어 하는 뿅글이의 첫 번째 재테크 에세이! 재테크로 고민하는 Z세대에게 전하는 따스한 위로와 응원',
    image: new URL('@/assets/books3.png', import.meta.url).href,
    link: 'https://search.shopping.naver.com/book/catalog/37284682641'
  },
  {
    id: 4,
    title: '바빌론 부자들의 돈 버는 지혜',
    author: '조지 사무엘 클레이슨',
    description: '"왜 누구는 부자가 되고 누구는 평생 가난한가?" 평생 돈에 휘둘리지 않는 삶을 위해 100세까지 간직할 인생의 지혜를 배우다',
    image: new URL('@/assets/books4.png', import.meta.url).href,
    link: 'https://search.shopping.naver.com/book/catalog/49379961637?query=%EB%B0%94%EB%B9%8C%EB%A1%A0%20%EB%B6%80%EC%9E%90%EB%93%A4%EC%9D%98%20%EB%8F%88%20%EB%B2%84%EB%8A%94%20%EC%A7%80%ED%98%9C&NaPm=ct%3Dm3re5068%7Cci%3Dc0b2cfdb5cd99bb01c5cbdce1733f7acea2a3a94%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3Dc2c67bcd51ba3f90c9022f33992481dddad199f2'
  },
  {
    id: 5,
    title: '1일 1단어 1분으로 끝내는 경제공부',
    author: '태지원',
    description: '하루 1분, 읽기만 해도 경제의 기본지식이 쌓인다! 카드뉴스처럼 설명은 짧고, 재밌게! 시각 자료는 풍부하게!',
    image: new URL('@/assets/books5.png', import.meta.url).href,
    link: 'https://search.shopping.naver.com/book/catalog/32445223427?query=1%EC%9D%BC%201%EB%8B%A8%EC%96%B4%201%EB%B6%84%EC%9C%BC%EB%A1%9C%20%EB%81%9D%EB%82%B4%EB%8A%94%20%EA%B2%BD%EC%A0%9C%EA%B3%B5%EB%B6%80&NaPm=ct%3Dm3re5l08%7Cci%3D8ef87e3810c2b30212a9655cb46b071f223d104b%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3Da7daa191001131be0f7aa473698a3c8260e2386d'
  },
  {
    id: 6,
    title: '난처한 경제 이야기 1 : 기본 편',
    author: '송병건',
    description: '『난처한 경제 이야기』는 난생 처음 한번 공부하는 이 세상의 모든 지식 시리즈, 즉 "난처한 시리즈"의 새로운 도전이다. 기존 난처한 시리즈에서 호평을 받았던 술술 읽히는 구성은 그대로 유지한 채, 이제는 전 국민의 필수 교양이 된 경제를 이야기한다.',
    image: new URL('@/assets/books6.png', import.meta.url).href,
    link: 'https://search.shopping.naver.com/book/catalog/32988652622?query=%EC%86%A1%EB%B3%91%EA%B1%B4&NaPm=ct%3Dm3re6agw%7Cci%3D5ad71ec8c3c434408e23992e723b60dd1dd1c321%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3Dea07f92d9c5ab050d481a657029b46818285f97a'
  },
  {
    id: 7,
    title: '부의 시나리오',
    author: '오건영',
    description: '"인플레 공포 너머 다음 스텝을 준비하라! " 금융천재 오건영의 똑똑한 투자 포트폴리오 불안한 금융시장, 중심을 잡아줄 친절하고 생생한 인사이트',
    image: new URL('@/assets/books7.png', import.meta.url).href,
    link: 'https://search.shopping.naver.com/book/catalog/32464775973?query=%EB%B6%80%EC%9D%98%20%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4&NaPm=ct%3Dm3re6nl4%7Cci%3Deb8dd3597f40927eda654b5ac4a9884302a6862f%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3De0489b17281df5bf060659437ed09218e7de790d'
  },
  {
    id: 8,
    title: '최진기의 경제상식',
    author: '최진기',
    description: '꼭 필요한 것만 경제적으로, 경제 상식을 공부한다!',
    image: new URL('@/assets/books8.png', import.meta.url).href,
    link: 'https://search.shopping.naver.com/book/catalog/32467937822?query=%EC%B5%9C%EC%A7%84%EA%B8%B0%EC%9D%98%20%EA%B2%BD%EC%A0%9C%EC%83%81%EC%8B%9D%20%EC%98%A4%EB%8A%98%EB%B6%80%ED%84%B0%201%EC%9D%BC&NaPm=ct%3Dm3re6z5s%7Cci%3Dec17bdef2587d732dd3b219c49e44d94321426b9%7Ctr%3Dboksl%7Csn%3D95694%7Chk%3D843bd501778945214de5603ead3ab3e2599b039b'
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
  font-weight: 600;
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

.book-thumbnail {
  position: relative;
  cursor: pointer;
}

.book-image {
  width: 100%;
  height: 300px;
  object-fit: contain;
  background-color: #f5f5f5;
  padding: 10px;
}

.link-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(5, 104, 0, 0.8);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.book-thumbnail:hover .link-button {
  opacity: 1;
}

.link-button i {
  color: white;
  font-size: 20px;
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