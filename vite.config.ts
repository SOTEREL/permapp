import legacy from '@vitejs/plugin-legacy';
import { parse } from 'comment-json';
import favicons from 'favicons';
import fs from 'fs';
import path from 'path';
import { defineConfig, Plugin } from 'vite';

interface IPluginFaviconsConfig {
  source: string;
  templatePath: string;
  metadataPath: string;
  publicPath: string;
  faviconConfig: Partial<favicons.FaviconOptions>;
}

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

const pluginFavicons = (config: IPluginFaviconsConfig) => ({
  name: 'pluginFavicons',
  async generateBundle() {
    const response = await favicons(config.source, config.faviconConfig);

    // Compute all paths.
    const metadataRootPath = path.resolve(__dirname, config.metadataPath || '');
    response.files.forEach((image) => {
      response.images.push({
        name: image.name,
        contents: Buffer.from(image.contents),
      });
    });

    // Create folders and subfolders.
    if (!fs.existsSync(metadataRootPath)) {
      fs.mkdirSync(metadataRootPath, { recursive: true });
    }

    // Write files.
    response.images.forEach((element) => {
      fs.writeFileSync(
        path.join(metadataRootPath, element.name),
        element.contents
      );
    });

    // Write the template
    if (config.templatePath) {
      fs.writeFileSync(
        path.resolve(__dirname, config.templatePath),
        response.html.join('\n')
      );
    }

    // Copy favicon.ico to the public path
    // (for admin and other system who don't read the HTML to get the favicon)
    const faviconPath = path.resolve(
      __dirname,
      config.metadataPath,
      'favicon.ico'
    );

    if (fs.existsSync(faviconPath)) {
      fs.copyFileSync(
        faviconPath,
        path.resolve(__dirname, config.publicPath, 'favicon.ico')
      );
    }
  },
});

export default defineConfig({
  root: path.resolve('./static/src'),
  base: '/static/',
  plugins: [
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
        main: path.resolve('./static/src/ts/main.ts'),
      },
      output: {
        chunkFileNames: undefined,
      },
      plugins: [
        pluginFavicons({
          source: path.resolve('./static/assets/images/favicon.png'),
          metadataPath: path.resolve('./static/dist/metadatas'),
          publicPath: path.resolve('./static/dist'),
          templatePath: path.resolve('./templates/permapp/favicons.html'),
          faviconConfig: parse(
            fs.readFileSync('./static/app.config.jsonc').toString()
          ),
        }),
      ],
    },
  },
});
