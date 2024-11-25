import { defineStore } from 'pinia'

export const useProductStore = defineStore('product', {
  state: () => ({
    subscribedProducts: JSON.parse(localStorage.getItem('subscribedProducts') || '[]')
  }),
  
  actions: {
    subscribeProduct(product) {
      if (!this.subscribedProducts.some(p => p.id === product.id)) {
        this.subscribedProducts.push({
          ...product,
          subscribeDate: new Date().toISOString()
        })
        this.saveToLocalStorage()
      }
    },
    
    unsubscribeProduct(productId) {
      this.subscribedProducts = this.subscribedProducts.filter(
        p => p.id !== productId
      )
      this.saveToLocalStorage()
    },

    saveToLocalStorage() {
      localStorage.setItem('subscribedProducts', JSON.stringify(this.subscribedProducts))
    }
  }
}) 