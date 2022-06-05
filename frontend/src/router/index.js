import { createRouter, createWebHistory } from 'vue-router'
const routes = [
  {
    path: '/',
    component: () => import('../components/Browse.vue'),
    alias: ['/home','/browse']
  },
  {
    path: '/login',
    component: () => import('../components/Login.vue')
  },
  {
    path: '/register',
    component: () => import('../components/Register.vue')
  },
  {
    path: '/cart',
    component: () => import('../components/Cart.vue')
  },
  {
    path: '/orders',
    component: () => import('../components/OrderPage.vue')
  },
  {
    path: '/favorite',
    component: () => import('../components/Favorite.vue')
  },
  {
    path: '/setting',
    component: () => import('../components/Setting.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
