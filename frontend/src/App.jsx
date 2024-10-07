import React from 'react';
import { Menu, Spin, Input, Space } from 'antd';
import axios from 'axios';
import { Routes } from 'react-router-dom';

import Navigation from "./components/Navigation.jsx";
import MyRoutes from "./components/MyRoutes.jsx";

const App = () => {
  return (
      <div>
          <Navigation />
          <MyRoutes />
      </div>
  )
};

export default App;