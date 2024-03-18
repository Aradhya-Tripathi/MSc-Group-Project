/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      backgroundImage: {
        'main-background':
          "url('/Users/aradhya/Desktop/Uni-Projects/group-project/AF-Desktop-Predictions/src/renderer/src/assets/background.jpg')"
      }
    }
  },
  plugins: []
}
