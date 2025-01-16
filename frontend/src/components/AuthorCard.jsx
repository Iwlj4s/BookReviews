import React, { useEffect, useState } from 'react';
import { Card, Tree, Button, Input, message, Modal, Typography, Avatar, Space } from 'antd';
import { useNavigate } from 'react-router-dom';
import { EditOutlined, DeleteOutlined, UserOutlined } from '@ant-design/icons';
import axios from 'axios';
import '../index.css';
import { updateAuthor } from '../utils/authorsUtils';
import { isAuthenticated, is401Error } from '../utils/authUtils';

function AuthorCard({ authors, user, setAuthors }) {
    const navigate = useNavigate();
    const [isEditing, setIsEditing] = useState(false);

    const [formData, setFormData] = useState({
        authorName: authors.name || '',
    });

    const handleEditClick = () => {
        if (!is401Error(navigate, "/authors_list")) return;
        setIsEditing(true);
    };

    const handleCancel = () => {
        setIsEditing(false);
        setFormData({
            authorName: authors.name,
        });
    };

    const handleSave = async () => {
        if (!is401Error(navigate, "/authors_list")) return;
        const requestData = {
            name: formData.authorName,
        };

        try {
            const response = await axios.put(`http://127.0.0.1:8000/book_reviews/admin/authors/change_author/${authors.id}`, requestData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`,
                },
            });
            console.log("Get response changed author: ", response)

            if (response.data.status_code === 200) {
                updateAuthor(authors, setAuthors, authors.id, requestData);
                message.success('Автор успешно обновлена');
                setIsEditing(false);
            }
        } catch (error) {
            message.error('Ошибка при обновлении автора');
            console.error('Ошибка при обновлении автора:', error);
        }
    };

    const handleDelete = async () => {
        if (!is401Error(navigate, "/authors_list")) return;
        Modal.confirm({
            title: 'Подтверждение удаления',
            content: 'Вы уверены, что хотите удалить этого автора?',
            okText: 'Да',
            okType: 'danger',
            cancelText: 'Нет',
            onOk: async () => {
                try {
                    const response = await axios.delete(`http://127.0.0.1:8000/book_reviews/admin/authors/delete_author/${authors.id}`, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`,
                        },
                    });

                    if (response.data.status_code === 200) {
                        message.success('Автор успешно удален');
                        setAuthors((prevAuthors) => prevAuthors.filter((a) => a.id !== authors.id));
                    }
                } catch (error) {
                    message.error('Ошибка при удалении автора');
                    console.error('Ошибка при удалении автора:', error.response.data.detail);
                }
            },
        });
    };

    return (
        <div id='card-authors'>
            <Card
                title={
                    <div id='card-title'>
                        <div id="title-and-img">
                            <Avatar shape="square" size={64} icon={<UserOutlined />} />
                        </div>
                        {user?.is_admin && (
                            <div id="card-update">
                                <Button
                                    type="link"
                                    icon={<EditOutlined />}
                                    onClick={handleEditClick}
                                    size="large"
                                />
                                <Button
                                    type="link"
                                    icon={<DeleteOutlined />}
                                    onClick={handleDelete}
                                    size="large"
                                />
                            </div>
                        )}
                        <div id="book-info">
                            <h3 id="text">{authors.name}</h3>
                        </div>
                    </div>
                }
            >
             {isEditing ? (
                    <div className="edit-book-container">
                        <Input
                            placeholder="Имя автора"
                            value={formData.authorName}
                            onChange={(e) => setFormData({ ...formData, authorName: e.target.value })}
                        />
                        <Button onClick={handleSave}>Сохранить</Button>
                        <Button onClick={handleCancel}>Отменить</Button>
                    </div>
                ) : (
                    null
                )}
            </Card>
        </div>
    );
};

export default AuthorCard;