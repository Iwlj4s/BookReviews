import React, { useEffect, useState } from 'react';
import { Card, Space, Tree } from 'antd';

import '../index.css';
import ReviewCard from './ReviewCard.jsx';

function UserProfile({ user }){
    if (!user) {
            return <div>Загрузка...</div>;
        }

        if (!user.reviews || user.reviews.length === 0) {
            return <div>Обзоры отсутствуют</div>;
        }

    const [reviews, setReviews] = useState(null);
        console.log(user.reviews)
        useEffect(() => {
           setReviews(user.reviews);
    }, []);

    return (
        <>
            <div id="user-info-container">
                <div id="user-info">
                    <p id="user-info-name">
                        <b>Имя пользователя:</b> {user.name}
                    </p>
                    <p id="user-info-email">
                        <b>Email пользователя:</b> {user.email}
                    </p>
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