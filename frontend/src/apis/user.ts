import request from '../utils/request'

export const getUserPageApi = async (params: any) => {
    return request.get('/user', { params })
}

export const getUserOptionListApi = async () => {
    return request.get('/user/option-list')
}

export const createUserApi = async (data: any) => {
    return request.post('/user', data)
}

export const updateUserApi = async (data: any) => {
    return request.put(`/user`, data)
}

export const deleteUserApi = async (params: any) => {
    return request.delete(`/user`,{ params })
}
