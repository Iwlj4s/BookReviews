import React from 'react';
import { LockOutlined, MailOutlined, UserOutlined } from '@ant-design/icons';
import { Button, Form, Input } from 'antd';

function SignUpForm({ onFinish }) {
    return (
        <Form
            name="sign_up"
            initialValues={{
                remember: true,
            }}
            style={{
                maxWidth: 360,
            }}
            onFinish={onFinish}
        >
            <Form.Item
                name="name"
                rules={[{ required: true, message: 'Пожалуйста, введите ваше имя пользователя!' }]}
            >
                <Input prefix={<UserOutlined />} placeholder="Имя пользователя" />
            </Form.Item>

            <Form.Item
                name="email"
                rules={[{ required: true, message: 'Пожалуйста, введите ваш email!' }]}
            >
                <Input prefix={<MailOutlined />} placeholder="Email" />
            </Form.Item>

            <Form.Item
                name="password"
                rules={[{ required: true, message: 'Пожалуйста, введите ваш пароль!' }]}
            >
                <Input prefix={<LockOutlined />} type="password" placeholder="Пароль" />
            </Form.Item>

            <Form.Item>
                <Button block type="primary" htmlType="submit">
                    Зарегистрироваться
                </Button>
                <a id="log-in-now-link" href="/sign_in">Уже есть аккаунт? Войти</a>
            </Form.Item>
        </Form>
    );
};

export default SignUpForm;