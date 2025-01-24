import React from 'react';

const DocumentEditor = ({ document, onChange }) => {
  return (
    <div>
      <h2>Edit Document</h2>
      <textarea
        value={document}
        onChange={(e) => onChange(e.target.value)}
        rows="10"
        cols="50"
      />
    </div>
  );
};

export default DocumentEditor;
