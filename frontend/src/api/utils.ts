import { apiClient } from './config'
import { type RcFile } from 'antd/es/upload/interface'

export const uploadLogo = async (file: RcFile, cafeId: string): Promise<string> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiClient.post<{logoUrl: string}>(`/cafes/upload-logo/${cafeId}`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        }
    });

    return response.data.logoUrl;
}