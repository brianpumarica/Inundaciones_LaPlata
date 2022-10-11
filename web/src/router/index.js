import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Inundables from '../views/Inundables.vue'
import Denuncias from '../views/Denuncias.vue'
import Locations from '../views/Locations.vue'
import Inundable from '../views/Inundable.vue'
import GetDenuncias from '../views/GetDenuncias.vue'


const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  },
  {
    path: '/inundables',
    name: 'Inundables',
    component: Inundables
  },
  {
    path: '/inundable/:id',
    component: Inundable
  },
  {
    path: '/denuncias',
    name: 'denuncias',
    component: Denuncias
  }, 
  {
    path: '/locations',
    name: 'locations',
    component: Locations
  },
  {
    path: '/GetDenuncias',
    name: 'GetDenuncias',
    component: GetDenuncias
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
