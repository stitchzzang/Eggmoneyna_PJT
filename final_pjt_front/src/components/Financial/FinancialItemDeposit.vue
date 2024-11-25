<template>
  <div class="products-container">
    <!-- 왼쪽 검색 필터 섹션 -->
    <div class="filter-sidebar">
      <h3 class="filter-title">검색 필터</h3>
      <div class="filter-group">
        <label class="filter-label">은행 선택</label>
        <select v-model="selectedBank" class="filter-select">
          <option value="">전체</option>
          <option v-for="bank in bankList" :key="bank" :value="bank">
            {{ bank }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label class="filter-label">예치기간 선택</label>
        <select v-model="selectedTerm" class="filter-select">
          <option value="">전체</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>
      </div>

      <button @click="handleSearch" class="search-btn">
        검색하기
      </button>
    </div>

    <!-- 오른쪽 결과 테이블 섹션 -->
    <div class="results-section">
      <div class="items-per-page-selector">
        <select v-model="itemsPerPage" class="items-per-page-select">
          <option v-for="count in [10, 20, 30, 40]" :key="count" :value="count">
            {{ count }}개씩 보기
          </option>
        </select>
      </div>

      <div class="table-header">
        <div class="header-item date-col">공시제출일</div>
        <div class="header-item bank-col">금융회사명</div>
        <div class="header-item name-col">상품명</div>
        <div class="interest-rates-header">
          <div 
            v-for="term in [6, 12, 24, 36]" 
            :key="term"
            class="header-item rate-col"
            @click="sortByRate(term)"
            :class="{ active: currentSortTerm === term }"
          >
            {{ term }}개월
            <span class="sort-arrow" :class="getSortArrowClass(term)">▼</span>
          </div>
        </div>
      </div>

      <div v-if="filteredDeposits.length">
        <div v-for="deposit in paginatedDeposits" :key="deposit.id" class="deposit-item">
          <span class="item-date">{{ getFormattedDate(deposit.submitDate) }}</span>
          <span class="item-bank">{{ deposit.bankName }}</span>
          <span class="item-name product-link" @click="openModal(deposit)">
            {{ deposit.name }}
          </span>
          
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

    <!-- 모달 컴포넌트 추가 -->
    <FinancialProductDetailModal
      v-if="showModal"
      :product="selectedProduct"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import FinancialProductDetailModal from './FinancialProductDetailModal.vue'

const deposits = ref([])  // 상품 데이터
const filteredDeposits = ref([])  // 필터링된 상품
const currentPage = ref(1)  // 현재 페이지
const itemsPerPage = ref(10)  // 한 페이지에 보여줄 항목 수
const selectedBank = ref('')  // 선택된 은행
const selectedTerm = ref('')  // 선택된 예치기간

// 정렬 관련 상태 추가
const currentSortTerm = ref(null)
const sortDirection = ref('asc')

// 모달 관련 상태 추가
const showModal = ref(false)
const selectedProduct = ref(null)

const bankList = computed(() => {
  const banks = new Set(deposits.value.map(item => item.bankName))
  return Array.from(banks)
})

const handleSearch = () => {
  let filtered = deposits.value

  // 선택된 은행 필터링
  if (selectedBank.value) {
    filtered = filtered.filter(item => item.bankName === selectedBank.value)
  }

  // 선택된 기간 필터링
  if (selectedTerm.value) {
    filtered = filtered.filter(item => {
      const term = parseInt(selectedTerm.value)
      return item.options.some(opt => 
        opt.saveTerm === term && opt.interestRate > 0
      )
    })
  }

  filteredDeposits.value = filtered
  currentPage.value = 1
}

const paginatedDeposits = computed(() => {
  const items = filteredDeposits.value.length ? filteredDeposits.value : deposits.value
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return items.slice(start, end)
})

const totalPages = computed(() => {
  const items = filteredDeposits.value.length ? filteredDeposits.value : deposits.value
  return Math.ceil(items.length / itemsPerPage.value)
})

const getInterestRate = (deposit, term) => {
  const option = deposit.options.find(opt => opt.saveTerm === term)
  return option ? option.interestRate : null
}

const getFormattedDate = (dateString) => {
  return dateString.slice(2)  // 날짜 형식 변환
}

// 금리로 정렬하는 함수
const sortByRate = (term) => {
  if (currentSortTerm.value === term) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    currentSortTerm.value = term
    sortDirection.value = 'asc'
  }

  const items = [...(filteredDeposits.value.length ? filteredDeposits.value : deposits.value)]
  
  items.sort((a, b) => {
    const rateA = getInterestRate(a, term) || 0
    const rateB = getInterestRate(b, term) || 0
    return sortDirection.value === 'asc' ? rateA - rateB : rateB - rateA
  })

  filteredDeposits.value = items
}

