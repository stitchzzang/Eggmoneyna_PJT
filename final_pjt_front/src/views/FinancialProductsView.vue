<template>
  <div class="whole">
    <div class="container mt-4">
      <h2>🔍 금융 상품 조회</h2>
      <!-- 상품 유형 선택 탭 -->
      <div class="product-type-tabs mb-4">
        <button 
          @click="productType = 'deposit'"
          :class="['tab-btn', { active: productType === 'deposit' }]"
        >
          정기예금
        </button>
        <button 
          @click="productType = 'saving'"
          :class="['tab-btn', { active: productType === 'saving' }]"
        >
          정기적금
        </button>
      </div>

      <!-- 컴포넌트 렌더링 -->
      <FinancialItemDeposit v-if="productType === 'deposit'" />
      <FinancialItemSaving v-else />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import FinancialItemDeposit from '@/components/Financial/FinancialItemDeposit.vue'
import FinancialItemSaving from '@/components/Financial/FinancialItemSaving.vue'

const productType = ref('deposit')
</script>

<style scoped>
.whole {
  margin: 30px 30px;
  padding: 20px;
  background-color: rgb(255, 255, 255, 0.5);
  border-radius: 20px;  
}

.whole h2 {  
  color: #056800;
  font-size: 1.8rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 30px;
}

.product-type-tabs {
  margin-top: 30px;
  display: flex;
  gap: 20px;
  justify-content: center;
}

.tab-btn {
  padding: 10px 30px;
  border: none;
  background: none;
  font-size: 1.4rem;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.tab-btn.active {
  color: #008d57;
  font-weight: bold;
  border-bottom: 2px solid #008d57;
}
</style>