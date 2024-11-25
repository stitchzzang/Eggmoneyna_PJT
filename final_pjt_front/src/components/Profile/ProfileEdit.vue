<template>
  <div class="profile-edit">
    <h2>회원정보 조회/수정</h2>
    <hr>
    
    <form @submit.prevent="handleSubmit" class="edit-form">
      <!-- 이름 텍스트 -->
      <div class="info-group">
        <label>이름</label>
        <div class="info-text">{{ authStore.name }}</div>
      </div>

      <!-- 아이디 텍스트 -->
      <div class="info-group">
        <label>아이디</label>
        <div class="info-text">{{ authStore.userInfo.username }}</div>
      </div>

      <!-- 비밀번호와 비밀번호 확인 필드 -->
      <div class="form-row">
        <div class="form-group half-width">
          <label>비밀번호</label>
          <div class="password-input-container">
            <input 
              :type="showPassword ? 'text' : 'password'"
              v-model="formData.password"
            >
            <span 
              class="password-toggle"
              @click="togglePassword"
            >
              {{ showPassword ? '🔒' : '👁️' }}
            </span>
          </div>
        </div>

        <div class="form-group half-width">
          <label>비밀번호 확인</label>
          <div class="password-input-container">
            <input 
              :type="showPassword ? 'text' : 'password'"
              v-model="formData.passwordConfirm"
            >
            <span 
              class="password-toggle"
              @click="togglePassword"
            >
              {{ showPassword ? '🔒' : '👁️' }}
            </span>
          </div>
          <!-- 비밀번호 불일치 메시지 -->
          <span v-if="isEditing && formData.password && formData.passwordConfirm && !passwordsMatch" class="password-mismatch">
            비밀번호가 일치하지 않습니다.
          </span>
        </div>
      </div>

      <!-- 이메일 필드 -->
      <div class="form-group">
        <label>이메일</label>
        <input 
          type="email" 
          v-model="formData.email"
        >
      </div>

      <!-- 생년월일 필드 -->
      <div class="form-group">
        <label for="birthdate">생년월일</label>
        <input type="date" id="birthdate" v-model.trim="formData.birth_date" required>
      </div>

      <!-- 성별 선택 필드 -->
      <div class="form-group">
        <label>성별</label>
        <select v-model="formData.gender">
          <option value="M">남성</option>
          <option value="F">여성</option>
        </select>
      </div>

      <!-- 소득수준 선택 필드 -->
      <div class="form-group">
        <label>소득수준</label>
        <select v-model="formData.income_level">
          <option value="low">저소득층 (월 소득 200만원 이하)</option>
          <option value="middle">중소득층 (월 소득 200만원 ~ 700만원)</option>
          <option value="high">고소득층 (월 소득 700만원 이상)</option>
        </select>
      </div>

      <!-- 버튼 그룹 -->
      <div class="button-group">
        <template v-if="!isEditing">
          <button type="button" @click="startEditing" class="edit-btn">
            수정하기
          </button>
        </template>
        <template v-else>
          <button type="submit" class="save-btn">저장</button>
          <button type="button" @click="cancelEditing" class="cancel-btn">
            취소
          </button>
        </template>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import axios from 'axios'

const store = useProfileStore()
const authStore = useAuthStore()
const router = useRouter()
const isEditing = ref(false)
const showPassword = ref(false)

// 인증 관련 computed 속성들
const isAuthenticated = computed(() => authStore.isAuthenticated)
const name = computed(() => authStore.name || '사용자') // 기본값 설정

const formData = reactive({
  name: '',
  username: '',
  password: '',
  passwordConfirm: '',
  email: '',
  birth_date: '',
  gender: '',
  income_level: '',
  member_type: '',
})

// 사용자 정보 로딩
onMounted(async () => {
  try {
    // 토큰 확인 및 유효성 검사 강화
    const token = localStorage.getItem('token')
    if (!token) {
      alert('로그인이 필요합니다')
      router.push('/login')
      return
    }

    // 순차적으로 사용자 정보 로딩
    try {
      await authStore.fetchUserInfo()
    } catch (error) {
      if (error.response?.status === 401) {
        localStorage.removeItem('token') // 토큰 삭제
        alert('인증이 만료되었습니다. 다시 로그인해주세요.')
        router.push('/login')
        return
      }
      throw error
    }

    const userData = await store.fetchUserInfo()
    
    // 사용자 정보 업데이트
    Object.assign(formData, {
      name: authStore.name || '',
      username: userData.username || '',
      email: userData.email || '',
      birth_date: userData.birth_date || '',
      gender: userData.gender || 'M',
      income_level: userData.income_level || 'middle'
    })
  } catch (error) {
    console.error('사용자 정보 로딩 실패:', error)
    alert('사용자 정보를 불러오는데 실패했습니다.')
  }
})

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const startEditing = () => {
  isEditing.value = true
  formData.email = store.userInfo.email
  formData.birth_date = store.userInfo.birth_date
  formData.gender = store.userInfo.gender
  formData.income_level = store.userInfo.income_level
}

