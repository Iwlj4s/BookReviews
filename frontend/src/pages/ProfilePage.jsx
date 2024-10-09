import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

import '../index.css';
import UserProfile from '../components/UserProfile.jsx';

const ProfilePage = () => {
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState();

   useEffect(() => {
    const fetchUserData = async () => {
        const token = localStorage.getItem('user_access_token');
        if (!token) {
            navigate("/login")
        }
        console.log('Token:', token);
        try {
            const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/me', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            setUserData(response.data);
            console.log("name", response.data.name);
            console.log("email", response.data.email);
        } catch (error) {
            console.error('Ошибка при входе:', error.response.data);
            setError('Ошибка при загрузке данных');
        }
    };

    fetchUserData();
}, []);

    return (
        <div id="user-profile-container">
            <h1 id="title">Мой профиль</h1>
            <div id="profile-content">
                <UserProfile user={userData} />
            </div>
        </div>
    );
};

export default ProfilePage;