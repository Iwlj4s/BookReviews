import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Alert } from 'antd';
import axios from 'axios';

import '../index.css';
import SignUpForm from '../components/SignUpForm';

const SignUpPage = () => {
    const navigate = useNavigate();
    const [errorMessage, setErrorMessage] = useState(null);

   const handleSignUp = async (values) => {
    const { name, email, password } = values;
    console.log(name, email, password);
    if (!name || !email || !password) {
        console.error('User name, Email и пароль обязательны для входа');
        return;
    } else {
        const requestData = {
            name: name,
            email: email,
            password: password
        };
        console.log('Отправляемые данные from sign up page:', requestData);
        try {
            const response = await axios.post('http://127.0.0.1:8000/book_reviews/users/sign_up', requestData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            console.log("Status code: ", response.data.status_code);
            if (response.data.status_code === 201) {
                console.log("Account created!");
                navigate('/sign_in');
            }
        } catch (error) {
                console.error('Ошибка при входе:', error.response ? error.response.data : error.message);
                if (error.response && error.response.status === 409) {
                    if (error.response.data.message === "Email already exist") {
                        setErrorMessage("Эта почта уже занята!");
                    } else if (error.response.data.message === "This username already exists") {
                        setErrorMessage("Это имя пользователя уже занято!");
                    } else {
                        setErrorMessage("Ошибка входа");
                    }
                } else {
                    setErrorMessage("Ошибка входа");
                }
            }
        }
    };

    return (
        <>
            <div id="sign-up-form-container">
                <h1 id="title">Регистрация</h1>
                <div id="sign-up-form-error-alert">
                    {errorMessage &&
                        <Alert message={errorMessage} type="error" />
                    }
                </div>
                <div id="sign-up-form">
                    <SignUpForm onFinish={handleSignUp} />
                </div>
            </div>
        </>
    );
};

export default SignUpPage;