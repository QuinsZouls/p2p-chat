import React from 'react';
import { Form, Input } from 'antd';
import PropTypes from 'prop-types';

const ContactForm = ({ onSubmit, formRef, edit = false }) => {
  return (
    <Form
      name="User"
      onFinish={onSubmit}
      className="login-form"
      layout="vertical"
      form={formRef}
    >
      <Form.Item
        label="Alias"
        name="label"
        rules={[{ required: true, message: 'Este campo es requerido' }]}
      >
        <Input />
      </Form.Item>
      <Form.Item
        name="address"
        label="Dirección"
        rules={[
          {
            required: !edit,
            message: 'Este campo es requerido!',
          },
        ]}
      >
        <Input.TextArea style={{ minHeight: 100 }} />
      </Form.Item>
    </Form>
  );
};
ContactForm.propTypes = {
  onSubmit: PropTypes.func,
  edit: PropTypes.bool,
  formRef: PropTypes.any,
};
export default ContactForm;
