<template>
  <div class="profile-products">
    <h2>가입한 상품 보기</h2>
    <hr>
    
    <!-- 가입한 상품 목록 -->
    <div class="products-section">
      <div class="products-grid">
        <div v-for="product in productStore.subscribedProducts" 
             :key="product.id" 
             class="product-card">
          <h3>{{ product.name }}</h3>
          <div class="product-info">
            <p><strong>은행:</strong> {{ product.bankName }}</p>
            <p><strong>가입일:</strong> {{ new Date(product.subscribeDate).toLocaleDateString() }}</p>
            <p><strong>금리:</strong> {{ getMaxInterestRate(product) }}%</p>
            <button class="unsubscribe-btn" @click="handleUnsubscribe(product.id)">
              해지하기
            </button>
          </div>
        </div>
        <div v-if="!productStore.subscribedProducts.length" class="no-products">
          가입한 상품이 없습니다.
        </div>
      </div>
    </div>
    <hr>
    <!-- 금리 비교 그래프 -->
    <div v-if="productStore.subscribedProducts.length > 1" class="chart-section">
      <div class="chart-header">
        <h3>금리 비교</h3>
        <select v-model="selectedTerm" class="period-filter">
          <option value="all">전체 기간</option>
          <option value="6">6개월</option>
          <option value="12">12개월</option>
          <option value="24">24개월</option>
          <option value="36">36개월</option>
        </select>
      </div>
      <div class="chart-container">
        <Bar
          :data="chartData"
          :options="chartOptions"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useProductStore } from '@/stores/product'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'

// Chart.js 컴포넌트 등록
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const productStore = useProductStore()

const selectedTerm = ref('all')

// 선택된 기간에 따른 금리 데이터 계산
const getInterestRateForTerm = (product, term) => {
  if (term === 'all') {
    return getMaxInterestRate(product)
  }
  const termOption = product.options.find(opt => opt.saveTerm === parseInt(term))
  return termOption ? termOption.interestRate : 0
}

// 차트 데이터 수정
const chartData = computed(() => ({
  labels: productStore.subscribedProducts.map(p => p.name),
  datasets: [{
    label: `금리 (${selectedTerm.value === 'all' ? '최고' : selectedTerm.value + '개월'})`,
    data: productStore.subscribedProducts.map(p => getInterestRateForTerm(p, selectedTerm.value)),
    backgroundColor: [
      'rgba(4, 116, 4, 0.7)',
      'rgba(75, 192, 192, 0.7)',
      'rgba(175, 44, 164, 0.7)',
      'rgba(153, 102, 255, 0.7)',
      'rgba(255, 159, 64, 0.7)',
    ],
    borderColor: [
      'rgb(4, 116, 4)',
      'rgb(75, 192, 192)',
      'rgba(175, 44, 164)',
      'rgb(153, 102, 255)',
      'rgb(255, 159, 64)'
    ],
    borderWidth: 1
  }]
}))

// 차트 옵션 수정
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        usePointStyle: false,
        boxWidth: 40,
        boxHeight: 20,
        generateLabels: function(chart) {
          const datasets = chart.data.datasets;
          return datasets.map(dataset => ({
            text: dataset.label,
            fillStyle: 'white',
            strokeStyle: 'black',
            lineWidth: 1,
            hidden: !chart.isDatasetVisible(0),
            index: 0
          }));
        }
      }
    },
    title: {
      display: true,
      text: '상품별 금리 비교'
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          return `금리: ${context.raw}%`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '금리 (%)'
      }
    }
  }
}

const getMaxInterestRate = (product) => {
  return Math.max(...product.options.map(opt => opt.interestRate))
}

const handleUnsubscribe = (productId) => {
  if (confirm('정말 해지하시겠습니까?')) {
    productStore.unsubscribeProduct(productId)
    alert('상품이 해지되었습니다.')
  }
}
</script>

<style scoped>
.period-filter {
  padding: 5px;
}

.profile-products {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;  /* 전체 높이 사용 */
  display: flex;
  flex-direction: column;
}

h2 {
  color: #056800;
  font-weight: bold;
  margin-bottom: 15px;
}

/* 상품 목록 섹션 */
.products-section {
  margin-bottom: 40px;
  max-height: 400px;  /* 최대 높이 설정 */
  overflow-y: auto;  /* 스크롤 추가 */
  padding-right: 10px;  /* 스크롤바 여백 */
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);  /* 2열로 고정 */
  gap: 20px;
  margin-top: 20px;
}

/* 스크롤바 스타일링 */
.products-section::-webkit-scrollbar {
  width: 8px;
}

.products-section::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.products-section::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.products-section::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.product-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
  height: fit-content;  /* 내용에 맞게 높이 조정 */
}

.product-info {
  margin-top: 15px;
}

.product-info p {
  margin: 8px 0;
  font-size: 0.95em;
}

/* 그래프 섹션 */
.chart-section {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-top: 30px;
}

.chart-container {
  height: 400px;
  margin-top: 20px;
}

.chart-section h3 {
  color: #056800;
  font-weight: bold;
}

h3 {
  color: #000000;
  margin-bottom: 20px;
  font-size: 1.3em;
}

.unsubscribe-btn {
  background: linear-gradient(45deg, #db7a7a, #eb1c1c);
  border: 2px solid #b5221a;
  cursor: pointer;
  font-size: 16px;
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

.no-products {
  grid-column: 1 / -1;
  text-align: center;
  padding: 30px;
  color: #666;
  background-color: #f8f9fa;
  border-radius: 8px;
  font-size: 1.1em;
}

/* 반응형 디자인 수정 */
@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;  /* 모바일에서는 1열로 */
  }
  
  .products-section {
    max-height: 500px;  /* 모바일에서는 더 큰 높이 */
  }
  
  .chart-container {
    height: 300px;
  }
  
  .product-card {
    padding: 15px;
  }
}
</style>