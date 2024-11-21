<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-container">
        <div class="nav-left">
          <router-link to="/" class="logo">
            <img src="@/assets/eggmoneyna_logo.png" alt="eggmoneyna" class="logo-image">
          </router-link>

          <!-- 햄버거 버튼 (모바일에서만 보임) -->
          <button class="hamburger-btn" @click="toggleMenu" v-show="isMobile">
            <span>☰</span>
          </button>

          <!-- PC 메뉴 -->
          <div class="nav-links" v-show="!isMobile">
            <div class="nav-item">
              <router-link to="/financial-products/recommend">금융상품</router-link>
              <div class="submenu">
                <router-link to="/financial-products/recommend">상품 추천</router-link>
                <router-link to="/financial-products/all">전체 상품 조회</router-link>
              </div>
            </div>

            <div class="nav-item">
              <router-link to="/news/tips">뉴스 & 트렌드</router-link>
              <div class="submenu">
                <router-link to="/news/tips">알쓸금잡</router-link>
                <router-link to="/news/books">도서 추천</router-link>
              </div>
            </div>

            <div class="nav-item">
              <router-link to="/education/contents">교육</router-link>
              <div class="submenu">
                <router-link to="/education/contents">콘텐츠 수강</router-link>
                <router-link to="/education/terms">금융 용어</router-link>
              </div>
            </div>

            <div class="nav-item">
              <router-link to="/community">커뮤니티</router-link>
            </div>

            <div class="nav-item">
              <router-link to="/utilities/exchange">편의기능</router-link>
              <div class="submenu">
                <router-link to="/utilities/exchange">환율 조회</router-link>
                <router-link to="/utilities/findbanks">주변 은행 찾기</router-link>
              </div>
            </div>
          </div>

          <!-- 모바일 메뉴 -->
          <div class="mobile-menu" :class="{ 'active': isMenuOpen }" v-show="isMobile">
            <div class="mobile-menu-content">
              <div class="mobile-menu-item">
                <div class="menu-title" @click="toggleSubmenu('financial')">
                  <router-link to="/financial-products/recommend" @click="closeMenu">금융상품</router-link>
                  <span class="arrow">▼</span>
                </div>
                <div class="submenu" v-show="activeSubmenu === 'financial'">
                  <router-link to="/financial-products/recommend" @click="closeMenu">상품 추천</router-link>
                  <router-link to="/financial-products/all" @click="closeMenu">전체 상품 조회</router-link>
                </div>
              </div>

              <div class="mobile-menu-item">
                <div class="menu-title" @click="toggleSubmenu('news')">
                  <router-link to="/news/tips" @click="closeMenu">뉴스 & 트렌드</router-link>
                  <span class="arrow">▼</span>
                </div>
                <div class="submenu" v-show="activeSubmenu === 'news'">
                  <router-link to="/news/tips" @click="closeMenu">알쓸금잡</router-link>
                  <router-link to="/news/books" @click="closeMenu">도서 추천</router-link>
                </div>
              </div>

              <div class="mobile-menu-item">
                <div class="menu-title" @click="toggleSubmenu('education')">
                  <router-link to="/education/contents" @click="closeMenu">교육</router-link>
                  <span class="arrow">▼</span>
                </div>
                <div class="submenu" v-show="activeSubmenu === 'education'">
                  <router-link to="/education/contents" @click="closeMenu">콘텐츠 수강</router-link>
                  <router-link to="/education/terms" @click="closeMenu">금융 용어</router-link>
                </div>
              </div>

              <div class="mobile-menu-item">
                <div class="menu-title" @click="toggleSubmenu('community')">
                  <router-link to="/community" @click="closeMenu">커뮤니티</router-link>
                  <span class="arrow">▼</span>
                </div>
              </div>

              <div class="mobile-menu-item">
                <div class="menu-title" @click="toggleSubmenu('utilities')">
                  <router-link to="/utilities/exchange" @click="closeMenu">편의기능</router-link>
                  <span class="arrow">▼</span>
                </div>
                <div class="submenu" v-show="activeSubmenu === 'utilities'">
                  <router-link to="/utilities/exchange" @click="closeMenu">환율 조회</router-link>
                  <router-link to="/utilities/findbanks" @click="closeMenu">주변 은행 찾기</router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="nav-right">
          <!-- <div class="search-container">
            <input type="text" placeholder="검색" class="search-input">
            <button class="search-button">
              🔍
            </button>
          </div> -->
          
          <div v-if="auth.isAuthenticated" class="user-menu">
            <div class="user-info">
              <router-link to="/profilepage" class="username">
                <strong>🐣 {{ auth.user }}</strong> 님 안녕하세요!
              </router-link>
              <!-- <div class="greeting">안녕하세요!</div> -->
            </div>
            <button @click="logout" class="logout-button">로그아웃</button>
          </div>
          
          <div v-else class="auth-buttons">
            <RouterLink :to="{ name: 'LoginView' }" class="login-button">로그인</RouterLink>
            <RouterLink :to="{ name: 'SignupView' }" class="signup-button">회원가입</RouterLink>
          </div>
        </div>
      </div>
    </nav>
    <RouterView />
    
    <!-- 푸터 사이트맵 추가 -->
    <footer class="footer">
      <div class="footer-container">
        <div class="sitemap">
          <div class="sitemap-section">
            <h3>금융상품</h3>
            <ul>
              <li><router-link to="/financial-products/recommend">상품 추천</router-link></li>
              <li><router-link to="/financial-products/all">전체 상품 조회</router-link></li>
            </ul>
          </div>

          <div class="sitemap-section">
            <h3>뉴스 & 트렌드</h3>
            <ul>
              <li><router-link to="/news/tips">알쓸금잡</router-link></li>
              <li><router-link to="/news/books">도서 추천</router-link></li>
            </ul>
          </div>

          <div class="sitemap-section">
            <h3>교육</h3>
            <ul>
              <li><router-link to="/education/contents">콘텐츠 수강</router-link></li>
              <li><router-link to="/education/terms">금융 용어</router-link></li>
            </ul>
          </div>

          <div class="sitemap-section">
            <h3>커뮤니티</h3>
            <ul>
              <li><router-link to="/community">커뮤니티 홈</router-link></li>
            </ul>
          </div>

          <div class="sitemap-section">
            <h3>편의기능</h3>
            <ul>
              <li><router-link to="/utilities/exchange">환율 조회</router-link></li>
              <li><router-link to="/utilities/findbanks">주변 은행 찾기</router-link></li>
            </ul>
          </div>
        </div>
        
        <div class="footer-bottom">
          <p>&copy; 2024 에그머니나. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ref, onMounted, onUnmounted } from 'vue'

