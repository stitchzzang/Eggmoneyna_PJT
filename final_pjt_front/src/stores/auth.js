import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: null,
    userInfo: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    name: (state) => state.userInfo?.name || '',
  },

  actions: {
    async login({ username, password }) {
      try {
        // 로그인 요청
        const loginResponse = await axios.post('http://127.0.0.1:8000/accounts/login/', {
          username,
          password
        })
        
        if (loginResponse.data.key) {
          // 토큰 저장
          this.token = loginResponse.data.key
          localStorage.setItem('token', loginResponse.data.key)
          axios.defaults.headers.common['Authorization'] = `Token ${loginResponse.data.key}`
          
          // 사용자 상세 정보 요청
          const userResponse = await axios.get('http://127.0.0.1:8000/accounts/user/', {
            headers: {
              Authorization: `Token ${loginResponse.data.key}`
            }
          })
          
          // 사용자 정보 저장
          this.userInfo = userResponse.data
          localStorage.setItem('user', JSON.stringify(userResponse.data))
          
          return true
        }
        return false
      } catch (error) {
        console.error('로그인 에러:', error)
        throw error
      }
    },

    async logout() {
      try {
        const token = localStorage.getItem('token')
        
        // Django 서버에 로그아웃 요청
        if (token) {
          try {
            await axios({
              method: 'post',
              url: 'http://127.0.0.1:8000/accounts/logout/',
              headers: {
                'Authorization': `Token ${token}`,
                'Content-Type': 'application/json'
              },
              withCredentials: true
            })
          } catch (serverError) {
            console.warn('서버 로그아웃 실패:', serverError)
            // 서버 에러는 무시하고 계속 진행
          }
        }

        // 로컬 상태 초기화 (항상 실행)
        this.$patch({
          token: null,
          userInfo: null,
        })
        
        // 로컬 스토리지 클리어
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        
        return true
      } catch (error) {
        console.error('로그아웃 처리 중 오류:', error)
        // 에러가 발생해도 로컬 상태는 초기화
        this.$patch({
          token: null,
          userInfo: null,
        })
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        
        return true  // 로컬에서의 로그아웃은 성공으로 처리
      }
    },

    async deleteAccount() {
      try {
        const response = await axios.delete('http://127.0.0.1:8000/accounts/delete/', {
          headers: {
            Authorization: `Token ${this.token}`
          }
        })
        if (response.status === 204) {
          this.token = null
          this.userInfo = null
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          return true
        }
      } catch (error) {
        console.error('회원탈퇴 실패:', error)
        throw error
      }
    },

    async fetchUserInfo() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/accounts/user/', {
          headers: { Authorization: `Token ${this.token}` }
        })
        this.userInfo = response.data
      } catch (error) {
        console.error('사용자 정보 가져오기 실패:', error)
        throw error
      }
    }
  }
})
