import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const SignInPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        if (!email || !password) {
            console.error('Email и пароль обязательны для входа');
            return;
        } else {
            const requestData = {
                email: email,
                password: password
            };
            console.log('Отправляемые данные:', requestData);
            axios.post('http://127.0.0.1:8000/book_reviews/users/sign_in', requestData, {
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(function(response) {
                console.log("User access token: ", response.data.user_access_token);
                console.log("User name: ", response.data.name);
                if (response.data.user_access_token) {
                    localStorage.setItem("user_access_token", response.data.user_access_token);
                    navigate('/me');
                }
            })
            .catch(function(error) {
                console.error('Ошибка при входе:', error.response.data);
                alert('Ошибка входа: ' + error.response.data.message);
            });
        }
    };

    return (
        <form>
            <h1>Вход</h1>
            <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            <input
                type="password"
                placeholder="Пароль"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            <button onClick={handleLogin} type="submit">Войти</button>
        </form>
    );
};

export default SignInPage;