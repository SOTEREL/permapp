import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/views/Home.vue';
import Project from '@/views/Project.vue';
import Error404 from '@/views/404.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: 'home',
    component: Home
  },
  {
    path: "/p/:id",
    name: 'project',
    component: Project
  },
  {
    path: '*',
    component: Error404
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
