import { NavLink } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { MenuOutlined, CloseOutlined } from '@ant-design/icons';

const Navigation = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('user_access_token');
        setIsLoggedIn(!!token);
    }, []);

    const toggleMobileMenu = () => {
        setMobileMenuOpen(!mobileMenuOpen);
        
        // Блокируем/разблокируем скролл страницы при открытии/закрытии меню
        if (!mobileMenuOpen) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    };

    const closeMobileMenu = () => {
        setMobileMenuOpen(false);
        document.body.style.overflow = ''; // Восстанавливаем скролл
    };

    return (
        <div id="navbar-container">
            <nav id="navbar">
                <button 
                    id="mobile-menu-button" 
                    onClick={toggleMobileMenu}
                    aria-label="Меню"
                >
                    {mobileMenuOpen ? <CloseOutlined /> : <MenuOutlined />}
                </button>
                
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
            
            {/* Мобильное меню */}
            <div id="mobile-menu" className={mobileMenuOpen ? "active" : ""}>
                <ul>
                    <li><NavLink to='/' onClick={closeMobileMenu}>Главная</NavLink></li>
                    <li><NavLink to='/reviews' onClick={closeMobileMenu}>Обзоры</NavLink></li>
                    <li><NavLink to='/books_list' onClick={closeMobileMenu}>Книги</NavLink></li>
                    <li><NavLink to='/authors_list' onClick={closeMobileMenu}>Авторы</NavLink></li>
                    <li><NavLink to='/users_list' onClick={closeMobileMenu}>Пользователи</NavLink></li>
                    {isLoggedIn ? (
                        <li><NavLink to='/me' onClick={closeMobileMenu}>Профиль</NavLink></li>
                    ) : (
                        <li><NavLink to='/sign_in' onClick={closeMobileMenu}>Войти</NavLink></li>
                    )}
                </ul>
            </div>
        </div>
    );
};

export default Navigation;