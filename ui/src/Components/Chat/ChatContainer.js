import React, { useState } from 'react';
import { Input, Row, Col, Button, List } from 'antd';
import { PaperClipOutlined } from '@ant-design/icons';

import { minimizeAddress } from '../../Utils/url';
const ChatContainer = ({ contact, chat, connection, auth }) => {
  const [text, setText] = useState('');
  const _handleSendMessage = () => {
    let message;
    if (chat === null) {
      //Creamos el chat con el mensaje
      message = {
        content: text,
        from: auth.token,
        to: contact.destination,
        created_at: new Date().getTime(),
        create_chat: true,
        contact_id: contact.id,
      };
    } else {
      message = {
        content: text,
        from: auth.token,
        to: contact.destination,
        created_at: new Date().getTime(),
        chat_id: chat.id,
        create_chat: false,
      };
    }
    setText('');
    connection.send(
      JSON.stringify({
        option: 'message',
        data: message,
      })
    );
  };
  return (
    <div className="chat-container">
      <div className="chat-head">
        <h1>{contact.label}</h1>
        <h3>{minimizeAddress(contact.destination)}</h3>
      </div>
      <div className="message-container">
        <List
          itemLayout="horizontal"
          dataSource={chat?.messages}
          renderItem={(item) => (
            <List.Item>
              <div
                className={
                  auth.user.id === item.author ? 'r-message' : 'l-message'
                }
              >
                <div className="message-content">{item.content}</div>
              </div>
            </List.Item>
          )}
        />
      </div>
      <div className="input-container">
        <Row justify="space-between">
          <Col xs={18} xl={20}>
            <Input
              autoFocus
              onChange={(e) => setText(e.target.value)}
              value={text}
            />
          </Col>
          <Col xs={6} xl={4} style={{ textAlign: 'right' }}>
            <Button>
              <PaperClipOutlined />
            </Button>
            <Button type="primary" onClick={_handleSendMessage}>
              Enviar
            </Button>
          </Col>
        </Row>
      </div>
    </div>
  );
};
export default ChatContainer;
