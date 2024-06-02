/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      './hub_web_app/templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {

      colors: {
        complementary1: '#eeed78',
        },
    },
  },
  plugins: [
      require('flowbite/plugin')
  ],
}
