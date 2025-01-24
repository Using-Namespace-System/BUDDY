import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [document, setDocument] = useState('');
  const [sections, setSections] = useState([]);
  const [fullSummary, setFullSummary] = useState('');

  // Load document and process sections on initial load
  useEffect(() => {
    if (document) {
      axios.post('http://localhost:5000/process_document', { document })
        .then(response => {
          setSections(response.data.sections);
          setFullSummary(response.data.full_summary);
        })
        .catch(error => console.error("There was an error processing the document:", error));
    }
  }, [document]);

  const handleSectionEdit = (sectionId, updatedText) => {
    axios.post('http://localhost:5000/update_section', {
      section_id: sectionId,
      updated_section: updatedText
    })
      .then(response => {
        const updatedSections = sections.map((section, index) => {
          if (index === sectionId) {
            section.summary = response.data.updated_section_summary;
          }
          return section;
        });
        setSections(updatedSections);
      })
      .catch(error => console.error("There was an error updating the section:", error));
  };

  const handleDocumentChange = (e) => {
    setDocument(e.target.value);
  };

  return (
    <div className="App">
      <h1>Interactive Document Editor</h1>
      <textarea 
        value={document} 
        onChange={handleDocumentChange}
        placeholder="Paste your document here..."
        rows="10" 
        cols="80"
      />
      
      <div>
        <h3>Full Summary:</h3>
        <p>{fullSummary}</p>
      </div>

      <div>
        <h3>Document Sections:</h3>
        {sections.map((section, index) => (
          <div key={index}>
            <h4>Section {index + 1}</h4>
            <textarea 
              value={section.section}
              onChange={(e) => handleSectionEdit(index, e.target.value)}
            />
            <p><strong>Summary:</strong> {section.summary}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
