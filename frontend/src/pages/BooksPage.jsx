import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Spin, Input } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import '../index.css';
import BookCard from '../components/BookCard.jsx';

function BooksPage (){
    const [books, setBooks] = useState(null);
    const [searchText, setSearchText] = useState('');
    useEffect(() => {
       const fetchBooks = async () => {
           const response = await axios.get('http://127.0.0.1:8000/book_reviews/books/books_list');
           setBooks(response.data);
       };

       fetchBooks();
    }, []);

    if (!books) {
       return <div id="spin"><Spin size="large" /> </div>;
    }

    const handleSearchChange = (e) => {
        setSearchText(e.target.value);
    };

    const filteredBooks = books.filter(book => {
        if (!searchText) return true;
        return (
            (book.book_name && book.book_name.toLowerCase().includes(searchText.toLowerCase())) ||
            (book.author.name && book.author.name.toLowerCase().includes(searchText.toLowerCase()))
        );
    });

    return (

        <>
            <div id="title">
                <h1>Книги, на которые можно сделать обзор</h1>
            </div>
            <div id="user-reviews-search">
                <Input
                    placeholder="Поиск по книгам"
                    value={searchText}
                    onChange={handleSearchChange}
                    prefix={<SearchOutlined />}
                    style={{ marginBottom: '20px', width: '100%' }}
                />
            </div>
            <div id="cards-container">
                {filteredBooks.length > 0 ? (
                    filteredBooks.map((book, index) => (
                        <BookCard key={index} books={book} />
                    ))
                ) : (
                    <div>По таким фильтрам книга не найдена</div>
                )}
            </div>
        </>
    );

}
export default BooksPage;