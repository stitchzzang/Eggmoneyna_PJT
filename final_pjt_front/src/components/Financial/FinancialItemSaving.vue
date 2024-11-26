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
          <option v-for="term in availableTerms" 
                  :key="term" 
                  :value="term">
            {{ term }}개월
          </option>
        </select>
      </div>

      <button @click="handleSearch" class="search-btn">
        검색하기
      </button>
    </div>

    <!-- 오른쪽 결과 테이블 섹션 -->
    <div class="results-section">
      <div class="table-header">
        <div class="header-item date-col">공시제출일</div>
        <div class="header-item bank-col">금융회사명</div>
        <div class="header-item name-col">상품명</div>
        <div class="interest-rates-header">
          <div 
            v-for="term in availableTerms" 
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

      <div v-if="filteredSavings.length">
        <div v-for="saving in paginatedSavings" :key="saving.id" class="saving-item">
          <span class="item-date">{{ getFormattedDate(saving.submitDate) }}</span>
          <span class="item-bank">{{ saving.bankName }}</span>
          <span class="item-name product-link" @click="openModal(saving)">
            {{ saving.name }}
          </span>
          
          <div class="interest-rates">
            <span 
              v-for="term in availableTerms" 
              :key="term" 
              class="rate-item"
            >
              {{ getInterestRate(saving, term) ? `${getInterestRate(saving, term)}%` : '-' }}
            </span>
          </div>
        </div>
        
        <div class="pagination">
          <div class="pagination-controls">
            <button 
              :disabled="currentPage === 1"
              @click="currentPage = 1"
              class="page-btn"
            >
              ≪
            </button>
            <button 
              :disabled="currentPage === 1"
              @click="currentPage--"
              class="page-btn"
            >
              ◀
            </button>
            
            <span class="page-info">
              {{ currentPage }} / {{ totalPages }}
            </span>
            
            <button 
              :disabled="currentPage === totalPages"
              @click="currentPage++"
              class="page-btn"
            >
              ▶
            </button>
            <button 
              :disabled="currentPage === totalPages"
              @click="currentPage = totalPages"
              class="page-btn"
            >
              ≫
            </button>
          </div>

          <select v-model="itemsPerPage" class="items-per-page-select">
            <option v-for="count in [10, 20, 30, 40]" :key="count" :value="count">
              {{ count }}개씩 보기
            </option>
          </select>
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

const savings = ref([])
const filteredSavings = ref([])
const currentPage = ref(1)
const itemsPerPage = ref(10)
const selectedBank = ref('')
const selectedTerm = ref('')

// 정렬 관련 상태 추가
const currentSortTerm = ref(null)
const sortDirection = ref('asc')

// 모달 관련 상태 추가
const showModal = ref(false)
const selectedProduct = ref(null)

const bankList = computed(() => {
  const banks = new Set(savings.value.map(item => item.bankName))
  return Array.from(banks).sort((a, b) => a.localeCompare(b, 'ko'))
})

const handleSearch = () => {
  let filtered = savings.value

  if (selectedBank.value) {
    filtered = filtered.filter(item => item.bankName === selectedBank.value)
  }

  if (selectedTerm.value) {
    filtered = filtered.filter(item => {
      const term = parseInt(selectedTerm.value)
      return item.options.some(opt => 
        opt.saveTerm === term && opt.interestRate > 0
      )
    })
  }

  filteredSavings.value = filtered
  currentPage.value = 1
}

const paginatedSavings = computed(() => {
  const items = filteredSavings.value.length ? filteredSavings.value : savings.value
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return items.slice(start, end)
})

const totalPages = computed(() => {
  const items = filteredSavings.value.length ? filteredSavings.value : savings.value
  return Math.ceil(items.length / itemsPerPage.value)
})

const getInterestRate = (saving, term) => {
  const option = saving.options.find(opt => opt.saveTerm === term)
  return option ? option.interestRate : null
}

const getFormattedDate = (dateString) => {
  return dateString.slice(2)
}

// 금리로 정렬하는 함수
const sortByRate = (term) => {
  if (currentSortTerm.value === term) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    currentSortTerm.value = term
    sortDirection.value = 'asc'
  }

  const items = [...(filteredSavings.value.length ? filteredSavings.value : savings.value)]
  
  items.sort((a, b) => {
    const rateA = getInterestRate(a, term) || 0
    const rateB = getInterestRate(b, term) || 0
    return sortDirection.value === 'asc' ? rateA - rateB : rateB - rateA
  })

  filteredSavings.value = items
}

