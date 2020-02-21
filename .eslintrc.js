module.exports = {
  root: true,

  parserOptions: {
    parser: "babel-eslint",
    sourceType: "module"
  },

  env: {
    browser: true
  },

  extends: [
    "plugin:vue/recommended",
    "prettier",
    "prettier/vue",
  ],

  // required to lint *.vue files
  plugins: [
    "prettier",
    "vue",
  ],

  globals: {
    "ga": true, // Google Analytics
    "cordova": true,
    "__statics": true,
    "process": true,
    "Capacitor": true,
    "chrome": true,
  },

  "rules": {
    "prettier/prettier": "error"
  }
}
