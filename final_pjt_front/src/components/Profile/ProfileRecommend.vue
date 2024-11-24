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
</template>

<script setup>
import { useProfileStore } from '@/stores/profile'

const store = useProfileStore()

const moveToTest = () => {
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
}

.test-link.retake:hover {
  background-color: #5a6268;
}
</style>