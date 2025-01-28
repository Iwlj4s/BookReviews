import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Spin, message, Input } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import '../index.css';
import UserCard from '../components/UserCard.jsx';

import { isAuthenticated, is401Error } from '../utils/authUtils';

function UsersPage() {
    const navigate = useNavigate();

    const [searchText, setSearchText] = useState('');
    const [user, setUser ] = useState(null);
    const [users, setUsers] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
       if (!is401Error(navigate, "/users_list")) return;
        const token = localStorage.getItem('user_access_token');
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
        const fetchUsers= async () => {
            try {
                const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/users_list');
                console.log("User  ", response.data);
                setUsers(response.data);
                setLoading(false);
            } catch (err) {
                setError(err);
                message.error("Failed to fetch Users");
                setLoading(false);
            }
        };
        fetchUsers();
    }, []);

    if (loading) {
        return <Spin />;
    }

    if (error) {
        return <div>{error.message || 'Произошла ошибка при загрузке пользователей'}</div>;
    }

     if (!users || users.length === 0) {
        return <div id="spin">Пока что пользователей нет</div>;
    }

    const handleSearchChange = (e) => {
        setSearchText(e.target.value);
    };

    const filteredUsers = users.filter(user => {
        if (!searchText) return true;
        return (
             (user.user_name && user.user_name.toLowerCase().includes(searchText.toLowerCase()))
        );
    });

    return (
        <>
            <div id="title">
                <h1>Пользователи</h1>
            </div>

            <div id="user-reviews-search">
                <Input
                    placeholder="Поиск пользователей"
                    value={searchText}
                    onChange={handleSearchChange}
                    prefix={<SearchOutlined />}
                    style={{ marginBottom: '20px', width: '100%' }}
                />
            </div>

             <div id="cards-authors-container">
                 {filteredUsers.length > 0 ? (
                    filteredUsers.map((user, index) => (
                        <UserCard key={index}
                        user={user}
                        setUser={setUsers}/>
                    ))
                ) : (
                    <div> По таким фильтрам пользователи не найдены </div>
                )}
            </div>
        </>
    );
}

export default UsersPage;