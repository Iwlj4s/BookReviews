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
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    if (loading) {
        return <Spin id="spin" />;
    }

    return (
         <div id="user-profile-container">
            <div id="profile-content">
                <OtherUserProfile userId={userId} />
            </div>
        </div>
    );

};

export default OtherUserProfilePage;
