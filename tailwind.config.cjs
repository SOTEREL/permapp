module.exports = {
  mode: 'jit',
  purge: {
    content: ['./**/*.html', './static/src/**/*.vue'],
    layers: ['base', 'components', 'utilities'],
    options: {
      keyframes: true,
      fontFace: true,
    },
    safelist: [],
  },
  darkMode: false,
  plugins: [require('@tailwindcss/forms')],
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
};
