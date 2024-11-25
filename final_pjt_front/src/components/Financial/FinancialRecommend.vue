<template>
  <div class="container">
    <div class="row mb-4">
      <div class="col">
        <button @click="$emit('back')" class="btn btn-secondary">
          뒤로가기
        </button>
      </div>
      <hr>
      <h3>추천 상품</h3>
    </div>

    <!-- 추천 상품 그리드 -->
    <div class="row row-cols-1 row-cols-md-3 g-4">
      <div v-for="product in recommendedProducts" :key="product.id" class="col">
        <div class="card h-100" @click="showDetail(product)">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p class="card-text">금리: {{ product.interestRate }}%</p>
            <div class="recommendation-tag">
              맞춤 추천 상품
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 상세 정보 모달 -->
    <ProductDetail
      v-if="showModal"
      :product="selectedProduct"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ProductDetail from '@/components/Financial/FinancialProductDetailModal.vue'

const showModal = ref(false)
const selectedProduct = ref(null)
const recommendedProducts = ref([
  // 추천 알고리즘으로 받아올 상품 데이터
])

const showDetail = (product) => {
  selectedProduct.value = product
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedProduct.value = null
}
</script>

<style scoped>
.btn {
  margin-bottom: 10px;
}

.card {
  cursor: pointer;
  transition: transform 0.2s;
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.recommendation-tag {
  position: absolute;
  top: 10px;
  right: -30px;
  background: linear-gradient(45deg, #86da8a, #047404);
  color: white;
  padding: 5px 30px;
  transform: rotate(45deg);
  font-size: 0.8rem;
}
</style>