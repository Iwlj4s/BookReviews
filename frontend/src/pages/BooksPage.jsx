import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Spin, Input, message } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import '../index.css';
import BookCard from '../components/BookCard.jsx';

function BooksPage (){
    const navigate = useNavigate();
    const [books, setBooks] = useState(null);
    const [user, setUser] = useState(null);
    const [searchText, setSearchText] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState();


    useEffect(() => {
        const token = localStorage.getItem('user_access_token');
        if (!token) {
            setLoading(false);
            return;
        }
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
       const fetchBooks = async () => {
           const response = await axios.get('http://127.0.0.1:8000/book_reviews/books/books_list');
           setBooks(response.data);
       };

       fetchBooks();
    }, []);

    if (loading) {
        return <Spin id="spin" />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (!books) {
       return <div id="spin">Пока что книг нет </div>;
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
                        <BookCard key={index}
                        books={book}
                        setBooks={setBooks}
                        user={user}/>
                    ))
                ) : (
                    <div>По таким фильтрам книга не найдена</div>
                )}
            </div>
        </>
    );

}

export default BooksPage;
