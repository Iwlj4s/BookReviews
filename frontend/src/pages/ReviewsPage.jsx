import React, { useEffect, useState } from 'react';
import axios from 'axios';

import { Spin } from 'antd';

import '../index.css';
import ReviewCard from '../components/ReviewCard.jsx';

function ReviewsPage(){
    const [reviews, setReviews] = useState(null);

    useEffect(() => {
           const fetchReviews = async () => {
               const response = await axios.get('http://127.0.0.1:8000/book_reviews/reviews/');
               setReviews(response.data);
           };

           fetchReviews();
       }, []);

    if (!reviews) {
           return <div id="spin"><Spin size="large" /> </div>;
       }

       return (
           <>
               <div id="last-record-title">
                   <h1>Обзоры пользователей</h1>
               </div>
               <div id="cards-container">
                    {reviews.map((review, index) => (
                        <ReviewCard key={index} reviews={review} />
                    ))}
               </div>
           </>
       );
   }

export default ReviewsPage;