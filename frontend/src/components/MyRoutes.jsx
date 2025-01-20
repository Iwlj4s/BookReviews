import React from "react";
import { Link, Route, Routes } from "react-router-dom";

import HomePage from "../pages/HomePage.jsx"
import ReviewsPage from "../pages/ReviewsPage.jsx"
import BooksPage from "../pages/BooksPage.jsx"
import SignInPage from "../pages/SignInPage.jsx"
import SignUpPage from "../pages/SignUpPage.jsx"
import ProfilePage from "../pages/ProfilePage.jsx"
import OtherUserProfilePage from "../pages/OtherUserProfilePage.jsx"
import AuthorsPage from "../pages/AuthorsPage.jsx"
import UsersPage from "../pages/UsersPage.jsx"


const MyRoutes = () => (
    <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/reviews" element={<ReviewsPage />} />
        <Route path="/books_list" element={<BooksPage />} />
        <Route path="/sign_in" element={<SignInPage />} />
        <Route path="/sign_up" element={<SignUpPage />} />
        <Route path="/me" element={<ProfilePage />} />
        <Route path="/user/:userId" element={<OtherUserProfilePage />} />
        <Route path="/authors_list" element={<AuthorsPage />} />
        <Route path="/users_list" element={<UsersPage />} />
    </Routes>
);

export default MyRoutes;