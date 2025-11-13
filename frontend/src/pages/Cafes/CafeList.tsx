import React, { useState, useMemo } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import { Typography, Input, Button, Space, Card, Tag, Modal, message } from "antd";
import { useQueryClient } from "@tanstack/react-query"; 
import { useCafesQuery, type CafeListObject, useDeleteMutation } from "../../api/cafe.services";
import { AgGridReact } from "ag-grid-react";
import { ModuleRegistry, ClientSideRowModelModule, type ICellRendererParams, type ColDef  } from 'ag-grid-community';
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import { EditOutlined, DeleteOutlined, PlusOutlined, ExclamationCircleOutlined } from "@ant-design/icons";


const { Search } = Input;
const { Title } = Typography;
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

ModuleRegistry.registerModules([ClientSideRowModelModule]);

const CafeList: React.FC = () => {
  const queryClient = useQueryClient();

  const [searchParams, setSearchParams] = useSearchParams();
  const initialLocationFilter = searchParams.get('location');
  const [locationFilter, setLocationFilter] = useState<string | null>(initialLocationFilter);
  const { data, isLoading, error } = useCafesQuery(locationFilter);
  const { mutate, isPending } = useDeleteMutation();
  const [modal, contextHolder] = Modal.useModal(); 

  const showDeleteConfirm = (cafeId: string) => {
    modal.confirm({
      title: 'Are you sure you want to delete this cafe?',
      icon: <ExclamationCircleOutlined />,
      content: "This action cannot be undone once confirmed. All associated employees will be deleted.",
      okText: 'Yes, Delete',
      okType: 'danger',
      cancelText: 'Cancel',
      onOk() {
        mutate(cafeId, {
          onSuccess: () => {
            message.success('Cafe deleted successfully');
            queryClient.invalidateQueries({ queryKey: ['cafes'] }); 
          },
          onError: (error) => {
             message.error(`Deletion failed: ${error.message || 'An unknown error occurred'}`);
          }
        })
      },
    });
  };


  const ActionsRenderer = (params: ICellRendererParams<CafeListObject>) => {
    const navigate = useNavigate();
    const cafeId = params.data?.id;

    const handleEdit = () => {
      if (cafeId) {
        navigate(`/cafes/edit/${cafeId}`);
      }
    };

    return (
      <Space>
        <Button
          size="small"
          icon={<EditOutlined />}
          onClick={handleEdit}
        />
        <Button
          size="small"
          danger
          icon={<DeleteOutlined />}
          onClick={() => cafeId && showDeleteConfirm(cafeId)}
          loading={isPending}
        />
      </Space>
    );
  };

  const columnDefs: ColDef<CafeListObject>[] = useMemo(
    () => [
      {
        field: "logo",
        headerName: "Logo",
        width: 80,
        cellRenderer: (params: ICellRendererParams) => {
          const logoPath = params.value;
          if (logoPath) {
            const fullUrl = `${API_BASE_URL}${logoPath}`;
            return  (
              <img
                src = {fullUrl}
                alt = "Logo"
                style = {{ width: 30, height: 30 }}
                />
            );
          }
          return (<Tag>N/A</Tag>);
        },
      },
      { field: "name", headerName: "Name", sortable: true, filter: true, flex: 1 },
      { field: "description", headerName: "Description", filter: true, flex: 2 },
      { field: "location", headerName: "Location", sortable: true, filter: true, width: 150 },
      {
        field: "employees",
        headerName: "Employees",
        sortable: true,
        width: 120,
        cellRenderer: (params: ICellRendererParams<CafeListObject>) => {
            if (!params.data || !params.data.name) return params.value;
            return <Link to={`/employees?cafe=${params.data.name}`}>{params.value}</Link>;
        },
      },
      {
        headerName: "Actions",
        cellRenderer: ActionsRenderer,
        width: 120,
        pinned: "right",
        resizable: false,
      },
    ],
    [] 
  );

  const handleSearch = (value: string) => {
    const trimmedValue = value.trim();
    const newFilter = trimmedValue ? trimmedValue : null;

    setLocationFilter(newFilter); 

    if (newFilter) {
        setSearchParams({ location: newFilter });
    } else {
        setSearchParams({});
    }
  };

  if (error) {
    return (
      <Typography.Text type="danger">
        Error loading cafes: {error.message}
      </Typography.Text>
    );
  }

  return (
    <Card
      style={{ border: 'none' }}
    >
      {contextHolder}
      <Title level={4}>Café Management</Title>

      <Space
        style={{
          marginBottom: 16,
          width: "100%",
          justifyContent: "space-between",
        }}
      >
        <Search
          placeholder="Filter by Location"
          allowClear
          onSearch={handleSearch}
          style={{ width: 300 }}
          loading={isLoading}
          defaultValue={initialLocationFilter || ''}
        />
        <Link to="/cafes/add">
          <Button type="primary" icon={<PlusOutlined />}>
            Add New Café
          </Button>
        </Link>
      </Space>

      <div className="ag-theme-alpine" style={{ height: 600, width: "100%" }}>
        <AgGridReact<CafeListObject>
          rowData={data}
          columnDefs={columnDefs}
          defaultColDef={{ sortable: true, filter: true, resizable: true }}
          pagination={true}
          paginationPageSize={15}
          loadingOverlayComponent={
            isLoading ? () => <div>Loading...</div> : undefined
          }
        />
      </div>
    </Card>
  );
};

export default CafeList;