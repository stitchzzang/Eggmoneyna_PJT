<template>
  <div class="products-list">
    <div v-if="deposits.length">
      <div v-for="deposit in paginatedDeposits" :key="deposit.id" class="deposit-item">
        <span class="item-date">{{ getFormattedDate(deposit.submitDate) }}</span>
        <span class="item-bank">{{ deposit.bankName }}</span>
        <span class="item-name">{{ deposit.name }}</span>
        
        <div class="interest-rates">
          <span class="rate-item">{{ getInterestRate(deposit, 6) ? `${getInterestRate(deposit, 6)}%` : '-' }}</span>
          <span class="rate-item">{{ getInterestRate(deposit, 12) ? `${getInterestRate(deposit, 12)}%` : '-' }}</span>
          <span class="rate-item">{{ getInterestRate(deposit, 24) ? `${getInterestRate(deposit, 24)}%` : '-' }}</span>
          <span class="rate-item">{{ getInterestRate(deposit, 36) ? `${getInterestRate(deposit, 36)}%` : '-' }}</span>
        </div>
      </div>
      
      <div class="pagination">
        <button 
          :disabled="currentPage === 1"
          @click="currentPage--"
          class="page-btn"
        >
          이전
        </button>
        
        <span class="page-info">
          {{ currentPage }} / {{ totalPages }}
        </span>
        
        <button 
          :disabled="currentPage === totalPages"
          @click="currentPage++"
          class="page-btn"
        >
          다음
        </button>
      </div>
    </div>
    <div v-else>
      로딩 중이거나 상품이 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

const deposits = ref([])
const currentPage = ref(1)
const itemsPerPage = 10

// 페이지네이션된 데이터를 계산하는 computed 속성 추가
const paginatedDeposits = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return deposits.value.slice(start, end)
})

// 전체 페이지 수를 계산하는 computed 속성 추가
const totalPages = computed(() => {
  return Math.ceil(deposits.value.length / itemsPerPage)
})

// 특정 기간의 이자율을 찾는 함수
const getInterestRate = (deposit, term) => {
  const option = deposit.options.find(opt => Number(opt.saveTerm) === term)
  return option ? option.interestRate : null
}

// 날짜 형식을 변환하는 함수 추가
const getFormattedDate = (dateString) => {
  return dateString.slice(2)  // 앞의 2자리(20)를 제외한 나머지 반환
}

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/deposit-products/')
    if (response.data && response.data.data) {
      deposits.value = response.data.data.map(product => ({
        id: product.product_code,
        name: product.product_name,
        bankName: product.bank_name,
        submitDate: product.dcls_start_day,
        options: product.options.map(option => ({
          id: `${product.product_code}-${option.save_term}`,
          interestRate: option.basic_rate,
          saveTerm: option.save_term
        }))
      }))
    }
  } catch (error) {
    console.error('적금 상품 데이터 로딩 실패:', error)
  }
})
</script>

<style scoped>
.products-list {
  width: 100%;
}

.deposit-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  border-bottom: 1px solid #eee;
}

.item-bank {
  width: 120px;
  margin-right: 20px;
}

.item-name {
  flex: 1;
  margin-right: 20px;
}

.item-date {
  width: 100px;
  margin-right: 20px;
}

.interest-rates {
  display: flex;
  gap: 15px;
}

.rate-item {
  background-color: #f5f5f5;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.9em;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 20px;
}

.page-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
}

.page-btn:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9em;
}

.product-link {
  text-decoration: none;
  color: #2c3e50;
}

.product-link:hover {
  color: #42b983;
  text-decoration: underline;
}
</style>
  