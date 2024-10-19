import React from "react";
import { Link, Route, Routes } from "react-router-dom";

import HomePage from "../pages/HomePage.jsx"
import ReviewsPage from "../pages/ReviewsPage.jsx"
import BooksPage from "../pages/BooksPage.jsx"
import SignInPage from "../pages/SignInPage.jsx"
import SignUpPage from "../pages/SignUpPage.jsx"
import ProfilePage from "../pages/ProfilePage.jsx"


const MyRoutes = () => (
    <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/reviews" element={<ReviewsPage />} />
        <Route path="/books_list" element={<BooksPage />} />
        <Route path="/sign_in" element={<SignInPage />} />
        <Route path="/sign_up" element={<SignUpPage />} />
        <Route path="/me" element={<ProfilePage />} />
    </Routes>
);

export default MyRoutes;