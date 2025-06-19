import React, { useEffect, useState } from 'react';
import axios from 'axios';

import { Spin } from 'antd';

import '../index.css';
import ReviewCard from '../components/ReviewCard.jsx';


function HomePage() {
   const [reviews, setReviews] = useState(null);

   useEffect(() => {
       const fetchReviews = async () => {
           const response = await axios.get('https://87.228.10.180/api');
           setReviews(response.data);
       };

       fetchReviews();
   }, []);


   return (
       <>
           <div id="explore-title">
               <h1>Исследуйте мир литературы вместе с нами</h1>
               <p id="explore-title-subtitle">Мы создаем пространство, где каждый может высказать свои мысли и рекомендации. Вот что вы можете сделать:</p>
               <div id="user-features">
                   <ul id="user-features-ul">
                       <li id="user-features-item"><b>Публикация обзоров:</b> Делитесь своими мыслями о прочитанных книгах и вдохновляйте других на чтение.</li>
                       <li id="user-features-item"><b>Просмотр обзоров:</b> Исследуйте мнения других читателей о различных книгах и находите новые произведения для чтения.</li>
                       <li id="user-features-item"><b>Изучение книг:</b> Ознакомьтесь с описаниями книг, доступных на сайте, чтобы выбрать, что почитать дальше.</li>
                    </ul>
               </div>
           </div>

           <div id="last-record-title">
               <h1>Последний обзор</h1>
               <p id="explore-title-subtitle">Не пропустите последний обзор, который поможет вам определиться с выбором следующей книги.</p>
               <p id="explore-title-subtitle">Мы рады видеть вас в нашем сообществе читателей и надеемся, что вы найдете здесь вдохновение для новых литературных открытий!</p>
           </div>

            <div id="card-container">
                {reviews ? (
                  <ReviewCard reviews={reviews} />
                ) : (
                  <div>Пока что обзоров нет</div>
                )}
          </div>
       </>
   );
}

export default HomePage;