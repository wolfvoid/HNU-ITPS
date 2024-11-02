import request from '../utils/request'

export const updateUserPasswordApi = async (data: any) => {
    return request.put(`/password/user`, data)
}

export const updateAdminPasswordApi = async (data: any) => {
    return request.put(`/password/admin`, data)
}