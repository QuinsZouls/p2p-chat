import React, { useEffect } from 'react';
import { Row, Col } from 'antd';
const DashboardScreen = (props) => {
  useEffect(() => {
    let connection = new WebSocket(process.env.REACT_APP_WS_URL);
    connection.onopen = () => {
      console.log('CONNECTION OPEN');
      connection.send(
        JSON.stringify({
          option: 'enable',
        })
      );
    };
    connection.onmessage = (msg) => {
      const response = JSON.parse(msg.data);
      switch (response.type) {
        case 'registerSuccessful':
          connection.close();
          break;
        case 'error':
          connection.close();
          break;
        default:
          _handleGetInfo(response);
      }
    };
    return () => {
      connection.close();
    };
  }, []);
  const _handleGetInfo = (response) => {
    console.log(response);
  };
  return (
    <div className="chat-main">
      <div className="content">
        <Row gutter={[10, 10]} style={{ height: '100%' }}>
          <Col span={5} className="chats-side">
            chats
          </Col>
          <Col span={19} className="chat-container">
            text
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default DashboardScreen;
