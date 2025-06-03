import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Spin, message, Input } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import '../index.css';
import AuthorCard from '../components/AuthorCard.jsx';
import { isAuthenticated, is401Error } from '../utils/authUtils';

function AuthorsPage() {
    const navigate = useNavigate();

    const [searchText, setSearchText] = useState('');
    const [user, setUser ] = useState(null);
    const [authors, setAuthors] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    if (!authors) {
       return <div >Пока что авторов нет </div>;
    }


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
                    return;
                }
                setUser (response.data);
            } catch (err) {
                if (err.response && err.response.status === 401) {
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
        if (!is401Error(navigate, "/authors_list")) return;
    }, [navigate]);

    useEffect(() => {
        const fetchAuthors = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/book_reviews/authors/authors_list');
                console.log("Authors: ", response.data)
                setAuthors(response.data);
                setLoading(false);
            } catch (err) {
                setError(err);
                message.error("Failed to fetch authors");
                setLoading(false);
            }
        };
        fetchAuthors();
    }, []);

    if (loading) {
        return <Spin />;
    }

    if (error) {
        return <div>{error}</div>;
    }
    const handleSearchChange = (e) => {
        setSearchText(e.target.value);
    };

    const filteredAuthors = authors.filter(author => {
        if (!searchText) return true;
        return (
            (author.name && author.name.toLowerCase().includes(searchText.toLowerCase()))
        );
    });

    return (
        <>
            <div id="title">
                <h1>Авторы</h1>
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

             <div id="cards-authors-container">
                 {filteredAuthors.length > 0 ? (
                    filteredAuthors.map((author, index) => (
                        <AuthorCard key={index}
                        authors={author}
                        setAuthors={setAuthors}
                        user={user}/>
                    ))
                ) : (
                    <div> По таким фильтрам авторы не найдены </div>
                )}
            </div>
        </>
    );
}

export default AuthorsPage;