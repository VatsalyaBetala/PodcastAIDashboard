// src/App.js
import React, { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Container, Typography } from '@mui/material';
import UploadForm from './components/UploadForm';
import ResultDisplay from './components/ResultDisplay';

function App() {
  const [results, setResults] = useState(null);

  const theme = createTheme({
    palette: {
      primary: {
        main: '#1976d2', // Customize your primary color
      },
      secondary: {
        main: '#ff4081', // Customize your secondary color
      },
    },
    typography: {
      fontFamily: 'Roboto, sans-serif',
    },
  });

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Typography variant="h3" align="center" gutterBottom>
          Audio Transcription and Analysis
        </Typography>
        {!results ? (
          <UploadForm setResults={setResults} />
        ) : (
          <ResultDisplay results={results} setResults={setResults} />
        )}
      </Container>
    </ThemeProvider>
  );
}

export default App;
