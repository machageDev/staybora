import axios from "axios";
import {ACCES_TOKEN} from "./constants";
const apiUrl = "/";

const api = axios.create({
    baseURL: import .meta.env.VITE_API_URL || apiUrl,

});
api.interceptors.request.use(
    (config) =>{
        const token = localStorage.getItem(ACCES_TOKEN);
        if(token){
            config.headers.Authorization = `Bearer ${token}`;

        }
        return config;
    },
    (error)=>{
        return Promise.reject(error);
    }
);
export default api;