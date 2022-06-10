import { createStore } from 'vuex'
//import axios from 'axios'
const store = createStore({
    state() {
        return {
            user: true,
            seller: false,
        }
    },
    getters: {
        user: (state) => {
            return state.user;
        },
        seller: (state) => {
            return state.seller;
        }
    },
    actions: {
        user(context, user) {
            context.commit('user', user)
        },
    },
    mutations: {
        user(state, user) {
            state.user = user;
        },
    }
});

export default store;