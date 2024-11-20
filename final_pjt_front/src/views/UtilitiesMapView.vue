<template>
  <div class="map-container">
    <h2>주변 은행 찾기</h2>
    <div class="search-box">
      <input 
        type="text" 
        v-model="searchQuery" 
        placeholder="지역을 입력하세요"
        @keyup.enter="searchLocation"
      >
      <button @click="searchLocation" class="search-btn">검색</button>
    </div>
    <div id="map" class="map"></div>
    <div v-if="banks.length" class="bank-list">
      <h3>주변 은행 목록</h3>
      <ul>
        <li v-for="bank in banks" :key="bank.id" class="bank-item">
          <h4>{{ bank.name }}</h4>
          <p>{{ bank.address }}</p>
          <p>{{ bank.distance }}m</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UtilitiesMap',
  data() {
    return {
      searchQuery: '',
      banks: [],
      map: null
    }
  },
  mounted() {
    // TODO: 카카오맵 또는 네이버맵 API 초기화
    this.initializeMap();
  },
  methods: {
    initializeMap() {
      // TODO: 지도 초기화 로직 구현
      console.log('지도 초기화');
    },
    searchLocation() {
      // TODO: 위치 검색 및 주변 은행 검색 로직 구현
      console.log('위치 검색:', this.searchQuery);
    }
  }
}
</script>

<style scoped>
.map-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.search-box input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-btn {
  padding: 10px 20px;
  background-color: #056800;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.search-btn:hover {
  background-color: #045500;
}

.map {
  width: 100%;
  height: 400px;
  background-color: #f5f5f5;
  margin-bottom: 20px;
  border-radius: 8px;
}

.bank-list {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.bank-item {
  padding: 15px;
  border-bottom: 1px solid #eee;
}

.bank-item:last-child {
  border-bottom: none;
}

.bank-item h4 {
  color: #056800;
  margin-bottom: 5px;
}

.bank-item p {
  color: #666;
  margin: 5px 0;
}
</style>