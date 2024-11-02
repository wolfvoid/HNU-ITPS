import request from '../utils/request'

export const postLoginApi = async (data: any) => {
    return request.post('/login', data)
}