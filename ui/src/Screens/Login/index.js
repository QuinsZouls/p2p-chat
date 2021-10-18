import React, { useState } from 'react';
import { message } from 'antd';
import LoginForm from '../../Components/Form/Login.form';
import { useAuth } from '../../Hooks/Auth.hook';
const LoginScreen = () => {
  const [loading, setLoading] = useState(false);
  const [, post] = useAuth();
  const _handleLogin = (values) => {
    setLoading(true);
    let connection = new WebSocket(process.env.REACT_APP_WS_URL);
    connection.onopen = () => {
      connection.send(
        JSON.stringify({
          option: 'auth',
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
        case 'authSuccessful':
          setLoading(false);
          post(response.response);
          console.log('Auth Success');
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
      <LoginForm onSubmit={_handleLogin} loading={loading} />
    </div>
  );
};

export default LoginScreen;
