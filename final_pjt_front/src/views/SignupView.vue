# views/SignupView.vue
<template>
  <div class="signup-container">
    <div class="logo-container">
      <img src="@/assets/eggmoneyna_logo.png" alt="eggmoneyna" class="logo-image" >
    </div>
    <h1 style="text-align: center; font-size: 24px;">회원가입</h1>
    
    <!-- 회원 유형 선택 -->
    <div class="member-type-selection">
      <button 
        :class="['type-btn', { active: formData.memberType === 'regular' }]"
        @click="changeType('regular')"
      >
        일반회원
      </button>
      <button 
        :class="['type-btn', { active: formData.memberType === 'expert' }]"
        @click="changeType('expert')"
      >
        전문가회원
      </button>
    </div>

    <form @submit.prevent="signUp" class="signup-form">
      <!-- 약관 동의 -->
      <div class="agreement-section">
        <div class="form-group checkbox">
          <input 
            type="checkbox" 
            id="allAgreement" 
            v-model="allAgreed"
            @change="toggleAllAgreements"
          >
          <label for="allAgreement">전체 동의</label>
        </div>

        <div class="agreement-divider"></div>

        <div class="form-group checkbox">
          <input 
            type="checkbox" 
            id="termsAgreement" 
            v-model="formData.termsAgreed"
            @change="checkAgreements"
            required
          >
          <label for="termsAgreement">서비스 이용약관 동의 (필수)</label>
        </div>

        <div class="form-group checkbox">
          <input 
            type="checkbox" 
            id="privacyAgreement" 
            v-model="formData.privacyAgreed"
            @change="checkAgreements"
            required
          >
          <label for="privacyAgreement">개인정보 처리방침 동의 (필수)</label>
        </div>
      </div>

      <!-- 기본 정보 -->
      <div class="form-group">
        <label for="username">아이디</label>
        <input placeholder="영문 소문자, 숫자" type="text" id="username" v-model.trim="formData.username" required>
      </div>

      <div class="form-group">
        <label for="password1">비밀번호</label>
        <input placeholder="영문 소문자, 대문자, 특수문자, 숫자" type="password" id="password1" v-model.trim="formData.password1" required>
      </div>

      <div class="form-group">
        <label for="password2">비밀번호 확인</label>
        <input v-model="formData.password2" type="password" placeholder="비밀번호 확인">
        <p v-if="formData.password2" :style="{ color: passwordMatch ? '#2196F3' : '#F44336' }">
          {{ passwordMatch ? '비밀번호가 일치합니다.' : '비밀번호가 일치하지 않습니다.' }}
        </p>
      </div>

      <div class="form-group">
        <label for="email">이메일</label>
        <input placeholder="example@site.com" type="email" id="email" v-model.trim="formData.email" required>
      </div>

      <div class="form-group">
        <label for="name">이름</label>
        <input type="text" id="name" v-model.trim="formData.name" required>
      </div>

      <div class="form-group">
        <label for="birthdate">생년월일</label>
        <input type="date" id="birthdate" v-model.trim="formData.birth_date" required>
      </div>

      <!-- 전문가 회원 추가 정보 -->
      <div v-if="formData.memberType === 'expert'" class="expert-info">
        <h5>자격증 등록</h5>
        <div class="form-group">
          <label for="certification">자격증 종류</label>
          <select id="certification" v-model="formData.certificationType" required>
            <option value="">선택하세요</option>
            <option value="CFP">CFP</option>
            <option value="CFA">CFA</option>
            <option value="CPA">CPA</option>
            <option value="FRM">FRM</option>
            <option value="ChFC">ChFC</option>
          </select>
        </div>

        <div class="form-group">
          <label for="certDate">취득일자</label>
          <input type="date" id="certDate" v-model="formData.certificationDate" required>
        </div>

        <div class="form-group">
          <label for="certNumber">자격증 번호</label>
          <input type="text" id="certNumber" v-model="formData.certificationNumber" required>
        </div>
      </div>

      <button type="submit" class="submit-btn">회원가입</button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';

const router = useRouter()
const store = useCounterStore()
const allAgreed = ref(false)

