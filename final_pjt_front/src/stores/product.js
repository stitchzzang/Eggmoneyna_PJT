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
          productCode: product.product_code,
          bankName: product.bank_name,
          productName: product.product_name,
          productDescription: product.product_description,
          joinWay: product.join_way,
          joinDeny: product.join_deny,
          joinMember: product.join_member,
          maxLimit: product.max_limit,
          dclsStartDay: product.dcls_start_day,
          dclsEndDay: product.dcls_end_day,
          finCoSubmDay: product.fin_co_subm_day,
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