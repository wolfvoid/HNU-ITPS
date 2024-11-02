import request from '../utils/request';


export const getVisionApi = async (params: any) => {
    const response = await request.get('/vision', { params });
    return response.data.images;
}

