<template>
  <div class="exchange-container">
    <h2>환율 계산기</h2>
    <p class="notice">* 엔화 / 인도네시아 루피아는 100단위, 나머지는 모두 1단위 입니다.</p>
    <div class="exchange-form">
      <!-- 상단 통화 -->
      <div class="currency-group">
        <div class="currency-select">
          <select id="fromCurrency" v-model="fromCurrency">
            <option value="KRW">한국 원화 (KRW)</option>
            <option value="USD">미국 달러 (USD)</option>
            <option value="EUR">유로 (EUR)</option>
            <option value="JPY">일본 엔화 (JPY)</option>
          </select>
        </div>
        <div class="amount-input">
          <input 
            type="number" 
            v-model="amount" 
            placeholder="금액을 입력하세요"
          >
        </div>
      </div>

      <!-- 중간 변환 표시 -->
      <div class="conversion-symbol">
        <span>=</span>
      </div>

      <!-- 하단 통화 -->
      <div class="currency-group">
        <div class="currency-select">
          <select id="toCurrency" v-model="toCurrency">
            <option value="USD">미국 달러 (USD)</option>
            <option value="KRW">한국 원화 (KRW)</option>
            <option value="EUR">유로 (EUR)</option>
            <option value="JPY">일본 엔화 (JPY)</option>
          </select>
        </div>
        <div class="result-amount" v-if="result">
          {{ result }}
        </div>
        <div class="result-amount placeholder" v-else>
          변환된 금액이 표시됩니다
        </div>
      </div>

      <button @click="convertCurrency" class="convert-btn">환율 계산</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UtilitiesExchange',
  data() {
    return {
      amount: '',
      fromCurrency: 'KRW',
      toCurrency: 'USD',
      result: null
    }
  },
  methods: {
    convertCurrency() {
      // TODO: API 연동 로직 구현
      console.log('환율 변환 요청:', {
        amount: this.amount,
        from: this.fromCurrency,
        to: this.toCurrency
      });
    }
  }
}
</script>

<style scoped>
.exchange-container {
  max-width: 500px;
  margin: 40px auto;
  padding: 20px;
}

.notice {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 20px;
  text-align: center;
}

.exchange-form {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.currency-group {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.currency-select {
  margin-bottom: 15px;
}

.currency-select select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  background-color: white;
}

.amount-input input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1.1rem;
  text-align: right;
}

.conversion-symbol {
  text-align: center;
  margin: 10px aut;
  font-size: 2rem;
  color: #056800;
  font-weight: bold;
}

.result-amount {
  padding: 12px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1.1rem;
  min-height: 48px;
  line-height: 24px;
  box-sizing: border-box;
  width: 100%;
}

.result-amount.placeholder {
  color: #999;
  text-align: left;
}

.convert-btn {
  width: 100%;
  padding: 15px;
  background-color: #056800;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 20px;
}

.convert-btn:hover {
  background-color: #045500;
}

h2 {
  text-align: center;
  color: #056800;
  margin-bottom: 15px;
}

/* 반응형 디자인 */
@media (max-width: 576px) {
  .exchange-container {
    padding: 10px;
  }

  .exchange-form {
    padding: 20px;
  }

  .currency-group {
    padding: 15px;
  }
}
</style>