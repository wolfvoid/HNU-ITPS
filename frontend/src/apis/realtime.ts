import request from '../utils/request';

export const getRealtimeApi = async (params: any) => {
    return request.get('/realtime', { params });
}

// export const importDataApi = async (formData: any) => {
//     return request.post('/upload', formData)
// }

