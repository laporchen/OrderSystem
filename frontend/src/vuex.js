import { createStore } from 'vuex'
import axios from 'axios'
const store = createStore({
    state() {
        return {
            user: null,
            todoList: [],
        }
    },
    getters: {
        user: (state) => {
            return state.login
        },
        todoList: (state) => {
            return state.todoList
        }
    },
    actions: {
        user(context, user) {
            context.commit('user', user)
        },
        todoList(context, todoList) {
            context.commit('todoList', todoList)
        },
        updateTodoList(context, todoList) {
            context.commit('updateTodoList', todoList)
        },
        delTodoList(context, todoList, index) {
            context.commit('delTodoList', todoList, index)
        }
    },
    mutations: {
        user(state, user) {
            state.login = user;
        },
        todoList(state, todoList) {
            state.todoList = todoList;
        },
        async updateTodoList(state, todoList) {
            state.todoList = todoList;
            await axios.post("/update", state.todoList);
        },
        async delTodoList(state, todoList) {
            state.todoList = todoList;
            await axios.post("/update", state.todoList);
        }
    }
});

export default store;