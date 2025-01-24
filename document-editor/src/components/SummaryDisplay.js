import React from 'react';

const SummaryDisplay = ({ summary }) => {
  return (
    <div>
      <h2>Updated Document</h2>
      <pre>{summary}</pre>
    </div>
  );
};

export default SummaryDisplay;
