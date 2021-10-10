import React from 'react';
import { Route, Redirect } from 'react-router-dom';

const ProtectedRoute = ({ component: Component, token, redirect, ...rest }) => {
  return (
    <Route
      {...rest}
      render={(props) => {
        if (token !== '') {
          return <Component {...props} />;
        } else {
          return <Redirect to={redirect} />;
        }
      }}
    />
  );
};

export default ProtectedRoute;
