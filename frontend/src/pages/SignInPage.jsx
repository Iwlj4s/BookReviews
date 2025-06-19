import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Alert, message } from 'antd';
import axios from 'axios';

import '../index.css';
import SignInForm from '../components/SignInForm';

const SignInPage = () => {
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState(null);

    const handleLogin = async (values) => {
        const { email, password } = values;
        console.log(email, password);
        if (!email || !password) {
            console.error('Email и пароль обязательны для входа');
            return;
        } else {
            const requestData = {
                email: email,
                password: password
            };
            console.log('Отправляемые данные from sign in page:', requestData);
            try {
                const response = await axios.post('http://87.228.10.180/api/users/sign_in', requestData, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                console.log("User access token: ", response.data.user_access_token);
                console.log("User data: ", response.data);
                if (response.data.user_access_token) {
                    localStorage.setItem("user_access_token", response.data.user_access_token);
                    navigate('/me');
                }
            } catch (error) {
                console.error('Ошибка при входе:', error.response ? error.response.data : error.message);
                if (error.response && error.response.status === 403) {
                    setErrorMessage("Неверная почта/пароль");
                } else {
                    setErrorMessage("Ошибка входа");
                }
            }
        }
    };

    return (
        <>
            <div id="sign-in-form-container">
                <h1 id="title">Вход</h1>
                <div id="sign-in-form-error-alert">
                    {errorMessage &&
                        <Alert message={errorMessage} type="error" />
                    }
                </div>
                <div id="sign-in-form">
                    <SignInForm onFinish={handleLogin} />
                </div>
            </div>
        </>
    );
};

export default SignInPage;