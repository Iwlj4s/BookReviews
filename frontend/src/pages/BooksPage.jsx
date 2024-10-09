import React, { useEffect, useState } from 'react';
import '../index.css';
import BookCard from '../components/BookCard.jsx';
import axios from 'axios';

function BooksPage (){
    const [books, setBooks] = useState(null);
    useEffect(() => {
       const fetchBooks = async () => {
           const response = await axios.get('http://127.0.0.1:8000/book_reviews/books/books_list');
           setBooks(response.data);
       };

       fetchBooks();
    }, []);

    if (!books) {
       return <div>Загрузка...</div>;
    }

    return (
      <>
        <div id="cards-container">
            {books.map((books, index) => (
              <BookCard key={index} books={books} />
            ))}
        </div>
      </>
    );

}
export default BooksPage;