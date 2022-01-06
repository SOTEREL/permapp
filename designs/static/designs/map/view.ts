import { createApp } from 'vue';
import ViewApp from './ViewApp.vue';

createApp(ViewApp)
  .component('map-view', ViewApp)
  .mount('#vue-app');
