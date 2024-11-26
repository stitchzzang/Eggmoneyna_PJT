<template>
  <div class="content">
    <div class="test-container">
      <!-- 시작 화면 -->
      <div v-if="!started" class="start-section">
        <div class="left-column">
          <img src="@/assets/test_main.png" alt="profile_test_img">
        </div>
        <div class="right-column">
          <h1>금융 성향 테스트</h1>
          <p>나의 금융 성향을 알아보고<br>맞춤형 금융 상품을 추천 받아보세요!</p>
          <button @click="startTest" class="start-btn">테스트 시작하기</button>
        </div>
      </div>

      <!-- 테스트 진행 중일 때 -->
      <div v-else-if="!testCompleted" class="question-section">
        <div class="progress-bar">
          <div :style="{ width: `${(currentQuestion + 1) * 16.67}%` }" class="progress"></div>
        </div>
        
        <h2>질문 {{ currentQuestion + 1 }}</h2>
        <p class="question">{{ questions[currentQuestion].question }}</p>
        
        <div class="options">
          <button 
            v-for="(option, index) in questions[currentQuestion].options" 
            :key="index"
            @click="selectAnswer(option.score)"
            class="option-btn"
          >
            {{ option.text }}
          </button>
        </div>
      </div>

      <!-- 테스트 완료 후 결과 화면 -->
      <div v-else class="result-section">
        <h1>당신의 금융 성향은...!</h1>
        <div class="result-type">
          <h3>{{ result.type }}</h3>
          <div class="result-image">
            <img :src="result.image" :alt="result.type">
          </div>
        </div>
        
        <div class="result-description">
          <h4>특징</h4>
          <p>{{ result.description }}</p>
        </div>
        <hr>
        <div class="recommended-products">
          <h4>추천 금융 상품</h4>
          <ul>
            <li v-for="(product, index) in result.recommendations" :key="index">
              <strong>{{ product.name }}</strong>
              <p>{{ product.description }}</p>
            </li>
          </ul>
        </div>

        <button @click="restartTest" class="restart-btn">테스트 다시하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { useRouter } from 'vue-router'

const store = useProfileStore()
const router = useRouter()

const started = ref(false)
const currentQuestion = ref(0)
const totalScore = ref(0)
const testCompleted = ref(false)
const result = ref(null)

const questions = [
  {
    question: "자주 발생하는 지출 항목은 무엇인가요?",
    options: [
      { text: "주거비, 식비, 교통비, 공과금", score: 4 },
      { text: "쇼핑, 외식, 여행, 문화생활", score: 3 },
      { text: "저축 및 투자", score: 2 },
      { text: "불규칙한 지출 (비상 지출, 갑작스러운 지출)", score: 1 }
    ]
  },
  {
    question: "월별 소득에서 얼마를 저축하고 투자하시나요?",
    options: [
      { text: "소득의 대부분을 저축하고 투자", score: 4 },
      { text: "저축은 하지만, 대부분은 소비", score: 3 },
      { text: "소비가 많고 저축은 거의 하지 않음", score: 2 },
      { text: "저축이나 투자보다는 비상 지출에 대비", score: 1 }
    ]
  },
  {
    question: "금융 상품을 선택할 때 가장 중요한 요소는 무엇인가요?",
    options: [
      { text: "안정성, 신뢰성", score: 4 },
      { text: "고정적인 금리, 예측 가능한 수익", score: 3 },
      { text: "빠른 현금화 가능성", score: 2 },
      { text: "유연한 조건과 수수료가 낮은 상품", score: 1 }
    ]
  },
  {
    question: "금융 계획을 세울 때 주로 어떤 방식으로 접근하시나요?",
    options: [
      { text: "고정적인 예산을 세워 생활비를 철저히 관리", score: 4 },
      { text: "일정 부분을 유동성 있게 소비하고 나머지는 저축", score: 3 },
      { text: "생활비와 소비를 유동적으로 조절", score: 2 },
      { text: "계획 없이 지출하고 나서야 예산을 조정", score: 1 }
    ]
  },
  {
    question: "위급 상황에서의 대처 방식은 무엇인가요?",
    options: [
      { text: "대출이나 신용카드를 사용하지 않고, 예비 자금을 사용", score: 4 },
      { text: "여유 자금이 없다면 신용카드나 대출을 고려", score: 3 },
      { text: "신용카드나 대출을 자주 이용", score: 2 },
      { text: "비상 자금이 없어 바로 대출을 받아야 함", score: 1 }
    ]
  },
  {
    question: "금융 투자에서 고려하는 위험 수준은?",
    options: [
      { text: "위험을 최소화하고 안정적인 수익을 추구", score: 4 },
      { text: "중간 정도의 위험을 감수하고 안정적인 수익을 원함", score: 3 },
      { text: "고위험 고수익을 추구", score: 2 },
      { text: "가능한 한 위험을 회피하고 유동성을 중시", score: 1 }
    ]
  }
]

