import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
const router = useRouter()

export const useCounterStore = defineStore('counter', () => {
  const threads = ref([])
  const API_URL = 'http://127.0.0.1:8000'

  // DRF로 전체 게시글 요청을 보내고 응답을 받아 
  // threads에 저장하는 함수
  const getThreads = function () {
    // localStorage에서 토큰 가져오기
    const token = localStorage.getItem('token')
    
    axios({
      method: 'get',
      url: `${API_URL}/community/`,
      headers: {
        Authorization: `Token ${token}`  // 인증 토큰 추가
      }
    })
      .then((res) => {
        // console.log(res.data)
        threads.value = res.data  // 장고가 준 데이터(res.data)를 threads에 저장
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 회원가입 요청을 보내는 함수
  const signUp = async function (payload) {
    try {
      const response = await axios.post('http://127.0.0.1:8000/accounts/signup/', payload)
      if (response.status === 201) {
        return true  // 성공 시 true 반환
      }
    } catch (error) {
      console.error('회원가입 실패:', error)
      throw error
    }
  }

  // 로그인 요청을 보내는 함수
  const logIn = async function (payload) {
    try {
      const response = await axios({
        method: 'post',
        url: `${API_URL}/accounts/login/`,
        data: {
          username: payload.username,
          password: payload.password
        },
        headers: {
          'Content-Type': 'application/json',
        }
      })
  
      // 성공 응답 처리
      if (response.data.token) {
        // 토큰 저장
        localStorage.setItem('token', response.data.token)
        
        // 상태 업데이트
        isLoggedIn.value = true
        currentUser.value = payload.username
        
        // axios 기본 설정에 토큰 추가
        axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`
        
        // 메인 페이지로 이동
        router.push('/')
        return response
      }
    } catch (error) {
      console.error('로그인 에러:', error)
      if (error.response) {
        // 서버에서 오는 에러 메시지 표시
        alert(error.response.data.error || '로그인에 실패했습니다.')
      } else {
        alert('서버와 통신 중 오류가 발생했습니다.')
      }
      throw error
    }
  }


  return { threads, API_URL, getThreads, signUp, logIn }
}, {persist: true} )
