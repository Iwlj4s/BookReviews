   import React, { useEffect, useState } from 'react';
   import '../index.css';
   import ReviewCard from '../components/ReviewCard.jsx';
   import axios from 'axios';

   function HomePage() {
       const [reviews, setReviews] = useState(null);

       useEffect(() => {
           const fetchReviews = async () => {
               const response = await axios.get('http://127.0.0.1:8000/');
               setReviews(response.data);
           };

           fetchReviews();
       }, []);

       if (!reviews) {
           return <div>Загрузка...</div>;
       }

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
                   <ReviewCard reviews={reviews} />
               </div>
           </>
       );
   }

   export default HomePage;