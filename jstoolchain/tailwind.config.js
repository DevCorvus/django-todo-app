module.exports = {
  purge: {
    enabled: true,
    content: ['../templates/**/*.html', '../base/templates/**/*.html'],
    safelist: ['resize-none', 'h-24']
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
