import path from 'path'
import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
//
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver} from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
    base: './',
    build: {
        chunkSizeWarningLimit: 1000
    },
    plugins: [
        vue(),
        //
        AutoImport({resolvers: [ElementPlusResolver()]}),
        Components({resolvers: [ElementPlusResolver()]}),
    ],
    resolve: {
        alias: {
            '~': path.resolve(__dirname, 'src'),
        }
    },
    server: {
        proxy: {
            '/api': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, ''),
            },
        }
    }
})
