// tailwind.config.js
module.exports = {
    content: [
      "./docai/templates/**/*.html",  
      "./templates/**/*.html",        
    ],
    theme: {
      extend: {},
    },
    plugins: [
      require('tailwind-scrollbar-hide'),
    ],
  }