import Vuex from 'vuex'
import { createStore } from 'vuex'

export const store = createStore({
    state() {
        return {
            user: undefined
        }
    },

    actions: {
        register({commit}, data) {
            fetch('https://late-glitter-4431.fly.dev/api/v54/users', {
                headers: {
                    'X-Access-Token': '50f1a5fded92970d2c46d4649605aedd0ed8d319f2f27da183eecf6b8b9af6cc',
                    'Content-Type': 'application/json',
                },
                method: 'POST',
                body: JSON.stringify({data})
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not OK');
                    }
                    return response.json()
                })
                .then(info => {
                    commit('registerUser', info)
                    console.log('Success:', info);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        }
    },

    mutations: {
        registerUser(state, data) {
            state.user = data
        }
    }
})
