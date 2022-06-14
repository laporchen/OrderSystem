import { createStore } from 'vuex'
//import axios from 'axios'
const store = createStore({
    state() {
        return {
            user: null,
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
        seller(context,seller) {
            context.commit('seller', seller)
        }
    },
    mutations: {
        async user(state, user) {
            state.user = user;
        },
        async seller(state, seller) {
            state.seller = seller;
        }
    }
});

export default store;