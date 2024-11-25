import { createRouter, createWebHistory } from 'vue-router'
import MainPageView from '@/views/MainPageView.vue'  // 메인 컴포넌트 import
import LoginView from '@/views/LoginView.vue'
import SignupView from '@/views/SignupView.vue'
import ProfilePageView from '@/views/ProfilePageView.vue'
import CommunityView from '@/views/CommunityView.vue'
import CommunityDetail from '@/components/Community/CommunityDetail.vue'
import CommunityWriteForm from '@/components/Community/CommunityWriteForm.vue'
import FinancialProductsView from '@/views/FinancialProductsView.vue'
import FinancialItemDeposit from '@/components/Financial/FinancialItemDeposit.vue'
import FinancialItemSaving from '@/components/Financial/FinancialItemSaving.vue'
import ProfileTest from '@/components/Profile/ProfileTest.vue'

const routes = [
  {
    path: '/',
    name: 'main',
    component: MainPageView
  },
  {
    path: '/financial-products',
    name: 'financial-products',
    component: FinancialProductsView,
    children: [
      {
        path: 'deposit',
        name: 'deposit',
        component: FinancialItemDeposit
      },
      {
        path: 'saving',
        name: 'saving',
        component: FinancialItemSaving
      },
    ] 
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
    component: CommunityView
  },
  {
    path: '/community/:id',
    name: 'community-detail',
    component: CommunityDetail
  },
  {
    path: '/community/create',
    name: 'community-write',
    component: CommunityWriteForm
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
    meta: { requiresAuth: true },
    children: [
      {
        path: 'profiletest',
        name: 'profiletest',
        component: ProfileTest
      },
    ] 
  },
  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
