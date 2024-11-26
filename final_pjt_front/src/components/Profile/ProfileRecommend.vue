<template>
  <div class="recommend-container">
    <div v-if="store.testResult" class="profile-result">
      <h2>나의 금융 투자 성향</h2>
      <hr>
      
      
      <div class="profile-result-info">
        <h3>{{ store.testResult.type }}</h3>
        <img :src="store.testResult.image" :alt="store.testResult.type">
        <div class="type-description">
          <p>{{ store.testResult.description }}</p>
        </div>
      </div>
      <hr>
      <div class="recommended-products">
        <h3>추천 금융 상품</h3>
        <ul>
          <li v-for="(product, index) in store.testResult.recommendations" :key="index">
            <strong>{{ product.name }}</strong>
            <p>{{ product.description }}</p>
          </li>
        </ul>
      </div>
      <div class="score-summary">
        <h3>테스트 결과 상세</h3>
        <div class="score-details">
          <p>나이 점수: {{ store.ageScore ? Math.round(store.ageScore * 0.2) : '0' }} / 20 (20%)</p>
          <p>소득 점수: {{ store.incomeScore ? Math.round(store.incomeScore * 0.3) : '0' }} / 30 (30%)</p>
          <p>투자성향 점수: {{ store.habitScore ? Math.round(store.habitScore) : '0' }} / 50 (50%)</p>
          <p class="final-score">최종 점수: {{ store.finalScore ? Math.round(store.finalScore) : '0' }}</p>
        </div>
      </div>
      <button @click="moveToTest" class="test-link retake">
        다시 테스트하기
      </button>
      <div class="type-table">
        <h3>투자 성향 유형 안내</h3>
        <table>
          <thead>
            <tr>
              <th>점수</th>
              <th>유형</th>
              <th>특성</th>
              <th>추천 상품</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>90점 이상</td>
              <td>안정적 장기 투자 선호형</td>
              <td>안정성과 장기 투자를 선호</td>
              <td>
                - 3~5년 장기 예금<br>
                - 우대 금리 적금
              </td>
            </tr>
            <tr>
              <td>70~89점</td>
              <td>중기적 계획적 저축형</td>
              <td>중기적으로 계획적인 저축 성향</td>
              <td>
                - 6개월~12개월 정기 예금<br>
                - 정기 적금
              </td>
            </tr>
            <tr>
              <td>50~69점</td>
              <td>단기 자금 유연 운용형</td>
              <td>단기적으로 자금 활용을 선호</td>
              <td>
                - 1~6개월 정기 예금<br>
                - 자유 적금
              </td>
            </tr>
            <tr>
              <td>49점 이하</td>
              <td>즉시 유동성 필요형</td>
              <td>즉시 자금 유동성이 필요, 자산 운용이 자유로운 성향</td>
              <td>
                - 입출금 자유 예금<br>
                - 입출금 자유 적금
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <hr>
    </div>
    <div v-else class="no-result">
      <p>먼저 금융 성향 테스트를 완료해주세요!</p>
      <button @click="moveToTest" class="test-link">
        테스트 하러가기
      </button>
    </div>
  </div>
  <div class="financial-products">
    <h3>예금/적금 추천 상품</h3>
    <div class="sort-controls">
      <select v-model="sortOrder" @change="sortProducts">
        <option value="high">금리 높은순</option>
        <option value="low">금리 낮은순</option>
      </select>
    </div>
    <div class="products-container">
      <div class="deposits-section">
        <h4>예금 상품</h4>
        <div class="view-controls">
          <button @click="showMoreDeposits" class="show-more-btn" v-if="!showAllDeposits && depositProducts.length > displayCount">
            더보기 (3개씩)
          </button>
          <button @click="showAllDeposits = true" class="view-all-btn" v-if="!showAllDeposits && depositProducts.length > displayCount">
            전체보기 (+{{ depositProducts.length - displayCount }}개)
          </button>
          <button @click="resetDepositView" class="show-less-btn" v-if="showAllDeposits || displayCount > 3">
            접기
          </button>
        </div>
        <div class="product-cards">
          <div v-for="depositProduct in displayedDepositProducts" :key="depositProduct.fin_prdt_cd" class="product-card" @click="openModal(depositProduct)">
            <h5>{{ depositProduct.fin_prdt_nm }}</h5>
            <p class="bank-name">은행: {{ depositProduct.kor_co_nm }}</p>
            <p class="interest-rate">기본금리: {{ depositProduct.intr_rate }}%</p>
            <p class="term">가입기간: {{ depositProduct.options[0]?.save_trm || '-' }}개월</p>
            <p class="max-limit">최대한도: {{ depositProduct.max_limit || '제한없음' }}</p>
            <p class="join-way">가입방법: {{ depositProduct.join_way }}</p>
            <p class="special-benefit" v-if="depositProduct.spcl_cnd">특별혜택: {{ depositProduct.spcl_cnd }}</p>
          </div>
        </div>
      </div>
      
      <div class="savings-section">
        <h4>적금 상품</h4>
        <div class="view-controls">
          <button @click="showMoreSavings" class="show-more-btn" v-if="!showAllSavings && savingProducts.length > displayCount">
            더보기 (3개씩)
          </button>
          <button @click="showAllSavings = true" class="view-all-btn" v-if="!showAllSavings && savingProducts.length > displayCount">
            전체보기 (+{{ savingProducts.length - displayCount }}개)
          </button>
          <button @click="resetSavingView" class="show-less-btn" v-if="showAllSavings || displayCount > 3">
            접기
          </button>
        </div>
        <div class="product-cards">
          <div v-for="savingProduct in displayedSavingProducts" :key="savingProduct.fin_prdt_cd" class="product-card" @click="openModal(savingProduct)">
            <h5>{{ savingProduct.fin_prdt_nm }}</h5>
            <p class="bank-name">은행: {{ savingProduct.kor_co_nm }}</p>
            <p class="interest-rate">기본금리: {{ savingProduct.intr_rate }}%</p>
            <p class="term">가입기간: {{ savingProduct.options[0]?.save_trm || '-' }}개월</p>
            <p class="max-limit">최대한도: {{ savingProduct.max_limit || '제한없음' }}</p>
            <p class="join-way">가입방법: {{ savingProduct.join_way }}</p>
            <p class="special-benefit" v-if="savingProduct.spcl_cnd">특별혜택: {{ savingProduct.spcl_cnd }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
  <FinancialProductDetailModal
    v-if="showModal"
    :product="selectedProduct"
    @close="showModal = false"
  />
</template>

<script setup>
import { useProfileStore } from '@/stores/profile'
import { onMounted, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import FinancialProductDetailModal from '@/components/Financial/FinancialProductDetailModal.vue'

const store = useProfileStore()
const router = useRouter()

const depositProducts = ref([])
const savingProducts = ref([])

const showModal = ref(false)
const selectedProduct = ref(null)

const sortOrder = ref('high')

const showAllDeposits = ref(false)
const showAllSavings = ref(false)

const displayCount = ref(3)

const getFilteredProducts = (products, type) => {
  console.log(`${type} 전체 상품:`, products)
  
  products.forEach(product => {
    console.log(`${product.fin_prdt_nm}의 save_trm 값들:`, product.options.map(opt => opt.save_trm))
  })
  
  let filteredProducts = products
  
  if (store.finalScore) {
    const score = Math.round(store.finalScore)
    console.log(`현재 점수: ${score}`)
    
    if (type === 'saving') {
      if (score >= 90) {
        filteredProducts = products.filter(p => {
          const hasLongTerm = p.options.some(opt => opt.save_trm >= 24)
          const hasPreferentialRate = p.spcl_cnd && (p.spcl_cnd.includes('우대') || p.spcl_cnd.includes('특별'))
          return hasLongTerm && hasPreferentialRate
        })
      } else if (score >= 70) {
        filteredProducts = products.filter(p => {
          return p.options.some(opt => opt.save_trm >= 12 && opt.save_trm < 24)
        })
      } else if (score >= 50) {
        filteredProducts = products.filter(p => {
          return p.options.some(opt => opt.save_trm >= 6 && opt.save_trm < 12)
        })
      } else {
        filteredProducts = products.filter(p => {
          return p.options.some(opt => opt.save_trm < 6)
        })
      }
    } else if (type === 'deposit') {
      if (score >= 90) {
        filteredProducts = products.filter(p => {
          const maxTerm = Math.max(...p.options.map(opt => opt.save_trm || 0))
          return maxTerm >= 24 // 24개월 이상의 최대 가입기간을 가진 상품만 필터링
        })
      } else if (score >= 70) {
        filteredProducts = products.filter(p => {
          const terms = p.options.map(opt => opt.save_trm || 0)
          return terms.some(term => term >= 12 && term < 24) // 12개월 이상 24개월 미만인 가입기간이 있는 상품
        })
      } else if (score >= 50) {
        filteredProducts = products.filter(p => {
          const terms = p.options.map(opt => opt.save_trm || 0)
          return terms.some(term => term >= 6 && term < 12) // 6개월 이상 12개월 미만인 가입기간이 있는 상품
        })
      } else {
        filteredProducts = products.filter(p => {
          const terms = p.options.map(opt => opt.save_trm || 0)
          return terms.some(term => term < 6) // 6개월 미만인 가입기간이 있는 상품
        })
      }
    }
  }
  
  console.log(`${type} 필터링 후 상품:`, filteredProducts)
  
  const filteredAndSorted = filteredProducts
    .filter(p => p && p.intr_rate !== undefined)
    .sort((a, b) => sortOrder.value === 'high' ? 
      (b.intr_rate || 0) - (a.intr_rate || 0) : 
      (a.intr_rate || 0) - (b.intr_rate || 0))
    
  return filteredAndSorted
}

const displayedDepositProducts = computed(() => {
  if (showAllDeposits.value) {
    return depositProducts.value
  } else {
    return depositProducts.value.slice(0, displayCount.value)
  }
})

const displayedSavingProducts = computed(() => {
  if (showAllSavings.value) {
    return savingProducts.value
  } else {
    return savingProducts.value.slice(0, displayCount.value)
  }
})

const showMoreDeposits = () => {
  displayCount.value += 3
}

const showMoreSavings = () => {
  displayCount.value += 3
}

const resetDepositView = () => {
  displayCount.value = 3
  showAllDeposits.value = false
}

const resetSavingView = () => {
  displayCount.value = 3
  showAllSavings.value = false
}

onMounted(async () => {
  try {
    // 적금 상품 데이터 가져오기
    const response_saving = await axios.get('http://127.0.0.1:8000/saving-products/')
    const allSavingProducts = response_saving.data.data.map(product => ({
      id: product.id,
      fin_prdt_nm: product.fin_prdt_nm,
      kor_co_nm: product.kor_co_nm,
      etc_note: product.etc_note,
      intr_rate: product.options[0]?.intr_rate || 0,
      join_way: product.join_way,
      join_deny: product.join_deny,
      join_member: product.join_member,
      dcls_strt_day: product.dcls_strt_day,
      dcls_month: product.dcls_month,
      fin_co_no: product.fin_co_no,
      fin_prdt_cd: product.fin_prdt_cd,
      mtrt_int: product.mtrt_int,
      spcl_cnd: product.spcl_cnd,
      max_limit: product.max_limit,
      dcls_end_day: product.dcls_end_day,
      fin_co_subm_day: product.fin_co_subm_day,
      options: product.options.map(option => ({
        id: `${product.fin_prdt_cd}-${option.save_trm}`,
        intr_rate: option.intr_rate,
        save_trm: option.save_trm,
        dcls_month: option.dcls_month,
        fin_prdt_cd: option.fin_prdt_cd,
        intr_rate_type: option.intr_rate_type,
        intr_rate_type_nm: option.intr_rate_type_nm,
        intr_rate2: option.intr_rate2,
        rsrv_type: option.rsrv_type,
        rsrv_type_nm: option.rsrv_type_nm
      }))
    }))
    savingProducts.value = getFilteredProducts(allSavingProducts, 'saving')

    // 예금 상품 데이터 가져오기
    const response_deposit = await axios.get('http://127.0.0.1:8000/deposit-products/')
    const allDepositProducts = response_deposit.data.data.map(product => ({
      id: product.id,
      fin_prdt_nm: product.fin_prdt_nm,
      kor_co_nm: product.kor_co_nm,
      etc_note: product.etc_note,
      join_way: product.join_way,
      join_deny: product.join_deny,
      join_member: product.join_member,
      dcls_strt_day: product.dcls_strt_day,
      dcls_month: product.dcls_month,
      fin_co_no: product.fin_co_no,
      fin_prdt_cd: product.fin_prdt_cd,
      mtrt_int: product.mtrt_int,
      spcl_cnd: product.spcl_cnd,
      max_limit: product.max_limit,
      dcls_end_day: product.dcls_end_day,
      fin_co_subm_day: product.fin_co_subm_day,
      intr_rate: product.options[0]?.intr_rate || 0,
      options: product.options.map(option => ({
        id: `${product.fin_prdt_cd}-${option.save_trm}`,
        intr_rate: option.intr_rate,
        save_trm: option.save_trm,
        dcls_month: option.dcls_month,
        fin_co_no: option.fin_co_no,
        fin_prdt_cd: option.fin_prdt_cd,
        intr_rate_type: option.intr_rate_type,
        intr_rate_type_nm: option.intr_rate_type_nm,
        intr_rate2: option.intr_rate2
      }))
    }))
    depositProducts.value = getFilteredProducts(allDepositProducts, 'deposit')
  } catch (error) {
    console.error('금융 상품 데이터 로딩 실패:', error)
  }
})

const moveToTest = () => {
  // 테스트 다시 시작할 때 localStorage 초기화
  localStorage.removeItem('habitScore')
  localStorage.removeItem('ageScore')
  localStorage.removeItem('incomeScore')
  localStorage.removeItem('finalScore')
  
  store.testResult = null
  store.currentView = 'test'
}

const openModal = (product) => {
  selectedProduct.value = {
    ...product,
    id: product.id,
    fin_prdt_nm: product.fin_prdt_nm,
    kor_co_nm: product.kor_co_nm,
    etc_note: product.etc_note,
    join_way: product.join_way,
    join_deny: product.join_deny,
    join_member: product.join_member,
    dcls_strt_day: product.dcls_strt_day,
    dcls_month: product.dcls_month,
    fin_co_no: product.fin_co_no,
    fin_prdt_cd: product.fin_prdt_cd,
    mtrt_int: product.mtrt_int,
    spcl_cnd: product.spcl_cnd,
    max_limit: product.max_limit,
    dcls_end_day: product.dcls_end_day,
    fin_co_subm_day: product.fin_co_subm_day,
    intr_rate: product.options[0]?.intr_rate || 0,
    bankName: product.kor_co_nm,
    productName: product.fin_prdt_nm,
    interestRate: product.intr_rate,
    joinWay: product.join_way,
    maxLimit: product.max_limit,
    specialCondition: product.spcl_cnd,
    options: product.options.map(opt => ({
      ...opt,
      id: `${product.fin_prdt_cd}-${opt.save_trm}`,
      intr_rate: opt.intr_rate,
      save_trm: opt.save_trm,
      dcls_month: opt.dcls_month,
      fin_prdt_cd: opt.fin_prdt_cd,
      intr_rate_type: opt.intr_rate_type,
      intr_rate_type_nm: opt.intr_rate_type_nm,
      intr_rate2: opt.intr_rate2,
      interestRate: opt.intr_rate,
      saveTerm: opt.save_trm
    }))
  }
  showModal.value = true
}

const sortProducts = () => {
  const sortFunction = (a, b) => {
    const rateA = a.intr_rate || 0
    const rateB = b.intr_rate || 0
    return sortOrder.value === 'high' ? rateB - rateA : rateA - rateB
  }
  
  depositProducts.value = [...depositProducts.value].sort(sortFunction)
  savingProducts.value = [...savingProducts.value].sort(sortFunction)
}
</script>

<style scoped>
.profile-result h2{
  color: #056800;
  font-weight: bold;
}


.profile-result-info {
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.profile-result-info img {
  width: 150px;
  height: auto;
}

.profile-result-info h3 {
  margin-top: 10px;
  margin-bottom: 20px;
  font-weight: bold;
}

.recommended-products {
  padding: 10px;
  border-radius: 10px;
}

.recommended-products h3{
  margin-top: 10px;
  margin-bottom: 20px;
  font-weight: bold;
}

.recommended-products li{
  font-size: 18px;
}

.recommend-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.type-description {
  display: flex;
  align-items: center;
  gap: 20px;
  margin: 25px 0;
  background-color: #e0d4222a;
  padding: 30px;
  border-radius: 10px;
}

.type-description p {
  margin: 0;
  white-space: pre-line;
  color: #000000;
  font-size: 18px;
}

.type-description img {
  width: 150px;
  height: auto;
}

.no-result {
  text-align: center;
  padding: 40px;
}

.no-result p{
  font-size: 18px;
}

.test-link {
  padding: 10px 20px;
  margin-top: 15px;
  background: linear-gradient(45deg, #86da8a, #047404) !important;
  color: white;
  border: 2px solid #128004;
  border-radius: 25px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  letter-spacing: 1.3px;
  display: inline-block;
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.test-link:hover {
  padding: 10px 20px;
  background: linear-gradient(45deg, #e9eea7, #d6e227) !important;
  color: rgb(0, 0, 0);
  border: 2px solid #989b0d;
  border-radius: 25px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  transform: translateY(-2px);
}


.test-link.retake {
  padding: 10px 20px;
  margin-top: 10px;
  background: linear-gradient(45deg, #86da8a, #047404) !important;
  color: white;
  border: 2px solid #128004;
  border-radius: 25px;
  cursor: pointer;
  font-size: 19px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  letter-spacing: 1.3px;
  margin-bottom: 10px;
}

.test-link.retake:hover {
  background-color: #5a6268;
}

.score-summary {
  margin: 20px 0;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
}

.score-details {
  margin-top: 15px;
}

.score-details p {
  margin: 10px 0;
  font-size: 16px;
}

.final-score {
  font-weight: bold;
  color: #056800;
  font-size: 18px !important;
}

.financial-products {
  margin: 20px 0;
  padding: 20px;
}

.products-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.product-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 15px;
}

.product-card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: transform 0.2s;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-card h5 {
  color: #056800;
  margin-bottom: 10px;
  font-weight: bold;
}

.product-card p {
  margin: 8px 0;
  color: #666;
  font-size: 14px;
}

.product-card .bank-name {
  color: #056800;
  font-weight: 500;
}

.product-card .interest-rate {
  color: #e74c3c;
  font-weight: bold;
}

.product-card .special-benefit {
  color: #3498db;
  font-size: 13px;
  margin-top: 12px;
  padding-top: 8px;
  border-top: 1px dashed #ddd;
}

.sort-controls {
  margin: 20px 0;
  text-align: right;
}

.sort-controls select {
  padding: 8px 16px;
  border-radius: 5px;
  border: 1px solid #ddd;
  background-color: white;
  color: #056800;
  font-size: 14px;
  cursor: pointer;
}

.sort-controls select:focus {
  outline: none;
  border-color: #056800;
}

.type-table {
  margin: 30px 0;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 10px;
}

.type-table h3 {
  color: #056800;
  margin-bottom: 20px;
  font-weight: bold;
}

.type-table table {
  width: 100%;
  border-collapse: collapse;
}

.type-table th,
.type-table td {
  padding: 10px;
  text-align: left;
}

.type-table th {
  background-color: #f0f0f0;
}

.view-controls {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  margin: 15px 0;
}

.show-more-btn,
.show-less-btn,
.view-all-btn {
  padding: 8px 15px;
  background: linear-gradient(45deg, #047404, #86da8a) !important;
  color: white;
  border: 1px solid #128004;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.show-more-btn:hover,
.show-less-btn:hover,
.view-all-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.15);
  background: linear-gradient(45deg, #086808, #98e99c) !important;
}

.show-less-btn {
  background: linear-gradient(45deg, #6c757d, #adb5bd) !important;
  border-color: #6c757d;
}

.show-less-btn:hover {
  background: linear-gradient(45deg, #5a6268, #999fa5) !important;
}
</style>