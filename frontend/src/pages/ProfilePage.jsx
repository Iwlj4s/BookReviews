import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Button, message, Spin } from 'antd';
import { LogoutOutlined } from '@ant-design/icons';
import '../index.css';
import UserProfile from '../components/UserProfile.jsx';
import { isAuthenticated, is401Error } from '../utils/authUtils';

const ProfilePage = () => {
    const navigate = useNavigate();

    const [user, setUser] = useState(null);

    const [error, setError] = useState();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUserData = async () => {

            try {
                if (!isAuthenticated(navigate, "/sign_in")) return;
                const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/me/', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                    }
                });
                if (!is401Error(navigate, "/sign_in")) return;

                console.log("Полные данные пользователя:", response.data);
                console.log("Тип данных пользователя:", typeof response.data);
                console.log("Имя пользователя:", response.data.name);
                console.log("Email пользователя:", response.data.email);
                setUser(response.data);
                setLoading(false);


            } catch (err) {
            if (err.response && err.response.status === 401) {
                console.log("error from err.response.status from profile page")
                console.log("error response: ", err.response)
                message.error(err.response.data.detail);
                navigate("/sign_in");
            } else {
                console.error("Error fetching user data:", err);
                setError("Ошибка при загрузке данных пользователя");
            }
            } finally {
                setLoading(false);
            }
        };

        fetchUserData();
    }, [navigate]);

   if (loading) {
        return <Spin id="spin" />;
    }

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
                <UserProfile user={user}
                    onUpdateUserData={(updatedUser) => setUser(updatedUser)} />
            </div>
        </div>
    );
};

export default ProfilePage;