const auth = useAuthStore()
const router = useRouter()

// 모바일 메뉴 관련 상태 추가
const isMobile = ref(false)
const isMenuOpen = ref(false)
const activeSubmenu = ref(null)

// 화면 크기에 따른 모바일 상태 업데이트
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

// 모바일 메뉴 토글
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

// 서브메뉴 토글
const toggleSubmenu = (menuName) => {
  activeSubmenu.value = activeSubmenu.value === menuName ? null : menuName
}

// 메뉴 닫기
const closeMenu = () => {
  isMenuOpen.value = false
  activeSubmenu.value = null
}

// 컴포넌트 마운트 시 이벤트 리스너 등록
onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

// 컴포넌트 언마운트 시 이벤트 리스너 제거
onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

// isLoggedIn 대신 auth.isAuthenticated 사용
const logout = async () => {
  try {
    await auth.logout()
    router.push('/login')
    alert('로그아웃되었습니다.')
  } catch (error) {
    console.error('로그아웃 중 오류 발생:', error)
    alert('로그아웃 중 오류가 발생했습니다.')
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "Nanum Gothic", sans-serif;
  font-weight: 400;
  font-style: normal;
}

/* router-view를 위한 스타일 추가 */
#app {
  min-height: 100vh;
}

/* router-view 컨테이너에 패딩 추가 */
.router-view-container {
  padding: 5px;  /* 상단 여백 최소화 */
}

body {
  margin : 0;
  min-height: 100vh;
  background : linear-gradient(
    rgba(255, 255, 255, 0.5),
    rgb(238, 238, 157, 0.81) 40%,
    rgb(61, 171, 61, 0.63) 100%
  );
}

.navbar {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: transparent;  
  position: fixed;
  width: 100%;
  top: 10px;
  z-index: 1000;
  padding: 5px 0;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

/* 에그머니나 로고 이미지 */
.logo-image {
  height: 70px;
  width: auto;
  vertical-align: middle;
  margin-left: 10px;
}

.nav-links {
  display: flex;
  gap: 2rem;
  position: relative;
  white-space: nowrap;
}

.nav-item {
  position: relative;
  padding: 10px 0;
}

.nav-item > a {
  text-decoration: none;
  color: #000;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.submenu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: rgba(255, 255, 255, 0.534);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  padding: 10px 0;
  min-width: 150px;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-10px);
  transition: all 0.3s ease;
  z-index: 1000;
}

.nav-item:hover .submenu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.submenu a {
  display: block;
  padding: 8px 20px;
  color: #333;
  text-decoration: none;
  font-size: 0.9rem;
  transition: background-color 0.2s;
  white-space: nowrap;
}

.submenu a:hover {
  background-color: #f8f9faa2;
  color: #056800;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 3rem;
}

