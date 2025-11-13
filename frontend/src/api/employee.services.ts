import { message } from 'antd'
import { apiClient, queryClient } from './config';
import { useMutation, useQuery, type UseQueryResult } from '@tanstack/react-query';

export interface EmployeeListObject {
  id: string; 
  name: string;
  email_address: string;
  phone_number: string;
  days_worked: number; 
  cafe_name?: string;
}

export interface EmployeeFormObject {
  id?: string;
  name: string;
  email_address: string;
  phone_number: string;
  gender: 'Male' | 'Female';
  assigned_cafe_id: string | null;
}


const fetchEmployees = async (cafeName: string | null): Promise<EmployeeListObject[]> => {
  const params = cafeName ? { cafe: cafeName } : {}; 
  const response = await apiClient.get<EmployeeListObject[]>('/employees', { params });
  return response.data;
};

const saveEmployee = async (data: EmployeeFormObject): Promise<EmployeeListObject> => {
  if (data.id) {
    // update employee
    const employeeId = data.id;
    const payload = { ...data };
    delete payload.id;
    return apiClient.put<EmployeeListObject>(`/employees/${employeeId}`, payload).then(res => res.data);
  } else {
    // add employee
    return apiClient.post<EmployeeListObject>('/employees', data).then(res => res.data);
  }
};


export const useEmployeesQuery = (cafeName: string | null): UseQueryResult<EmployeeListObject[], Error> => {
  return useQuery({
    queryKey: ['employees', { cafeName }], 
    queryFn: () => fetchEmployees(cafeName),
    staleTime: 5 * 60 * 1000, 
  });
};

export const useSaveEmployeeMutation = () => {
  return useMutation({
    mutationFn: saveEmployee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees'] });
      queryClient.invalidateQueries({ queryKey: ['cafes'] });
    },
  });
};

const deleteEmployee = async (employeeId: string) => {
  return apiClient.delete(`/employees/${employeeId}`)
}

export const useDeleteMutation = () => {
  return useMutation({
    mutationFn: deleteEmployee,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['employees']});
      queryClient.invalidateQueries({ queryKey: ['cafes'] });
      message.success('Employee deleted successfully');
    },
    onError: (error) => {
      message.error(`Deletion failed: ${error.message}`);
    }
  })
}