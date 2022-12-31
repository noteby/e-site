import {useCookies} from "@vueuse/integrations/useCookies"

const accessTokenKey = 'access-token'
const cookie = useCookies()

// Get cookie
export function getAccessToken() {
    return cookie.get(accessTokenKey)
}


// Set cookie
export function setAccessToken(token) {
    cookie.set(accessTokenKey, token)
}


// Remove cookie
export function removeAccessToken() {
    cookie.remove(accessTokenKey)
}
