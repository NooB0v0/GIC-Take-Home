import React, { useEffect } from "react";
import {
  Form,
  Button,
  Space,
  Typography,
  message,
  Card,
  Radio,
  Select,
} from "antd";
import { useNavigate, useParams } from "react-router-dom";
import ReusableTextbox from "../../components/shared/ReusableTextbox";
import {
  useSaveEmployeeMutation,
  type EmployeeFormObject,
  useEmployeesQuery,
} from "../../api/employee.services";
import { useCafesQuery } from "../../api/cafe.services";
import useUnsavedChangesWarning from "../../hooks/useUnsavedChangesWarning";
import { EditOutlined } from "@ant-design/icons";
import { type Rule } from "antd/es/form";

const { Title } = Typography;
const { Option } = Select;

const EmployeeForm: React.FC = () => {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const isEdit = !!id;

  const { data: employeesData } = useEmployeesQuery(null); 
  const { data: cafesData, isLoading: isLoadingCafes } = useCafesQuery(null); 

  const saveMutation = useSaveEmployeeMutation();

  const isFormDirty = Form.useWatch([], form);
  const [showWarning, saveForm, resetForm] =
    useUnsavedChangesWarning(isFormDirty);

  useEffect(() => {
    if (isEdit && employeesData && cafesData) {
      const employeeToEdit = employeesData.find((e) => e.id === id);

      if (employeeToEdit) {
        const initialValues = {
          ...employeeToEdit,
          assigned_cafe_id:
            cafesData.find((c) => c.name === employeeToEdit.cafe_name)?.id ||
            null,
        };
        form.setFieldsValue(initialValues);
      } else if (!saveMutation.isPending) {
        message.error("Employee not found.");
        navigate("/employees");
      }
    }
  }, [
    isEdit,
    id,
    employeesData,
    cafesData,
    form,
    navigate,
    saveMutation.isPending,
  ]);

  const onFinish = async (values: EmployeeFormObject) => {
    const payload: EmployeeFormObject = {
      ...values,
      id: isEdit ? id : undefined,
      assigned_cafe_id: values.assigned_cafe_id || null,
    };

    try {
      console.log(payload);
      await saveMutation.mutateAsync(payload);
      message.success(
        `Employee ${isEdit ? "updated" : "created"} successfully!`
      );
      console.log(payload);
      saveForm();
      resetForm();
      navigate("/employees");
    } catch (error: unknown) {
      const isAxiosError = (
        e: unknown
      ): e is { response: { data: { error: string } } } => {
        return (
          !!e &&
          typeof e === "object" &&
          "response" in e &&
          !!(e).response
        );
      };

      if (isAxiosError(error)) {
        message.error(
          `Submission failed: ${error.response.data.error || "Unknown error"}`
        );
      } else {
        message.error(`Submission failed: Unknown error.`);
        console.error(error);
      }
    }
  };

  const onCancel = () => {
    navigate("/employees");
  };

  const nameRules: Rule[] = [
    { required: true, message: "Please input the employee name!" },
    { min: 6, message: "Name must be at least 6 characters." },
    { max: 10, message: "Name cannot exceed 10 characters." },
  ];

  const emailRules: Rule[] = [
    { required: true, message: "Please input the email address!" },
    { type: "email", message: "The input is not a valid E-mail!" },
  ];

  const phoneRules: Rule[] = [
    { required: true, message: "Please input the phone number!" },
    { len: 8, message: "Phone number must be exactly 8 digits." },
    { pattern: /^[89]\d{7}$/, message: "Phone number must start with 8 or 9." }, 
  ];

  const genderRules: Rule[] = [
    { required: true, message: "Please select gender!" },
  ];

  return (
    <Card style={{ border: "none" }}>
      <Title level={3}>
        {isEdit ? `Edit Employee: ${id}` : "Add New Employee"}
      </Title>

      <Form form={form} layout="vertical" onFinish={onFinish}>
        <ReusableTextbox
          label="Name"
          name="name"
          rules={nameRules}
          placeholder="Employee Name"
        />
        <ReusableTextbox
          label="Email Address"
          name="email_address"
          rules={emailRules}
          placeholder="example@corp.com"
        />
        <ReusableTextbox
          label="Phone Number (SG 8-digit)"
          name="phone_number"
          rules={phoneRules}
          placeholder="8-digit number starting with 8 or 9"
        />
        <Form.Item label="Gender" name="gender" rules={genderRules}>
          <Radio.Group>
            <Radio value="Male">Male</Radio>
            <Radio value="Female">Female</Radio>
          </Radio.Group>
        </Form.Item>
        <Form.Item
          label="Assigned Café"
          name="assigned_cafe_id"
          tooltip="Employee can only be assigned to one cafe."
        >
          <Select
            placeholder="Select a Café"
            loading={isLoadingCafes}
            allowClear 
          >
            {cafesData?.map((cafe) => (
              <Option key={cafe.id} value={cafe.id}>
                {cafe.name} ({cafe.location})
              </Option>
            ))}
          </Select>
        </Form.Item>

        <Form.Item>
          <Space>

            <Button
              type="primary"
              htmlType="submit"
              loading={saveMutation.isPending}
            >
              <EditOutlined /> {isEdit ? "Update" : "Add"} Employee
            </Button>

            <Button onClick={onCancel}>Cancel</Button>
          </Space>

          {showWarning && (
            <span style={{ marginLeft: 20, color: "orange" }}>
              * Unsaved changes exist!
            </span>
          )}
        </Form.Item>
      </Form>
    </Card>
  );
};

export default EmployeeForm;
