import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Card, Descriptions, Input, message, Spin } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import '../index.css';
import { updateReview } from '../utils/reviewsUtils.jsx';
import ReviewCard from './ReviewCard.jsx';

function OtherUserProfile({ userId }) {
    const navigate = useNavigate();
    const [user, setUser ] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [searchText, setSearchText] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

   useEffect(() => {
    const fetchUserData = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/book_reviews/users/user/${userId}`);
            console.log(response.data);
            setUser (response.data);
            setReviews(response.data.reviews || []);
        } catch (err) {
            console.error(err);
            setError('Ошибка при загрузке данных пользователя');
            message.error('Ошибка при загрузке данных пользователя');
        } finally {
            setLoading(false);
        }
    };

    fetchUserData();
    }, [userId]);


    const handleUpdateReview = (reviewId, updatedData) => {
        updateReview(reviews, setReviews, reviewId, updatedData);
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

    if (loading) return <Spin />;
    if (error) return <div>{error}</div>;

    return (
        <>
            {/* User Info */}
            <div id="user-info-container">
                <div id="user-info">
                    <div className="user-info-header">
                        <h2>Информация о пользователе</h2>
                    </div>
                    <Descriptions layout="vertical">
                        <Descriptions.Item label="Имя пользователя">{user.user_name || 'Не указано'}</Descriptions.Item>
                        <Descriptions.Item label="Email">{user.user_email || 'Не указано'}</Descriptions.Item>
                        {user.is_admin && (
                            <Descriptions.Item label="Администратор">Да</Descriptions.Item>
                        )}
                    </Descriptions>
                </div>
            </div>

            {/* My Reviews */}
            <div id="title">
                <h1>Обзоры Пользователя</h1>
            </div>

            {/* Reviews Search */}
            <div id="user-reviews-search">
                <Input
                    placeholder="Поиск по обзорам"
                    value={searchText}
                    onChange={handleSearchChange}
                    prefix={<SearchOutlined />}
                />
            </div>

            {/* Reviews Cards */}
            <div id="cards-container">
                {reviews.length === 0 ? (
                    <div>У пользователя пока нет обзоров</div>
                ) : filteredReviews.length > 0 ? (
                    filteredReviews.map((userReviews, index) => (
                        <ReviewCard key={index}
                                    reviews={userReviews}
                                    user={user}
                                    setReviews={setReviews} />
                    ))
                ) : (
                    <div>По таким фильтрам обзоры не найдены</div>
                )}
            </div>
        </>
    );
};

export default OtherUserProfile;
