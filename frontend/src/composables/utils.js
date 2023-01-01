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


export function formatDateStr(dateStr) {
    function patch(i) {
        return i < 10 ? ('0' + i) : i
    }

    let dateObj = new Date(dateStr)
    let y = dateObj.getFullYear()
    let m = patch(dateObj.getMonth() + 1)
    let d = patch(dateObj.getDate())
    let H = patch(dateObj.getHours())
    let M = patch(dateObj.getMinutes())
    let S = patch(dateObj.getSeconds())

    return y + '-' + m + '-' + d + ' ' + H + ':' + M + ':' + S
}