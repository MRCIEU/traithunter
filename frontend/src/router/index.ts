import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/about",
    name: "About",
    component: () =>
      import(/* webpackChunkName: "pairwise" */ "../views/About.vue"),
  },
  {
    path: "/pairwise",
    name: "Pairwise",
    component: () =>
      import(/* webpackChunkName: "pairwise" */ "../views/Pairwise.vue"),
  },
  {
    path: "/data-explorer",
    name: "DataExplorer",
    component: () =>
      import(/* webpackChunkName: "pairwise" */ "../views/Hello.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
