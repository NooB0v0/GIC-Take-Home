import React from 'react';
import { Form, Input, type InputProps } from 'antd';
import type { Rule } from 'antd/es/form';
import type { TextAreaProps } from 'antd/es/input/TextArea';

type CommonInputProps = Omit<InputProps & TextAreaProps, 'rows' | 'maxRows' | 'type'>;

interface ReusableTextboxProps extends CommonInputProps {
  label: string;
  name: string;
  rules?: Rule[];
  maxRows?: number;
}

const ReusableTextbox: React.FC<ReusableTextboxProps> = ({ label, name, rules, maxRows, ...inputProps }) => {
  const InputComponent = maxRows ? Input.TextArea : Input;

  return (
    <Form.Item
      label={label}
      name={name}
      rules={rules}
      style={{ marginBottom: 16 }}
    >
      <InputComponent 
        {...inputProps} 
        rows={maxRows} 
      />
    </Form.Item>
  );
};

export default ReusableTextbox;