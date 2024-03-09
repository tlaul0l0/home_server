/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './hub_web_app/templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('flowbite/plugin')
  ],
}
