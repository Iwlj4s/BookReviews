import React, { useEffect, useState } from 'react';
import { Card, Tree, Button, Input, message, Modal, Typography } from 'antd';
import { useNavigate } from 'react-router-dom';
import { EditOutlined, DeleteOutlined } from '@ant-design/icons';
import axios from 'axios';
import '../index.css';
import { updateBook } from '../utils/booksUtils';
import { isAuthenticated, is401Error } from '../utils/authUtils';

const { Paragraph } = Typography;

function BookCard({ books, user, setBooks }) {
    const navigate = useNavigate();
    const [treeData, setTreeData] = useState([]);
    const [isEditing, setIsEditing] = useState(false);
    const [formData, setFormData] = useState({
        bookName: books.book_name || '',
        bookDescription: books.book_description || '',
    });

    const bookDescription = books.book_description;

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

    const handleEditClick = () => {
        if (!is401Error(navigate, "/books_list")) return;
        setIsEditing(true);
    };

    const handleCancel = () => {
        setIsEditing(false);
        setFormData({
            bookName: books.book_name,
            bookDescription: books.book_description,
        });
    };

    const handleSave = async () => {
        if (!is401Error(navigate, "/books_list")) return;
        const requestData = {
            book_name: formData.bookName,
            book_description: formData.bookDescription,
        };

        try {
            const response = await axios.put(`http://127.0.0.1:8000/book_reviews/admin/book/change_book/${books.id}`, requestData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`,
                },
            });

            if (response.data.status_code === 200) {
                updateBook(books, setBooks, books.id, requestData);
                message.success('Книга успешно обновлена');
                setIsEditing(false);
            }
        } catch (error) {
            message.error('Ошибка при обновлении книги');
            console.error('Ошибка при обновлении книги:', error.response.data.detail);
        }
    };

    const handleDelete = async () => {
        if (!is401Error(navigate, "/books_list")) return;
        Modal.confirm({
            title: 'Подтверждение удаления',
            content: 'Вы уверены, что хотите удалить эту книгу?',
            okText: 'Да',
            okType: 'danger',
            cancelText: 'Нет',
            onOk: async () => {
                try {
                    const response = await axios.delete(`http://127.0.0.1:8000/book_reviews/admin/books/delete_book/${books.id}`, {
                        headers: {
                            'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`,
                        },
                    });

                    if (response.data.status_code === 200) {
                        message.success('Книга успешно удалена');
                        setBooks((prevBooks) => prevBooks.filter((b) => b.id !== books.id));
                    }
                } catch (error) {
                    message.error('Ошибка при удалении книги');
                    console.error('Ошибка при удалении книги:', error.response.data.detail);
                }
            },
        });
    };

    return (
        <div id='card-books'>
            <Card
                title={
                    <div id='card-title'>
                        <div id="title-and-img">
                            <img src={books.book_cover} alt='img' width="80" />
                            <h1 id="text">{books.book_name}</h1>
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
                            <h3 id="text">{books.author.name}</h3>
                            <div className="tree-container" id="text">
                                <Tree
                                    treeData={treeData}
                                    className="custom-tree"
                                />
                            </div>
                        </div>
                    </div>
                }
            >
                {isEditing ? (
                    <div className="edit-book-container">
                        <Input
                            placeholder="Название книги"
                            value={formData.bookName}
                            onChange={(e) => setFormData({ ...formData, bookName: e.target.value })}
                        />
                        <Input.TextArea
                            placeholder="Описание книги"
                            value={formData.bookDescription}
                            onChange={(e) => setFormData({ ...formData, bookDescription: e.target.value })}
                        />
                        <Button onClick={handleSave}>Сохранить</Button>
                        <Button onClick={handleCancel}>Отменить</Button>
                    </div>
                ) : (
                    <Paragraph></Paragraph>
                )}
            </Card>
        </div>
    );
}

export default BookCard;