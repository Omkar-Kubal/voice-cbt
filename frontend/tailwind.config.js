// frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}", // Scans all files in pages/
    "./components/**/*.{js,ts,jsx,tsx}", // Scans all files in components/
  ],
  darkMode: 'class', // This enables dark mode based on the 'dark' class on the html or body tag
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Example: If you want to use the Inter font
      },
    },
  },
  plugins: [],
}