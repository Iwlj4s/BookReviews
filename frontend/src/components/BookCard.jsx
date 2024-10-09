import React, { useEffect, useState } from 'react';
import { Card, Space, Tree } from 'antd';

function BookCard(props) {
    const { books } = props;

    const bookDescription = books.book_description

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
        <div id='card-books'>
            <Card
                title={
                    <div id='card-title'>
                        <div id="title-and-img">
                            <img src={books.book_cover} alt='img' width="80" />
                            <h1 id="text">{books.book_name}</h1>
                            <h1 id="text">{books.author_name}</h1>
                        </div>
                        <div id="book-info">
                            <div className="tree-container" id="text">
                              <Tree
                                treeData={treeData}
                                className="custom-tree"
                              />
                            </div>
                        </div>
                    </div>
                }
            >
            </Card>
        </div>
    );
}

export default BookCard;