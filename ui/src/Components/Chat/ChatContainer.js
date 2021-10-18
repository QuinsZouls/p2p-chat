import React, { useState } from 'react';
import { Input, Row, Col, Button, List, Image } from 'antd';
import { PaperClipOutlined, CloseCircleOutlined } from '@ant-design/icons';

import { minimizeAddress, getBase64 } from '../../Utils/url';
const ChatContainer = ({ contact, chat, connection, auth }) => {
  const [text, setText] = useState('');
  const [imageRaw, setImageRaw] = useState(null);
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
    if (imageRaw !== null) {
      message.attachment = imageRaw;
    }
    setText('');
    setImageRaw(null);
    connection.send(
      JSON.stringify({
        option: 'message',
        data: message,
      })
    );
  };
  const _handleFileInput = async (e) => {
    let file = e.target.files[0];
    let imageData = await getBase64(file);
    setImageRaw({
      raw: imageData,
      size: file.size,
      type: file.type,
      id: new Date().getTime(),
    });
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
          style={{ height: '100%' }}
          dataSource={chat?.messages}
          renderItem={(item) => (
            <List.Item>
              <div
                className={
                  auth.user.id === item.author ? 'r-message' : 'l-message'
                }
              >
                <div className="message-content">
                  {item.attachment !== 0 ? (
                    <div>
                      <Image src={item.multimedia} alt="attachment" />
                      <p>{item.content}</p>
                    </div>
                  ) : (
                    item.content
                  )}
                </div>
              </div>
            </List.Item>
          )}
        />
      </div>
      <div className="input-container">
        {imageRaw !== null && (
          <div className="image-container">
            <div className="trigger" onClick={() => setImageRaw(null)}>
              <CloseCircleOutlined />
            </div>
            <div className="image">
              <img src={imageRaw.raw} alt="photos" />
            </div>
          </div>
        )}
        <Row justify="space-between">
          <Col xs={18} xl={20}>
            <Input
              autoFocus
              onChange={(e) => setText(e.target.value)}
              value={text}
            />
          </Col>
          <Col xs={6} xl={4} style={{ textAlign: 'right' }}>
            <label className="custom-file-upload">
              <input type="file" onChange={_handleFileInput} />
              <PaperClipOutlined />
            </label>
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
