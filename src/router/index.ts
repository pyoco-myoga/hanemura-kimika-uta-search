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
      {
        path: "playlist-detail/:playlistId",
        name: "PlaylistDetail",
        component: () => import("@/views/PlaylistDetail.vue"),
        props: true,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
