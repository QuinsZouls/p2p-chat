import React from 'react';
import { Form, Input, Button, Row, Col } from 'antd';
import PropTypes from 'prop-types';

//Hooks
import { useNavigation } from '../../Hooks/Nav.hook';
const LoginForm = ({ onSubmit, loading = false }) => {
  const [, navPush] = useNavigation();
  /**
   * Send action with input values
   * @param {Object} values
   */
  const onFinish = async (values) => {
    if (typeof onSubmit === 'function') {
      await onSubmit(values);
    }
  };

  return (
    <Form
      name="normal_login"
      className="login-form"
      initialValues={{ remember: true }}
      onFinish={onFinish}
      layout="vertical"
    >
      <Form.Item
        name="username"
        label="Usuario"
        rules={[{ required: true, message: 'Este campo es requerido' }]}
      >
        <Input className="sub-input" />
      </Form.Item>
      <Form.Item
        name="password"
        label="Contraseña"
        rules={[{ required: true, message: 'Este campo es requerido' }]}
      >
        <Input type="password" className="sub-input" />
      </Form.Item>
      <Form.Item>
        <Row justify="space-between">
          <Col></Col>
          <Col>
            <span
              className="login-form-forgot"
              onClick={() => navPush('/register')}
            >
              Registrarse
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
          Login
        </Button>
      </Form.Item>
    </Form>
  );
};
LoginForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
  loading: PropTypes.bool,
};

export default LoginForm;
