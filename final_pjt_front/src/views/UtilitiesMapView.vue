<template>
<div class="whole">
  <div class="map-container">
    <h1>🏡 주변 은행 찾기</h1>
    <br>
    <div class="filter-container">
      <div class="filter-group">
        <label>광역시/도</label>
        <select v-model="selectedRegion" @change="updateCities" class="filter-select">
          <option value="">선택해주세요</option>
          <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
        </select>
      </div>
      
      <div class="filter-group">
        <label>시/군/구</label>
        <select v-model="selectedCity" class="filter-select">
          <option value="">선택해주세요</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
      </div>

      <div class="filter-group">
        <label>은행</label>
        <select v-model="selectedBank" class="filter-select">
          <option value="">선택해주세요</option>
          <option v-for="bank in banks" :key="bank" :value="bank">{{ bank }}</option>
        </select>
      </div>

      <button @click="searchWithFilters" class="search-btn">검색하기</button>
    </div>

    <div class="map_wrap">
      <div class="current-location-btn-wrapper">
        <button @click="searchNearbyBanks" class="current-location-btn">
          <i class="fas fa-crosshairs"></i>
          ⛯ 현 위치에서 검색
        </button>
      </div>
      
      <div id="map" style="width:100%;height:700px;position:relative;overflow:hidden;"></div>

      <div id="menu_wrap" class="bg_white" v-show="places.length > 0">
        <ul id="placesList">
          <li v-for="(place, index) in places" :key="index" 
              class="item"
              @mouseover="displayInfowindow(markers[index], place.place_name)"
              @mouseout="closeInfowindow">
            <div class="marker-number">{{ index + 1 }}</div>
            <div class="info">
              <h5>{{ place.place_name }}</h5>
              <template v-if="place.road_address_name">
                <span>{{ place.road_address_name }}</span>
                <span class="jibun gray">{{ place.address_name }}</span>
              </template>
              <span v-else>{{ place.address_name }}</span>
              <span class="tel">{{ place.phone }}</span>
            </div>
          </li>
        </ul>
        <div id="pagination">
          <a v-for="page in totalPages" 
            :key="page"
            href="#"
            :class="{ on: page === currentPage }"
            @click.prevent="goToPage(page)">
            {{ page }}
          </a>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// 상태 관리를 위한 ref 선언
const map = ref(null)
const markers = ref([])
const infowindow = ref(null)
const places = ref([])
const keyword = ref('') // 초기값 제거
const BANK_CATEGORY_CODE = 'BK9' // 은행 카테고리 코드
const ps = ref(null)
const currentPage = ref(1)
const totalPages = ref(1)
const pagination = ref(null)

// 필터링을 위한 ref 추가
const selectedRegion = ref('')
const selectedCity = ref('')
const selectedBank = ref('')
const cities = ref([])

// 광역시/도 목록
const regions = [
  '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', 
  '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', 
  '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'
]

// 은행 목록
const banks = [
  '국민은행', '신한은행', '우리은행', '하나은행', 'SC제일은행',
  '농협은행', '기업은행', '수협은행', '부산은행', '대구은행',
  '광주은행', '제주은행', '전북은행', '경남은행', '새마을금고'
]

