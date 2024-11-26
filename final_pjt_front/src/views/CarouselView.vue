<template>
  <div class="carousel-container">
    <div id="carouselExampleCaptions" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
        <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
      </div>
      <div class="carousel-inner">
        <div class="carousel-item active">
          <img src="@/assets/main.png" class="d-block w-100" alt="Slide 1">
        </div>
        <div class="carousel-item">
          <router-link to="/profilepage/profiletest">
            <img src="@/assets/carousel2.png" class="d-block w-100" alt="Slide 2">
          </router-link>
        </div>
        <div class="carousel-item">
          <img src="@/assets/carousel3.png" class="d-block w-100" alt="Slide 3">
        </div>
      </div>
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Carousel',
  };
</script>

<style scoped>
.carousel {
  width: 100%;
  max-width: 2000px;
  margin: 0 auto;
  padding-top: 0;
  position: relative;
  overflow: visible !important;
}

.carousel-container {
  margin-top: 0;
  padding-top: 0;
  position: relative;
  overflow: visible !important;
}

/* 각 슬라이드 */
.carousel-item {
  position: relative;
}

.carousel-item img {
  width: 100%;
  height: 700px;
  object-fit: contain;
  padding: 0;
  margin: 0;
}

/* 반응형 디자인 - 화면 크기에 맞게 조정 */
@media (max-width: 1400px) {
  .carousel-item img {
    height: 650px;
  }
  
  .carousel-caption h3 {
    font-size: 23px;
  }
}

@media (max-width: 1200px) {
  .carousel-item img {
    height: 600px;
  }
  
  .carousel-caption h3 {
    font-size: 21px;
    padding: 0 20px;  /* 좌우 여백 추가 */
  }
}

@media (max-width: 992px) {
  .carousel-item img {
    height: 500px;
  }
  
  .carousel-caption h3 {
    font-size: 19px;
    padding: 0 15px;
  }
}

@media (max-width: 768px) {
  .carousel-item img {
    height: 400px;
  }
  
  .carousel-caption h3 {
    font-size: 17px;
    padding: 0 10px;
  }
  
  .carousel-caption p {
    font-size: 14px;
  }
}

@media (max-width: 576px) {
  .carousel-item img {
    height: 300px;
  }
  
  .carousel-caption h3 {
    font-size: 15px;
    padding: 0 5px;
  }
  
  .carousel-caption p {
    font-size: 12px;
  } 
}

/* 인디케이터 스타일 */
.carousel-indicators {
  bottom: -10px;
}

.carousel-indicators button {
  background-color: #006609 !important;
  height: 12px;
  width: 12px;
  border-radius: 50%;
}

/* 이전, 다음 버튼 */
.carousel-control-prev, .carousel-control-next {
  z-index: 10;
}

.carousel-control-prev {
  left: -120px;
  opacity: 1;
}

.carousel-control-next {
  right: -120px;
  opacity: 1;
}

/* 버튼 스타일 강화 */
.carousel-control-prev-icon,
.carousel-control-next-icon {
  background-color: rgba(0, 114, 0, 0.493);
  padding: 25px;
  border-radius: 10px;
  border: 1px solid #198322;
}

/* 호버 효과 추가 */
.carousel-control-prev:hover,
.carousel-control-next:hover {
  opacity: 1;
}

/* 캐러셀 캡션 스타일 */
.carousel-caption {
  color: #202020;
  font-weight: 600;
  font-size: 30px;
  text-align: center;
  margin-bottom: 10px;
}

.carousel-caption h3 {
  font-size: 25px;
  margin-bottom: 15px;
  
}

.carousel-caption p {
  font-size: 18px;
  margin : 0 auto;
}

@media (max-width: 768px) {
  .carousel-caption {
    font-size: 16px;
  }
}

/* 링크 스타일 추가 */
.carousel-item router-link {
  cursor: pointer;
  display: block;
}

.carousel-item img:hover {
  opacity: 0.9;
  transition: opacity 0.3s ease;
}
</style>