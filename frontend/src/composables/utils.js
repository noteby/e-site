import {ElNotification} from "element-plus"
import {useRouter} from "vue-router"


export function getCurrentRouteName() {
    return useRouter().currentRoute.value.name
}

export function getCurrentRoutePath() {
    return useRouter().currentRoute.value.path
}

//
export function notify(message, duration = 2000) {
    ElNotification({
        message,
        duration, // 2s
    })
}
