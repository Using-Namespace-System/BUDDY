import React, { useState } from 'react';
import './App.css';
import DocumentEditor from './components/DocumentEditor';
import SummaryDisplay from './components/SummaryDisplay';

function App() {
  const [document, setDocument] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleDocumentChange = (newDocument) => {
    setDocument(newDocument);
  };

  const handleSaveDocument = () => {
    setLoading(true);
    // Send document to Flask backend for processing
    fetch('http://localhost:5000/process_document', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ document }),
    })
      .then((response) => response.json())
      .then((data) => {
        setSummary(data.updated_document); // Get updated document from Flask
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error processing document:', error);
        setLoading(false);
      });
  };

  return (
    <div className="App">
      <h1>Interactive Document Editor</h1>
      <DocumentEditor document={document} onChange={handleDocumentChange} />
      <button onClick={handleSaveDocument} disabled={loading}>
        {loading ? 'Processing...' : 'Save Document'}
      </button>
      <SummaryDisplay summary={summary} />
    </div>
  );
}

export default App;
