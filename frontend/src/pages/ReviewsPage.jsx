import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Spin, Input, message } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import '../index.css';
import ReviewCard from '../components/ReviewCard.jsx';
import { isAuthenticated, is401Error } from '../utils/authUtils';


function ReviewsPage(){
    const navigate = useNavigate();
    const [searchText, setSearchText] = useState('');
    const [user, setUser] = useState(null);
    const [reviews, setReviews] = useState([]);

    const [error, setError] = useState();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
       if (!is401Error(navigate, "/reviews")) return;
        const token = localStorage.getItem('user_access_token');
        const fetchUserData = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/me/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                if (response.status_code === 401) {
                    message.warning('Вы не зашли в аккаунт');
                    return;
                }
                setUser (response.data);
            } catch (err) {
                if (err.response && err.response.status === 401) {
                    message.warning('Вы не зашли в аккаунт');
                } else {
                    console.error("Error fetching user data:", err);
                    setError("Ошибка при загрузке данных пользователя");
                }
            } finally {
                setLoading(false);
            }
        };
        fetchUserData();
    }, []);

    useEffect(() => {
           const fetchReviews = async () => {
               const response = await axios.get('http://127.0.0.1:8000/book_reviews/reviews/');
               setReviews(response.data);

               console.log("Reviews: ", response.data)
           };

           fetchReviews();
       }, []);

   if (loading) {
        return <Spin id="spin" />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (!reviews) {
           return <div id="spin">Пока что обзоров нет</div>;
       }

    const handleSearchChange = (e) => {
        setSearchText(e.target.value);
    };

    const filteredReviews = reviews.filter(review => {
        if (!searchText) return true;
        return (
            (review.reviewed_book_author_name && review.reviewed_book_author_name.toLowerCase().includes(searchText.toLowerCase())) ||
            (review.reviewed_book_name && review.reviewed_book_name.toLowerCase().includes(searchText.toLowerCase())) ||
            (review.review_title && review.review_title.toLowerCase().includes(searchText.toLowerCase())) ||
            (review.user && review.user.name && review.user.name.toLowerCase().includes(searchText.toLowerCase()))
        );
    });

    return (
        <>
            <div id="title">
                <h1>Обзоры пользователей</h1>
            </div>
            <div id="user-reviews-search">
                <Input
                    placeholder="Поиск по обзорам"
                    value={searchText}
                    onChange={handleSearchChange}
                    prefix={<SearchOutlined />}
                    style={{ marginBottom: '20px', width: '100%' }}
                />
            </div>
            <div id="cards-container">
                {filteredReviews.length > 0 ? (
                    filteredReviews.map((userReviews, index) => (
                        <ReviewCard key={index}
                                    reviews={userReviews}
                                    user={user}
                                    isProfilePage={false}
                                    setReviews={setReviews}/>
                    ))
                ) : (
                    <div>По таким фильтрам обзоры не найдены</div>
                )}
            </div>
        </>
    );
}

export default ReviewsPage;