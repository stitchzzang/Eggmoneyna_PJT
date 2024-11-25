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
            <span class="info-label">은행명:</span>
            <span class="info-value">{{ product.bankName }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">공시일:</span>
            <span class="info-value">{{ product.submitDate }}</span>
          </div>
          
          <h3>금리 정보</h3>
          <div class="interest-rates-grid">
            <div v-for="term in [6, 12, 24, 36]" :key="term" class="rate-info">
              <span class="term">{{ term }}개월</span>
              <span class="rate">{{ getInterestRate(product, term) }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    required: true
  }
})

const getInterestRate = (product, term) => {
  const option = product.options.find(opt => opt.saveTerm === term)
  return option ? option.interestRate : '-'
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
  gap: 15px;
  margin-top: 10px;
}

.rate-info {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.term {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.rate {
  color: #047404;
  font-size: 1.2em;
}
</style>
