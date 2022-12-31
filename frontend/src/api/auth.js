import axios from '~/axios'


export function login(email, password) {
    return axios.post('/v1/auth/token', {
        email, password
    }, {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
}