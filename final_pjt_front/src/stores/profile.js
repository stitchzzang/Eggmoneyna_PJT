import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export const useProfileStore = defineStore('profile', () => {
  // localStorage에서 저장된 테스트 결과 불러오기
  const savedResult = localStorage.getItem('testResult')
  const testResult = ref(savedResult ? JSON.parse(savedResult) : null)
  const currentView = ref('edit')
  const userInfo = ref(null)  // 사용자 정보 저장용
  const habitScore = ref(0)
  const totalScore = ref(0)
  
  const setTotalScore = (score) => {
    totalScore.value = score
  }

  const setTestResult = async (result) => {
    testResult.value = result
    localStorage.setItem('testResult', JSON.stringify(result))
    
    // 금융성향 점수 계산 및 저장
    const score = await saveFinancialScore()
    if (score) {
      // 추천 상품 정보 추가
      const recommendations = getRecommendedProducts(score)
      testResult.value = { ...testResult.value, ...recommendations }
      localStorage.setItem('testResult', JSON.stringify(testResult.value))
    }
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

  // 사용자 정보 업데이트
  const updateUserInfo = async (updatedData) => {
    try {
      const token = localStorage.getItem('token')
      const response = await axios.put('http://127.0.0.1:8000/accounts/user/update/', updatedData, {
        headers: {
          Authorization: `Token ${token}`
        }
      })
      userInfo.value = response.data
      return response.data
    } catch (error) {
      console.error('사용자 정보 업데이트 실패:', error)
      throw error
    }
  }

  // 새로운 코드 추가
  const calculateFinancialScore = () => {
    if (!userInfo.value || !testResult.value) {
      console.log('userInfo 또는 testResult가 없습니다:', { userInfo: userInfo.value, testResult: testResult.value })
      return null
    }

    // 연령대 점수 계산
    let ageScore = 0
    const age = calculateAge(userInfo.value.birth_date)
    if (age <= 39) ageScore = 50
    else if (age >= 40 && age <= 59) ageScore = 100
    else if (age >= 60) ageScore = 75

    // 소득수준 점수 계산
    let incomeScore = 0
    switch (userInfo.value.income_level) {
      case 'low': incomeScore = 30; break
      case 'middle': incomeScore = 60; break
      case 'high': incomeScore = 100; break
      default: incomeScore = 0
    }

    // habitScore 참조 방식 수정
    const habitScoreValue = Math.round((habitScore.value / 24) * 50)

    // 최종 점수 계산
    const finalScore = Math.round(
      (ageScore * 0.2) + 
      (incomeScore * 0.3) + 
      (habitScoreValue)  // 수정된 변수 사용
    )


    return {
      ageScore,
      incomeScore,
      habitScore: habitScoreValue,  // 수정된 변수 사용
      finalScore
    }
  }


  // 만 나이 계산 함수 추가
  const calculateAge = (birthDate) => {
    const today = new Date()
    const birth = new Date(birthDate)
    let age = today.getFullYear() - birth.getFullYear()
    const monthDiff = today.getMonth() - birth.getMonth()
    
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--
    }
    return age
  }

  // 금융 상품 추천 함수 추가
  const getRecommendedProducts = (score) => {
    if (score >= 80) {
      return {
        type: '공격투자형',
        image: '/images/aggressive.png',
        description: '위험을 감수하고 높은 수익을 추구하는 투자자 유형입니다.',
        recommendations: [
          { name: '주식형 펀드', description: '높은 위험, 높은 수익을 추구하는 상품' },
          { name: '해외주식ETF', description: '글로벌 시장 투자로 높은 수익 기대' }
        ]
      }
    } else if (score >= 60) {
      return {
        type: '적극투자형',
        image: '/images/moderate.png',
        description: '적절한 위험을 감수하고 안정적인 수익을 추구하는 유형입니다.',
        recommendations: [
          { name: '혼합형 펀드', description: '중위험 중수익 추구' },
          { name: '채권형 ETF', description: '안정적인 수익 추구' }
        ]
      }
    } else {
      return {
        type: '안정추구형',
        image: '/images/conservative.png',
        description: '안전한 투자를 선호하는 보수적인 유형입니다.',
        recommendations: [
          { name: '예금/적금', description: '원금 보장형 상품' },
          { name: '국채', description: '안정적인 수익 추구' }
        ]
      }
    }
  }

  // setHabitScore 함수 추가
  const setHabitScore = (score) => {
    habitScore.value = score
  }

  return {
    testResult,
    currentView,
    userInfo,
    setTestResult,
    fetchUserInfo,
    updateUserInfo,
    calculateFinancialScore,
    ageScore: computed(() => calculateFinancialScore()?.ageScore || 0),
    incomeScore: computed(() => calculateFinancialScore()?.incomeScore || 0),
    habitScore: computed(() => calculateFinancialScore()?.habitScore || 0),
    finalScore: computed(() => calculateFinancialScore()?.finalScore || 0),
    setHabitScore,
    totalScore,
    setTotalScore
  }
})