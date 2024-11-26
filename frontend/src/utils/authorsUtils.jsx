import React, { useEffect, useState } from 'react';
import axios from 'axios';

export const updateAuthor = (authors, setAuthors, authorId, updatedData) => {
    if (Object.keys(updatedData).length === 0) {
        setAuthors((prevAuthors) => prevAuthors.filter((author) => author.id !== authorId));
    } else {
        setAuthors((prevAuthors) =>
            prevAuthors.map((author) =>
                author.id === authorId ? { ...author, ...updatedData } : author
            )
        );
    }
};