import React, { useEffect, useState } from 'react';
import { Menu, Spin, Input, Space } from 'antd';
import axios from 'axios';

import ReviewCard from "./components/ReviewCard.jsx";

const App = () => {
  const [reviews, setReviews] = useState([]);

  const fetchReviews = () => {
      axios.get("http://127.0.0.1:8000/home").then(response => {
      const reviewsResponse = response.data;
      console.log("Fetched reviews: ", reviewsResponse);
      setReviews(reviewsResponse);
      });
  };

  useEffect(() => { fetchReviews() }, []);

  return (
      <>
        <div id="card-container">
            {reviews.map((review, index) => (
              <ReviewCard key={index} reviews={review} />
            ))}
        </div>
      </>
  );
};

export default App;