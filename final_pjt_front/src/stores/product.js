import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('product', {
  state: () => ({
    subscribedProducts: [],
    products: []
  }),

  getters: {
    getAllDepositProducts: (state) => {
      return state.products.filter(product => 
        product.options[0] && !product.options[0].rsrvTypeNm
      )
    }
  },

  actions: {
    subscribeProduct(product) {
      const newSubscription = {
        ...product,
        subscribeDate: new Date().toISOString()
      }
      this.subscribedProducts.push(newSubscription)
    },

    unsubscribeProduct(productId) {
      this.subscribedProducts = this.subscribedProducts.filter(
        product => product.id !== productId
      )
    }
  }
}) 