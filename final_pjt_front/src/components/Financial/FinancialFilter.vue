<template>
  <div>
    <h4>필터링된 상품 목록</h4>
    <table class="table">
      <thead>
        <tr>
          <th>공시제출일</th>
          <th>금융회사명</th>
          <th>상품명</th>
          <th>6개월</th>
          <th>12개월</th>
          <th>24개월</th>
          <th>36개월</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredData" :key="product.id">
          <td>{{ product.dcls_month || '-' }}</td>
          <td>{{ product.bank_name || '-' }}</td>
          <td>{{ product.fin_prdt_nm || '-' }}</td>
          <td>{{ product.intr_rate_6 || '-' }}%</td>
          <td>{{ product.intr_rate_12 || '-' }}%</td>
          <td>{{ product.intr_rate_24 || '-' }}%</td>
          <td>{{ product.intr_rate_36 || '-' }}%</td>
        </tr>
      </tbody>
    </table>
    <button @click="$emit('back')" class="btn btn-primary">
      돌아가기
    </button>
  </div>
</template>

<script setup>

</script>

<style scoped>

</style>