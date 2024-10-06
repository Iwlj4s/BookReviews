import React, { useEffect, useState } from 'react';
import { Card, Space, Tree } from 'antd';

function ReviewCard(props) {
    const { reviews } = props;

    const bookDescription = reviews.book.book_description

    const [treeData, setTreeData] = useState([])


     useEffect(() => {
      const data = [
          {
            title: <div className='tree-container'>Описание книги</div>,
              key: '0-0',
              children: [
                  {
                      title: <div className='tree-container'>{bookDescription}</div>,
                      key: '0-0-0',
                  },
              ],
          },
      ];
      setTreeData(data);
    }, [bookDescription]);

    return (
        <div id='card'>
            <Card
                title={
                    <div id='card-title'>
                        <div id="title-and-img">
                            <img src={reviews.reviewed_book_cover} alt='img' width="80" />
                            <h1 id="text">{reviews.review_title}</h1>
                            <h3>{reviews.author_name}</h3>
                        </div>
                        <div id="book-info">
                            <h3 id="text">{reviews.reviewed_book_author_name} || {reviews.reviewed_book_name}</h3>
                            <div className="tree-container" id="text">
                              <Tree
                                treeData={treeData}
                                className="custom-tree"
                              />
                            </div>
                        </div>
                        <p>Автор обзора: {reviews.user.name}</p>
                        <p>Обзор обновлен: {reviews.updated}</p>
                    </div>
                }
            >
                <div id='card-content'>
                    <p>{reviews.review_body}</p>
                </div>
            </Card>
        </div>
    );
}

export default ReviewCard;