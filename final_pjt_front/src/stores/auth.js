import { defineStore } from 'pinia'
import axios from 'axios'

axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    userInfo: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    name: (state) => state.userInfo?.name || '',
  },

  actions: {

    async initializeAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        this.token = token
        axios.defaults.headers.common['Authorization'] = `Token ${token}`
        await this.fetchUserInfo()
      }
    },

    async fetchUserInfo() {
      try {
        if (!this.token) return null

        const response = await axios.get('http://127.0.0.1:8000/accounts/user/', {
          headers: { Authorization: `Token ${this.token}` }
        })
        
        this.userInfo = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
        return response.data
      } catch (error) {
        console.error('사용자 정보 로딩 실패:', error)
        if (error.response?.status === 401) {
          this.logout()
        }
        throw error

      }
    },

    async login({ username, password }) {
      try {
        const response = await axios.post('http://127.0.0.1:8000/accounts/login/', {
          username,
          password
        })
        
        if (response.data.key) {
          this.token = response.data.key
          localStorage.setItem('token', response.data.key)
          axios.defaults.headers.common['Authorization'] = `Token ${response.data.key}`
          
          await this.fetchUserInfo()
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
        if (this.token) {
          await axios.post('http://127.0.0.1:8000/accounts/logout/')
        }
      } catch (error) {
        console.warn('로그아웃 에러:', error)
      } finally {
        this.token = null
        this.userInfo = null
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        delete axios.defaults.headers.common['Authorization']
      }
    },

    async deleteAccount() {
      try {
        if (this.token) {
          await axios.delete('http://127.0.0.1:8000/accounts/delete/')
          // 계정 삭제 후 로그아웃 처리
          await this.logout()
          return true
        }
        return false
      } catch (error) {
        console.error('계정 삭제 실패:', error)
        throw error
      }
    }
  }
})
