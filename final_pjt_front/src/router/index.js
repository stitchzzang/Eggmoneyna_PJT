import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '@/views/MainPageView.vue'  // 메인 컴포넌트 import
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import ProfilePageView from '@/views/ProfilePageView.vue'
import ProfileTest from '@/components/Profile/ProfileTest.vue'
import ProfileRecommend from '@/components/Profile/ProfileRecommend.vue'
import ProfileEdit from '@/components/Profile/ProfileEdit.vue'

const routes = [
  {
    path: '/',
    name: 'main',
    component: MainPageView
  },
  {
    path: '/financial-products',
    name: 'financial-products',
    component: () => import('@/views/FinancialProductsView.vue')
  },
  {
    path: '/library/tips',
    name: 'library-tips',
    component: () => import('@/views/LibraryTipsPageView.vue')
  },
  {
    path: '/library/contents',
    name: 'library-contents',
    component: () => import('@/views/LibraryContentsPageView.vue')
  },
  {
    path: '/library/books',
    name: 'library-books',
    component: () => import('@/views/LibraryBooksPageView.vue')
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
    component: () => import('@/views/UtilitiesMapView.vue')
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
  },
  {
    path: '/profilepage',
    name: 'ProfilePageView',
    component: ProfilePageView,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
