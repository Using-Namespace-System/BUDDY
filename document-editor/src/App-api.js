// In App.js (for example):
import { processDocument } from './api/api';

// Inside handleSaveDocument:
processDocument(document)
  .then((updatedDocument) => {
    setSummary(updatedDocument);
    setLoading(false);
  })
  .catch((error) => {
    console.error('Error processing document:', error);
    setLoading(false);
  });