// 지도 초기화
const initMap = () => {
  const script = document.createElement('script')
  script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_API_KEY}&libraries=services&autoload=false`
  
  script.onload = () => {
    kakao.maps.load(() => {
      const mapContainer = document.getElementById('map')
      const mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567),
        level: 3
      }

      map.value = new kakao.maps.Map(mapContainer, mapOption)
      ps.value = new kakao.maps.services.Places()
      infowindow.value = new kakao.maps.InfoWindow({ zIndex: 1 })
    })
  }
  
  document.head.appendChild(script)
}

// 장소 검색
const searchPlaces = () => {
  if (!keyword.value.trim()) {
    alert('지역명을 입력해주세요.');
    return;
  }

  // 키워드에 '은행'을 추가하여 검색
  const searchKeyword = `${keyword.value} 은행`;

  // 장소검색 객체를 통해 키워드로 장소검색을 요청
  ps.value.keywordSearch(searchKeyword, (data, status, pagination) => {
    if (status === kakao.maps.services.Status.OK) {
      // 은행 카테고리만 필터링
      const bankData = data.filter(place => place.category_group_code === BANK_CATEGORY_CODE);
      
      if (bankData.length === 0) {
        alert('해당 지역에서 은행을 찾을 수 없습니다.');
        return;
      }

      displayPlaces(bankData);
      displayPagination(pagination);
    } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
      alert('검색 결과가 존재하지 않습니다.');
    } else if (status === kakao.maps.services.Status.ERROR) {
      alert('검색 중 오류가 발생했습니다.');
    }
  }, {
    size: 15, // 한 페이지에 표시될 최대 결과 수
    useMapBounds: true
  });
};

// 검색 결과 표시 함수 수정
const displayPlaces = (placesData) => {
  const bounds = new window.kakao.maps.LatLngBounds();
  removeMarker();
  
  places.value = placesData;

  places.value.forEach((place, index) => {
    const placePosition = new window.kakao.maps.LatLng(place.y, place.x);
    const marker = addMarker(placePosition, index);
    bounds.extend(placePosition);

    window.kakao.maps.event.addListener(marker, 'mouseover', () => {
      displayInfowindow(marker, place.place_name);
    });

    window.kakao.maps.event.addListener(marker, 'mouseout', () => {
      infowindow.value.close();
    });
  });

  // 검색된 장소 위치 기준으로 지도 범위를 재설정
  map.value.setBounds(bounds);
};

// 페이지네이션 표시
const displayPagination = (paginationResult) => {
  totalPages.value = paginationResult.last
  currentPage.value = paginationResult.current
}

// 페이지 이동
const goToPage = (page) => {
  pagination.value.gotoPage(page)
}

// 마커 추가
const addMarker = (position, idx) => {
  const imageSrc = 'https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png'
  const imageSize = new window.kakao.maps.Size(36, 37)
  const imgOptions = {
    spriteSize: new window.kakao.maps.Size(36, 691),
    spriteOrigin: new window.kakao.maps.Point(0, (idx * 46) + 10),
    offset: new window.kakao.maps.Point(13, 37)
  }
  const markerImage = new window.kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions)
  const marker = new window.kakao.maps.Marker({
    position: position,
    image: markerImage
  })

  marker.setMap(map.value)
  markers.value.push(marker)
  return marker
}

// 마커 제거
const removeMarker = () => {
  markers.value.forEach(marker => marker.setMap(null))
  markers.value = []
}

// 인포윈도우 표시
const displayInfowindow = (marker, content) => {
  infowindow.value.setContent(content)
  infowindow.value.open(map.value, marker)
}

// 인포윈도우 닫기
const closeInfowindow = () => {
  infowindow.value.close()
}

// 현재 위치 찾기 및 주변 은행 검색
const searchNearbyBanks = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        
        // 현재 위치로 지도 이동
        const currentPos = new kakao.maps.LatLng(lat, lng);
        map.value.setCenter(currentPos);
        
        // 현재 위치 마커 표시
        const currentPosMarker = new kakao.maps.Marker({
          position: currentPos,
          map: map.value
        });

        // 주변 은행 검색
        ps.value.categorySearch(
          BANK_CATEGORY_CODE, 
          (data, status, pagination) => {
            if (status === kakao.maps.services.Status.OK) {
              const limitedData = data.slice(0, 15);
              displayPlaces(limitedData);
              displayPagination(pagination);
            }
          },
          {
            location: currentPos,
            radius: 2000,
            sort: kakao.maps.services.SortBy.DISTANCE
          }
        );
      },
      (error) => {
        console.error(error);
        let errorMessage = '';
        
        switch(error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 
              '위치 정보 접근이 거부되었습니다.\n' +
              '\n위치 정보를 허용하는 방법:\n' +
              '1. 브라우저 주소창 왼쪽의 자물쇠/느낌표 아이콘을 클릭\n' +
              '2. 위치 정보 접근 권한을 "허용"으로 변경\n' +
              '3. 페이지를 새로고침한 후 다시 시도해주세요.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = '위치 정보를 사용할 수 없습니다.';
            break;
          case error.TIMEOUT:
            errorMessage = '위치 정보 요청 시간이 초과되었습니다.';
            break;
          default:
            errorMessage = '알 수 없는 오류가 발생했습니다.';
            break;
        }
        
        alert(errorMessage);
      },
      {
        enableHighAccuracy: true,
        maximumAge: 0,
        timeout: 5000
      }
    );
  } else {
    alert('이 브라우저에서는 위치 정보를 지원하지 않습니다.\n다른 브라우저를 사용해주세요.');
  }
};

// 시/군/구 업데이트 함수
const updateCities = () => {
  if (selectedRegion.value === '서울특별시') {
    cities.value = ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구', '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구', '용산구', '은평구', '종로구', '중구', '중랑구']
  } else if (selectedRegion.value === '부산광역시') {
    cities.value = ['강서구', '금정구', '남구', '동구', '동래구', '부산진구', '북구', '사상구', '사하구', '서구', '수영구', '연제구', '영도구', '중구', '해운대구', '기장군']
  } else if (selectedRegion.value === '대구광역시') {
    cities.value = ['남구', '달서구', '동구', '북구', '서구', '수성구', '중구', '달성군']
  } else if (selectedRegion.value === '인천광역시') {
    cities.value = ['계양구', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '중구', '강화군', '옹진군']
  } else if (selectedRegion.value === '광주광역시') {
    cities.value = ['광산구', '남구', '동구', '북구', '서구']
  } else if (selectedRegion.value === '대전광역시') {
    cities.value = ['대덕구', '동구', '서구', '유성구', '중구']
  } else if (selectedRegion.value === '울산광역시') {
    cities.value = ['남구', '동구', '북구', '중구', '울주군']
  } else if (selectedRegion.value === '세종특별자치시') {
    cities.value = ['세종시']
  } else if (selectedRegion.value === '경기도') {
    cities.value = ['고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '동두천시', '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', '안양시', '양주시', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시', '가평군', '양평군', '여주시', '연천군']
  } else if (selectedRegion.value === '강원도') {
    cities.value = ['강릉시', '동해시', '삼척시', '속초시', '원주시', '춘천시', '태백시', '고성군', '양구군', '양양군', '영월군', '인제군', '정선군', '철원군', '평창군', '홍천군', '화천군', '횡성군']
  } else if (selectedRegion.value === '충청북도') {
    cities.value = ['제천시', '청주', '충주시', '괴산군', '단양군', '보은군', '영동군', '옥천군', '음성군', '증평군', '진천군']
  } else if (selectedRegion.value === '충청남도') {
    cities.value = ['계룡시', '공주시', '논산시', '당진시', '보령시', '서산시', '아산시', '천안시', '금산군', '부여군', '서천군', '예산군', '청양군', '태안군', '홍성군']
  } else if (selectedRegion.value === '전라북도') {
    cities.value = ['군산시', '김제시', '남원시', '익산시', '전주시', '정읍시', '고창군', '무주군', '부안군', '순창군', '완주군', '임실군', '장수군', '진안군']
  } else if (selectedRegion.value === '전라남도') {
    cities.value = ['광양시', '나주시', '목포시', '순천시', '여수시', '강진군', '고흥군', '곡성군', '구례군', '담양군', '무안군', '보성군', '신안군', '영광군', '영암군', '완도군', '장성군', '장흥군', '진도군', '함평군', '해남군', '화순군']
  } else if (selectedRegion.value === '경상북도') {
    cities.value = ['경산시', '경주시', '구미시', '김천시', '문경시', '상주시', '안동시', '영주시', '영천시', '포항시', '고령군', '군위군', '봉화군', '성주군', '영덕군', '영양군', '예천군', '울릉군', '울진군', '의성군', '청도군', '청송군', '칠곡군']
  } else if (selectedRegion.value === '경상남도') {
    cities.value = ['거제시', '김해시', '밀양시', '사천시', '양산시', '진주시', '창원시', '통영시', '거창군', '고성군', '남해군', '산청군', '의령군', '창녕군', '하동군', '함안군', '함양군', '합천군']
  } else if (selectedRegion.value === '제주특별자치도') {
    cities.value = ['제주시', '서귀포시']
  } else {
    cities.value = []
  }
  
  selectedCity.value = '' // 지역 변경시 시/군/구 선택 초기화
}

// 필터 검색 함수
const searchWithFilters = () => {
  const searchQuery = [selectedRegion.value, selectedCity.value, selectedBank.value]
    .filter(Boolean)
    .join(' ')
  
  if (!searchQuery) {
    alert('검색할 지역이나 은행을 선택해주세요.')
    return
  }

  keyword.value = searchQuery
  searchPlaces()
}

// 컴포넌트 마운트 시 지도 초기화
onMounted(() => {
  if (window.kakao && window.kakao.maps) {
    initMap()
  } else {
    initMap()
  }
})

onUnmounted(() => {
  removeMarker()
  if (infowindow.value) {
    infowindow.value.close()
  }
})
</script>

<style scoped>
.whole {
  background-color: #ffffff7a;
  border-radius: 20px;
  margin: 20px auto;
  padding: 20px;
  max-width: 90%;
  width: 1200px;
  position: relative;
  overflow: hidden;
}

h1 {
  color: #056800;
  margin-bottom: 10px;
  font-size: 30px;
  font-weight: bold;
  text-align: center;
}


.map-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.map-container form input[type="text"] {
  padding: 8px;
  margin: 0 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 300px;  
}

.info h5 {
  margin: 0;
  padding: 0;
  font-size: 13px;
  font-weight: bold;
}

.info .category {
  color: #666;
  font-size: 11px;
  margin-top: 2px;
}

input[type="text"] {
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.map-container form button {
  padding: 10px 20px;
  background: linear-gradient(45deg, #00BFA5, #00897B) !important;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  margin-left: 15px;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.map-container form button:hover {
  background: linear-gradient(45deg, #00897B, #00796B) !important;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.map-container form button:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.map_wrap, .map_wrap * {margin:0;padding:0;font-family:'Malgun Gothic',dotum,'움',sans-serif;font-size:12px;}
.map_wrap a, .map_wrap a:hover, .map_wrap a:active{color:#000;text-decoration: none;}
.map_wrap {position:relative;width:100%;height:700px;}
#menu_wrap {position:absolute;top:0;left:0;bottom:0;width:250px;margin:10px 0 30px 10px;padding:5px;overflow-y:auto;background:rgba(255, 255, 255, 0.7);z-index: 1;font-size:12px;border-radius: 10px;}
.bg_white {background:#fff;}
#menu_wrap hr {display: block; height: 1px;border: 0; border-top: 2px solid #5F5F5F;margin:3px 0;}
/* #menu_wrap .option{text-align: center;}
#menu_wrap .option p {margin:10px 0;}  
#menu_wrap .option button {margin-left:5px;} */
#map-container .option{text-align: center;}
#map-container .option p {margin:10px 0;}  
#map-container .option button {margin-left:5px;}
#placesList li {list-style: none;}
#placesList .item {position:relative;border-bottom:1px solid #888;overflow: hidden;cursor: pointer;min-height: 65px;}
#placesList .item span {display: block;margin-top:4px;}
#placesList .item h5, #placesList .item .info {text-overflow: ellipsis;overflow: hidden;white-space: nowrap;}
#placesList .item .info{padding:10px 0 10px 45px;}
#placesList .info .gray {color:#8a8a8a;}
#placesList .info .jibun {padding-left:26px;background:url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_jibun.png) no-repeat;}
#placesList .info .tel {color:#009900;}
#placesList .item .markerbg {
  float: left;
  position: absolute;
  width: 36px;
  height: 37px;
  margin: 10px 0 0 10px;
  background: url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png) no-repeat;
}

.marker-number {
  display: inline-block;
  width: 24px;
  height: 24px;
  background-color: #4AA8D8;
  color: white;
  border-radius: 50%;
  text-align: center;
  line-height: 24px;
  margin: 10px;
  font-weight: bold;
  position: absolute;
  left: 0;
  border: 1px solid black;
  text-shadow: -1px -1px 0 #000,
               1px -1px 0 #000,
               -1px 1px 0 #000,
               1px 1px 0 #000;
}

/* 각 마커별 배경 위치 설정 */
#placesList .item .markerbg.marker_1 {background-position: 0 -10px;}
#placesList .item .markerbg.marker_2 {background-position: 0 -56px;}
#placesList .item .markerbg.marker_3 {background-position: 0 -102px;}
#placesList .item .markerbg.marker_4 {background-position: 0 -148px;}
#placesList .item .markerbg.marker_5 {background-position: 0 -194px;}
#placesList .item .markerbg.marker_6 {background-position: 0 -240px;}
#placesList .item .markerbg.marker_7 {background-position: 0 -286px;}
#placesList .item .markerbg.marker_8 {background-position: 0 -332px;}
#placesList .item .markerbg.marker_9 {background-position: 0 -378px;}
#placesList .item .markerbg.marker_10 {background-position: 0 -423px;}
#placesList .item .markerbg.marker_11 {background-position: 0 -470px;}
#placesList .item .markerbg.marker_12 {background-position: 0 -516px;}
#placesList .item .markerbg.marker_13 {background-position: 0 -562px;}
#placesList .item .markerbg.marker_14 {background-position: 0 -608px;}
#placesList .item .markerbg.marker_15 {background-position: 0 -654px;}

#pagination {margin:10px auto;text-align: center;position: absolute;bottom: 0;left: 0;right: 0;padding: 10px 0;border-radius: 0 0 10px 10px;}
#pagination a {display:inline-block;margin-right:10px;}
#pagination .on {font-weight: bold; cursor: default;color:#777;}

.custom-location-btn {
  padding: 10px 20px;
  background: linear-gradient(45deg, #00BFA5, #00897B) !important;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.custom-location-btn:hover {
  background: linear-gradient(45deg, #00897B, #00796B) !important;
  
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2);
}

.custom-location-btn:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}

.search-container form {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-container {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  padding: 0 10px;
}

.filter-select {
  padding: 12px;
  border: 2px solid #ddd;
  border-radius: 8px;
  width: 100%;
  background-color: white;
  position: relative;
  color: black;
}

.filter-select option[value=""] {
  color: #999;
}

.current-location-btn-wrapper {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}

.current-location-btn {
  display: flex;
  align-items: center;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.9);
  border: none;
  border-radius: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 15px;
  font-weight: bold;
  color: #005c43;
}

.current-location-btn:hover {
  background:linear-gradient(45deg, #7de1c4, #01966c);
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.current-location-btn:active {
  transform: translateY(1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.current-location-btn i {
  color: inherit;
}

.search-btn {
  padding: 8px 20px;
  background: linear-gradient(45deg, #00BFA5, #00897B);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  position: relative;
  min-width: 200px;
  flex: 1;
  max-width: 300px;
}

.filter-group label {
  font-size: 14px;
  color: #056800;
  font-weight: bold;
  position: absolute;
  top: -8px;
  left: 10px;
  background-color: white;
  padding: 0 5px;
  z-index: 1;
}

/* 반응형 스타일 추가 */
@media screen and (max-width: 768px) {
  .whole {
    padding: 10px;
    margin: 10px auto;
  }

  .filter-group {
    min-width: 100%;
    max-width: 100%;
  }

  .map_wrap {
    height: 500px;
  }

  #menu_wrap {
    width: 200px;
  }

  .current-location-btn {
    padding: 8px 15px;
    font-size: 12px;
  }

  h1 {
    font-size: 24px;
  }
}

@media screen and (max-width: 480px) {
  .filter-container {
    gap: 10px;
  }

  #menu_wrap {
    width: 150px;
  }

  .current-location-btn {
    padding: 6px 12px;
    font-size: 11px;
  }
}

</style>