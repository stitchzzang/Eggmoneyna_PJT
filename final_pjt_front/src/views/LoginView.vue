<template>
  <div class="login-container">
    <div class="login-modal">
      <h1>로그인</h1>
      
      <form @submit.prevent="submitForm" class="login-form">
        <div class="form-group">
          <label for="username">ID</label>
          <input 
            type="text" 
            id="username" 
            v-model="username"
            required
          >
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <div class="password-input-container">
            <input 
              :type="showPassword ? 'text' : 'password'"
              id="password" 
              v-model="password"
              required
            >
            <span 
              class="password-toggle"
              @click="togglePassword"
            >
              {{ showPassword ? '🔒' : '👁️' }}
            </span>
          </div>
        </div>

        <button type="submit" class="login-btn">Log In</button>
      </form>
      <div class="signup-section">
        <p>아직 회원이 아니신가요?</p>
        <router-link to="/signup" class="signup-btn">Sign Up !</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'

const auth = useAuthStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const showPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const submitForm = async () => {
  try {
    const success = await auth.login({
      username: username.value,
      password: password.value
    })
    console.log('로그인 성공 여부:', success)
    console.log('현재 인증 상태:', auth.isAuthenticated)
    
    if (success) {
      const redirectPath = localStorage.getItem('redirectPath')
      if (redirectPath) {
        localStorage.removeItem('redirectPath')
        router.push(redirectPath)
      } else {
        router.push('/')
      }
    }
  } catch (error) {
    console.error('로그인 에러:', error)
    if (error.response) {
      alert(error.response.data.detail || "아이디 또는 비밀번호가 일치하지 않습니다.")
    } else {
      alert('서버에 연결할 수 없습니다.')
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 80vh;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin: 0 auto;
  padding-top: 40px; /* 세 번째 레이어 - 더 넓은 영역 */
}

.login-modal {
  background-color: rgba(154, 214, 186, 0.7);
  padding: 30px;
  border-radius: 40px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 360px;
  margin: 20px auto;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2rem;
}

.login-form {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group label {
  font-weight: 600;
  color: #333;
}

.form-group input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.password-input-container {
  position: relative;
}

.password-input-container input {
  width: 100%;
  padding-right: 40px;  /* 눈 아이콘을 위한 공간 */
}

.password-toggle {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  user-select: none;
  filter: grayscale(100%);
  opacity: 0.6;
}

.login-btn {
  transition: all 0.3s ease;
  text-decoration: none;
  padding: 10px 20px;
  background: linear-gradient(45deg, #98d49a, #338133) !important;
  color: white;
  border: 2px solid #4b9e40;
  border-radius: 25px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.login-btn:hover {
  background-color: #45a049;
}

/* 입력창 포커스 효과 */
.form-group input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

.signup-section {
  margin-top: 25px;
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.signup-section p {
  color: #000000;
  font-weight: 500;
  margin-bottom: 20px;
  font-size: 16px;
}

.signup-btn {
  text-decoration: none;
  padding: 10px 20px;
  background: linear-gradient(45deg, #0bb68b, #1adaaa) !important;
  color: white;
  border: 2px solid #0fad86;
  border-radius: 25px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}


/* 반응형 디자인 */
@media (max-width: 480px) {
  .login-modal {
    padding: 20px;
  }
}
</style>