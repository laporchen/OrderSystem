import { createRouter, createWebHistory } from 'vue-router'
import store from '../vuex'
const routes = [
  {
    path: '/browse',
    component: () => import('../components/Browse.vue'),
    alias: ['/home','/']
  },
  {
    path: '/store/:storeName',
    component: () => import('../components/Store.vue'),
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
  {
    path: '/myStore',
    component: () => import('../components/MyStore.vue')
  },
  {
    path: '/myOrders',
    component: () => import('../components/MyOrders.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('../components/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to) => {
  if(to.path === '/login' || to.path === '/register') {
    return;
  }
  else if(store.getters.user == null){
    router.push('/login');
  }
  const sellerPath = ["/myStore", "/myOrders","/setting"];
  const userPath = ["/browse", "/cart", "/orders", "/favorite","/store","/","/setting"];


  if(store.getters.seller === true) {
    if(sellerPath.includes(to.path)) {
      return;
    }
    else {
      router.push('/myStore');
    }
  }
  else {
    if(userPath.includes(to.path) || to.path.match(/\/store\/*/)) {
      return;
    }
    else {
      router.push('/browse');
    }
  }
})

export default router
