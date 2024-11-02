import request from '../utils/request'


export const getPreApi = async (params: any) => {
    return request.get('/pre', { params })
}

