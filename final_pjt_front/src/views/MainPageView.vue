<template>
  <div class="home">
    <div class="carousel">
      <Carousel /> 
    </div>

    <div class="weekly-products">
      <hr>
      <h2 class="section-title">금주의 상품 추천</h2>
      <div class="product-grid">
        <div class="product-card" 
             v-for="product in gridProducts" 
             :key="product.id"
             @click="openModal(product.finId)"
             style="cursor: pointer">
          <div class="product-image">
            <img :src="product.image" :alt="product.name">
          </div>
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <p class="product-content">{{ product.rate }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 상품 상세 모달 -->
    <FinancialProductDetailModal
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Carousel from '@/views/CarouselView.vue'
import FinancialProductDetailModal from '@/components/Financial/FinancialProductDetailModal.vue'
import { useProductStore } from '@/stores/product'
import grid1 from '@/assets/products1.png'
import grid2 from '@/assets/products2.png'
import grid3 from '@/assets/products3.png'
import grid4 from '@/assets/products4.png'
import grid5 from '@/assets/products5.png'
import grid6 from '@/assets/products6.png'

const productStore = useProductStore()
const selectedProduct = ref(null)

const gridProducts = [
  {
    id: 1,
    name: 'KB - 특⭐한 적금',
    rate: '연 2% ~ 6%',
    image: grid1,
    fin_prdt_cd: '10-003-1384-0001'  // 실제 금융상품 ID
  },
  {
    id: 2,
    name: 'NH - 올원e예금',
    rate: '연 4.8%',
    image: grid2,
    finId: '10-003-1384-0001' // 실제 금융상품 ID
  },
  {
    id: 3,
    name: '우리은행 - WON플러스 예금',
    rate: '연 2.7 ~ 3.0%',
    image: grid3,
    finId: 'WR0001B'  // 실제 금융상품 ID
  },
  {
    id: 4,
    name: 'IM뱅크 - 내가만든보너스적금',
    rate: '연 3.65% ~ 4.45%',
    image: grid4,
    finId: '10527001001272000'  // 실제 금융상품 ID
  },
  {
    id: 5,
    name: '케이뱅크 - 코드K 자유적금',
    rate: '연 3.8%',
    image: grid5,
    finId: '01012000200000000003'  // 실제 금융상품 ID
  },
  {
    id: 6,
    name: '광주은행 - 스마트모아Dream정기예금',
    rate: '연 2.69 ~ 2.89%',
    image: grid6,
    finId: 'TD11300031000' // 실제 금융상품 ID
  }
]

const openModal = async (finId) => {
  try {
    const product = await productStore.getProductById(finId)
    if (product) {
      selectedProduct.value = product
    } else {
      console.error('상품을 찾을 수 없습니다')
    }
  } catch (error) {
    console.error('상품 정보를 불러오는데 실패했습니다:', error)
  }
}

const closeModal = () => {
  selectedProduct.value = null
}
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
  margin: 25px auto;
  padding-top: 10px;
  padding-bottom: 30px;
}

.section-title {
  padding: 15px 10px;
  background-color: #f8f9fa67;
  border: 2px solid #08630096;
  border-radius: 5px;
  text-align: center;
  margin-top: 50px;
  margin-bottom: 30px;
  font-size: 24px;
  font-weight: bold;
  color: #2b2b2b;
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