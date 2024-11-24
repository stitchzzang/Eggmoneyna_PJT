<template>
  <div class="whole">
    <div class="container mt-4">
      <!-- 추건부 렌더링으로 컴포넌트 표시 -->
      <FinancialRecommend 
        v-if="showRecommend" 
        @back="showRecommend = false"
      />

      <!-- 기존 필터링 및 상품 목록 -->
      <div v-else>
        <!-- 추천 상품 버튼 -->
        <div class="row mb-4">
          <div class="col">
            <button @click="showRecommend = true" class="btn btn-primary">
              추천 상품 보러가기
            </button>
          </div>
        </div>
        
        <div class="row">
          <!-- 왼쪽 필터링 섹션 -->
          <div class="col-md-3">
            <div class="card">
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
          </div>

          <!-- 상품 목록 섹션 (게시판 형식) -->
          <div class="col-md-9">
            <div class="card">
              <div class="card-body">
                <table class="table">
                  <thead>
                    <tr>
                      <th>은행명</th>
                      <th>상품명</th>
                      <th>금리</th>
                      <th>예치기간</th>
                      <th>최소예치금</th>
                      <th>상세보기</th>
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
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import FinancialRecommend from '@/components/Financial/FinancialRecommend.vue'

const showRecommend = ref(false)

// 은행 목록 데이터
const banks = ref([
  { id: 1, name: '국민은행' },
  { id: 2, name: '신한은행' },
  { id: 3, name: '우리은행' },
  // ... 추가 은행
])

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
</style>