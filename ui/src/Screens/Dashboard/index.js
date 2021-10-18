import React, { useEffect, useState } from 'react';
import {
  Row,
  Col,
  Avatar,
  Popover,
  Modal,
  Button,
  Descriptions,
  Form,
  message,
  Input,
  List,
} from 'antd';
import ContactView from '../../Components/Chat/ContactsView';
import ContactForm from '../../Components/Form/Contact.form';
import ChatContainer from '../../Components/Chat/ChatContainer';
import { UserOutlined, PlusOutlined } from '@ant-design/icons';
import { useAuth } from '../../Hooks/Auth.hook';
let connection;
const DashboardScreen = () => {
  const [view, setView] = useState('home');
  const [profileModal, setProfileModal] = useState(false);
  const [contactModal, setContactModal] = useState(false);
  const [requestModal, setRequestModal] = useState(false);
  const [aliasTxt, setAliasTxt] = useState('');
  const [request, setRequest] = useState({});
  const [chats, setChats] = useState([]);
  const [currentContact, setCurrentContact] = useState(null);
  const [contactModalLoading, setContactModalLoading] = useState(false);
  const [contacts, setContacts] = useState([]);
  const [auth, , logout] = useAuth();
  const [formRef] = Form.useForm();
  const content = (
    <div className="action-options">
      <p onClick={() => setContactModal(true)}>Nuevo Contacto</p>
      <p onClick={() => setView('contacts')}>Nuevo Chat</p>
    </div>
  );
  useEffect(() => {
    connection = new WebSocket(process.env.REACT_APP_WS_URL);
    connection.onopen = () => {
      console.log('CONNECTION OPEN');
      connection.send(
        JSON.stringify({
          option: 'connect',
          data: auth.user.id,
        })
      );
      connection.send(
        JSON.stringify({
          option: 'get-chats',
          data: {
            user_id: auth.user.id,
          },
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
        case 'addContactSuccessful':
          setContactModalLoading(false);
          setContactModal(false);
          setAliasTxt('');
          setRequest({});
          setRequestModal(false);
          message.success('Contacto agregado');
          break;
        case 'getContactSuccessful':
          console.log(response);
          setContacts(response.response);
          break;
        case 'getChatsSuccessful':
          console.log(response.response);
          setChats(response.response);
          break;
        case 'connectionRequest':
          setRequestModal(true);
          setRequest(response.response);
          break;
        case 'connectionRequestAccepted':
          message.success(response.response);
          break;
        default:
          _handleGetInfo(response);
      }
    };
    return () => {
      connection.send(
        JSON.stringify({
          option: 'disconnect',
          data: auth.user.id,
        })
      );
      connection.close();
    };
  }, [auth.user.id]);
  const _handleGetInfo = (response) => {
    console.log(response);
    if (response.type === 'error-contact') {
      message.error(response.response);
      setContactModalLoading(false);
    }
  };
  const _handleAddContact = (values) => {
    setContactModalLoading(true);
    connection.send(
      JSON.stringify({
        option: 'add-contact',
        data: {
          ...values,
          user_id: auth.user.id,
        },
      })
    );
  };
  const _handleAcceptRequest = () => {
    setContactModalLoading(true);
    connection.send(
      JSON.stringify({
        option: 'accept-communication-request',
        data: {
          label: aliasTxt,
          address: request.address,
          user_address: auth.token,
          contact_id: request.contact_id,
        },
      })
    );
  };
  const _filterCurrentChat = () => {
    for (let c of chats) {
      if (c.destination === currentContact.destination) {
        return c;
      }
    }
    return null;
  };
  const _getLastMessage = (messages) => {
    const last = messages[messages.length - 1];
    if (last.author === auth.user.id) {
      if (last.attachment !== 0) {
        return `Tú: Imagen`;
      }
      return `Tú: ${last.content}`;
    }
    if (last.attachment !== 0) {
      return `Imagen`;
    }
    return `${last.content}`;
  };
  const _renderViews = () => {
    if (view === 'contacts') {
      return (
        <ContactView
          connection={connection}
          auth={auth}
          contacts={contacts}
          handler={() => setView('home')}
          contactHandler={(contact) => {
            setCurrentContact(contact);
            setView('home');
          }}
        />
      );
    }
    return (
      <div className="side-left-container">
        <div className="header">
          <Row justify="space-between">
            <Col>
              <div onClick={() => setProfileModal(true)}>
                <Avatar
                  size="large"
                  icon={<UserOutlined />}
                  className="profile-trigger"
                />
              </div>
            </Col>
            <Col>
              <Popover placement="bottom" content={content} trigger="hover">
                <PlusOutlined size={56} className="options-trigger" />
              </Popover>
            </Col>
          </Row>
        </div>
        <List
          itemLayout="horizontal"
          dataSource={chats}
          renderItem={(item) => (
            <List.Item
              onClick={() => {
                setCurrentContact(item);
              }}
            >
              <List.Item.Meta
                avatar={<Avatar size="large" icon={<UserOutlined />} />}
                title={item.label}
                description={_getLastMessage(item.messages)}
              />
            </List.Item>
          )}
        />
      </div>
    );
  };
  return (
    <div className="chat-main">
      <Modal
        title="Detalles de la cuenta"
        visible={profileModal}
        width={900}
        centered
        closable={false}
        footer={[
          <Button
            type="primary"
            onClick={() => setProfileModal(false)}
            key="btn"
          >
            Cerrar
          </Button>,
        ]}
      >
        <Descriptions column={1}>
          <Descriptions.Item label="Dirección">{auth.token}</Descriptions.Item>
          <Descriptions.Item label="Usuario">
            {auth.user.username}
          </Descriptions.Item>
        </Descriptions>
        <Button onClick={logout}>Salir</Button>
      </Modal>
      <Modal
        title="Solicitud de comunicación"
        visible={requestModal}
        width={900}
        centered
        okButtonProps={{ loading: contactModalLoading }}
        closable={false}
        onCancel={() => setRequestModal(false)}
        onOk={_handleAcceptRequest}
        okText="Aceptar"
        cancelText="Declinar"
      >
        <Descriptions column={1}>
          <Descriptions.Item label="Dirección">
            {request.address}
          </Descriptions.Item>
          <Descriptions.Item label="Usuario">
            {request.username}
          </Descriptions.Item>
        </Descriptions>
        <Input
          value={aliasTxt}
          onChange={(e) => setAliasTxt(e.target.value)}
          placeholder="Alias de contacto"
        />
      </Modal>
      <Modal
        title="Nuevo contacto"
        visible={contactModal}
        width={600}
        centered
        closable={false}
        okText="Agregar"
        cancelText="Cancelar"
        okButtonProps={{
          loading: contactModalLoading,
        }}
        onOk={() => {
          formRef.submit();
        }}
        onCancel={() => {
          setContactModal(false);
          formRef.resetFields();
        }}
      >
        <ContactForm formRef={formRef} onSubmit={_handleAddContact} />
      </Modal>
      <div className="content">
        <Row gutter={[10, 10]} style={{ height: '100%' }}>
          <Col xl={5} xs={8} className="chats-side">
            {_renderViews()}
          </Col>
          <Col xl={19} xs={16} className="chat-container">
            {currentContact !== null && (
              <ChatContainer
                contact={currentContact}
                connection={connection}
                chat={_filterCurrentChat()}
                auth={auth}
              />
            )}
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default DashboardScreen;
