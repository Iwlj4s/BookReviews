import React, { useState, useEffect } from 'react';
import { Modal, Input, Select, message, Spin } from 'antd';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import axios from 'axios';

const { Option } = Select;

const ReviewModal = ({ visible, onClose, onSubmit }) => {
    const [formData, setFormData] = useState({
        reviewTitle: '',
        author: '',
        book: '',
        reviewBody: ''
    });
    const [loading, setLoading] = useState(false);
    const [authors, setAuthors] = useState([]);
    const [books, setBooks] = useState([]);
    const [filteredBooks, setFilteredBooks] = useState([]);
    const [filteredAuthors, setFilteredAuthors] = useState([]);

    useEffect(() => {
        if (visible) {
            fetchAuthorsAndBooks();
        }
    }, [visible]);

    const fetchAuthorsAndBooks = async () => {
        setLoading(true);
        try {
            const authorsResponse = await axios.get('http://127.0.0.1:8000/book_reviews/authors/authors_list');
            const booksResponse = await axios.get('http://127.0.0.1:8000/book_reviews/books/books_list');
            setAuthors(authorsResponse.data);
            setBooks(booksResponse.data);
        } catch (error) {
            message.error('Ошибка при загрузке авторов и книг');
        } finally {
            setLoading(false);
        }
    };

    const handleAuthorChange = (value) => {
        setFormData({ ...formData, author: value });
        const selectedAuthor = authors.find(author => author.name === value);
        setFilteredBooks(selectedAuthor ? selectedAuthor.books : []);
        setFormData({ ...formData, book: '' });
    };

    const handleBookChange = (value) => {
        setFormData({ ...formData, book: value });
        const selectedBook = books.find(book => book.book_name === value);
        if (selectedBook) {
            setFilteredAuthors([selectedBook.author]);
        } else {
            setFilteredAuthors([]);
        }
        setFormData({ ...formData, author: '' });
    };

    const handleSubmit = async () => {
        const { reviewTitle, author, book, reviewBody, rating } = formData;

        setLoading(true);
        try {
            // Находим ID автора и книги
            const selectedAuthor = authors.find(a => a.name === author);
            const selectedBook = books.find(b => b.book_name === book);

            const reviewData = {
                review_title: reviewTitle,
                reviewed_book_id: selectedBook.id,
                reviewed_book_author_id: selectedAuthor.id,
                review_body: reviewBody,
                rating: rating // Добавляем оценку
            };

            await onSubmit(reviewData);
            onClose();
        } catch (error) {
            message.error('Ошибка при добавлении обзора.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal
            title="Добавить обзор"
            visible={visible}
            onOk={handleSubmit}
            onCancel={onClose}
            confirmLoading={loading}
        >
            {loading ? (
                <Spin />
            ) : (
                <>
                    <Input
                        placeholder="Заголовок обзора"
                        value={formData.reviewTitle}
                        onChange={(e) => setFormData({ ...formData, reviewTitle: e.target.value })}
                    />
                    <Select
                        placeholder="Выберите автора"
                        style={{ width: '100%', marginTop: '10px' }}
                        onChange={handleAuthorChange}
                    >
                        {authors.map(author => (
                            <Option key={author.id} value={author.name}>{author.name}</Option>
                        ))}
                    </Select>
                    <Select
                        placeholder="Выберите книгу"
                        style={{ width: '100%', marginTop: '10px' }}
                        onChange={handleBookChange}
                    >
                        {filteredBooks.length > 0 ? (
                            filteredBooks.map(book => (
                                <Option key={book.id} value={book.book_name}>{book.book_name}</Option>
                            ))
                        ) : (
                            books.map(book => (
                                <Option key={book.id} value={book.book_name}>{book.book_name}</Option>
                            ))
                        )}
                    </Select>
                    <Input.TextArea
                        placeholder="Тело обзора"
                        value={formData.reviewBody}
                        onChange={(e) => setFormData({ ...formData, reviewBody: e.target.value })}
                        style={{ marginTop: '10px' }}
                    />
                </>
            )}
        </Modal>
    );
};

export default ReviewModal;