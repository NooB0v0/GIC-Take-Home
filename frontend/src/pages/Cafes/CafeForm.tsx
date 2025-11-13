import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Form, Button, Space, Typography, Upload, message, Card } from 'antd';
import { type RcFile, type UploadFile } from 'antd/es/upload/interface';
import { InboxOutlined } from '@ant-design/icons';
import { isAxiosError } from 'axios';

import ReusableTextbox from '../../components/shared/ReusableTextbox';
import { useSaveCafeMutation, useCafesQuery, type CafeFormObject } from '../../api/cafe.services';
import useUnsavedChangesWarning from '../../hooks/useUnsavedChangesWarning';
import { uploadLogo } from '../../api/utils';

const { Title } = Typography;
const { Dragger } = Upload;

const beforeUpload = (file: RcFile) => {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  if (!isJpgOrPng) {
    message.error('You can only upload JPG/PNG file!');
    return Upload.LIST_IGNORE;
  }
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    message.error('Image must smaller than 2MB!');
    return Upload.LIST_IGNORE;
  }
  return true;
};

interface ApiError {
  response?: {
    data?: {
      error?: string;
    };
  };
}

const CafeForm: React.FC = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEdit = !!id;
  const { data: cafesData } = useCafesQuery(null);
  const saveMutation = useSaveCafeMutation();
  const [fileList, setFileList] = useState<UploadFile[]>([]);
  const isFormDirty = Form.useWatch([], form); 
  const [showWarning, saveForm, resetForm] = useUnsavedChangesWarning(isFormDirty);

  useEffect(() => {
    if (isEdit && cafesData && !form.getFieldValue('name')) {
      const cafeToEdit = cafesData.find(c => c.id === id);
      if (cafeToEdit) {
        const formValues = { ...cafeToEdit };
        delete formValues.logo;
        form.setFieldsValue(formValues);

        if (cafeToEdit.logo && fileList.length === 0) {
            setFileList([{
                uid: '-1',
                name: 'current_logo.png',
                status: 'done',
                url: cafeToEdit.logo,
            }]);
        }
      } else if (!saveMutation.isPending) {
        message.error('Cafe not found.');
        navigate('/cafes');
      }
    }
  }, [isEdit, id, cafesData, form, navigate, saveMutation.isPending, fileList.length]);


  const onFinish = async (values: CafeFormObject) => {
    let logoUrl = values.logo || undefined;
    const fileUpload = fileList[0]?.originFileObj;

    if (isEdit && !fileList.length && values.logo) {
              logoUrl = values.logo; 
          } else if (fileList.length > 0 && fileList[0].status === 'done') {
              logoUrl = fileList[0].url || fileList[0].name;
          } else if (fileList.length === 0) {
              logoUrl = undefined;
          }

    const payload: CafeFormObject = {
      ...values,
      id: isEdit ? id : undefined,
      logo: logoUrl || null,
    };

    const cafeStorageId = isEdit ? id : 'temp-' + Date.now().toString();

    try {
      if (fileUpload) {
        message.loading({ content: 'Uploading Logo...', key: 'uploadKey' });
        const uploadedUrl = await uploadLogo(fileUpload, cafeStorageId);
        message.success({ content: "Logo Uploaded", key: 'uploadKey', duration: 2});
        payload.logo = uploadedUrl || null;
        console.log(uploadedUrl);
      }

      if (isEdit && fileList.length === 0) {
            payload.logo = null;
      }

      await saveMutation.mutateAsync(payload);

      message.success(`Cafe ${isEdit ? 'updated' : 'created'} successfully!`);
      saveForm();
      resetForm(); 
      navigate('/cafes');
    } catch (error) {
      const apiError = error as ApiError;

      if (isAxiosError(apiError)) {
            const errorMessage = apiError.response?.data?.error || 'Unknown network error';
            message.error(`Submission failed: ${errorMessage}`);
        } else {
            message.error('Submission failed: An unexpected client error occurred.');
            console.error(error);
        }
    }
  };

  const onCancel = () => {
    navigate('/cafes');
  };

  const nameRules = [
    { required: true, message: 'Please input the cafe name!' },
    { min: 6, message: 'Name must be at least 6 characters.' }, 
    { max: 10, message: 'Name cannot exceed 10 characters.' }, 
  ];
  
  const descriptionRules = [
    { required: true, message: 'Please input the description!' },
    { max: 256, message: 'Description cannot exceed 256 characters.' },
  ];
  
  const locationRules = [{ required: true, message: 'Please input the location!' }];


  return (
    <Card style={{ border: 'none' }}>
        <Title level={3}>{isEdit ? `Edit Café: ${id}` : 'Add New Café'}</Title>

        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={{ logo: undefined }}
        >
          <ReusableTextbox 
            label="Name" 
            name="name" 
            rules={nameRules} 
            placeholder="Cafe Name"
          />

          <ReusableTextbox 
            label="Description" 
            name="description" 
            rules={descriptionRules}
            maxRows={4}
            placeholder="A short description of the cafe"
          />

          <ReusableTextbox 
            label="Location" 
            name="location" 
            rules={locationRules} 
            placeholder="Location of the cafe"
          />

          <Form.Item label="Logo" name="logo" valuePropName="fileList" getValueFromEvent={(e) => e?.fileList}>
            <Dragger
              name="file"
              beforeUpload={beforeUpload}
              onChange={(info) => setFileList(info.fileList)}
              fileList={fileList}
              maxCount={1}
              listType="picture"
            >
              <p className="ant-upload-drag-icon">
                <InboxOutlined />
              </p>
              <p className="ant-upload-text">Click or drag file to this area to upload (Max 2MB)</p>
            </Dragger>
          </Form.Item>

          <Form.Item>
            <Space>
              <Button type="primary" htmlType="submit" loading={saveMutation.isPending}>
                {isEdit ? 'Update' : 'Add'} Café
              </Button>
              <Button onClick={onCancel}>
                Cancel
              </Button>
              {isEdit && <Button onClick={() => form.resetFields()}>Reset Changes</Button>}
            </Space>
            {showWarning && (
                <span style={{ marginLeft: 20, color: 'orange' }}>
                    * Unsaved changes exist!
                </span>
            )}
          </Form.Item>
        </Form>
    </Card>
  );
};

export default CafeForm;