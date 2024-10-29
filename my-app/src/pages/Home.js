// src/pages/Home.js
import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <Container sx={{ mt: 8, textAlign: 'center' }}>
      <Typography variant="h3" gutterBottom>
        Welcome to Audio Analyzer
      </Typography>
      <Typography variant="h6" gutterBottom>
        Transcribe and analyze your audio files effortlessly.
      </Typography>
      <Box sx={{ mt: 4 }}>
        <Button variant="contained" color="primary" size="large" component={Link} to="/transcription">
          Get Started
        </Button>
      </Box>
    </Container>
  );
}

export default Home;