// 정렬 화살표 클래스 반환
const getSortArrowClass = (term) => {
  if (currentSortTerm.value !== term) return 'sort-arrow-inactive'
  return sortDirection.value === 'asc' ? 'sort-arrow-up' : 'sort-arrow-down'
}

// 모달 열기/닫기 함수
const openModal = (product) => {
  selectedProduct.value = product
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  selectedProduct.value = null
}

onMounted(async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/saving-products/')
    savings.value = response.data.data.map(product => ({
      id: product.id,
      name: product.fin_prdt_nm,
      bankName: product.kor_co_nm,
      description: product.etc_note,
      joinWay: product.join_way,
      joinDeny: product.join_deny,
      joinMember: product.join_member,
      submitDate: product.dcls_strt_day,
      dclsMonth: product.dcls_month,
      finCoNo: product.fin_co_no,
      finPrdtCd: product.fin_prdt_cd,
      mtrtInt: product.mtrt_int,
      spclCnd: product.spcl_cnd,
      maxLimit: product.max_limit,
      dclsEndDay: product.dcls_end_day,
      finCoSubmDay: product.fin_co_subm_day,
      options: product.options.map(option => ({
        id: `${product.fin_prdt_cd}-${option.save_trm}`,
        interestRate: option.intr_rate,
        saveTerm: option.save_trm,
        dclsMonth: option.dcls_month,
        finPrdtCd: option.fin_prdt_cd,
        intrRateType: option.intr_rate_type,
        intrRateTypeNm: option.intr_rate_type_nm,
        intrRate2: option.intr_rate2,
        rsrvType: option.rsrv_type,
        rsrvTypeNm: option.rsrv_type_nm
      }))
    }))
    filteredSavings.value = savings.value
  } catch (error) {
    console.error('적금 상품 데이터 로딩 실패:', error)
  }
})

// itemsPerPage가 변경될 때 첫 페이지로 돌아가도록 watch 추가
watch(itemsPerPage, () => {
  currentPage.value = 1
})

// computed 속성 수정
const availableTerms = computed(() => {
  return [6, 12, 24, 36]  // 고정된 기간 값
})
</script>

<style scoped>
.products-container {
  display: flex;
  gap: 20px;
  width: 100%;
  flex-direction: row;  /* 기본값 */
}

@media screen and (max-width: 1200px) {
  .products-container {
    flex-direction: column;  /* 화면이 작아지면 세로로 배치 */
  }

  .filter-sidebar {
    width: 100%;  /* 필터 섹션 전체 너비로 */
    margin-bottom: 20px;
  }
}

@media screen and (max-width: 768px) {
  .table-header, .saving-item {
    font-size: 0.9em;
    padding: 8px 10px;
  }

  .interest-rates-header, .interest-rates {
    grid-template-columns: repeat(4, 60px);  /* 금리 칼럼 너비 축소 */
    gap: 8px;
  }

  .item-bank {
    width: 100px;
  }

  .item-date {
    width: 80px;
  }

  .rate-item {
    padding: 3px 5px;
  }
}

@media screen and (max-width: 576px) {
  .pagination {
    flex-direction: column;
    gap: 10px;
  }

  .pagination-controls {
    width: 100%;
    justify-content: center;
  }

  .items-per-page-select {
    width: 100%;
    max-width: 200px;
  }

  .table-header, .saving-item {
    font-size: 0.8em;
    padding: 6px 8px;
  }

  .interest-rates-header, .interest-rates {
    grid-template-columns: repeat(4, 50px);
    gap: 5px;
  }

  .item-bank {
    width: 80px;
    margin-right: 10px;
  }

  .item-date {
    width: 70px;
    margin-right: 10px;
  }

  .item-name {
    margin-right: 10px;
  }
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
  color: #000000;
  font-size: 1.3em;
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
  padding: 10px 20px;
  background: linear-gradient(45deg, #47e0cc, #049b8c) !important;
  color: white;
  border: 2px solid #00897B;
  border-radius: 25px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  font-size: 18px;
  width: 100%;
  margin-top: 5px;
  opacity: 0.8;
  transition: all 0.3s ease;
}

.search-btn:hover {
  background-color: #035703;
}

.results-section {
  flex: 1;
  min-height: 100vh;
}

.saving-item {
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
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 0 20px;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 5px;
}

.page-btn {
  padding: 4px 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  cursor: pointer;
  font-size: 0.9em;
}

.page-btn:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.page-info {
  margin: 0 3px;
  min-width: 60px;
  text-align: center;
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
  text-align: left;
}

.bank-col {
  text-align: left;
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
  font-size: 1em;
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
  font-size: 17px;
  cursor: pointer;
  font-weight: semibold;
  color: #000000;
}

.product-link:hover {
  text-decoration: underline;
}
</style>
  