const cancelEditing = () => {
  isEditing.value = false
  formData.password = ''
  formData.passwordConfirm = ''
  formData.email = store.userInfo.email
  formData.birth_date = store.userInfo.birth_date
  formData.gender = store.userInfo.gender
  formData.income_level = store.userInfo.income_level
}

const handleSubmit = async () => {
  if (formData.password !== formData.passwordConfirm) {
    alert('비밀번호가 일치하지 않습니다.')
    return
  }

  // 수정된 데이터만 포함하는 객체 생성
  const updatedData = {
    email: formData.email,
    birth_date: formData.birth_date,
    gender: formData.gender,
    income_level: formData.income_level,
  }

  // 비밀번호가 입력된 경우에만 포함
  if (formData.password) {
    updatedData.password = formData.password
  }

  try {
    // store.updateUserInfo 대신 axios를 직접 사용
    const token = localStorage.getItem('token')
    await axios.put('http://127.0.0.1:8000/accounts/update/', updatedData, {
      headers: {
        Authorization: `Token ${token}`
      }
    })
    
    // 업데이트 성공 후 상태 갱신
    await store.fetchUserInfo()  // 최신 정보로 다시 불러오기
    isEditing.value = false
    formData.password = ''
    formData.passwordConfirm = ''
    alert('회원정보가 수정되었습니다.')
  } catch (error) {
    console.error('회원정보 수정 실패:', error)
    alert('회원정보 수정에 실패했습니다.')
  }
}

// 비밀번호 일치 여부 확인
const passwordsMatch = computed(() => {
  if (!formData.password || !formData.passwordConfirm) return true
  return formData.password === formData.passwordConfirm
})

// 컴포넌트 마운트 시 사용자 정보 가져오기
onMounted(async () => {
  if (authStore.isAuthenticated) {
    try {
      await authStore.fetchUserInfo()
    } catch (error) {
      console.error('사용자 정보 로딩 실패:', error)
    }
  }
})

</script>

<style scoped>
.profile-edit {
  max-width: 600px;
  margin: 0;
}

.profile-edit h2{
  color: #056800;
  font-weight: bold;
}

.edit-form {
  background-color: white;
  padding-top: 30px;
  padding-left: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  gap: 20px;
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

.disabled-input {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.password-input-container {
  position: relative;
}

.password-input-container input {
  width: 100%;
  padding-right: 40px;
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

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 5px;
}

button {
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.edit-btn, .save-btn {
  padding: 10px 20px;
  background: linear-gradient(45deg, #86da8a, #047404) !important;
  color: rgb(255, 255, 255);
  border: 2px solid #128004;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  letter-spacing: 1.3px;
}

.edit-btn:hover, .save-btn:hover {
  padding: 10px 20px;
  background: linear-gradient(45deg, #e9eea7, #d6e227) !important;
  color: rgb(0, 0, 0);
  border: 2px solid #989b0d;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.cancel-btn {
  padding: 10px 20px;
  background: linear-gradient(45deg, #a5a5a5, #4e4e4e) !important;
  color: rgb(255, 255, 255);
  border: 2px solid #363633;
  border-radius: 8px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

input:disabled {
  background-color: #f5f5f5;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 2px;
}

.half-width {
  flex: 1;
  min-width: 0; /* flex item 최소 너비 설정 */
}

.form-group {
  margin-bottom: 20px;
}

.short-input {
  width: 200px; /* 또는 원하는 너비로 조정 */
}

.info-group {
  margin-bottom: 7px;
}

.info-group label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.info-text {
  color: #000;
  font-size: 1rem;
  font-weight: extrabold;
}

.password-mismatch {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 4px;
}

select {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  background-color: white;
}

select:disabled {
  background-color: #f5f5f5;
}
</style>