const formData = reactive({
  memberType: 'regular',
  username: '',
  password1: '',
  password2: '',
  email: '',
  name: '',
  birth_date: '',
  termsAgreed: false,
  privacyAgreed: false,

  certificationType: '',
  certificationDate: '',
  certificationNumber: '',
})

// 전체 동의 토글 함수
const toggleAllAgreements = () => {
  formData.termsAgreed = allAgreed.value
  formData.privacyAgreed = allAgreed.value
}

// 개별 약관 체크 시 전체 동의 상태 확인
const checkAgreements = () => {
  allAgreed.value = formData.termsAgreed && formData.privacyAgreed
}

// 개별 약관 변경 감지
watch([() => formData.termsAgreed, () => formData.privacyAgreed], () => {
  checkAgreements()
})


const changeType = (type) => {
  formData.memberType = type
  if (type === 'regular') {
    formData.certificationType = ''
    formData.certificationDate = ''
    formData.certificationNumber = ''
  }
}

const signUp = async function () {
  // 비밀번호 일치 여부 확인
  if (formData.password1 !== formData.password2) {
    alert('비밀번호가 일치하지 않습니다.')
    return  // 함수 실행 중단
  }

  // 날짜 형식을 YYYY-MM-DD로 변환
  const formattedBirthDate = formData.birth_date ? new Date(formData.birth_date).toISOString().split('T')[0] : null;

  const payload = {
    username: formData.username,
    password1: formData.password1,
    password2: formData.password2,
    email: formData.email,
    name: formData.name,
    birth_date: formattedBirthDate,
    member_type: formData.memberType,
    terms_agreement: formData.termsAgreed,
    privacy_agreement: formData.privacyAgreed,
  }

  // 전문가 회원인 경우 자격증 정보 추가
  if (formData.memberType === 'expert') {
    payload.certification_type = formData.certificationType;
    payload.certification_date = formData.certificationDate;
    payload.certification_number = formData.certificationNumber;
  }

  try {
    const success = await store.signUp(payload)
    if (success) {
      alert('회원가입이 완료되었습니다.')
      router.push({ name: 'LoginView' })  // 여기서 라우팅 처리
    }
  } catch (error) {
    alert('회원가입 중 오류가 발생했습니다: ' + error.message)
    console.error('회원가입 오류:', error)
  }
}

const passwordMatch = computed(() => {
  if (formData.password1 && formData.password2) {
    return formData.password1 === formData.password2
  }
  return true  // 둘 다 비어있을 때는 true 반환
})

</script>

<style scoped>
.signup-container {
  background-color: white;
  padding: 100px;
  /* border-radius: 15px; */
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  margin: 60px auto;
  border-radius: 15px;
}

.initial-selection {
  /* background-color: white; */
  padding: 40px;
  /* border-radius: 15px; */
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  gap: 20px;
  align-items: center;
  margin-top: 50px;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.member-type-selection {
  /* background-color: white; */
  padding: 15px;
  border-radius: 10px;
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  margin-top: 20px;
}

.type-btn {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  background: none;
  cursor: pointer;
}

.type-btn.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  padding: 10px;
}

.form-group label {
  font-weight: bold;
}

.form-group input,
.form-group select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.expert-info {
  background-color: #f8f9fa;
  margin-top: 20px;
  padding: 20px;
  border-radius: 10px;
  border: 1px solid #e9ecef;
}

.agreement-section {
  margin-top: 20px;
  font-size: 12px;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
}

.agreement-divider {
  height: 1px;
  background-color: #ddd;
  margin: 10px 0;
}

.checkbox {
  flex-direction: row;
  align-items: center;
  gap: 10px;
}

.checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

.checkbox label {
  cursor: pointer;
  user-select: none;
}

/* 전체 동의 강조 스타일 */
#allAgreement + label {
  font-weight: bold;
  font-size: 14px;
  color: #333;
}

.submit-btn {
  margin-top: 20px;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #45a049;
}

.logo-container {
  display: flex;  /* Flexbox 사용 */
  justify-content: center;  /* 수평 중앙 정렬 */
  align-items: center;  /* 수직 중앙 정렬 */
  margin-bottom: 20px;
}

.logo-image {
  margin-top: 10px;
  margin-right: 10px;
  height: 70px;
  width: auto;
  object-fit: contain;  /* 이미지 비율 유지 */
}
</style>