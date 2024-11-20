import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import UtilitiesMapView from '@/views/UtilitiesMapView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: () => import('@/views/MainPageView.vue')
    },
    {
      path: '/financial-products',
      name: 'financial-products',
      component: () => import('@/views/FinancialProductsView.vue')
    },
    {
      path: '/news/tips',
      name: 'news-tips',
      component: () => import('@/views/NewsTipsPageView.vue')
    },
    {
      path: '/news/books',
      name: 'news-books',
      component: () => import('@/views/NewsBooksPageView.vue')
    },
    {
      path: '/education',
      name: 'education',
      component: () => import('@/views/EducationPageView.vue')
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('@/views/CommunityView.vue')
    },
    {
      path: '/utilities/exchange',
      name: 'utilities-exchange',
      component: () => import('@/views/UtilitiesExchangeView.vue')
    },
    {
      path: '/utilities/findbanks',
      name: 'utilities-findbanks',
      component: UtilitiesMapView
    },
    {
      path: '/login',
      name: 'LoginView',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'SignupView',
      component: SignupView
    }
  ]
})

export default router
