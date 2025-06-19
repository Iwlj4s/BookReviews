import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Descriptions, Button, Spin, Input, message, Modal, Select, Form } from 'antd';
import { EditOutlined, MailOutlined, UserOutlined, LockOutlined, PlusCircleOutlined, SearchOutlined } from '@ant-design/icons';
import { LogoutOutlined } from '@ant-design/icons';
import '../index.css';

import OtherUserProfile from '../components/OtherUserProfile.jsx';

const OtherUserProfilePage = () => {
    const { userId } = useParams();
    const [currentUser, setCurrentUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchCurrentUser = async () => {
            try {
                const token = localStorage.getItem('user_access_token');
                if (!token) {
                    setLoading(false);
                    return;
                }
                
                const response = await axios.get('https://87.228.10.180/api/users/me/', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                setCurrentUser(response.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchCurrentUser();
    }, []);

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div id="user-profile-container">
           <div id="profile-content">
                <OtherUserProfile userId={userId} currentUser={currentUser} />  
           </div>
       </div>
   ); 
};

export default OtherUserProfilePage;