.search-container {
  display: flex;
  align-items: center;
  margin-right: 1rem;
}

.search-input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 20px;
  width: 250px;
  font-size: 0.9rem;
}

.search-button {
  background: none;
  border: none;
  margin-left: -40px;
  cursor: pointer;
}

.user-menu {
  display: flex;
  align-items: center;
}

.user-info {
  text-align: left;
  margin-right: 20px;
  font-size: 18px;
  background-color: #e7e7e773;
  border-radius: 20px;
  padding: 5px 10px;
}

.username {
  text-decoration: none;
  color: #333;
  font-size: 20px;
}

.username strong {
  color: #056800;
}

.greeting {
  font-size: 0.85rem;
  color: #666;
  margin-top: 2px;
}

.logout-button {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.auth-buttons {
  display: flex;
  gap: 1.5rem;
  margin-left: 1rem;
  white-space: nowrap;
  flex-wrap: nowrap;
}

.login-button, .signup-button, .logout-button {
  padding: 0.5rem 1.5rem;
  border-radius: 20px;
  text-decoration: none;
  font-weight: 600;
  white-space: nowrap;
  background-color: rgba(5, 104, 0, 1);
  color: rgb(255, 255, 255);
  border: 1px solid rgba(5, 104, 0, 1);
}

.signup-button {
  background-color: rgb(137, 179, 134);
  color:rgb(2, 48, 0);
  border: 1px solid rgb(2, 48, 0);
}

.login-button:hover, .signup-button:hover {
  opacity: 0.9;
}


/* 반응형 디자일을 위한 미디어 쿼리 수정 */
@media (max-width: 1400px) {
  .nav-container {
    max-width: 1300px;
    padding: 0 20px;
  }
  
  .nav-links, .main-menu {
    gap: 1.5rem;
  }
  
  .main-menu a {
    padding: 0.5rem 0.8rem;
  }

  .search-input {
    width: 220px;
  }

  .auth-buttons {
    gap: 1.2rem;
  }
  
  .login-button, .signup-button {
    padding: 0.5rem 1.2rem;
  }
}

@media (max-width: 1250px) {
  .nav-container {
    max-width: 1200px;
    padding: 0 20px;
  }
  
  .nav-links, .main-menu {
    gap: 1.2rem;
  }
  
  .main-menu a {
    font-size: 0.95rem;
    padding: 0.4rem 0.7rem;
  }

  .search-input {
    width: 200px;
  }

  .auth-buttons {
    gap: 1rem;
  }
  
  .login-button, .signup-button {
    padding: 0.4rem 1rem;
    font-size: 0.95rem;
  }
}

@media (max-width: 1184px) {
  .nav-container {
    max-width: 1100px;
    padding: 0 20px;
  }
  
  .nav-links, .main-menu {
    gap: 1rem;
  }
  
  .main-menu a {
    font-size: 0.9rem;
    padding: 0.4rem 0.6rem;
  }

  .search-input {
    width: 160px;
  }

  .auth-buttons {
    gap: 0.8rem;
  }
  
  .login-button, .signup-button {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 992px) {
  .nav-container {
    max-width: 950px;
    padding: 0 15px;
  }
  
  .nav-links, .main-menu {
    gap: 0.8rem;
  }
  
  .main-menu a {
    font-size: 0.85rem;
    padding: 0.3rem 0.5rem;
  }

  .search-input {
    width: 140px;
  }

  .auth-buttons {
    gap: 0.6rem;
  }
  
  .login-button, .signup-button {
    padding: 0.3rem 0.7rem;
    font-size: 0.85rem;
  }
}

@media (max-width: 900px) {
  .nav-links {
    gap: 0.5rem;
  }
  
  .nav-links a {
    font-size: 0.8rem;
    padding: 0.3rem 0.5rem;
  }
  
  .search-input {
    width: 140px;
  }
  
  .login-button, .signup-button {
    padding: 0.4rem 1rem;
  }
}

@media (max-width: 768px) {
  .navbar {
    padding: 10px 0;
  }

  .nav-container {
    flex-direction: column;
    padding: 0 10px;
  }
  
  .nav-left {
    width: 100%;
    justify-content: space-between;
  }
  
  .nav-links {
    display: flex;
    flex-wrap: wrap;  /* 줄바꿈 허용 */
    justify-content: center;
    gap: 0.5rem;
  }
  
  .nav-links a {
    font-size: 0.8rem;
    padding: 0.3rem 0.6rem;
    white-space: nowrap;  /* 텍스트 줄바꿈 방지 */
  }

  .nav-right {
    width: 100%;
    justify-content: center;
    flex-wrap: wrap;
    gap: 1rem;
  }
  
  .search-container {
    width: 100%;
    max-width: 300px;
    margin: 0.5rem 0;
  }
  
  .search-input {
    width: 100%;
  }
  
  .auth-buttons {
    margin: 0;
  }

  .nav-item {
    position: static;
  }
  
  .submenu {
    position: relative;
    box-shadow: none;
    opacity: 1;
    visibility: visible;
    transform: none;
    padding-left: 20px;
  }
}

/* 더 작은 화면을 위한 추가 미디어 쿼리 */
@media (max-width: 576px) {
  .logo-image {
    height: 60px;
  }
  
  .nav-links {
    gap: 0.3rem;
  }
  
  .nav-links a {
    font-size: 0.75rem;
    padding: 0.2rem 0.4rem;
  }
  
  .auth-buttons {
    gap: 0.8rem;
  }
  
  .login-button, .signup-button {
    padding: 0.4rem 1rem;
    font-size: 0.9rem;
  }
}

.main-menu {
  display: flex;
  gap: 2rem;
  white-space: nowrap;
  flex-wrap: nowrap;
}

.main-menu a {
  text-decoration: none;
  color: #000;
  font-weight: 600;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
  white-space: nowrap;
}

/* 반응형 조정 - 더 세밀하게 */
@media (max-width: 1400px) {
  .nav-container {
    max-width: 1300px;
  }
  
  .nav-links, .main-menu {
    gap: 1.5rem;
  }
  
  .main-menu a {
    padding: 0.5rem 0.8rem;
  }
}

@media (max-width: 1250px) {
  .nav-container {
    max-width: 1200px;
  }
  
  .nav-links, .main-menu {
    gap: 1.2rem;
  }
  
  .main-menu a {
    font-size: 0.95rem;
    padding: 0.4rem 0.7rem;
  }
}

@media (max-width: 1184px) {
  .nav-container {
    max-width: 1100px;
  }
  
  .nav-links, .main-menu {
    gap: 1rem;
  }
  
  .main-menu a {
    font-size: 0.9rem;
    padding: 0.4rem 0.6rem;
  }

  .search-input {
    width: 160px;
  }
}

@media (max-width: 992px) {
  .nav-container {
    max-width: 950px;
  }
  
  .nav-links, .main-menu {
    gap: 0.8rem;
  }
  
  .main-menu a {
    font-size: 0.85rem;
    padding: 0.3rem 0.5rem;
  }

  .search-input {
    width: 140px;
  }
}

/* 로고 크기 조정 */
@media (max-width: 1100px) {
  .logo-image {
    height: 65px;
  }
}

/* 모바일 메뉴 전환 */
@media (max-width: 768px) {
  .mobile-menu-btn {
    display: block;
  }
  
  .nav-links {
    display: none;
  }
}

.hamburger-btn {
  display: none;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 10px;
}

.mobile-menu {
  display: none;
  position: fixed;
  top: 80px;  /* navbar 높이에 맞춰 조정 */
  left: 0;
  width: 100%;
  height: calc(100vh - 80px);
  background-color: white;
  z-index: 1000;
  transform: translateX(-100%);
  transition: transform 0.3s ease;
}

.mobile-menu.active {
  transform: translateX(0);
}

.mobile-menu-content {
  padding: 20px;
  overflow-y: auto;
}

.mobile-menu-item {
  margin-bottom: 15px;
}

.menu-title {
  display: flex;
  justify-content: space-between;
  padding: 10px;
  background-color: #f8f9fa;
  cursor: pointer;
  border-radius: 5px;
}

.submenu {
  padding: 10px 20px;
}

.submenu a {
  display: block;
  padding: 10px;
  color: #333;
  text-decoration: none;
  transition: color 0.2s;
}

.submenu a:hover {
  color: #056800;
}

.arrow {
  transition: transform 0.3s;
}

.menu-title[aria-expanded="true"] .arrow {
  transform: rotate(180deg);
}

@media (max-width: 768px) {
  .hamburger-btn {
    display: block;
  }

  .mobile-menu {
    display: block;
  }

  .nav-links {
    display: none;
  }
}

/* 푸터 스타일 추가 */
.footer {
  background-color: #f8f9fa;
  padding: 40px 0;
  margin-top: auto;
}

.footer-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

.sitemap {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  margin-bottom: 30px;
}

.sitemap-section h3 {
  color: #056800;
  font-size: 1.1rem;
  margin-bottom: 15px;
  font-weight: 600;
}

.sitemap-section ul {
  list-style: none;
  padding: 0;
}

.sitemap-section ul li {
  margin-bottom: 8px;
}

.sitemap-section ul li a {
  color: #666;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}

.sitemap-section ul li a:hover {
  color: #056800;
}

.footer-bottom {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #ddd;
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .sitemap {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .sitemap {
    grid-template-columns: 1fr;
  }
}
</style>