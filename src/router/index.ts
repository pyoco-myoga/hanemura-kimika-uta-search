// Composables
import {createRouter, createWebHistory} from "vue-router"

const routes = [
  {
    path: "/",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "",
        name: "Search",
        component: () => import("@/views/Search.vue"),
      },
      {
        path: "playlist",
        name: "Playlist",
        component: () => import("@/views/Playlist.vue"),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
