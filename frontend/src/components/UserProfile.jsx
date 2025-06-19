import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Descriptions, Button, Spin, Input, message, Modal, Select, Spin as AntdSpin, Form, Typography, Rate } from 'antd';
import { EditOutlined, MailOutlined, UserOutlined, LockOutlined, PlusCircleOutlined, SearchOutlined } from '@ant-design/icons';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import '../index.css';
import { updateReview } from '../utils/reviewsUtils.jsx'
import ReviewCard from './ReviewCard.jsx';
import AdminStuff from './AdminStuff.jsx';

import { isAuthenticated, is401Error } from '../utils/authUtils';

{/* TODO: Add Icons to add author, send email etc ... */}

const { Option } = Select;
const { Paragraph } = Typography;

function UserProfile({ user, onLogout, onUpdateUserData }) {
    if (!user) {
        console.log("can't get user in UserProfile");
        return <div id="spin"><Spin /> </div>;
    }
    const navigate = useNavigate();

    const [reviews, setReviews] = useState([]);

    const [isEditing, setIsEditing] = useState(false);
    const [isEditingBio, setIsEditingBio] = useState(false);


    const [formData, setFormData] = useState({
        id: user?.id,
        name: user?.name || null,
        email: user?.email || null,
        bio: user?.bio || null,
        password: ''
    });

    const [searchText, setSearchText] = useState('');

    const [reviewFormData, setReviewFormData] = useState({
        reviewTitle: '',
        author: '',
        book: '',
        reviewBody: '',
        rating: 0
    });

    const [books, setBooks] = useState([]);
    const [authors, setAuthors] = useState([]);
    const [selectedAuthor, setSelectedAuthor] = useState(null);

    const [isModalVisible, setIsModalVisible] = useState(false);
    const [reviewForm, setReviewForm] = useState({
        review_title: '',
        review_body: '',
        rating: 0,
        reviewed_book_id: null,
        reviewed_book_author_id: null
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');


    useEffect(() => {
        if (user) {
            setFormData({
                id: user.id,
                name: user.name,
                email: user.email,
                password: ''
            });
            setReviews(user.reviews || []);
            console.log("Users Reviews: ", user.reviews)
        }
    }, [user]);

    const fetchBooksAndAuthors = async () => {
        try {
            const booksResponse = await axios.get('http://87.228.10.180/api/books/books_list/');
            const authorsResponse = await axios.get('http://87.228.10.180/api/authors/authors_list/');
            setBooks(booksResponse.data);
            setAuthors(authorsResponse.data);
            console.log("Fetched books", booksResponse.data);
        } catch (error) {
            message.error('Ошибка при загрузке книг и авторов.');
            console.error(error);
        }
    };

    const filteredBooks = selectedAuthor
        ? books.filter(book => book.author.id === selectedAuthor)
        : books;


    const fetchUserData = async () => {
        try {
            if (!isAuthenticated(navigate, "/sign_in")) return;
            const response = await axios.get('http://87.228.10.180/api/users/me/', {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });
            if (response.status === 401) {
                message.error('Токен недействителен');
                navigate("/sign_in");
                return;
            }
            return response.data;
        } catch (error) {
            if (error.response && error.response.status === 401) {
                message.error('Токен недействителен');
                navigate("/sign_in");
            } else {
                console.error('Ошибка при получении данных пользователя:', error.response ? error.response.data : error.message);
                throw error;
            }
        }
    };

    const handleEditClick = () => {
        if (!isAuthenticated(navigate, "/sign_in")) return;
        setIsEditing(true);
    };

    const handleCancel = () => {
        setIsEditing(false);
        setFormData({
            name: user.name,
            email: user.email,
            password: ''
        });
    };

    const handleSave = async () => {
        if (!isAuthenticated(navigate, "/sign_in")) return;
        setLoading(true);
        setError('');

        const requestData = {
            id: user.id || null,
            name: formData.name || null,
            email: formData.email || null,
            bio: formData.bio || null,
            ...(formData.password ? { password: formData.password } : {})
        };

        try {
            const response = await axios.put('http://87.228.10.180/api/users/change_me/', requestData, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });

            console.log("Request data: ", requestData)
            console.log("status code: ", response.data.status_code)
            console.log("Taking data in user profile:", response.data.data)

            if (response.data.status_code === 401) {
                console.log("Navigate to login after pass change")
                message.success('Данные обновлены успешно!');
                const updatedUser = await fetchUserData();
                onUpdateUserData(updatedUser);

                localStorage.removeItem('user_access_token');
                navigate('/sign_in');
                setIsEditing(false);

            } else {
                console.log("Data changed")
                message.success('Данные обновлены успешно!');
                const updatedUser = await fetchUserData();
                onUpdateUserData(updatedUser);
                // Закрываем оба режима редактирования
                setIsEditing(false);
                setIsEditingBio(false);
            }
        } catch (err) {
            console.error('Ошибка при сохранении данных:', err.response ? err.response.data : err.message);
            setError('Ошибка при сохранении данных');
        } finally {
            setLoading(false);
        }
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

    const showModal = async () => {
        setIsModalVisible(true);
        await fetchBooksAndAuthors();
    };

    const handleCancelModal = () => {
        setIsModalVisible(false);
        setReviewForm({
            review_title: '',
            review_body: '',
            rating: 0,
            reviewed_book_id: null,
            reviewed_book_author_id: null
        });
    };

    const handleAddReview = async () => {
        if (!isAuthenticated(navigate, "/sign_in")) return;
        const { review_title, review_body, reviewed_book_id, reviewed_book_author_id, rating } = reviewForm;

        if (!review_title || !review_body || !reviewed_book_id || !reviewed_book_author_id) {
            message.error('Пожалуйста, заполните все поля.');
            return;
        }

        try {
            const response = await axios.post('http://87.228.10.180/api/reviews/create_review/', {
                review_title,
                review_body,
                rating,
                reviewed_book_id,
                reviewed_book_author_id
            }, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.data.status_code === 200) {
                message.success('Обзор добавлен успешно!');
                handleCancelModal();
                // Получаем обновлённые данные пользователя и обновляем обзоры
                const updatedUser = await fetchUserData();
                setReviews(updatedUser.reviews || []);
            }
        } catch (error) {
            message.error('Ошибка при добавлении обзора.');
            console.error(error);
        }
    };

    const handleEditBioClick = () => {
        if (!isAuthenticated(navigate, "/sign_in")) return;
        setIsEditingBio(true);
    };

    const handleCancelBio = () => {
        setIsEditingBio(false);
        setFormData({
            ...formData,
            bio: user.bio
        });
    };

    const renderBioContent = () => {
        const bioToShow = isEditingBio ? formData.bio : (user.bio || formData.bio);

        if (!bioToShow) {
            return <Paragraph>Биография не указана</Paragraph>;
        }

        return <div dangerouslySetInnerHTML={{ __html: bioToShow }} />;
    };

    return (
        <>
            {/* User Info */}
            <div id="user-info-container">
                <div id="user-info">
                    <div className="user-info-header">
                        <h2>Моя информация</h2>
                        <Button
                            type="link"
                            icon={<EditOutlined />}
                            onClick={handleEditClick}
                            size="large"
                        />
                    </div >

                    {/* Edit User */}
                    {isEditing ? (
                        <div id="change-user-data">
                            <Input
                                placeholder="Имя пользователя"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                prefix={<UserOutlined />}
                            />
                            <Input
                                placeholder="Email"
                                value={formData.email}
                                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                prefix={<MailOutlined />}
                            />
                            <Input.Password
                                placeholder="Пароль"
                                value={formData.password}
                                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                                prefix={<LockOutlined />}
                            />
                            <Button onClick={handleSave} loading={loading}>Сохранить</Button>
                            <Button onClick={handleCancel}>Отменить</Button>
                            {error && <div style={{ color: 'red' }}>{error}</div>}
                        </div>
                    ) : (
                        <Descriptions layout="vertical">
                            <Descriptions.Item label="Имя пользователя">{user.name || 'Не указано'}</Descriptions.Item>
                            <Descriptions.Item label="Email">{user.email || 'Не указано'}</Descriptions.Item>
                            {user.is_admin && (
                                <Descriptions.Item label="Администратор">Да</Descriptions.Item>
                            )}
                        </Descriptions>
                    )}
                </div>

                {/* Bio Section */}
                <div id="user-bio" style={{ marginTop: '20px' }}>
                    <Card
                        title={
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <h2>Моя биография</h2>
                                <Button
                                    type="link"
                                    icon={<EditOutlined />}
                                    onClick={handleEditBioClick}
                                    size="large"
                                />
                            </div>
                        }
                    >
                        {isEditingBio ? (
                            <div>
                                <ReactQuill
                                    value={formData.bio || user.bio || ''}
                                    onChange={(value) => setFormData({ ...formData, bio: value })}
                                    modules={{
                                        toolbar: [
                                            [{ 'header': [1, 2, false] }],
                                            ['bold', 'italic', 'underline', 'strike', 'blockquote'],
                                            [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                                            ['link', 'image'],
                                            ['clean']
                                        ],
                                    }}
                                />
                                <div style={{ marginTop: '20px' }}>
                                    <Button onClick={handleSave} loading={loading}>Сохранить</Button>
                                    <Button onClick={handleCancelBio} style={{ marginLeft: '10px' }}>Отменить</Button>
                                </div>
                            </div>
                        ) : (
                            <div style={{ minHeight: '100px' }}>
                                {renderBioContent()}
                            </div>
                        )}
                    </Card>
                </div>
            </div>


            {/* AdminStuff */}
            {user.is_admin && (
                   <div id="admin-stuff-container">
                        {user.is_admin && (
                            <AdminStuff user={user}/>
                        )}
                    </div>
            )}

            {/* My Reviews */}
            <div id="title">
                <h1>Мои обзоры</h1>
                <div id="new-review-btn">
                    <Button
                        type="link"
                        icon={<PlusCircleOutlined />}
                        onClick={showModal}
                        size="large"
                    />
                </div>
            </div>

            {/* Add Review */}
            <div id="add-review-modal">
                <Modal
                    title="Добавить обзор"
                    visible={isModalVisible}
                    onCancel={handleCancelModal}
                    footer={[
                        <Button key="back" onClick={handleCancelModal}>
                            Отмена
                        </Button>,
                        <Button key="submit" type="primary" onClick={handleAddReview}>
                            Добавить
                        </Button>,
                    ]}
                >
                    <Form layout="vertical">

                        <Form.Item label="Заголовок обзора">
                            <Input
                                value={reviewForm.review_title}
                                onChange={(e) => setReviewForm({ ...reviewForm, review_title: e.target.value })}
                            />
                        </Form.Item>
                        <Form.Item label="Оценка книги">
                            <Rate
                                value={reviewForm.rating}
                                onChange={(value) => setReviewForm({...reviewForm, rating: value})}
                            />
                        </Form.Item>
                        <Form.Item label="Выбор автора">
                            <Select
                                showSearch
                                onChange={(value) => {
                                    setReviewForm({ ...reviewForm, reviewed_book_author_id: value });
                                    setSelectedAuthor(value);
                                }}
                                placeholder="Выберите автора"
                                value={reviewForm.reviewed_book_author_id}
                            >
                                {authors.map(author => (
                                    <Option key={author.id} value={author.id}>
                                        {author.name}
                                    </Option>
                                ))}
                            </Select>
                        </Form.Item>

                        <Form.Item label="Выбор книги">
                            <Select
                                showSearch
                                onChange={(value) => setReviewForm({ ...reviewForm, reviewed_book_id: value })}
                                placeholder="Выберите книгу"
                                value={reviewForm.reviewed_book_id}
                            >
                                {filteredBooks.map(book => (
                                    <Option key={book.id} value={book.id}>
                                        {book.book_name}
                                    </Option>
                                ))}
                            </Select>
                        </Form.Item>

                        <Form.Item label="Обзор">
                           <ReactQuill
                                value={reviewForm.review_body}
                                onChange={(value) => setReviewForm({ ...reviewForm, review_body: value })}
                            />
                        </Form.Item>
                    </Form>
                </Modal>
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
            <div id="cards-container">
                {reviews.length === 0 ? (
                    <div>У вас пока нет обзоров</div>
                ) : filteredReviews.length > 0 ? (
                    filteredReviews.map((review, index) => (
                        <ReviewCard key={review.id || index}
                                    reviews={review}
                                    user={user}
                                    isProfilePage={true}
                                    setReviews={setReviews}/>
                    ))
                ) : (
                    <div>По таким фильтрам обзоры не найдены</div>
                )}
            </div>
        </>
    );
};

export default UserProfile;