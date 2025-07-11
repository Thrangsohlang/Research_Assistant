import axios from 'axios';

const API = axios.create({
    baseURL:process.env.REACT_APP_API_BASE_URL || 'http://localhost:8001',
});

// Automatically attach token if present
API.interceptors.request.use(cfg => {
    const token = localStorage.getItem('access_token');
    if (token && cfg.headers) {
        cfg.headers.Authorization = `Bearer ${token}`;
    }
    return cfg;
})


export default API;