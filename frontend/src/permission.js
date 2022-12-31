import router from "~/router/index.js"
import {notify} from '~/composables/utils'
import {useUserStore} from "~/store/user.js"


router.beforeEach((to, from, next) => {
    const userStore = useUserStore()
    //
    if (to.meta['requiresAuth'] && !userStore.hasLoggedIn()) {
        notify('请先登录')
        return next({path: '/login'})
    }
    //
    if (to.name === 'Login' && userStore.hasLoggedIn()) {
        notify('请勿重复登录')
        return next({path: from.path ? from.path : '/'})
    }

    next()
})