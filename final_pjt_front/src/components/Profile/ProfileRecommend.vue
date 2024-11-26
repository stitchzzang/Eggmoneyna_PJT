################  profileRecommend.vue

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
      <hr>
      <button @click="moveToTest" class="test-link retake">
        다시 테스트하기
      </button>
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
    <div class="products-container">
      <div class="deposits-section">
        <h4>예금 상품</h4>
        <div class="product-cards">
          <div v-for="product in depositProducts" :key="product.id" class="product-card">
            <h5>{{ product.fin_prdt_nm }}</h5>
            <p>은행: {{ product.kor_co_nm }}</p>
            <p>금리: {{ product.intr_rate }}%</p>
            <p>{{ product.description }}</p>
            <p>{{ product }}</p>
          </div>
        </div>
      </div>
      
      <div class="savings-section">
        <h4>적금 상품</h4>
        <div class="product-cards">
          <div v-for="product in savingProducts" :key="product.id" class="product-card">
            <h5>{{ product.fin_prdt_nm }}</h5>
            <p>은행: {{ product.kor_co_nm }}</p>
            <p>금리: {{ product.intr_rate }}%</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useProfileStore } from '@/stores/profile'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const store = useProfileStore()
const router = useRouter()

const depositProducts = ref([])
const savingProducts = ref([])

const getFilteredProducts = (products, type) => {
  // 투자 성향에 따른 필터링 로직
  let filteredProducts = products
  
  if (store.testResult) {
    switch(store.testResult.type) {
      case '안정형':
        filteredProducts = products.filter(p => p.intr_rate <= 3)
        break
      case '중립형':
        filteredProducts = products.filter(p => p.intr_rate > 3 && p.intr_rate <= 4)
        break
      case '공격형':
        filteredProducts = products.filter(p => p.intr_rate > 4)
        break
    }
  }
  
  // 상위 3개 상품만 반환
  return filteredProducts
    .sort((a, b) => b.intr_rate - a.intr_rate)
    .slice(0, 3)
}

onMounted(async () => {
  try {
    // 적금 상품 데이터 가져오기
    const response_saving = await axios.get('http://127.0.0.1:8000/saving-products/')
    const allSavingProducts = response_saving.data.data.map(product => ({
      id: product.product_code,
      fin_prdt_nm: product.product_name,
      kor_co_nm: product.bank_name,
      intr_rate: product.options[0]?.basic_rate || 0,
      description: product.product_description,
      joinWay: product.join_way,
      joinDeny: product.join_deny,
      joinMember: product.join_member,
      submitDate: product.dcls_start_day,
      options: product.options.map(option => ({
        id: `${product.product_code}-${option.save_term}`,
        interestRate: option.basic_rate,
        saveTerm: option.save_term
      }))
    }))
    savingProducts.value = getFilteredProducts(allSavingProducts, 'saving')

    // 예금 상품 데이터 가져오기
    const response_deposit = await axios.get('http://127.0.0.1:8000/deposit-products/')
    const allDepositProducts = response_deposit.data.data.map(product => ({
      id: product.product_code,
      fin_prdt_nm: product.product_name,
      kor_co_nm: product.bank_name,
      intr_rate: product.options[0]?.basic_rate || 0,
      description: product.product_description,
      joinWay: product.join_way,
      joinDeny: product.join_deny,
      joinMember: product.join_member,
      submitDate: product.dcls_start_day,
      options: product.options.map(option => ({
        id: `${product.product_code}-${option.save_term}`,
        interestRate: option.basic_rate,
        saveTerm: option.save_term
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
  max-width: 1200px;
  margin: 0 auto;
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
  background-color: #45a049;
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
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 15px;
}

.product-card {
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.product-card h5 {
  color: #056800;
  margin-bottom: 10px;
  font-weight: bold;
}

.product-card p {
  margin: 5px 0;
  color: #666;
}
</style>