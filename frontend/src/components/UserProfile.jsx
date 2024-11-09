import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { Card, Descriptions, Button, Spin, Input, message, Modal, Select, Spin as AntdSpin, Form } from 'antd';
import { EditOutlined, MailOutlined, UserOutlined, LockOutlined, PlusCircleOutlined, SearchOutlined } from '@ant-design/icons';
import '../index.css';
import { updateReview } from '../utils/reviewsUtils.jsx'
import ReviewCard from './ReviewCard.jsx';
import AdminStuff from './AdminStuff.jsx';

const { Option } = Select;

function UserProfile({ user, onLogout, onUpdateUserData }) {
    if (!user) {
        console.log("can't get user in UserProfile");
        return <div id="spin"><Spin /> </div>;
    }
    const navigate = useNavigate();

    const [reviews, setReviews] = useState([]);

    const [isEditing, setIsEditing] = useState(false);

    const [formData, setFormData] = useState({
        name: user?.name || null,
        email: user?.email || null,
        password: ''
    });

    const [searchText, setSearchText] = useState('');

    const [reviewFormData, setReviewFormData] = useState({
        reviewTitle: '',
        author: '',
        book: '',
        reviewBody: ''
    });

    const [books, setBooks] = useState([]);
    const [authors, setAuthors] = useState([]);
    const [selectedAuthor, setSelectedAuthor] = useState(null);

    const [isModalVisible, setIsModalVisible] = useState(false);
    const [reviewForm, setReviewForm] = useState({
        review_title: '',
        reviewed_book_name: '',
        reviewed_book_author_name: '',
        review_body: ''
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');


    useEffect(() => {
        if (user) {
            setFormData({
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
            const booksResponse = await axios.get('http://127.0.0.1:8000/book_reviews/books/books_list/');
            const authorsResponse = await axios.get('http://127.0.0.1:8000/book_reviews/authors/authors_list/');
            setBooks(booksResponse.data);
            setAuthors(authorsResponse.data);
            console.log("Fetched books", booksResponse.data);
        } catch (error) {
            message.error('Ошибка при загрузке книг и авторов.');
            console.error(error);
        }
    };

    const filteredBooks = selectedAuthor ? books.filter(book => book.author.name === selectedAuthor) : books;


    const fetchUserData = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/book_reviews/users/me/', {
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
        setLoading(true);
        setError('');

        const requestData = {
            name: formData.name || null,
            email: formData.email || null,
            ...(formData.password ? { password: formData.password } : {})
        };

        try {
            const response = await axios.put('http://127.0.0.1:8000/book_reviews/users/change_me/', requestData, {
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
                setIsEditing(false);
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
            reviewed_book_name: '',
            reviewed_book_author_name: '',
            review_body: ''
        });
    };

    const handleAddReview = async () => {
        const { review_title, reviewed_book_name, reviewed_book_author_name, review_body } = reviewForm;

        if (!review_title || !reviewed_book_name || !reviewed_book_author_name || !review_body) {
            message.error('Пожалуйста, заполните все поля.');
            return;
        }

        try {
            const response = await axios.post('http://127.0.0.1:8000/book_reviews/reviews/create_review/', reviewForm, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`,
                    'Content-Type': 'application/json'
                }
            });

            if (response.data.status_code === 200) {
                console.log("Response: ", response.data)
                message.success('Обзор добавлен успешно!');
                const newReview = {
                    review_id: response.data.data.review_id,
                    id: response.data.data.id,
                    book_cover: response.data.data.book_cover,
                    book_name: response.data.data.book_name,
                    author_name: response.data.data.author_name,
                    review_title: response.data.data.review_title,
                    review_body: response.data.data.review_body,
                    book_description: response.data.data.book_description,
                    created_by: response.data.data['Created by'],
                    updated: new Date().toISOString()
                };

                setReviews((prev) => [...prev, newReview]);
                handleCancelModal();
                handleCancel();
            }
        } catch (error) {
            message.error('Ошибка при добавлении обзора.');
            console.error(error);
        }
    };


    return (
        <>
            {/* User Info */}
            <div id="user-info-container">
                <div id="user-info">
                    <div className="user-info-header">
                        <h2>Информация о пользователе</h2>
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
                        <Form.Item label="Выбор автора">
                            <Select
                                showSearch
                                onChange={(value) => {
                                    setReviewForm({ ...reviewForm, reviewed_book_author_name: value });
                                    setSelectedAuthor(value);
                                }}
                                placeholder="Выберите автора"
                            >
                                {authors.map(author => (
                                    <Option key={author.id} value={author.name}>
                                        {author.name}
                                    </Option>
                                ))}
                            </Select>
                        </Form.Item>

                        <Form.Item label="Выбор книги">
                            <Select
                                showSearch
                                onChange={(value) => setReviewForm({ ...reviewForm, reviewed_book_name: value })}
                                placeholder="Выберите книгу"
                            >
                                {filteredBooks.map(book => (
                                    <Option key={book.id} value={book.book_name}>
                                        {book.book_name}
                                    </Option>
                                ))}
                            </Select>
                        </Form.Item>

                        <Form.Item label="Обзор">
                            <Input.TextArea
                                value={reviewForm.review_body}
                                onChange={(e) => setReviewForm({ ...reviewForm, review_body: e.target.value })}
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
                    filteredReviews.map((userReviews, index) => (
                        <ReviewCard key={index}
                                    reviews={userReviews}
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