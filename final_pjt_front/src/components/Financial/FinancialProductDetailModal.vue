<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>{{ product.name }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="product-info">
          <div class="info-row">
            <span class="info-label">은행명:</span>
            <span class="info-value">{{ product.bankName }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">공시일:</span>
            <span class="info-value">{{ product.submitDate }}</span>
          </div>
          
          <h3>금리 정보</h3>
          <div class="interest-rates-grid">
            <div v-for="term in [6, 12, 24, 36]" :key="term" class="rate-info">
              <span class="term">{{ term }}개월</span>
              <span class="rate">{{ getInterestRate(product, term) }}%</span>
            </div>
          </div>
          
          <div class="subscribe-section">
            <button 
              :class="['action-btn', isSubscribed ? 'unsubscribe-btn' : 'subscribe-btn']" 
              @click="handleSubscriptionToggle"
            >
              {{ isSubscribed ? '해지하기' : '가입하기' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useProductStore } from '@/stores/product'

const productStore = useProductStore()
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

// 현재 상품의 가입 상태 확인
const isSubscribed = computed(() => {
  return productStore.subscribedProducts.some(p => p.id === props.product.id)
})

// 가입/해지 토글 핸들러
const handleSubscriptionToggle = () => {
  if (isSubscribed.value) {
    productStore.unsubscribeProduct(props.product.id)
    alert('상품 해지가 완료되었습니다!')
  } else {
    productStore.subscribeProduct(props.product)
    alert('상품 가입이 완료되었습니다!')
  }
}

const getInterestRate = (product, term) => {
  const option = product.options.find(opt => opt.saveTerm === term)
  return option ? option.interestRate : '-'
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 0 8px;
}

.info-row {
  display: flex;
  margin-bottom: 10px;
}

.info-label {
  width: 100px;
  font-weight: bold;
}

.interest-rates-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-top: 10px;
}

.rate-info {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.term {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.rate {
  color: #047404;
  font-size: 1.2em;
}

.subscribe-section {
  margin-top: 20px;
  text-align: center;
}

.action-btn {
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.subscribe-btn {
  transition: all 0.3s ease;
  text-decoration: none;
  padding: 10px 20px;
  background: linear-gradient(45deg, #98d49a, #338133) !important;
  color: white;
  border: 2px solid #4b9e40;
  border-radius: 5px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s eas
}

.subscribe-btn:hover {
  opacity: 1;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(20, 163, 51, 0.4);
}

.unsubscribe-btn {
  background: linear-gradient(45deg, #db7a7a, #eb1c1c);
  border: 2px solid #b5221a;
  cursor: pointer;
  font-size: 17px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  letter-spacing: 1.3px;
  color: white;
  opacity: 0.8;
  padding: 8px 20px;
  border-radius: 5px;
}

.unsubscribe-btn:hover {
  opacity: 1;
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(250, 82, 82, 0.4);
}
</style>
