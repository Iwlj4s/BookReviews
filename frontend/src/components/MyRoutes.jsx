import React from "react";
import { Link, Route, Routes } from "react-router-dom";

import HomePage from "../pages/HomePage.jsx"
import ReviewsPage from "../pages/ReviewsPage.jsx"


const MyRoutes = () => (
    <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/reviews" element={<ReviewsPage />} />
    </Routes>
);

export default MyRoutes;