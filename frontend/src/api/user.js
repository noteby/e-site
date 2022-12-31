import axios from '~/axios'


export function getUserInfo() {
    return axios.get('/v1/user/info')
}