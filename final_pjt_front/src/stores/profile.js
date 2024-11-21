import { defineStore } from 'pinia'
import axios from 'axios'

export const useProfileStore = defineStore('profile', {
  state: () => ({
    userInfo: {
      name: '',
      username: '',
      email: '',
      birthdate: '',
    },
    products: [],
    financialType: null,
    loading: false,
    error: null
  }),

  actions: {
    async fetchUserInfo() {
      try {
        this.loading = true
        const response = await axios.get('/api/user/profile')
        this.userInfo = response.data
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },

    async updateUserInfo(userData) {
      try {
        this.loading = true
        const response = await axios.put('/api/user/profile', userData)
        this.userInfo = response.data
        return true
      } catch (error) {
        this.error = error.message
        return false
      } finally {
        this.loading = false
      }
    },

    async fetchUserProducts() {
      try {
        const response = await axios.get('/api/user/products')
        this.products = response.data
      } catch (error) {
        this.error = error.message
      }
    },

    async deleteAccount() {
      try {
        await axios.delete('/api/user/account')
        // 로그아웃 처리 및 홈페이지로 리다이렉트 로직 추가
      } catch (error) {
        this.error = error.message
      }
    }
  }
})