// 정렬 화살표 클래스 반환
const getSortArrowClass = (term) => {
  if (currentSortTerm.value !== term) return 'sort-arrow-inactive'
  return sortDirection.value === 'asc' ? 'sort-arrow-up' : 'sort-arrow-down'
}

// itemsPerPage가 변경될 때 첫 페이지로 돌아가도록 watch 추가
watch(itemsPerPage, () => {
  currentPage.value = 1
})

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
      filteredDeposits.value = deposits.value
    }
  } catch (error) {
    console.error('예금 상품 데이터 로딩 실패:', error)
  }
})

// 모달 열기/닫기 함수
const openModal = (product) => {
  selectedProduct.value = product
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedProduct.value = null
}
</script>

<style scoped>
.products-container {
  display: flex;
  gap: 20px;
  width: 100%;
}

.filter-sidebar {
  width: 250px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  height: fit-content;
}

.filter-title {
  margin-bottom: 20px;
  color: #047404;
  font-size: 1.2em;
  font-weight: bold;
}

.filter-group {
  margin-bottom: 20px;
}

.filter-label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.filter-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.search-btn {
  width: 100%;
  padding: 10px;
  background-color: #047404;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #035703;
}

.results-section {
  flex: 1;
  min-height: 100vh;
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
  display: grid;
  grid-template-columns: repeat(4, 80px);
  gap: 15px;
}

.rate-item {
  background-color: #f5f5f5;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 0.9em;
  text-align: center;
  width: 100%;
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

.table-header {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  background-color: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
  font-weight: bold;
}

.header-item {
  text-align: center;
}

.date-col {
  width: 100px;
  margin-right: 20px;
}

.bank-col {
  width: 120px;
  margin-right: 20px;
}

.name-col {
  flex: 1;
  margin-right: 20px;
}

.interest-rates-header {
  display: grid;
  grid-template-columns: repeat(4, 80px);
  gap: 15px;
}

.rate-col {
  width: 80px;
  text-align: center;
  cursor: pointer;
  position: relative;
  user-select: none;
}

.rate-col:hover {
  background-color: #e9ecef;
}

.sort-arrow {
  font-size: 0.8em;
  margin-left: 4px;
  display: inline-block;
  transition: transform 0.2s;
}

.sort-arrow-inactive {
  opacity: 0.3;
}

.sort-arrow-up {
  transform: rotate(180deg);
  opacity: 1;
}

.sort-arrow-down {
  transform: rotate(0deg);
  opacity: 1;
}

.items-per-page-selector {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
  padding-right: 20px;
}

.items-per-page-select {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  font-size: 0.9em;
}

.items-per-page-select:hover {
  border-color: #047404;
}

.items-per-page-select:focus {
  outline: none;
  border-color: #047404;
  box-shadow: 0 0 0 2px rgba(4, 116, 4, 0.1);
}

.product-link {
  cursor: pointer;
  color: #047404;
}

.product-link:hover {
  text-decoration: underline;
}
</style>
  
