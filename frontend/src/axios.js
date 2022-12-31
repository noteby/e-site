import axios from "axios"
//
import {getAccessToken} from '~/composables/auth'
import {notify} from '~/composables/utils'

// https://axios-http.com/docs/intro
const instance = axios.create({
    //
    baseURL: '/api',
    //
    headers: {
        // 'Content-Type': 'application/x-www-form-urlencoded'
        'Content-Type': 'application/json'
    },
    //
    timeout: 6000, // 6s
})

// Add a request interceptor
instance.interceptors.request.use(function (config) {
    // Do something before request is sent
    const accessToken = getAccessToken()
    if (accessToken) {
        config.headers['Authorization'] = 'Bearer ' + accessToken
    }
    return config;
}, function (error) {
    // Do something with request error
    return Promise.reject(error);
})

// Add a response interceptor
instance.interceptors.response.use(function (response) {
    // Any status code that lie within the range of 2xx cause this function to trigger
    // Do something with response data
    let data = response.data
    if (data.code) {
        notify(data.detail || data.desc || '请求失败')
    }
    return data;
}, function (error) {
    // Any status codes that falls outside the range of 2xx cause this function to trigger
    // Do something with response error
    notify(error.response.data.detail || error.response.data.desc || '请求失败')
    return Promise.reject(error);
})

export default instance