<template>
  <div class="whole">
    <div class="container mt-4">
      <FinancialRecommend 
        v-if="showRecommend" 
        @back="showRecommend = false"
      />

      <div v-else>
        <div class="row">
          <!-- 왼쪽 필터링 섹션 -->
          <div class="col-md-3">
            <div class="card mt-5">
              <div class="card-body">
                <h4 class="card-title">검색 조건</h4>
                <hr>
                <!-- 은행 필터 -->
                <div class="mb-4">
                  <h6>은행선택</h6>
                  
                  <select class="form-select" v-model="selectedBank">
                    <option value="">전체</option>
                    <option 
                      v-for="bank in banks" 
                      :key="bank.id" 
                      :value="bank.id"
                    >
                      {{ bank.name }}
                    </option>
                  </select>
                </div>

                <!-- 예치 기간 필터 -->
                <div class="mb-4">
                  <h6>예치 기간</h6>
                  <select class="form-select" v-model="selectedPeriod">
                    <option value="">전체</option>
                    <option 
                      v-for="period in periods" 
                      :key="period.id" 
                      :value="period.id"
                    >
                      {{ period.name }}
                    </option>
                  </select>
                </div>

                <!-- 검색 버튼 -->
                <button 
                  @click="searchProducts" 
                  class="btn btn-primary w-100"
                >
                  검색하기
                </button>
              </div>
            </div>
            <button @click="showRecommend = true" class="btn btn-primary">
              추천 상품 보러가기
            </button>
          </div>

          <!-- 상품 목록 섹션 -->
          <div class="col-md-9">
            <!-- 상품 유형 선택 버튼을 여기로 이동 -->
            <div class="d-flex justify-content-between align-items-center mb-3">
              <div class="product-type-links">
                <router-link 
                  :to="{ name: 'deposit' }" 
                  class="product-link"
                  :class="{ 'active': productType === 'deposit' }"
                  @click="productType = 'deposit'"
                >
                  정기예금
                </router-link>
                <span class="mx-2">|</span>
                <router-link 
                  :to="{ name: 'saving' }" 
                  class="product-link"
                  :class="{ 'active': productType === 'saving' }"
                  @click="productType = 'saving'"
                >
                  정기적금
                </router-link>
              </div>
            </div>

            <div class="card">
              <div class="card-body">
                <table class="table">
                  <thead>
                    <tr>
                      <th>공시제출일</th>
                      <th>금융회사명</th>
                      <th>상품명</th>
                      <th>6개월</th>
                      <th>12개월</th>
                      <th>24개월</th>
                      <th>36개월</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="product in displayedProducts" :key="product.id">
                      <td>{{ getBankName(product.bankId) }}</td>
                      <td>{{ product.name }}</td>
                      <td>{{ product.interestRate }}%</td>
                      <td>{{ getPeriodName(product.periodId) }}</td>
                      <td>{{ formatAmount(product.minAmount) }}원</td>
                      <td>
                        <button 
                          @click="showProductDetail(product)" 
                          class="btn btn-outline-primary btn-sm"
                        >
                          상세보기
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <!-- 컴포넌트 조건부 렌더링 추가 -->
                <FinancialItemDeposit v-if="productType === 'deposit'" />
                <FinancialItemSaving v-else-if="productType === 'saving'" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import FinancialRecommend from '@/components/Financial/FinancialRecommend.vue'
import FinancialItemDeposit from '@/components/Financial/FinancialItemDeposit.vue'
import FinancialItemSaving from '@/components/Financial/FinancialItemSaving.vue'

const showRecommend = ref(false)
const productType = ref('deposit')

// 은행 목록 데이터를 빈 배열로 초기화
const banks = ref([])

// API에서 은행 목록을 가져오는 함수
const fetchBanks = async () => {
  try {
    const [depositRes, savingRes] = await Promise.all([
      axios.get('http://127.0.0.1:8000/deposit-products/'),
      axios.get('http://127.0.0.1:8000/saving-products/')
    ])

    // bank_name만 추출하여 Set으로 중복 제거
    const bankNames = new Set([
      ...depositRes.data.data.map(item => item.bank_name),
      ...savingRes.data.data.map(item => item.bank_name)
    ])

    // banks 배열로 변환
    banks.value = Array.from(bankNames).map((name, index) => ({
      id: index + 1,
      name: name
    }))

    // console.log('처리된 은행 목록:', banks.value)

  } catch (error) {
    console.error('은행 목록을 가져오는데 실패했습니다:', error)
    console.log('에러 상세:', error.response?.data)
  }
}

// 컴포넌트가 마운트될 때 은행 목록 가져오기
onMounted(() => {
  fetchBanks()
})

// 예치 기간 데이터
const periods = ref([
  { id: 1, name: '6개월' },
  { id: 2, name: '12개월' },
  { id: 3, name: '24개월' },
  { id: 4, name: '36개월' },
])

// 선택된 필터 값들
const selectedBank = ref(0)
const selectedPeriod = ref(0)

// 상품 목록 데이터 (API에서 받아올 예정)
const products = ref([])

// 필터링된 상품 목록
const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const bankMatch = selectedBank.value === 0 || selectedBank.value === product.bankId
    const periodMatch = selectedPeriod.value === 0 || selectedPeriod.value === product.periodId
    return bankMatch && periodMatch
  })
})

// 상품 상세보기 페이지로 이동
const showProductDetail = (product) => {
  // 상품 상세보기 페이지로 이동하는 로직을 구현해야 합니다.
}

// 은행 이름 가져오기
const getBankName = (bankId) => {
  const bank = banks.value.find(bank => bank.id === bankId)
  return bank ? bank.name : ''
}

// 예치 기간 이름 가져오기
const getPeriodName = (periodId) => {
  const period = periods.value.find(period => period.id === periodId)
  return period ? period.name : ''
}

// 금액 포맷팅
const formatAmount = (amount) => {
  return amount.toLocaleString() + '원'
}

const currentPage = ref(1)
const itemsPerPage = 10

const totalPages = computed(() => {
  return Math.ceil(filteredProducts.value.length / itemsPerPage)
})

const displayedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProducts.value.slice(start, end)
})
</script>

<style scoped>
.whole {
  margin: 30px 30px;
  padding: 20px;
  background-color: rgb(255, 255, 255, 0.5);
  border-radius: 20px;  
}
.card {
  transition: transform 0.2s;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
.btn-primary {
  padding: 10px 20px;
  background: linear-gradient(45deg, #86da8a, #047404) !important;
  color: rgb(255, 255, 255);
  border: 2px solid #128004;
  border-radius: 10px;
  cursor: pointer;
  font-size: 17px;
  font-weight: 600;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  letter-spacing: 1.3px;
}

.btn-primary:hover {
  padding: 10px 20px;
  background: linear-gradient(45deg, #e9eea7, #d6e227) !important;
  color: rgb(0, 0, 0);
  border: 2px solid #989b0d;
  border-radius: 10px;
  cursor: pointer;
  font-size: 17px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.product-type-links {
  display: inline-block;
}

.product-link {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  padding: 5px 10px;
}

.product-link.active {
  color: #047404;
  font-weight: 700;
}

.pagination .page-link {
  color: #047404;
  border-color: #047404;
}

.pagination .page-item.active .page-link {
  background-color: #047404;
  border-color: #047404;
  color: white;
}

.pagination .page-item.disabled .page-link {
  color: #6c757d;
  border-color: #dee2e6;
}

.col-md-3 {
  margin-top: 15px;
}

.btn-primary {
  margin-top: 20px;
}
</style>