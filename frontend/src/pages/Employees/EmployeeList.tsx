import React, { useState, useMemo } from 'react';
import { Typography, Input, Button, Space, Card, Modal, message } from 'antd';
import { useEmployeesQuery, type EmployeeListObject, useDeleteMutation } from '../../api/employee.services';
import { AgGridReact } from 'ag-grid-react';
import 'ag-grid-community/styles/ag-grid.css'; 
import 'ag-grid-community/styles/ag-theme-alpine.css'; 
import { EditOutlined, DeleteOutlined, PlusOutlined, ExclamationCircleOutlined } from '@ant-design/icons';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import dayjs from 'dayjs';
import { type ICellRendererParams, type ColDef, ModuleRegistry, ClientSideRowModelApiModule } from "ag-grid-community";
import { useQueryClient } from '@tanstack/react-query';

const { Search } = Input;
const { Title } = Typography;


ModuleRegistry.registerModules([ClientSideRowModelApiModule])


const EmployeeList: React.FC = () => {
    const [searchParams] = useSearchParams();
    const initialCafeFilter = searchParams.get('cafe');
    const [cafeFilter, setCafeFilter] = useState<string | null>(initialCafeFilter);

    const { data, isLoading, error } = useEmployeesQuery(cafeFilter);
    const queryClient = useQueryClient(); 
    const { mutate, isPending } = useDeleteMutation();
    
    const today = dayjs();
    console.log(`Dayjs loaded: ${today.format('YYYY-MM-DD')}`); 

    const [modal, contextHolder] = Modal.useModal();

    const showDeleteConfirm = (employeeId: string) => {
        modal.confirm({
        title: 'Are you sure you want to delete this employee?',
        icon: <ExclamationCircleOutlined />,
        content: "This action cannot be undone once confirmed.",
        okText: 'Yes, Delete',
        okType: 'danger',
        cancelText: 'Cancel',
        onOk() {
            mutate(employeeId, {
            onSuccess: () => {
                message.success('Employee deleted successfully');
                queryClient.invalidateQueries({ queryKey: ['employees'] }); 
            },
            onError: (error) => {
                message.error(`Deletion failed: ${error.message || 'An unknown error occurred'}`);
            }
            })
        },
        });
    };

    const ActionsRenderer = (params: ICellRendererParams<EmployeeListObject>) => {
        const navigate = useNavigate();
        const employeeId = params.data?.id;

        const handleEdit = () => {
            if (employeeId) {
                navigate(`/employees/edit/${employeeId}`);
            }
        };

        return (
        <Space>
            <Button size="small" icon={<EditOutlined />} onClick={handleEdit} />
            <Button size="small" danger icon={<DeleteOutlined />} onClick={() => employeeId && showDeleteConfirm(employeeId)} loading={isPending} />
        </Space>
        );
    };

    const columnDefs: ColDef<EmployeeListObject>[] = useMemo(() => [
        { field: 'id', headerName: 'Employee ID', width: 150 },
        { field: 'name', headerName: 'Name', flex: 1 },
        { field: 'email_address', headerName: 'Email Address', flex: 1 },
        { field: 'phone_number', headerName: 'Phone Number', width: 120 },
        { 
            field: 'days_worked', 
            headerName: 'Days Worked', 
            width: 130,
            sort: 'desc',
            cellRenderer: (params: ICellRendererParams) => params.value >= 0 ? `${params.value} days` : 'Unassigned'
        },
        { 
            field: 'cafe_name', 
            headerName: 'Café Name', 
            flex: 1,
            cellRenderer: (params: ICellRendererParams) => params.value || 'N/A'
        },
        { 
            headerName: 'Actions', 
            cellRenderer: ActionsRenderer, 
            width: 120, 
            pinned: 'right', 
            resizable: false 
        },
    ], []);

    const handleSearch = (value: string) => {
        setCafeFilter(value.trim() ? value.trim() : null);
    };

    if (error) {
        return <Typography.Text type="danger">Error loading employees: {error.message}</Typography.Text>;
    }

    return (
        <Card style={{ border: 'none' }}>
            {contextHolder}
            <Title level={4}>Employee Management</Title>
            
            <Space style={{ marginBottom: 16, width: '100%', justifyContent: 'space-between' }}>
                <Search
                    placeholder="Filter by Café Name"
                    allowClear
                    onSearch={handleSearch}
                    style={{ width: 300 }}
                    loading={isLoading}
                    defaultValue={initialCafeFilter || ''}
                />
                <Link to="/employees/add">
                    <Button type="primary" icon={<PlusOutlined />}>
                        Add New Employee
                    </Button>
                </Link>
            </Space>
            
            <div className="ag-theme-alpine" style={{ height: 600, width: '100%' }}>
                <AgGridReact<EmployeeListObject>
                    rowData={data}
                    columnDefs={columnDefs}
                    defaultColDef={{ sortable: true, filter: true, resizable: true }}
                    pagination={true}
                    paginationPageSize={15}
                    loadingOverlayComponent={isLoading ? () => <div>Loading...</div> : undefined}
                />
            </div>
        </Card>
    );
};

export default EmployeeList;