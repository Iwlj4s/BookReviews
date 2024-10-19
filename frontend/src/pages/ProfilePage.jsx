import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button } from 'antd';
import { LogoutOutlined } from '@ant-design/icons';
import '../index.css';
import UserProfile from '../components/UserProfile.jsx';

const ProfilePage = () => {
    const navigate = useNavigate();
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState();

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('user_access_token');
            if (!token) {
                navigate("/sign_in");
                return;
            }
            try {
                const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                setUserData(response.data);
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('user_access_token');
                    navigate("/sign_in");
                } else {
                    console.error('Ошибка при входе:', error.response.data);
                    setError('Ошибка при загрузке данных');
                }
            }
        };

        fetchUserData();
    }, [navigate]);

    const handleLogout = async () => {
        try {
            await axios.post('http://127.0.0.1:8000/book_reviews/users/logout', {}, {
                withCredentials: true
            });
            localStorage.removeItem('user_access_token');
            navigate('/sign_in');
        } catch (error) {
            console.error('Ошибка при выходе:', error.response.data);
        }
    };

    const updateUserData = (updatedUser) => {
        setUserData(updatedUser);
    };

    return (
         <div id="user-profile-container">
            <div className="profile-header">
                <h1 id="title">Мой профиль</h1>
                <div id="logout_button">
                    <Button
                        type="link"
                        icon={<LogoutOutlined />}
                        onClick={handleLogout}
                        size="large"
                    />
                </div>
            </div>
            <div id="profile-content">
                <UserProfile user={userData} onLogout={handleLogout} onUpdateUserData={updateUserData} />
            </div>
        </div>
    );
};

export default ProfilePage;