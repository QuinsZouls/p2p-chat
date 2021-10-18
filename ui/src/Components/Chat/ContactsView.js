import React, { useEffect } from 'react';
import { Row, Col, List, Avatar, Badge, Button, message } from 'antd';
import { LeftOutlined, UserOutlined } from '@ant-design/icons';

const ContactView = ({
  connection,
  auth,
  contacts = [],
  handler,
  contactHandler,
}) => {
  useEffect(() => {
    connection.send(
      JSON.stringify({
        option: 'get-contacts',
        data: {
          user_id: auth.user.id,
        },
      })
    );
  }, [connection, auth.user.id]);
  const _minimizeAddress = (address) => {
    return (
      address.substr(0, 8) +
      '.....' +
      address.substr(address.length - 8, address.length)
    );
  };
  const _handleActiveCom = (obj) => {
    connection.send(
      JSON.stringify({
        option: 'communication-request',
        data: {
          from: {
            username: auth.user.username,
            address: auth.token,
            contact_id: obj.id,
          },
          destination: obj.destination,
        },
      })
    );
    message.info('Solicitud de comunicación enviada');
  };
  const _parseStatus = (row) => {
    switch (row.status) {
      case 0:
        return (
          <div>
            <Badge status="default" text="Comunicación pendiente" />
            <br />
            <Button type="ghost" onClick={() => _handleActiveCom(row)}>
              Activar comunicación
            </Button>
          </div>
        );
      case '2':
        return <Badge status="error" text="Comunicación Rechazada" />;
      default:
        return <Badge status="success" text="Comunicación establecida" />;
    }
  };
  return (
    <div>
      <div className="header">
        <Row justify="space-between">
          <Col>
            <LeftOutlined style={{ cursor: 'pointer' }} onClick={handler} />
          </Col>
          <Col></Col>
        </Row>
      </div>
      <List
        itemLayout="horizontal"
        dataSource={contacts}
        renderItem={(item) => (
          <List.Item
            onClick={() => {
              if (item.status === 1) {
                contactHandler(item);
              }
            }}
          >
            <List.Item.Meta
              avatar={<Avatar size="large" icon={<UserOutlined />} />}
              title={item.label}
              description={
                <div>
                  {_minimizeAddress(item.destination)}
                  <br />
                  <div style={{ textAlign: 'right' }}>{_parseStatus(item)}</div>
                </div>
              }
            />
          </List.Item>
        )}
      />
    </div>
  );
};

export default ContactView;
