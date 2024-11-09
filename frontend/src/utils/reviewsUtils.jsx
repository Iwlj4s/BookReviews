import React, { useEffect, useState } from 'react';
import axios from 'axios';

export const updateReview = (reviews, setReviews, reviewId, updatedData) => {
    if (Object.keys(updatedData).length === 0) {
        setReviews((prevReviews) => prevReviews.filter((review) => review.id !== reviewId));
    } else {
        setReviews((prevReviews) =>
            prevReviews.map((review) =>
                review.id === reviewId ? { ...review, ...updatedData } : review
            )
        );
    }
};

