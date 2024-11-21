<template>
  <div class="exchange-container">
    <h2>환율 계산기</h2>
    <p class="notice">* 엔화 / 인도네시아 루피아는 100단위, 나머지는 모두 1단위 입니다.</p>
    <div class="exchange-form">
      <!-- 입력 금액 및 통화 선택 -->
      <div class="currency-group">
        <div class="currency-select">
          <select v-model="fromCurrency">
            <option 
              v-for="rate in exchangeRates" 
              :key="rate.currency_code"
              :value="rate.currency_code"
            >
              {{ getCurrencyName(rate.currency_code) }}
            </option>
          </select>
        </div>
        <div class="amount-input">
          <input 
            type="text"
            v-model="displayAmount"
            @input="handleInput"
            placeholder="금액을 입력하세요"
            class="text-right"
          >
          <div class="currency-display">
            {{ formatKoreanReadable(amount, true) }} {{ getCurrencySymbol(fromCurrency) }}
          </div>
        </div>
      </div>

      <!-- 변환 기호 -->
      <div class="conversion-symbol">
        <span>=</span>
      </div>

      <!-- 변환 결과 -->
      <div class="currency-group">
        <div class="currency-select">
          <select v-model="toCurrency">
            <option 
              v-for="rate in exchangeRates" 
              :key="rate.currency_code"
              :value="rate.currency_code"
            >
              {{ getCurrencyName(rate.currency_code) }}
            </option>
          </select>
        </div>
        <div class="result-amount" v-if="convertedAmount">
          {{ formatNumberWithCommas(convertedAmount) }}
          <div class="currency-display">
            {{ formatKoreanReadable(convertedAmount) }} {{ getCurrencySymbol(toCurrency) }}
          </div>
        </div>
        <div class="result-amount placeholder" v-else>
          변환된 금액이 표시됩니다
        </div>
      </div>
    </div>

    <!-- 고시환율 정보 -->
    <div class="exchange-rate-info">
      <h3>은행 고시환율 ({{ getCurrentDate() }})</h3>
      <div class="rate-table">
        <div v-for="rate in mainExchangeRates" :key="rate.currency_code" class="rate-item">
          <div class="currency-name">{{ getCurrencyName(rate.currency_code) }}</div>
          <div class="rate-value">{{ formatExchangeRate(rate.rate) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UtilitiesExchange',
  data() {
    return {
      amount: '',
      fromCurrency: 'KRW',
      toCurrency: 'USD',
      convertedAmount: null,
      exchangeRates: [],  // 환율 정보를 저장할 배열
      displayAmount: '',
      mainExchangeRates: []  // 주요 통화 환율 정보 저장
    }
  },
  watch: {
    // amount, fromCurrency, toCurrency 중 어느 하나라도 변경되면 자동으로 환율 계산
    amount: {
      handler: 'convertCurrency',
      immediate: true
    },
    fromCurrency: 'convertCurrency',
    toCurrency: 'convertCurrency'
  },
  methods: {
    async getExchangeRates() {
      try {
        const response = await axios.get('/finlife/utilities/exchange/')
        this.exchangeRates = response.data.sort((a, b) => {
          const nameA = this.getCurrencyName(a.currency_code)
          const nameB = this.getCurrencyName(b.currency_code)
          return nameA.localeCompare(nameB, 'ko')
        })
        this.filterMainExchangeRates()
      } catch (error) {
        console.error('환율 정보 로드 오류:', error)
      }
    },

    convertCurrency() {
      if (!this.amount || this.amount <= 0 || !this.exchangeRates.length) {
        this.convertedAmount = null
        return
      }

      try {
        // 선택된 통화의 환율 찾기
        const fromRate = this.exchangeRates.find(rate => rate.currency_code === this.fromCurrency)?.rate.replace(',', '') || 1
        const toRate = this.exchangeRates.find(rate => rate.currency_code === this.toCurrency)?.rate.replace(',', '') || 1

        // JPY와 IDR은 100단위 처리
        let fromValue = parseFloat(fromRate)
        let toValue = parseFloat(toRate)

        if (this.fromCurrency === 'JPY(100)' || this.fromCurrency === 'IDR(100)') {
          fromValue = fromValue / 100
        }
        if (this.toCurrency === 'JPY(100)' || this.toCurrency === 'IDR(100)') {
          toValue = toValue / 100
        }

        // 수정된 환율 계산 로직
        // 1. 먼저 입력 금액을 원화로 변환
        let amountInKRW = this.amount
        if (this.fromCurrency !== 'KRW') {
          amountInKRW = this.amount * fromValue
        }

        // 2. 원화를 목표 통화로 변환
        let result = amountInKRW / toValue

        // 3. JPY나 IDR인 경우 100을 곱해줌
        if (this.toCurrency === 'JPY(100)' || this.toCurrency === 'IDR(100)') {
          result = result * 100
        }

        // 결과값 반올림 처리 (소수점 둘째자리까지)
        this.convertedAmount = Math.round(result * 100) / 100
        
      } catch (error) {
        console.error('환율 변환 오류:', error)
        alert('환율 변환 중 오류가 발생했습니다.')
      }
    },

    handleInput(e) {
      // 숫자만 추출
      let value = e.target.value.replace(/[^\d]/g, '')
      this.amount = value
      // 3자리마다 콤마 추가
      this.displayAmount = value.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
    },

    formatNumberWithCommas(value, isInput = false) {
      if (!value) return ''
      const num = parseFloat(value)
      
      // 한국 원화 입력값일 경우 소수점 제거
      if (isInput && this.fromCurrency === 'KRW') {
        return Math.floor(num).toLocaleString('ko-KR')
      }

      // 외화는 소수점 둘째자리까지 표시
      return num.toLocaleString('ko-KR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    },

    formatKoreanReadable(value, isInput = false) {
      if (!value) return ''
      const num = parseFloat(value)
      if (isNaN(num)) return ''

      // 한국 원화 입력값 처리
      if (isInput && this.fromCurrency === 'KRW') {
        if (num >= 100000000) { // 1억 이상
          const uk = Math.floor(num / 100000000)
          const man = Math.floor((num % 100000000) / 10000)
          if (man > 0) {
            return `${uk}억 ${man}천만`
          }
          return `${uk}억`
        }
        if (num >= 10000000) { // 1천만 이상
          const chunman = Math.floor(num / 10000000)
          const man = Math.floor((num % 10000000) / 10000)
          if (man > 0) {
            return `${chunman}천${man}만`
          }
          return `${chunman}천만`
        }
        if (num >= 10000) { // 1만 이상
          const man = Math.floor(num / 10000)
          const rest = Math.floor(num % 10000)
          if (rest > 0) {
            return `${man}만 ${rest.toLocaleString()}`
          }
          return `${man}만`
        }
        // 1만 미만인 경우 소수점 없이 표시
        return num.toLocaleString('ko-KR')
      }

      // 외화 결과값 처리 (기존 방식 유지)
      if (num >= 10000) {
        const man = Math.floor(num / 10000)
        const rest = (num % 10000).toFixed(2)
        if (rest > 0) {
          return `${man}만 ${rest}`
        }
        return `${man}만`
      }
      
      return num.toLocaleString('ko-KR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      })
    },

    getCurrencyName(code) {
      const currencyMap = {
        'KRW': '대한민국',
        'USD': '미국',
        'EUR': '유럽연합',
        'JPY(100)': '일본',
        'CNH': '중국',
        'HKD': '홍콩',
        'THB': '태국',
        'IDR(100)': '인도네시아',
        'AUD': '호주',
        'CAD': '캐나다',
        'CHF': '스위스',
        'GBP': '영국',
        'SGD': '싱가포르',
        'AED': '아랍에미리트',
        'BHD': '바레인',
        'BND': '브루나이',
        'DKK': '덴마크',
        'KWD': '쿠웨이트',
        'MYR': '말레이시아',
        'NOK': '노르웨이',
        'NZD': '뉴질랜드',
        'SAR': '사우디아라비아',
        'SEK': '스웨덴'
      }
      return currencyMap[code] ? `${currencyMap[code]} (${code})` : code
    },

    getCurrencySymbol(currencyCode) {
      const symbols = {
        'KRW': '원',
        'USD': '달러',
        'EUR': '유로',
        'JPY(100)': '엔',
        'CNH': '위안',
        'HKD': '달러',
        'IDR(100)': '루피아',
        'AUD': '달러',
        'CAD': '달러',
        'CHF': '프랑',
        'GBP': '파운드',
        'SGD': '달러',
        'THB': '바트',
        'AED': '디르함',
        'BHD': '디나르',
        'BND': '달러',
        'DKK': '크로네',
        'KWD': '디나르',
        'MYR': '링깃',
        'NOK': '크로네',
        'NZD': '달러',
        'SAR': '리얄',
        'SEK': '크로나'
      }
      return symbols[currencyCode] || currencyCode
    },

    formatAmount(value) {
      return new Intl.NumberFormat('ko-KR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(value)
    },

    // 현재 날짜 포맷팅
    getCurrentDate() {
      const date = new Date()
      return `${date.getFullYear()}.${String(date.getMonth() + 1).padStart(2, '0')}.${String(date.getDate()).padStart(2, '0')}`
    },


    // 환율 포맷팅
    formatExchangeRate(rate) {
      return parseFloat(rate.replace(',', '')).toLocaleString('ko-KR', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }) + ' 원'
    },

    // 주요 통화 환율 정보 필터링
    filterMainExchangeRates() {
      const mainCurrencies = ['USD', 'EUR', 'JPY(100)', 'CNH', 'GBP', 'AUD', 'CAD']
      this.mainExchangeRates = this.exchangeRates.filter(rate => 
        mainCurrencies.includes(rate.currency_code)
      )
    }
  },
  mounted() {
    this.getExchangeRates()
  }
}
</script>

<style scoped>
.exchange-container {
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  margin-top: 120px;
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
  text-align: right;
  font-weight: bold;
}

.result-amount.placeholder {
  color: #999;
  text-align: right;
  font-weight: normal;
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
  margin-bottom: 30px;
  font-size: 30px;
  font-weight: bold;
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

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}

.loading {
  text-align: center;
  color: #666;
  padding: 20px;
}

.rates-section {
  margin-top: 40px;
}

.rates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.rate-card {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.rate-card h3 {
  color: #056800;
  margin: 0 0 10px 0;
  font-size: 1.1rem;
}

.rate-card p {
  margin: 0;
  font-size: 1.2rem;
  font-weight: bold;
  color: #2c3e50;
}

.rates-title {
  color: #056800;
  text-align: center;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .rates-grid {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 15px;
  }
}

.amount-input {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.currency-display {
  font-size: 0.9em;
  color: #056800;
  margin-top: 4px;
  text-align: right;
}

.result-amount {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 200px;
  text-align: right;
  font-size: 16px;
}

.exchange-rate-info {
  margin-top: 40px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.exchange-rate-info h3 {
  color: #056800;
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.2em;
}

.rate-table {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  padding: 10px;
}

.rate-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 15px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.currency-name {
  color: #333;
  font-size: 0.9em;
}

.rate-value {
  color: #056800;
  font-weight: 500;
  font-size: 0.9em;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .rate-table {
    grid-template-columns: 1fr;
  }
  
  .rate-item {
    padding: 8px 12px;
  }
}
</style>