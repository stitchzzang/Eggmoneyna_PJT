<template>
  <div class="profile-quit">
    <h2>회원 탈퇴</h2>
    <hr>
    
    <div class="warning-box">
      <h3>회원탈퇴 전 안내 사항을 확인해 주세요.</h3>
      <ul>
        <li>회원탈퇴를 하시면 현재 로그인된 아이디는 사용하실 수 없습니다.</li>
        <li>가입된 금융 상품 정보가 모두 삭제됩니다.</li>
        <li>작성하신 게시물은 삭제되지 않으며, 익명처리 됩니다.</li>
        <li>탈퇴 후 개인정보는 즉시 파기됩니다.</li>
      </ul>
    </div>

    <div class="agreement-box">
      <label class="checkbox-label">
        <input 
          type="checkbox" 
          v-model="isAgreed"
          class="checkbox-input"
        >
        <span class="checkbox-text">안내 사항을 모두 확인하였으며, 이에 동의합니다.</span>
      </label>
    </div>

    <div class="button-container">
      <button 
        @click="handleQuit" 
        :disabled="!isAgreed"
        class="quit-button"
        :class="{ 'disabled': !isAgreed }"
      >
        회원 탈퇴
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const store = useProfileStore()
const auth = useAuthStore()
const router = useRouter()
const isAgreed = ref(false)

const handleQuit = async () => {
  if (!isAgreed.value) return

  if (confirm('정말로 탈퇴하시겠습니까?')) {
    try {
      const success = await auth.deleteAccount()
      if (success) {
        alert('회원탈퇴가 완료되었습니다.')
        router.push('/')
      }
    } catch (error) {
      alert('탈퇴 처리 중 오류가 발생했습니다.')
      console.error('탈퇴 처리 중 오류가 발생했습니다:', error)
    }
  }
}
</script>

<style scoped>
.profile-quit {
  max-width: 600px;
  margin: 0;
}

h2 {
  color: #343a40;
}

hr {
  margin-bottom: 30px;
}

.warning-box {
  background-color: #fff5f5;
  border: 1px solid #ffc9c9;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.warning-box h3 {
  color: #e03131;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.warning-box ul {
  list-style-type: none;
  padding: 0;
}

.warning-box li {
  color: #495057;
  margin-bottom: 0.5rem;
  padding-left: 1.2rem;
  position: relative;
}

.warning-box li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #e03131;
}

.agreement-box {
  margin: 2rem 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-input {
  margin-right: 0.8rem;
  width: 18px;
  height: 18px;
}

.checkbox-text {
  color: #495057;
  font-weight: 500;
}

.button-container {
  margin-top: 2rem;
  text-align: left;
}

.quit-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.8rem 1rem;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quit-button:hover:not(.disabled) {
  background-color: #c82333;
}

.quit-button.disabled {
  background-color: #adb5bd;
  cursor: not-allowed;
}
</style>