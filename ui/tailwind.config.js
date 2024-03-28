/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      backgroundImage: {
        'main-background': 'src/renderer/src/assets/background.jpg'
      }
    }
  },
  plugins: []
}
