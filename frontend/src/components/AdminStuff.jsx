import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Button, Input, message, Form, Collapse, Select, Modal } from 'antd';
import { QuestionCircleOutlined } from '@ant-design/icons';
import '../index.css';

const { Option } = Select;

function AdminStuff({ user }) {
    const [form] = Form.useForm();
    const [authors, setAuthors] = useState([]);
    const [loading, setLoading] = useState(false);

    const [authorName, setAuthorName] = useState('');

    const [bookName, setBookName] = useState('');
    const [bookDescription, setBookDescription] = useState('');

    const [selectedAuthor, setSelectedAuthor] = useState('');

    const [mailTheme, setMailTheme] = useState('');
    const [mailBody, setMailBody] = useState('');

    useEffect(() => {
        fetchAuthors();
    }, []);

    const fetchAuthors = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/book_reviews/authors/authors_list/');
            setAuthors(response.data);
        } catch (error) {
            message.error('Ошибка при загрузке авторов');
            console.error(error);
        }
    };

    const AddAuthor = async () => {
        setLoading(true);
        const values = { name: authorName };
        try {
            const response = await axios.post('http://127.0.0.1:8000/book_reviews/admin/authors/add_author', values, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });
            if (response.data.status_code === 409) {
                message.error('Такой автор уже существует');
            } else if (response.data.status_code === 200) {
                message.success(response.data.message);
                form.resetFields();
                fetchAuthors();
            }
        } catch (error) {
            message.error(error.response?.data?.message || 'Произошла ошибка при добавлении автора');
        } finally {
            setLoading(false);
        }
    };

    const AddBook = async () => {
        setLoading(true);
        const requestData = {
            book_author_name: selectedAuthor,
            book_name: bookName,
            book_description: bookDescription
        };
        console.log("Add book requestData: ", requestData)
        try {
            const response = await axios.post('http://127.0.0.1:8000/book_reviews/admin/books/add_book', requestData, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });
            console.log("Add book requestData: ", requestData)
            console.log("Add book response: ", response)
            if (response.data.status_code === 404) {
                message.error(response.data.message);
            } else if (response.data.status_code === 200) {
                message.success(response.data.message);
                form.resetFields();
            }
        } catch (error) {
            message.error(error.response?.data?.message || 'Произошла ошибка при добавлении книги');
        } finally {
            setLoading(false);
        }
    };

    const sendNewsletter = async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://127.0.0.1:8000/book_reviews/admin/mail/send_newsletter', {
                mail_theme: mailTheme,
                mail_body: mailBody
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('user_access_token')}`
                }
            });
            if (response.data.status_code === 200) {
                message.success(response.data.message);
                form.resetFields();
            }
        } catch (error) {
            console.error("Error sending newsletter: ", error);
            console.log("Mail Theme: ", mail_theme)
            console.log("Mail Body: ", mail_body)
            message.error(error.response?.data?.message || 'Произошла ошибка при отправке рассылки');
        } finally {
            setLoading(false);
        }
    };

    const adminFuncs = [
        {
            key: '1',
            label: 'Добавить автора',
            children: (
                <Form layout="vertical">
                    <Form.Item
                        label="Имя автора"
                        rules={[{ required: true, message: 'Пожалуйста, введите имя автора!' }]}
                    >
                        <Input
                            placeholder="Введите имя автора"
                            value={authorName}
                            onChange={(e) => setAuthorName(e.target.value)}
                        />
                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" onClick={AddAuthor} loading={loading}>
                            Добавить автора
                        </Button>
                    </Form.Item>
                </Form>
            )
        },
        {
            key: '2',
            label: 'Добавить книгу',
            children: (
                <Form layout="vertical">
                    <Form.Item
                        label="Автор"
                        rules={[{ required: true, message: 'Пожалуйста, выберите автора!' }]}
                    >
                        <Select
                            showSearch
                            placeholder="Выберите автора"
                            onChange={(value) => setSelectedAuthor(value)}
                            onFocus={fetchAuthors}
                        >
                            {authors.map(author => (
                                <Option key={author.id} value={author.name}>
                                    {author.name}
                                </Option>
                            ))}
                        </Select>
                    </Form.Item>

                    <Form.Item
                        label="Название книги"
                        rules={[{ required: true, message: 'Пожалуйста, введите название книги!' }]}
                    >
                        <Input
                            placeholder="Введите название книги"
                            value={bookName}
                            onChange={(e) => setBookName(e.target.value)}
                        />
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" onClick={AddBook} loading={loading}>
                            Добавить книгу
                        </Button>
                    </Form.Item>
                </Form>
            )
        },
        {
            key: '3',
            label: 'Отправить рассылку',
            children: (
                <Form layout="vertical">
                    <Form.Item
                        label="Тема письма"
                        rules={[{ required: true, message: 'Пожалуйста, введите тему письма!' }]}
                    >
                        <Input
                            placeholder="Введите тему письма"
                            value={mailTheme}
                            onChange={(e) => setMailTheme(e.target.value)}
                        />
                    </Form.Item>
                    <Form.Item
                        label="Текст письма"
                        rules={[{ required: true, message: 'Пожалуйста, введите текст письма!' }]}
                    >
                        <Input.TextArea
                            placeholder="Введите текст письма"
                            value={mailBody}
                            onChange={(e) => setMailBody(e.target.value)}

                        />

                    </Form.Item>
                    <Form.Item>
                        <Button type="primary" onClick={sendNewsletter} loading={loading}>
                            Отправить рассылку
                        </Button>
                    </Form.Item>
                </Form>
            )
        }
    ];

    const showAdminInfoModal = () => {
        Modal.info({
            title: 'Информация',
            content: (
                <div>
                    <p>Прямо с вашей страницы вы можете добавить автора или книгу, а также сделать рассылку информации всем пользователям.</p>
                    <p>Для изменения/удаления автора перейдите в раздел <a href="/authors">"Авторы"</a>, с помощью поиска найдите нужного автора и измените/удалите его.</p>
                    <p>Для изменения/удаления книги перейдите в раздел <a href="/books_list">"Книги"</a>, с помощью поиска найдите нужную книгу и измените/удалите ее.</p>
                    <p>Для изменения/удаления обзора перейдите в раздел <a href="/reviews">"Обзоры"</a>, с помощью поиска найдите нужный обзор и измените/удалите его.</p>
                </div>
            ),
            onOk() {},
        });
    };

    return (
        <>
            <div id="admin-stuff-items">
                <div className="user-info-header">
                    <h3>{user.name} Вы администратор</h3>
                    <Button
                        type="link"
                        icon={<QuestionCircleOutlined />}
                        size="large"
                        onClick={showAdminInfoModal}
                    />
                </div>
                <Collapse items={adminFuncs} />
            </div>
        </>
    );
}

export default AdminStuff;