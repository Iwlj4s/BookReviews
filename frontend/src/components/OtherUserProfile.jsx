import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import { Card, Descriptions, Input, message, Spin, Modal, Button } from 'antd';
import { SearchOutlined, MailOutlined } from '@ant-design/icons';
import '../index.css';
import { updateReview } from '../utils/reviewsUtils.jsx';
import ReviewCard from './ReviewCard.jsx';

{/* TODO: Add Other Users link in navigate and page for check them,
add search by user name and link to navigate in selected user's  */}

function OtherUserProfile({ userId, currentUser }) {
    const navigate = useNavigate();
    const [user, setUser ] = useState(null);
    const [reviews, setReviews] = useState([]);

    const [searchText, setSearchText] = useState('');

    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [isModalVisible, setIsModalVisible] = useState(false);
    const [emailTheme, setEmailTheme] = useState('');
    const [emailBody, setEmailBody] = useState('');

    console.log('Current user:', currentUser);
    console.log('Is admin:', currentUser?.is_admin);
   useEffect(() => {
    const fetchUserData = async () => {
        try {
            const response = await axios.get(`https://87.228.10.180/api/users/user/${userId}`);
            console.log(response.data);
            setUser (response.data);
            setReviews(response.data.reviews || []);
        } catch (err) {
            console.error(err);
            setError('Ошибка при загрузке данных пользователя');
            message.error('Ошибка при загрузке данных пользователя');
        } finally {
            setLoading(false);
        }
    };

    fetchUserData();
    }, [userId]);

    const handleSendEmail = async () => {
        const emailData = {
            receiver_email: user.email,
            mail_theme: emailTheme,
            mail_body: emailBody
        };


        try {
            const response = await axios.post(`https://87.228.10.180/api/admin/mail/send_letter`, emailData, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });
            if (response.data.status_code === 200) {
                message.success('Письмо успешно отправлено!');
                setIsModalVisible(false);
            }
        } catch (error) {
            message.error('Ошибка при отправке письма');
            console.error(error);
        }
    };

    const showModal = () => {
        setIsModalVisible(true);
    };


    const handleCancel = () => {
        setIsModalVisible(false);
        setEmailTheme('');
        setEmailBody('');
    };


    const handleUpdateReview = (reviewId, updatedData) => {
        updateReview(reviews, setReviews, reviewId, updatedData);
    };

    const handleSearchChange = (e) => {
        setSearchText(e.target.value);
    };

    const filteredReviews = reviews.filter(review => {
        if (!searchText) return true;
        return (
            (review.reviewed_book_author_name && review.reviewed_book_author_name.toLowerCase().includes(searchText.toLowerCase())) ||
            (review.reviewed_book_name && review.reviewed_book_name.toLowerCase().includes(searchText.toLowerCase())) ||
            (review.review_title && review.review_title.toLowerCase().includes(searchText.toLowerCase()))
        );
    });

    if (loading) return <Spin />;
    if (error) return <div>{error}</div>;

    return (
        <>
            {/* User Info */}
            <div className="profile-header">
                <h1 id="title">{user.name || 'Не указано'}</h1>

            </div>
            <div id="user-info-container">
                <div id="user-info">
                    {user.bio ? (
                        <div style={{ textAlign: 'center' }} dangerouslySetInnerHTML={{ __html: user.bio }}></div>
                    ) : (
                        <div style={{
                            textAlign: 'center',
                            color: '#888',
                            fontStyle: 'italic',
                            background: '#f5f5f5',
                            borderRadius: '8px',
                            padding: '16px',
                            margin: '16px 0',
                            boxShadow: '0 2px 8px rgba(0,0,0,0.03)'
                        }}>
                            Пользователь пока что не добавил биографию
                        </div>
                    )}
                    <Descriptions layout="vertical">
                        {user.is_admin && (
                            <Descriptions.Item label="Администратор">Да</Descriptions.Item>
                        )}
                    </Descriptions>
                </div>
            </div>

            {/* AdminStuff */}
            {currentUser?.is_admin && (
                <div id="admin-stuff-container">
                    {currentUser?.is_admin && (
                        <Button onClick={showModal} type="primary" icon={<MailOutlined />}>
                            Отправить письмо
                        </Button>
                    )}
                </div>
            )}
        
            {/* Email Modal */}
            {/* {currentUser?.is_admin && (
                <Button onClick={showModal} type="primary" icon={<MailOutlined />}>
                    Отправить письмо
                </Button>
            )} */}

            <Modal
                title="Отправить письмо пользователю"
                open={isModalVisible} // Изменено с visible на open
                onCancel={handleCancel}
                footer={[
                    <Button key="back" onClick={handleCancel}>
                        Отмена
                    </Button>,
                    <Button key="submit" type="primary" onClick={handleSendEmail}>
                        Отправить
                    </Button>,
                ]}
            >
                <Input
                    placeholder="Тема письма"
                    value={emailTheme}
                    onChange={(e) => setEmailTheme(e.target.value)}
                />
                <Input.TextArea
                    placeholder="Тело письма"
                    value={emailBody}
                    onChange={(e) => setEmailBody(e.target.value)}
                    rows={4}
                />
            </Modal>

            {/* My Reviews */}
            <div id="title">
                <h1>Обзоры Пользователя</h1>
            </div>

            {/* Reviews Search */}
            <div id="user-reviews-search">
                <Input
                    placeholder="Поиск по обзорам"
                    value={searchText}
                    onChange={handleSearchChange}
                    prefix={<SearchOutlined />}
                />
            </div>

            {/* Reviews Cards */}
            {reviews.length === 0 ? (
                <div id="title"><h3>У пользователя пока нет обзоров</h3></div>
            ) : (
                <div id="cards-container">
                    {filteredReviews.length > 0 ? (
                        filteredReviews.map((userReviews, index) => (
                            <ReviewCard key={index}
                                        reviews={userReviews}
                                        user={user}
                                        setReviews={setReviews} />
                        ))
                    ) : (
                        <div>По таким фильтрам обзоры не найдены</div>
                    )}
                </div>
            )}
        </>
    );
};

export default OtherUserProfile;
