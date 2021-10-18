import React, { useState } from 'react';
import { message } from 'antd';
import RegisterForm from '../../Components/Form/Register.form';
const RegisterScreen = () => {
  const [loading, setLoading] = useState(false);
  const _handleRegisterUser = (values) => {
    setLoading(true);
    let connection = new WebSocket(process.env.REACT_APP_WS_URL);
    connection.onopen = () => {
      console.log('CONNECTION OPEN');
      connection.send(
        JSON.stringify({
          option: 'register',
          data: {
            username: values.username,
            password: values.password,
          },
        })
      );
    };
    connection.onmessage = (msg) => {
      const response = JSON.parse(msg.data);
      switch (response.type) {
        case 'registerSuccessful':
          setLoading(false);
          message.success('Usuario creado exitosamente');
          connection.close();
          break;
        case 'error':
          setLoading(false);
          message.error(response.response);
          connection.close();
          break;
        default:
          console.log(response);
      }
    };
  };
  return (
    <div className="login-screen">
      <RegisterForm onSubmit={_handleRegisterUser} loading={loading} />
    </div>
  );
};

export default RegisterScreen;
