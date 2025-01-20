import React, { useEffect, useState } from 'react';
import { Card, Tree, Button, Input, message, Modal, Typography, Avatar, Space } from 'antd';
import { useNavigate } from 'react-router-dom';
import { EditOutlined, DeleteOutlined, UserOutlined } from '@ant-design/icons';
import axios from 'axios';
import '../index.css';

function UserCard({ user, setUser }) {
    const navigate = useNavigate();
    const [isEditing, setIsEditing] = useState(false);

    const [formData, setFormData] = useState({
        userName: user.name || '',
    });

    console.log("User in UserCard", user)


    return (
        <div id='card-authors'>
            <Card
                title={
                    <div id='card-title'>
                        <div id="title-and-img">
                            <Avatar shape="square" size={64} icon={<UserOutlined />} />
                        </div>
                        <div id="book-info">
                            <h3 id="text">
                                   <a
                                    href={`user/${user.id }`}
                                    target="_blank"
                                    rel="noopener noreferrer">
                                    {user.user_name}
                                </a>
                            </h3>
                        </div>
                    </div>
                }
            >
            </Card>
        </div>
    );
};

export default UserCard;