const results = {
  savingKing: {
    type: "꼬꼬마 저축왕 병아리",
    image: new URL('@/assets/꼬꼬마병아리.png', import.meta.url).href,
    description: "꼼꼼하게 알뜰살뜰 예산을 관리하는 병아리처럼,\n 매일 조금씩 자금을 모으고 계획적으로 소비하는 성향!\n 작은 것 하나도 소중히 여기며 철저하게 생활비를 관리하는 스타일.",
    recommendations: [
      {
        name: "정기예금",
        description: "1년~3년 정기예금으로 안정적인 수익 추구"
      },
      {
        name: "적금",
        description: "12개월~24개월 적금으로 꾸준한 저축 습관 형성"
      },
      {
        name: "우대형 예금",
        description: "조건 충족 시 우대금리를 제공받는 안정적인 상품"
      }
    ]
  },
  stableInvestor: {
    type: "차곡차곡 알토란 병아리",
    image: new URL('@/assets/알토란병아리.png', import.meta.url).href,
    description: "투자를 통해 자산을 쌓고 재정적 안정을 추구하는 병아리.\n 알토란처럼 조금씩 쌓아 가는 자산을 중요하게 생각하며,\n 안정적이고 계획적으로 투자하는 성향!",
    recommendations: [
      {
        name: "장기 정기예금",
        description: "3년~5년 정기예금으로 높은 이율 확보"
      },
      {
        name: "장기적금",
        description: "3년~5년 적금으로 장기적인 자산 형성"
      },
      {
        name: "변동금리 예금",
        description: "시장 금리에 따라 수익률이 변동하는 상품"
      }
    ]
  },
  freeSpender: {
    type: "자유로운 깃털 병아리",
    image: new URL('@/assets/깃털병아리.png', import.meta.url).href,
    description: "날개를 펴고 자유롭게 소비를 즐기는 병아리!\n 자신의 생활을 유동적으로 조절하면서, \n때로는 과감하게, 때로는 자유롭게 지출하는 성향.\n 고위험 고수익을 추구하기도 하죠.",
    recommendations: [
      {
        name: "단기예금",
        description: "3~6개월 단기예금으로 유동성 확보"
      },
      {
        name: "머니마켓예금",
        description: "수시입출금이 자유로운 MMF형 예금"
      },
      {
        name: "일일이자예금",
        description: "매일 이자가 지급되는 유동성 높은 상품"
      }
    ]
  },
  impulsiveSpender: {
    type: "폴짝폴짝 즉흥 병아리",
    image: new URL('@/assets/즉흥병아리.png', import.meta.url).href,
    description: "계획 없이 소비하고, 자주 변동이 심한 지출을 하는 유형.\n 비상 지출에 의존하고, 대체로 즉흥적이며 유동적인 소비를 하는 스타일!",
    recommendations: [
      {
        name: "단기예금",
        description: "1~3개월 단기예금으로 급한 자금 대비"
      },
      {
        name: "자유적금",
        description: "자유로운 입출금이 가능한 적금 상"
      },
      {
        name: "자동이체 예금",
        description: "자동으로 저축되는 편리한 예금 상품"
      }
    ]
  }
}

const startTest = () => {
  started.value = true
}

const selectAnswer = (score) => {
  totalScore.value += score
  
  if (currentQuestion.value < questions.length - 1) {
    currentQuestion.value++
  } else {
    calculateResult()
  }
}

