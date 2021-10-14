import React from 'react';
import { Form, Input, Button, Row, Col } from 'antd';
import PropTypes from 'prop-types';
import { useNavigation } from '../../Hooks/Nav.hook';

const RegisterForm = ({ onSubmit, formRef, edit = false, loading }) => {
  const [, navPush] = useNavigation();

  return (
    <Form
      name="User"
      onFinish={onSubmit}
      className="login-form"
      layout="vertical"
      form={formRef}
    >
      <Form.Item
        label="Username"
        name="username"
        rules={[{ required: true, message: 'Este campo es requerido' }]}
      >
        <Input />
      </Form.Item>
      <Form.Item
        name="password"
        label="Contraseña"
        rules={[
          {
            required: !edit,
            message: 'Este campo es requerido!',
          },
        ]}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item
        name="rpassword"
        label="Confirmar contraseña"
        dependencies={['password']}
        hasFeedback
        rules={[
          {
            required: !edit,
            message: 'Este campo es requerido',
          },
          ({ getFieldValue }) => ({
            validator(rule, value) {
              if (!value || getFieldValue('password') === value) {
                return Promise.resolve();
              }
              return Promise.reject('Las contraseñas no coinciden');
            },
          }),
        ]}
      >
        <Input.Password />
      </Form.Item>
      <Form.Item>
        <Row justify="space-between">
          <Col></Col>
          <Col>
            <span className="login-form-forgot" onClick={() => navPush('/')}>
              Entrar
            </span>
          </Col>
        </Row>
      </Form.Item>

      <Form.Item>
        <Button
          type="primary"
          htmlType="submit"
          className="login-form-button"
          loading={loading}
        >
          Registrarse
        </Button>
      </Form.Item>
    </Form>
  );
};
RegisterForm.propTypes = {
  onSubmit: PropTypes.func,
  edit: PropTypes.bool,
  formRef: PropTypes.any,
};
export default RegisterForm;
