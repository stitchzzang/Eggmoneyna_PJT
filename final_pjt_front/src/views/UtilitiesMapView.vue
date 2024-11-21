<template>
  <div class="map-container">
    <h2>주변 은행 찾기</h2>
    <br>
    <div class="option">
      <div class="search-container">
        <form @submit.prevent="searchPlaces">
          지역 검색: <input type="text" v-model="keyword" size="15" placeholder="지역명을 입력하세요"> 
          <button type="submit">은행 찾기</button>
          <button type="button" @click="searchNearbyBanks" class="custom-location-btn">내 주변 은행 찾기</button>
        </form>
      </div>
    </div>
    <hr>
    <div class="map_wrap">
      <div id="map" style="width:100%;height:700px;position:relative;overflow:hidden;"></div>

      <div id="menu_wrap" class="bg_white" v-show="places.length > 0">
        <ul id="placesList">
          <li v-for="(place, index) in places" :key="index" 
              class="item"
              @mouseover="displayInfowindow(markers[index], place.place_name)"
              @mouseout="closeInfowindow">
            <span :class="['markerbg', `marker_${index + 1}`]"></span>
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

  // 검색된 장소 위치를 기준으로 지도 범위를 재설정
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

.map_wrap, .map_wrap * {margin:0;padding:0;font-family:'Malgun Gothic',dotum,'돋움',sans-serif;font-size:12px;}
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
#placesList .item .info{padding:10px 0 10px 55px;}
#placesList .info .gray {color:#8a8a8a;}
#placesList .info .jibun {padding-left:26px;background:url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/places_jibun.png) no-repeat;}
#placesList .info .tel {color:#009900;}
#placesList .item .markerbg {float:left;position:absolute;width:36px; height:37px;margin:10px 0 0 10px;background:url(https://t1.daumcdn.net/localimg/localimages/07/mapapidoc/marker_number_blue.png) no-repeat;}

.marker_1 { background-position: 0 -10px; }
.marker_2 { background-position: 0 -56px; }
.marker_3 { background-position: 0 -102px }
.marker_4 { background-position: 0 -148px; }
.marker_5 { background-position: 0 -194px; }
.marker_6 { background-position: 0 -240px; }
.marker_7 { background-position: 0 -286px; }
.marker_8 { background-position: 0 -332px; }
.marker_9 { background-position: 0 -378px; }
.marker_10 { background-position: 0 -423px; }
.marker_11 { background-position: 0 -470px; }
.marker_12 { background-position: 0 -516px; }
.marker_13 { background-position: 0 -562px; }
.marker_14 { background-position: 0 -608px; }
.marker_15 { background-position: 0 -654px; }

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

</style>