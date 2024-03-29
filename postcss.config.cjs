module.exports = ({ env }) => {
  const isProduction = env === 'production';

  return {
    plugins: {
      'tailwindcss/nesting': {},
      tailwindcss: {},
      autoprefixer: isProduction ? {} : false,
      '@hail2u/css-mqpacker': isProduction ? {} : false,
      cssnano: isProduction ? {} : false,
    },
  };
};
