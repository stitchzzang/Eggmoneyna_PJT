import { defineStore } from 'pinia'
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export const useProfileStore = defineStore('profile', () => {
  const router = useRouter()
  
  // state를 ref로 정의
  const userInfo = ref({
    name: '',
    username: '',
    email: '',
    birth_date: '',
  })
  const products = ref([])
  const financialType = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // actions를 함수로 정의
  async function deleteAccount() {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.delete('http://127.0.0.1:8000/accounts/delete/', {
        headers: {
          Authorization: `Token ${token}`,
          'Content-Type': 'application/json',
        }
      })
      
      localStorage.removeItem('token')
      router.push('/')
      return response.data
    } catch (error) {
      console.error('회원탈퇴 실패:', error)
      throw error
    }
  }

  return {
    userInfo,
    products,
    financialType,
    loading,
    error,
    deleteAccount
  }
})