import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  // 设置别名
  resolve: {
    alias: [
      {
        // 设置别名， '@' 指向 'src' 目录
        find: "@",
        replacement: path.resolve(__dirname, './src')
      },
    ]
  },
})
