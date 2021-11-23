module.exports = {
  purge: {
    enabled: true,
    content: [
      '../templates/**/*.html',
      '../base/templates/**/*.html'
    ]
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
