import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import '../index.css';
import SignInForm from '../components/SignInForm';

const SignInPage = () => {
    const navigate = useNavigate();

    const handleLogin = async (values) => {
        const { email, password } = values;
        console.log(email, password)
        if (!email || !password) {
            console.error('Email и пароль обязательны для входа');
            return;
        }
        else {
            const requestData = {
                email: email,
                password: password
            };
            console.log('Отправляемые данные:', requestData);
            try {
                const response = await axios.post('http://127.0.0.1:8000/book_reviews/users/sign_in', requestData, {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                console.log("User access token: ", response.data.user_access_token);
                console.log("User name: ", response.data.name);
                if (response.data.user_access_token) {
                    localStorage.setItem("user_access_token", response.data.user_access_token);
                    navigate('/me');
                }
            } catch (error) {
                console.error('Ошибка при входе:', error.response.data);
                alert('Ошибка входа: ' + error.response.data.message);
            }
        }
    };

    return (
        <>
        <div id="sign-in-form-container">
            <h1 id="title">Вход</h1>
            <div id="sign-in-form">
                <SignInForm onFinish={handleLogin} />
            </div>
        </div>
        </>
    );
};

export default SignInPage;