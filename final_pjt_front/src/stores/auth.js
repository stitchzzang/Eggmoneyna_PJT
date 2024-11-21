import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: localStorage.getItem('user') || null,
    isAuthenticated: !!localStorage.getItem('token')
  }),

  getters: {
    isAuthenticated: (state) => !!state.token && !!state.user,
    username: (state) => state.user,
  },

  actions: {
    async login({ username, password }) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/accounts/login/', {
          username,
          password
        })
        
        if (response.data.key) {
          this.token = response.data.key
          this.user = username
          localStorage.setItem('token', response.data.key)
          localStorage.setItem('user', username)
          
          axios.defaults.headers.common['Authorization'] = `Token ${response.data.key}`
          return true
        }
        return false
      } catch (error) {
        console.error('Login error:', error)
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
          user: null,
          isAuthenticated: false
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
          user: null,
          isAuthenticated: false
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
          this.user = null
          localStorage.removeItem('token')
          localStorage.removeItem('user')
          return true
        }
      } catch (error) {
        console.error('회원탈퇴 실패:', error)
        throw error
      }
    }
  }
})
