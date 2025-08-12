import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/app/',  // ??????以꾩씠 ?듭떖 (React瑜?/app 諛묒뿉???뚮┫嫄곕씪??
})

