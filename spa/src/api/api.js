import axios from "axios";

const API = axios.create({
  baseURL: process.env.VUE_APP_API_URL,
});

export default API;
