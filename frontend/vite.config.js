import path from 'path'
import {defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'
//
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import {ElementPlusResolver} from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig(({mode, command}) => {
    const env = loadEnv(mode, '.')
    return {
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
                    target: env.VITE_TARGET,
                    changeOrigin: true,
                    rewrite: (path) => path.replace(/^\/api/, ''),
                },
            }
        }
    }
})
