import React, { useEffect, useState } from 'react';
import { Card, Space, Tree, Button, Input, message, Modal, Typography, Rate } from 'antd';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { updateReview } from '../utils/reviewsUtils.jsx'
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import DOMPurify from 'dompurify';
import '../index.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { isAuthenticated, is401Error } from '../utils/authUtils';


const { Paragraph } = Typography;

function ReviewCard({ reviews, user, isProfilePage, setReviews}) {
    const navigate = useNavigate();
    const bookDescription = reviews?.book?.book_description || reviews?.book_description || "Описание отсутствует";

    const [treeData, setTreeData] = useState([])

    const [isEditing, setIsEditing] = useState(false);

    const [formData, setFormData] = useState({
        reviewTitle: reviews.review_title || null,
        reviewBody: reviews.review_body || null,
        rating: reviews.rating || 0
    });

    const [isExpanded, setIsExpanded] = useState(false);
    const MAX_LENGTH = 100;

     useEffect(() => {
      const data = [
          {
            title: <div className='tree-container'>Описание книги</div>,
              key: '0-0',
              children: [
                  {
                      title: <div className='tree-container'>{bookDescription}</div>,
                      key: '0-0-0',
                  },
              ],
          },
      ];
      setTreeData(data);
    }, [bookDescription]);


    const handleUpdateReview = (reviewId, updatedData) => {
        updateReview(reviews, setReviews, reviewId, updatedData);
    };

    const handleEditClick = () => {

        const token = localStorage.getItem('user_access_token')
        if (!is401Error(navigate, "/reviews")) return;
        setIsEditing(true);
        console.log("Editing review id: ", reviews.id)
    };

    const handleCancel = () => {
        setIsEditing(false);
        setFormData({
            reviewTitle: reviews.review_title,
            reviewBody: reviews.review_body
        });
    };

     const handleSave = async () => {
        const requestData = {
            review_title: formData.reviewTitle || null,
            review_body: formData.reviewBody || null,
            rating: formData.rating || 0
        };

        try {
            const response = await axios.put(
                `http://127.0.0.1:8000/book_reviews/reviews/change_review/${reviews.id}`,
                requestData,
                {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                    }
                }
            );

            if (response.data.status_code === 200) {
                handleUpdateReview(reviews.id, requestData);
                setIsEditing(false);
                message.success('Обзор успешно обновлен');
            }
        } catch (error) {
            message.error(error.response?.data?.detail || 'Ошибка при обновлении обзора');
        }
    };

    const handleDelete = async () => {

        const token = localStorage.getItem('user_access_token')
        if (!is401Error(navigate, "/reviews")) return;
        Modal.confirm({
            title: 'Подтверждение удаления',
            content: 'Вы уверены, что хотите удалить этот обзор?',
            okText: 'Да',
            okType: 'danger',
            cancelText: 'Нет',
            onOk: async () => {
                try {
                    const response = await axios.delete(`http://127.0.0.1:8000/book_reviews/reviews/delete_review/${reviews.id}`, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                        }
                    });

                    if (response.data.status_code === 200) {
                        message.success('Обзор успешно удален');
                        setReviews((prevReviews) => prevReviews.filter((r) => r.id !== reviews.id));
                    }
                } catch (error) {
                    message.error('Ошибка при удалении обзора');
                    console.error('Ошибка при удалении обзора:', error.response ? error.response.data : error.message);
                }
            }
        });
    };

    const formatReviewBody = (body) => {
        if (!body) {
            return <Paragraph>Обзор отсутствует</Paragraph>;
        }
        return body.split('\n').map((line, index) => (
            <Paragraph key={index} style={{ fontSize: '18px' }}>{line}</Paragraph>
        ));
    };
    const renderReviewBody = (body) => {
        if (!body) {
            return <Paragraph>Обзор отсутствует</Paragraph>;
        }
        const cleanHTML = DOMPurify.sanitize(body);
        return (
            <div dangerouslySetInnerHTML={{ __html: cleanHTML }} />
        );
    };

    return (
            <div id='card'>
                <Card
                    title={
                        <div id='card-title'>
                            {console.log("User is admin?", user)}
                            {localStorage.getItem('user_access_token') && user?.is_admin ||
                             (isProfilePage && reviews.created_by === user?.id) ? (
                                <div id="card-update">
                                    <Button
                                        type="link"
                                        icon={<EditOutlined />}
                                        onClick={handleEditClick}
                                        size="large"
                                    />
                                </div>
                            ) : null}
                            <div id="title-and-img">
                                <img src={reviews.book?.book_cover || reviews.reviewed_book_cover} alt='img' width="80" />
                                <h1 id="text">{reviews.review_title}</h1>
                            </div>
                            <div id="book-info">
                                <h3 id="text">{reviews.book?.author?.name || reviews.reviewed_book_author_name}</h3>
                                <p>{reviews.book?.book_name || reviews.reviewed_book_name}</p>
                                <div className="tree-container" id="text">
                                    <Tree
                                        treeData={treeData}
                                        className="custom-tree"
                                    />
                                </div>
                            </div>
                            <p>
                                Автор обзора: <a
                                    href={`/user/${reviews.user?.id || reviews.created_by_name}`}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    {reviews.user?.name || reviews.created_by_name}
                                </a>
                            </p>
                            <p>Обзор обновлен: {new Date(reviews.updated).toLocaleString()}</p>
                        </div>
                    }
                >
                    <div id='card-content'>
                        {isEditing ? (
                            <div className="edit-review-container">
                                <Input
                                    placeholder="Заголовок обзора"
                                    value={formData.reviewTitle}
                                    onChange={(e) => setFormData({ ...formData, reviewTitle: e.target.value })}
                                />

                                <div>
                                    <Rate
                                        value={formData.rating}
                                        onChange={(value) => setFormData({...formData, rating: value})}
                                    />
                                </div>

                                <ReactQuill
                                    value={formData.reviewBody}
                                    onChange={(value) => setFormData({ ...formData, reviewBody: value })}
                                />
                                <Button onClick={handleSave}>Сохранить</Button>
                                <Button onClick={handleCancel}>Отменить</Button>
                                <Button type="danger" icon={<DeleteOutlined />} onClick={handleDelete}>Удалить</Button>
                            </div>
                        ) : (
                            <div>
                                <div>
                                    {isExpanded ? (
                                        <>
                                            {renderReviewBody(reviews.review_body)}
                                            <Rate
                                                value={formData.rating}
                                                disabled
                                                style={{ marginBottom: '10px' }}
                                            />
                                        </>
                                    ) : (
                                        <>
                                            {renderReviewBody(reviews.review_body.slice(0, MAX_LENGTH))}
                                            <Rate
                                                value={formData.rating}
                                                disabled
                                                style={{ marginBottom: '10px' }}
                                            />
                                        </>
                                    )}

                                    {reviews.review_body.length > MAX_LENGTH && (
                                        <Button type="link" onClick={() => setIsExpanded(!isExpanded)}>
                                            {isExpanded ? 'Свернуть' : 'Развернуть'}
                                        </Button>
                                    )}
                                </div>
                            </div>
                        )}
                    </div>
                </Card>
            </div>
        );
    };

export default ReviewCard;