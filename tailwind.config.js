/** @type {import('tailwindcss').Config} */
// Cấu hình này được port y nguyên từ khối `tailwind.config` inline cũ trong
// base.html (bản dùng cdn.tailwindcss.com). Mọi tên màu Tailwind được map sang
// CSS variable trong tokens.css để giữ nguyên giao diện.
module.exports = {
  // Quét class trong template Jinja và JS (app.js có vài chuỗi class động).
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        gray: {
          50:  'var(--paper)',
          100: 'var(--surface-2)',
          200: 'var(--line)',
          300: 'var(--line-strong)',
          400: 'var(--ink-3)',
          500: 'var(--ink-2)',
          600: 'var(--ink-2)',
          700: 'var(--ink-1)',
          800: 'var(--ink-1)',
          900: 'var(--ink)',
        },
        violet: {
          50:  'var(--accent-tint)',
          100: 'var(--accent-tint)',
          500: 'var(--accent)',
          600: 'var(--accent)',
          700: 'var(--accent-strong)',
          900: 'var(--accent-strong)',
        },
        blue: {
          50:  'var(--accent-tint)',
          100: 'var(--accent-tint)',
          500: 'var(--accent)',
          600: 'var(--accent)',
          700: 'var(--accent-strong)',
          900: 'var(--accent-strong)',
        },
        sky: {
          500: 'var(--accent)',
        },
        indigo: {
          500: 'var(--accent)',
        },
        cyan: {
          500: 'var(--accent)',
        },
        green: {
          50:  'var(--success-tint)',
          100: 'var(--success-tint)',
          200: 'var(--success-tint)',
          500: 'var(--success)',
          600: 'var(--success)',
          700: 'var(--success)',
        },
        red: {
          50:  'var(--danger-tint)',
          100: 'var(--danger-tint)',
          200: 'var(--danger-tint)',
          500: 'var(--danger)',
          600: 'var(--danger)',
          700: 'var(--danger)',
        },
        amber: {
          50:  'var(--warning-tint)',
          100: 'var(--warning-tint)',
          500: 'var(--warning)',
          600: 'var(--warning)',
        },
      },
      fontFamily: {
        sans:    ['var(--font-body)',    'system-ui', 'sans-serif'],
        display: ['var(--font-display)', 'serif'],
      },
      borderRadius: {
        sm:    'var(--radius-sm)',
        md:    'var(--radius-md)',
        lg:    'var(--radius-lg)',
        xl:    'var(--radius-xl)',
        '2xl': 'var(--radius-2xl)',
        full:  '9999px',
      },
      boxShadow: {
        xs: 'var(--shadow-xs)',
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
        xl: 'var(--shadow-xl)',
      },
      transitionTimingFunction: {
        out: 'var(--ease-out)',
        in:  'var(--ease-in)',
        std: 'var(--ease-std)',
      },
      transitionDuration: {
        fast:   'var(--duration-fast)',
        normal: 'var(--duration-normal)',
        slow:   'var(--duration-slow)',
      },
    },
  },
  plugins: [],
};
