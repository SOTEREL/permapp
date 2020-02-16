import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/views/Home.vue';
import Error404 from '@/views/404.vue';
import Project from '@/views/project/Root.vue';
import ProjectMap from '@/views/project/Map.vue';
import ProjectHome from '@/views/project/Home.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: 'home',
    component: Home,
  },
  {
    path: "/p/:pid",
    component: Project,
    children: [
      {
        path: '',
        name: 'project',
        component: ProjectHome,
      },
      {
        path: 'carte',
        name: 'projectMap',
        component: ProjectMap,
      },
    ],
  },
  {
    path: '*',
    component: Error404,
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
