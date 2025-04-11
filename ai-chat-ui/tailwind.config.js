/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#00A67E", // ChatGPT-like green
        secondary: "#F7F7F8", // Light gray for user messages
        dark: "#343541", // Dark background
        darker: "#202123", // Sidebar dark
        gray: {
          100: "#F7F7F8",
          200: "#ECECF1",
          300: "#D9D9E3",
          400: "#CDCDD6",
          500: "#9898A5",
          600: "#6E6E80",
          700: "#40414F",
          800: "#343541",
          900: "#202123",
        },
      },
    },
  },
  plugins: [],
}; 