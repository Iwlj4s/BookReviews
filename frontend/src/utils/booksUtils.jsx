import React, { useEffect, useState } from 'react';
import axios from 'axios';

export const updateBook = (books, setBooks, bookId, updatedData) => {
    if (Object.keys(updatedData).length === 0) {
        setBooks((prevBooks) => prevBooks.filter((book) => book.id !== bookId));
    } else {
        setBooks((prevBooks) =>
            prevBooks.map((book) =>
                book.id === bookId ? { ...book, ...updatedData } : book
            )
        );
    }
};