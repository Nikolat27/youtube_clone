/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        roboto: ['"Roboto"', 'sans-serif']
      },
      boxShadow: {
        'outer': '0 0 12px rgba(0, 0, 0, 0.13)',
      },
    },
  },
  plugins: [],
}

