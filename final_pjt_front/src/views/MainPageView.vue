<template>
  <div class="home">
    <div class="carousel">
      <Carousel /> 
    </div>

    <div class="weekly-products">
      <h2 class="section-title">금주의 상품 추천</h2>
      <hr>
      <div class="product-grid">
        <div class="product-card" v-for="i in 6" :key="i">
          <div class="product-image">
            <img src="@/assets/products1.png" alt="상품 이미지">
          </div>
          <div class="product-info">
            <h3 class="product-name">상품명 {{ i }}</h3>
            <p class="product-content">₩ 00,000</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Carousel from '@/views/CarouselView.vue'
export default {
  name: 'HomePage',
  components: {
    Carousel,
  }
};
</script>

<style scoped>
.carousel {
  width: 60%;
  max-width: 800px;
  margin: 20px auto;
}

.weekly-products {
  width: 80%;
  max-width: 1200px;
  margin: 50px auto;
  padding-top: 10px;
}

.section-title {
  text-align: left;
  margin-bottom: 10px;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);  /* 3열 그리드 */
  gap: 20px;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.692);
  border-radius: 5px;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.2s;
  background: white;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f8f9fa;
  padding: 10px;
}

.product-image img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  width: auto;
  height: auto;
}

.product-info {
  padding: 15px;
}

.product-name {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.product-content {
  margin: 8px 0 0;
  color: #007bff;
  font-weight: bold;
}

/* 반응형 디자인 */
@media (max-width: 992px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);  /* 2열로 변경 */
  }
}

@media (max-width: 576px) {
  .product-grid {
    grid-template-columns: 1fr;  /* 1열로 변경 */
  }
}
</style>