import { message } from 'antd';
import { apiClient, queryClient } from './config'
import { useQuery, useMutation, type UseQueryResult, type UseMutationResult } from '@tanstack/react-query'

export interface CafeListObject{
    id: string;
    name: string;
    description: string;
    logo?: string | null;
    location: string;
    employees: number;
}

export interface CafeFormObject {
  id?: string;
  name: string;
  description: string;
  logo?: string | null;
  location: string;
}

const fetchCafes = async (location: string | null): Promise<CafeListObject[]> => {
    const params = location ? { location } : {};
    const response = await apiClient.get<CafeListObject[]>('/cafes', { params });
    return response.data;
};

const saveCafe = async (data: CafeFormObject): Promise<CafeListObject> => {
  if (data.id) {
    // update cafe
    const cafeId = data.id;
    const payload =  { ...data }
    delete payload.id;
    if (!payload.logo || payload.logo.trim() === '') {
        payload.logo = null; 
    }
    return apiClient.put<CafeListObject>(`/cafes/${cafeId}`, payload).then(res => res.data);
  } else {
    // add cafe
    const payload =  { ...data }
    delete payload.id;
    if (!payload.logo || payload.logo.trim() === '') {
        payload.logo = null;
    }
    return apiClient.post<CafeListObject>('/cafes', payload).then(res => res.data);
  }
};

export const useSaveCafeMutation = (): UseMutationResult<CafeListObject, Error, CafeFormObject> => {
  return useMutation({
    mutationFn: saveCafe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cafes'] });
    },
  });
};

export const useCafesQuery = (location: string | null): UseQueryResult<CafeListObject[], Error> => {
    return useQuery({
        queryKey: ['cafes', { location }],
        queryFn: () => fetchCafes(location),
        staleTime: 5 * 60 * 1000
    });
};

const deleteCafe = async (cafeId: string) => {
  return apiClient.delete(`/cafes/${cafeId}`);
};

export const useDeleteMutation = () => {
  return useMutation({
    mutationFn: deleteCafe,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['cafes']});
      message.success('Cafe deleted successfully');
    },
    onError: (error) => {
      message.error(`Deletion failed: ${error.message}`);
    }
  })
}