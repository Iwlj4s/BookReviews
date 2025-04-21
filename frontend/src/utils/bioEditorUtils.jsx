import React, { useState } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { Button } from 'antd';

const modules = {
  toolbar: [
    [{ 'header': [1, 2, 3, false] }],
    ['bold', 'italic', 'underline', 'strike'],
    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
    ['link'],
    ['clean']
  ],
};

const formats = [
  'header',
  'bold', 'italic', 'underline', 'strike',
  'list', 'bullet',
  'link'
];

function BioEditor({ initialValue, onSave, onCancel }) {
  const [value, setValue] = useState(initialValue || '');

  return (
    <div className="bio-editor">
      <ReactQuill
        theme="snow"
        value={value}
        onChange={setValue}
        modules={modules}
        formats={formats}
        placeholder="Расскажите о себе..."
      />
      <div className="editor-actions">
        <Button onClick={() => onSave(value)} type="primary">
          Сохранить
        </Button>
        <Button onClick={onCancel} style={{ marginLeft: 8 }}>
          Отменить
        </Button>
      </div>
    </div>
  );
}

export default BioEditor;