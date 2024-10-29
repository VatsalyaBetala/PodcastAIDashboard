// src/pages/Transcription.js
import React, { useState } from 'react';
import { Container } from '@mui/material';
import UploadForm from '../components/UploadForm';
import ResultDisplay from '../components/ResultDisplay';

function Transcription() {
  const [results, setResults] = useState(null);

  return (
    <Container sx={{ mt: 4 }}>
      {!results ? (
        <UploadForm setResults={setResults} />
      ) : (
        <ResultDisplay results={results} setResults={setResults} />
      )}
    </Container>
  );
}

export default Transcription;
