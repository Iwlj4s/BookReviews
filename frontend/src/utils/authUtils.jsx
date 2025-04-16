import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { message} from 'antd';

export const isAuthenticated = (navigate, navigateTo) => {
    const token = localStorage.getItem('user_access_token');
    if (!token) {
        localStorage.removeItem('user_access_token');
        navigate(navigateTo);
        return false;
    }
    return true;
};

export const is401Error = async (navigate, navigateTo) => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/me/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
            }
        });
        if (response.status === 401) {
            console.log("Error 401 from is401Error");
            navigate(navigateTo);
            return true;
        }
    } catch (err) {

        if (err.response && err.response.status === 401) {
            console.log("error from err.response.status", err.response.data.detail)
            navigate(navigateTo);
        } else {
            console.error("Error fetching user data:", err);
            setError("Ошибка при загрузке данных пользователя");
        }
    };
    return false;
};