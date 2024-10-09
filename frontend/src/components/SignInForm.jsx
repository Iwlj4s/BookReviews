import React from 'react';
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Button, Checkbox, Form, Input, Flex } from 'antd';

function SignInForm({ onFinish }){
  return (
    <Form
      name="login"
      initialValues={{
        remember: true,
      }}
      style={{
        maxWidth: 360,
      }}
      onFinish={onFinish}
    >
      <Form.Item
        name="email"
        rules={[{ required: true, message: 'Пожалуйста, введите ваш email!' }]}
      >
        <Input prefix={<UserOutlined />} placeholder="email" />
      </Form.Item>
      <Form.Item
        name="password"
        rules={[{ required: true, message: 'Пожалуйста, введите ваш пароль!' }]}
      >
        <Input prefix={<LockOutlined />} type="password" placeholder="Password" />
      </Form.Item>
      <Form.Item>
        <Button block type="primary" htmlType="submit">
          Войти
        </Button>
        <a id="register-now-link" href="">Зарегистрироваться сейчас</a>
      </Form.Item>
    </Form>
  );
};

export default SignInForm;