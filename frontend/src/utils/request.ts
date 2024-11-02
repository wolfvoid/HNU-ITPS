import axios from 'axios'
import { ElMessage } from 'element-plus'

const request = axios.create({
    baseURL: 'http://localhost:5000',
    timeout: 5000,
})

request.interceptors.request.use((config) => {
    return config
})

request.interceptors.response.use((response) => {
    if (response.data.code !== 200) {
        ElMessage.error(response.data.msg)
        return Promise.reject(null)
    }
    return response.data.data
})

export default request
