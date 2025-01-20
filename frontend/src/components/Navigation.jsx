import { NavLink } from 'react-router-dom';
import { useEffect, useState } from 'react';

const Navigation = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('user_access_token');
        if (!token){
            setIsLoggedIn(false)
            }else{
                setIsLoggedIn(true)
                }
    }, []);

    return (
        <div id="navbar-container">
            <nav id="navbar">
                <ul id="navbar-ul">
                    <li id="navbar-item"><NavLink to='/'>Главная</NavLink></li>
                    <li id="navbar-item"><NavLink to='/reviews'>Обзоры</NavLink></li>
                    <li id="navbar-item"><NavLink to='/books_list'>Книги</NavLink></li>
                    <li id="navbar-item"><NavLink to='/authors_list'>Авторы</NavLink></li>
                    <li id="navbar-item"><NavLink to='/users_list'>Пользователи</NavLink></li>
                </ul>
                <div id="right-side-items">
                    {isLoggedIn ? (
                        <li id="navbar-item"><NavLink to='/me'>Профиль</NavLink></li>
                    ) : (
                        <li id="navbar-item"><NavLink to='/sign_in'>Войти</NavLink></li>
                    )}
                </div>
            </nav>
        </div>
    );
};

export default Navigation;