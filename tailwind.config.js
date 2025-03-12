/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        theme: {
          bg: 'var(--theme-bg)',
          bg1: 'var(--theme-bg1)',
          bg2: 'var(--theme-bg2)',
          fg: 'var(--theme-fg)',
          fg1: 'var(--theme-fg1)',
          accent: 'var(--theme-accent)',
          accent_hover: 'var(--theme-accent_hover)',
          success: 'var(--theme-success)',
          error: 'var(--theme-error)',
        }
      }
    }
  },
  plugins: [],
}
