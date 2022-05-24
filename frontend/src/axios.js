import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8081/';
axios.defaults.headers['Authorization'] = `Bearer ${localStorage.getItem("token")}`;