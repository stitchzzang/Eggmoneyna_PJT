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
            <!-- <span>{{ product }}</span> -->
            <span class="info-label">은행명:</span>
            <span class="info-value">{{ product.bankName }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">공시일:</span>
            <span class="info-value">{{ product.submitDate }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">상세조건:</span>
            <span class="info-value">{{ product.description }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">가입 방법:</span>
            <span class="info-value">{{ product.joinWay }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">가입 조건:</span>
            <span class="info-value">
              {{ product.joinDeny === '1' ? product.joinMember : '제한 없음' }}
            </span>
          </div>

          <hr>
          
          <h3>금리 정보</h3>
          <div class="interest-rates-grid">
            <div v-for="term in [6, 12, 24, 36]" :key="term" class="rate-info">
              <span class="term">{{ term }}개월</span>
              <span class="rate">{{ getBasicRate(term) }}%</span>
            </div>
          </div>
          
          <div class="chart-section">
            <h3>금리 비교</h3>
            <div class="chart-container">
              <Bar 
                :data="chartData" 
                :options="chartOptions"
              />
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
import { ref, computed } from 'vue'
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
)

defineEmits(['close'])

const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

console.log('Product data:', props.product)

// 현재 상품의 기본 금리
const getBasicRate = (term) => {
  const option = props.product.options?.find(opt => opt.saveTerm === term)
  return option ? Number(option.interestRate) : 0
}

// 현재 상품의 우대 금리
const getPremiumRate = (term) => {
  const option = props.product.options?.find(opt => opt.saveTerm === term)
  return option ? Number(option.intr_rate2) : 0
}

// 차트 데이터
const chartData = computed(() => {
  const selectedTerm = 12 // 12개월 기준
  
  const basicRate = getBasicRate(selectedTerm)
  const premiumRate = getPremiumRate(selectedTerm)
  const averageRate = 3.5 // 임시 평균값 (나중에 실제 평균으로 교체)

  console.log('Rates:', { basicRate, premiumRate, averageRate })

  return {
    labels: ['금리 비교'],
    datasets: [
      {
        label: '평균 금리',
        backgroundColor: 'rgba(255, 99, 132, 0.5)',
        data: [averageRate]
      },
      {
        label: '저축 금리',
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
        data: [basicRate]
      },
      {
        label: '우대 금리',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        data: [premiumRate]
      }
    ]
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: '금리 (%)'
      }
    }
  },
  plugins: {
    legend: {
      position: 'top'
    }
  }
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
  gap: 1rem;
  margin: 1rem 0;
  width: 100%;
}

.rate-info {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  min-width: 120px;
}

.term {
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.rate {
  font-size: 1.2em;
  color: #1089FF;
  font-weight: bold;
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

.info-row {
  white-space: pre-line; /* 줄바꿈을 유지하면서 텍스트를 여러 줄로 출력 */
  word-wrap: break-word; /* 긴 단어가 넘치지 않게 줄 바꿈 */
}

.chart-section {
  margin-top: 20px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
  margin-top: 15px;
}

.modal-content {
  max-height: 90vh;
  overflow-y: auto;
}

/* 모바일 반응형 */
@media (max-width: 768px) {
  .interest-rates-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

</style>
