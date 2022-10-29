import Vue from "vue";
import VueRouter, { RouteConfig } from "vue-router";
import Main from "../views/Main.vue";
import Docs from "../views/Docs.vue";
import GettingStarted from "../views/GettingStarted.vue";

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: "/",
    name: "Main",
    component: Main,
  },
  {
    path: "/getting-started",
    name: "GettingStarted",
    component: GettingStarted,
  },
  {
    path: "/docs",
    name: "Docs",
    component: Docs,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