const calculateResult = () => {
  testCompleted.value = true
  const resultData = getResultType(totalScore.value)
  result.value = resultData

  // store의 setHabitScore를 호출하여 점수 저장
  store.setHabitScore(totalScore.value)
  
  // store에 테스트 결과 저장
  store.setTestResult({
    type: resultData.type,
    image: resultData.image,
    description: resultData.description,
    recommendations: resultData.recommendations,
  })
  
  // // 5초 후 추천 페이지로 이동
  // setTimeout(() => {
  //   store.currentView = 'recommend'
  // }, 5000)
}

const getResultType = (score) => {
  if (score >= 20) return results.savingKing
  if (score >= 15) return results.stableInvestor
  if (score >= 10) return results.freeSpender
  return results.impulsiveSpender
}

const restartTest = () => {
  started.value = false
  currentQuestion.value = 0
  totalScore.value = 0
  testCompleted.value = false
}
</script>

<style scoped>
.content {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.test-container {
  max-width: 800px;
  width: 100%;
  margin: 0 auto;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
  min-height: 60vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.test-container h1 {
  color: #005c02;
  margin-bottom: 20px;
  margin-top: 20px;
  text-align: center;
}

.question-section h2 {
  background-color: #037c055e;
  border-radius: 10px;
  padding: 10px;
  color: white;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);  /* 추가: 텍스트 그림자 */
  font-weight: semibold;
}

.start-section,
.question-section,
.result-section {
  width: 100%;
  max-width: 700px;
}

.start-section {
  display: grid;
  grid-template-columns: 1fr 1fr;  /* 화면을 두 개의 동일한 컬럼으로 분할 */
  gap: 20px;
  padding: 40px 20px;
  align-items: center;
  justify-content: center;
}

.left-column {
  display: flex;
  justify-content: center;
  align-items: center;
}

.right-column {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.right-column h1 {
  font-size: 2.5rem;
  font-weight: bold;
}

.right-column p {
  white-space: pre-line;
  font-size: 1.2rem;
}

.start-section img {
  max-width: 100%;
  height: auto;
  width: 300px;
  object-fit: contain;
}

.start-btn,
.restart-btn {
  padding: 10px 20px;
  margin-top: 15px;
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
}

.start-btn:hover,
.restart-btn:hover {
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

.restart-btn {
  margin-top: 10px;
  margin-bottom: 10px;
}
.progress-bar {
  width: 100%;
  height: 10px;
  background-color: #eee;
  border-radius: 5px;
  margin-bottom: 50px;
}

.progress {
  height: 100%;
  background-color: #eaec40;
  border-radius: 5px;
  transition: width 0.3s ease;
}

.question-section {
  text-align: center;
}

.question {
  font-size: 1.5rem;
  margin-top: 30px;
  margin-bottom: 30px;
}

.question p {
  font-weight: extrabold;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 15px;
  max-width: 600px;
  margin: 20px auto;
  font-size: 1.1rem;
}

.option-btn {
  padding: 15px;
  border: 2px solid #b3b3b38f;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-btn:hover {
  background: #f0ed68bd;
  border: 2px solid #a3a52b;
}

.result-section {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
}

.result-image {
  margin: 30px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.result-image img {
  width: 200px;
  height: auto;
  object-fit: contain;
}

.result-description {
  margin: 20px 0;
  padding: 20px;
  background: #f5f5f5;
  border-radius: 8px;
  margin-bottom: 30px;
}

/* 줄바꿈 허용 */
.result-description p {
  white-space: pre-line;
  margin-top: 15px;
}
.recommended-products {
  margin: 20px 0;
}

.recommended-products h4{
  margin-top: 25px;
  margin-bottom: 30px;
}

.recommended-products p{
  margin-top: 10px;
  margin-bottom: 5px;
}

.recommended-products ul {
  list-style: none;
  padding: 0;
}

.recommended-products li {
  margin-bottom: 2ch;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  text-align: left;
}

.restart-btn:hover {
  opacity: 0.9;
}

@media (max-width: 600px) {
  .test-container {
    padding: 10px;
  }
  
  .option-btn {
    padding: 12px;
    font-size: 0.9rem;
  }
}
</style>