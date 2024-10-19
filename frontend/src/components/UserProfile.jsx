import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Descriptions, Button, Spin, Input } from 'antd';
import { EditOutlined, MailOutlined, UserOutlined, LockOutlined } from '@ant-design/icons';
import '../index.css';
import ReviewCard from './ReviewCard.jsx';

function UserProfile({ user, onLogout, onUpdateUserData }) {
    if (!user) {
        return <div id="spin"><Spin /> </div>;
    }

    if (!user.reviews || user.reviews.length === 0) {
        return <div id="spin"><Spin size="large" /> </div>;
    }

    const navigate = useNavigate();
    const [reviews, setReviews] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        name: user?.name || null,
        email: user?.email || null,
        password: ''
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        setReviews(user.reviews);
    }, [user]);

    useEffect(() => {
        if (user) {
            setFormData({
                name: user.name,
                email: user.email,
                password: ''
            });
        }
    }, [user]);

    const fetchUserData = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/me/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });
            return response.data;
        } catch (error) {
            console.error('Ошибка при получении данных пользователя:', error.response ? error.response.data : error.message);
            throw error;
        }
    };

    const handleEditClick = () => {
        setIsEditing(true);
    };

    const handleCancel = () => {
        setIsEditing(false);
        setFormData({
            name: user.name,
            email: user.email,
            password: user.password
        });
    };

    const handleSave = async () => {
        setLoading(true);
        setError('');

        const requestData = {
            name: formData.name || null,
            email: formData.email || null,
            ...(formData.password ? { password: formData.password } : {})
        };

        try {
            const response = await axios.put('http://127.0.0.1:8000/book_reviews/users/change_me/', requestData, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });

            console.log("Request data: ", requestData)
            console.log("status code: ", response.data.status_code)

            if (response.data.status_code === 401) {
                console.log("Navigate to login after pass change")
                const updatedUser = await fetchUserData();
                onUpdateUserData(updatedUser);

                localStorage.removeItem('user_access_token');
                navigate('/sign_in');

            } else {
                console.log("Data changed")
                const updatedUser = await fetchUserData();
                onUpdateUserData(updatedUser);
            }
        } catch (err) {
            console.error('Ошибка при сохранении данных:', err.response ? err.response.data : err.message);
            setError('Ошибка при сохранении данных');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div id="user-info-container">
                <div id="user-info">
                    <div className="user-info-header">
                        <h2>Информация о пользователе</h2>
                        <Button
                            type="link"
                            icon={<EditOutlined />}
                            onClick={handleEditClick}
                            size="large"
                        />
                    </div >
                    {isEditing ? (
                        <div id="change-user-data">
                            <Input
                                placeholder="Имя пользователя"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                prefix={<UserOutlined />}
                            />
                            <Input
                                placeholder="Email"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                prefix={<MailOutlined />}
                            />
                            <Input.Password
                                placeholder="Пароль"
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                prefix={<LockOutlined />}
                            />
                            <Button onClick={handleSave} loading={loading}>Сохранить</Button>
                            <Button onClick={handleCancel}>Отменить</Button>
                            {error && <div style={{ color: 'red' }}>{error}</div>}
                        </div>
                    ) : (
                        <Descriptions layout="vertical">
                            <Descriptions.Item label="Имя пользователя">{user.name}</Descriptions.Item>
                            <Descriptions.Item label="Email">{user.email}</Descriptions.Item>
                            {user?.is_admin && (
                                <Descriptions.Item label="Администратор">Да</Descriptions.Item>
                            )}
                        </Descriptions>
                    )}
                </div>
            </div>

            <div id="title"><h1>Мои обзоры</h1></div>
            <div id="cards-container">
                {user.reviews.map((userReviews, index) => (
                    <ReviewCard key={index} reviews={userReviews} user={user} />
                ))}
            </div>
        </>
    );
};

export default UserProfile;