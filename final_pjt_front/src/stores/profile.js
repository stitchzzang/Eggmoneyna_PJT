import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useProfileStore = defineStore('profile', () => {
  // localStorage에서 저장된 테스트 결과 불러오기
  const savedResult = localStorage.getItem('testResult')
  const testResult = ref(savedResult ? JSON.parse(savedResult) : null)
  const currentView = ref('edit')
  const userInfo = ref(null)  // 사용자 정보 저장용

  const setTestResult = (result) => {
    testResult.value = result
    // localStorage에 저장
    localStorage.setItem('testResult', JSON.stringify(result))
  }

  // 사용자 정보 가져오기
  const fetchUserInfo = async () => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://127.0.0.1:8000/accounts/user/', {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      userInfo.value = response.data
      return response.data
    } catch (error) {
      console.error('사용자 정보 가져오기 실패:', error)
      throw error
    }
  }

  return {
    testResult,
    currentView,
    userInfo,
    setTestResult,
    fetchUserInfo
  }
})