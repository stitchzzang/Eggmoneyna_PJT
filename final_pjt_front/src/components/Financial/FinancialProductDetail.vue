<template>
  <div class="product-detail-container">
    <h2>상품 상세 정보</h2>
    <div v-if="product" class="product-info">
      <router-link 
        :to="{ name: 'productDetail', params: { productType: productType, id: product.id }}" 
        class="product-name"
      >
        <h3>{{ product.name }}</h3>
      </router-link>
      <!-- 상품 상세 정보를 표시할 내용 -->
      <div class="info-grid">
        <div class="info-item">
          <strong>은행:</strong> {{ getBankName(product.bankId) }}
        </div>
        <div class="info-item">
          <strong>금리:</strong> {{ product.interestRate }}%
        </div>
        <div class="info-item">
          <strong>기간:</strong> {{ getPeriodName(product.periodId) }}
        </div>
        <div class="info-item">
          <strong>최소 금액:</strong> {{ formatAmount(product.minAmount) }}원
        </div>
      </div>
    </div>
    <div v-else>
      <p>상품을 불러오는 중입니다...</p>
    </div>
    <button @click="goBack" class="btn btn-secondary mt-3">
      목록으로 돌아가기
    </button>
  </div>
</template>

<script>
export default {
  name: 'FinancialProductDetailView',
  props: {
    productType: {
      type: String,
      required: true
    },
    id: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      product: null
    }
  },
  methods: {
    async fetchProductDetail() {
      try {
        // API 호출 로직 구현
        // const response = await axios.get(`/api/financial-products/${this.productType}/${this.id}`)
        // this.product = response.data
      } catch (error) {
        console.error('상품 정보를 불러오는데 실패했습니다:', error)
      }
    },
    goBack() {
      this.$router.go(-1)
    },
    getBankName(bankId) {
      // 은행 이름 반환 로직
    },
    getPeriodName(periodId) {
      // 기간 정보 반환 로직
    },
    formatAmount(amount) {
      // 금액 포맷팅 로직
      return amount.toLocaleString()
    }
  },
  created() {
    this.fetchProductDetail()
  }
}
</script>

<style scoped>
.product-detail-container {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
}

.product-info {
  background-color: #f8f9fa;
  padding: 2rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.info-item {
  padding: 0.5rem;
  border-bottom: 1px solid #dee2e6;
}

.product-name {
  text-decoration: none;
  color: inherit;
}

.product-name:hover {
  color: #007bff;
}
</style>
