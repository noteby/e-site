import {defineStore} from "pinia"
//
import {login} from "~/api/auth.js";
import {getUserInfo} from "~/api/user.js"
import {getAccessToken, removeAccessToken, setAccessToken} from "~/composables/auth.js"

const userStoreKey = 'userStore'

//
export const useUserStore = defineStore('user', {
    state: () => ({
        email: null
    }),
    actions: {
        async dispatchUserInfo() {
            this.email = null
            getUserInfo().then(res => {
                const email = res['email']
                this.email = email
                // Store
                sessionStorage.setItem(userStoreKey, email)
            }).catch(err => {
            })
            return this.email
        },
        async getEmail() {
            if (!this.email) {
                // Get from storage
                let email = sessionStorage.getItem(userStoreKey)
                if (email) {
                    this.email = email
                } else if (!this.email) {
                    // Get from Api
                    await this.dispatchUserInfo()

                }
            }
            return this.email
        },
        login(email, password) {
            return new Promise((resolve, reject) => {
                login(email, password)
                    .then(res => {
                        setAccessToken(res['access_token'])
                        this.email = email
                        //
                        resolve(res)
                    })
                    .catch(err => {
                        reject(err)
                    })
            })
        },
        logout() {
            removeAccessToken()
            this.email = null
        },
        hasLoggedIn() {
            return !!getAccessToken()
        },
    },
})