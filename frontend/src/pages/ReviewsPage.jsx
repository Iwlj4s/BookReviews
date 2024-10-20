import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Spin, Input } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import '../index.css';
import ReviewCard from '../components/ReviewCard.jsx';


function ReviewsPage(){
    const [reviews, setReviews] = useState(null);
    const [searchText, setSearchText] = useState('');

    useEffect(() => {
           const fetchReviews = async () => {
               const response = await axios.get('http://127.0.0.1:8000/book_reviews/reviews/');
               setReviews(response.data);

               console.log("Reviews: ", response.data)
           };

           fetchReviews();
       }, []);

    if (!reviews) {
           return <div id="spin"><Spin size="large" /> </div>;
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
            (review.user && review.user.name && review.user.name.toLowerCase().includes(searchText.toLowerCase())) // Фильтрация по имени пользователя
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
                    filteredReviews.map((review, index) => (
                        <ReviewCard key={index} reviews={review} />
                    ))
                ) : (
                    <div>По таким фильтрам обзоры не найдены</div>
                )}
            </div>
        </>
    );
}

export default ReviewsPage;