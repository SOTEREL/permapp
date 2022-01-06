import legacy from '@vitejs/plugin-legacy';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import { defineConfig, Plugin } from 'vite';

const htmlAutoReloadPlugin: Plugin = {
  name: 'htmlAutoReloadPlugin',
  configureServer({ watcher, ws }) {
    watcher.add('./**/*.html');
    watcher.on('change', (changedPath) => {
      if (
        changedPath &&
        !changedPath.includes('.venv') &&
        changedPath.endsWith('.html')
      ) {
        ws.send({ type: 'full-reload' });
      }
    });
  },
};

export default defineConfig({
  root: __dirname,
  base: '/static/',
  plugins: [
    vue(),
    htmlAutoReloadPlugin,
    legacy({
      targets: ['defaults', 'Firefox ESR'],
    }),
  ],
  resolve: {
    alias: {
      '@': path.resolve('./static/src/ts'),
    },
    extensions: ['.js', '.ts', '.vue'],
  },
  server: {
    host: 'localhost',
    port: 3000,
    https: false,
    open: false,
  },
  build: {
    target: 'es2015',
    outDir: path.resolve('./static/dist'),
    manifest: true,
    emptyOutDir: true,
    assetsDir: '',
    rollupOptions: {
      input: {
        main: path.resolve(__dirname, 'static/src/ts/main.ts'),
        design_map_view: path.resolve(__dirname, 'designs/static/designs/map/view.ts'),
      },
      output: {
        chunkFileNames: undefined,
      },
      plugins: [],
    },
  },
});
