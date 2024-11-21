import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: localStorage.getItem('user') || null,
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

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
