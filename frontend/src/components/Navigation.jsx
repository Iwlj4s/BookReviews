import { NavLink } from 'react-router-dom';

const Navigation = () => (
    <div id="navbar-container">
        <nav id="navbar">
            <ul id="navbar-ul">
                <li id="navbar-item"><NavLink to='/'>Главная</NavLink></li>
                <li id="navbar-item"><NavLink to='/reviews'>Обзоры</NavLink></li>
                <li id="navbar-item"><NavLink to='/books'>Книги</NavLink></li>
            </ul>
        </nav>
    </div>

    );

export default Navigation;