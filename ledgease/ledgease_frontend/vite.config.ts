import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Needed to listen on all network interfaces
    port: 5173,
    proxy: {
      '/api': {
        // 'backend' matches the service name in your docker-compose.yml
        target: 'http://backend:8000', 
        changeOrigin: true,
        secure: false,
      },
    },
    // Adding this is highly recommended for Windows/Mac Docker users
    watch: {
      usePolling: true,
    },
  },
});