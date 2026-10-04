import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  base: '/SIH2026-CIVIC-ME/',
  server: {
    port: 5173,
    host: '0.0.0.0'
  },
  build: {
    outDir: 'dist'
  }
});
