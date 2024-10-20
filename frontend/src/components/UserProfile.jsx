import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Descriptions, Button, Spin, Input, message } from 'antd';
import { EditOutlined, MailOutlined, UserOutlined, LockOutlined, PlusCircleOutlined, SearchOutlined } from '@ant-design/icons';
import '../index.css';
import ReviewCard from './ReviewCard.jsx';

function UserProfile({ user, onLogout, onUpdateUserData }) {
    if (!user) {
        console.log("can't get user in UserProfile");
        return <div id="spin"><Spin /> </div>;
    }
    const navigate = useNavigate();
    const [reviews, setReviews] = useState([]);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        name: user?.name || null,
        email: user?.email || null,
        password: ''
    });
    const [searchText, setSearchText] = useState('');

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');


    useEffect(() => {
        if (user) {
            setFormData({
                name: user.name,
                email: user.email,
                password: ''
            });
            setReviews(user.reviews || []);
            console.log("Users Reviews: ", user.reviews)
        }
    }, [user]);

    const updateReview = (reviewId, updatedData) => {
        if (Object.keys(updatedData).length === 0) {
            // Удаление обзора из списка
            setReviews((prevReviews) => prevReviews.filter((review) => review.id !== reviewId));
        } else {
            // Обновление обзора в списке
            setReviews((prevReviews) =>
                prevReviews.map((review) =>
                    review.id === reviewId ? { ...review, ...updatedData } : review
                )
            );
        }
    };

    const fetchUserData = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/me/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });
            if (response.status === 401) { // Изменено с response.data.status_code на response.status
                message.error('Токен недействителен');
                navigate("/sign_in");
                return;
            }
            return response.data;
        } catch (error) {
            if (error.response && error.response.status === 401) { // Добавлена проверка на 401
                message.error('Токен недействителен');
                navigate("/sign_in");
            } else {
                console.error('Ошибка при получении данных пользователя:', error.response ? error.response.data : error.message);
                throw error;
            }
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
            password: ''
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
            console.log("Taking data in user profile:", response.data.data)

            if (response.data.status_code === 401) {
                console.log("Navigate to login after pass change")
                message.success('Данные обновлены успешно!');
                const updatedUser = await fetchUserData();
                onUpdateUserData(updatedUser);

                localStorage.removeItem('user_access_token');
                navigate('/sign_in');
                setIsEditing(false);

            } else {
                console.log("Data changed")
                message.success('Данные обновлены успешно!');
                const updatedUser = await fetchUserData();
                onUpdateUserData(updatedUser);
                setIsEditing(false);
            }
        } catch (err) {
            console.error('Ошибка при сохранении данных:', err.response ? err.response.data : err.message);
            setError('Ошибка при сохранении данных');
        } finally {
            setLoading(false);
        }
    };

    const addReview = async () => {
        console.log("Add review func")
    };

    const handleSearchChange = (e) => {
        setSearchText(e.target.value);
    };

    const filteredReviews = reviews.filter(review => {
        if (!searchText) return true;
        return (
            (review.reviewed_book_author_name && review.reviewed_book_author_name.toLowerCase().includes(searchText.toLowerCase())) ||
            (review.reviewed_book_name && review.reviewed_book_name.toLowerCase().includes(searchText.toLowerCase())) ||
            (review.review_title && review.review_title.toLowerCase().includes(searchText.toLowerCase()))
        );
    });


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
                            <Descriptions.Item label="Имя пользователя">{user.name || 'Не указано'}</Descriptions.Item>
                            <Descriptions.Item label="Email">{user.email || 'Не указано'}</Descriptions.Item>
                            {user.is_admin && (
                                <Descriptions.Item label="Администратор">Да</Descriptions.Item>
                            )}
                        </Descriptions>
                    )}
                </div>
            </div>

            <div id="title">
                <h1>Мои обзоры</h1>
                <div id="new-review-btn">
                    <Button
                        type="link"
                        icon={<PlusCircleOutlined />}
                        onClick={addReview}
                        size="large"
                    />
                </div>
            </div>
            <div id="user-reviews-search">
                <Input
                    placeholder="Поиск по обзорам"
                    value={searchText}
                    onChange={handleSearchChange}
                    prefix={<SearchOutlined />}
                />
            </div>
            <div id="cards-container">
                {reviews.length === 0 ? (
                    <div>У вас пока нет обзоров</div>
                ) : filteredReviews.length > 0 ? (
                    filteredReviews.map((userReviews, index) => (
                        <ReviewCard key={index}
                                    reviews={userReviews}
                                    user={user}
                                    isProfilePage={true}
                                    onUpdateReview={updateReview}/>
                    ))
                ) : (
                    <div>По таким фильтрам обзоры не найдены</div> // Сообщение, если обзоры не найдены по фильтру
                )}
            </div>
        </>
    );
};

export default UserProfile;