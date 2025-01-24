// src/api/api.js

export const processDocument = async (document) => {
    const response = await fetch('http://localhost:5000/process_document', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ document }),
    });
  
    const data = await response.json();
    return data.updated_document;
  };
  