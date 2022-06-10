import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8081/api';
axios.defaults.headers['Authorization'] = `Bearer ${localStorage.getItem("token")}`;