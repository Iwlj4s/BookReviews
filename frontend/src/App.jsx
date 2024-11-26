import React, { useState } from 'react';
import { Routes } from 'react-router-dom';

import Navigation from "./components/Navigation.jsx";
import MyRoutes from "./components/MyRoutes.jsx";

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    return (
      <div>
          <Navigation isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn} />
          <MyRoutes setIsLoggedIn={setIsLoggedIn} />
      </div>
    )
};

export default App;