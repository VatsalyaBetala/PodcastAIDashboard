// src/pages/History.js
import React, { useEffect, useState } from 'react';
import { Container, Typography, Card, CardContent, CircularProgress } from '@mui/material';
import axios from 'axios';

function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch history from the backend
    axios.get('/api/history')
      .then(response => {
        setHistory(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching history:', error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <Container sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Transcription History
      </Typography>
      {history.length === 0 ? (
        <Typography variant="body1">No history available.</Typography>
      ) : (
        history.map((item, index) => (
          <Card key={index} sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6">Transcription {index + 1}</Typography>
              <Typography variant="body2" color="textSecondary">
                {new Date(item.date).toLocaleString()}
              </Typography>
              <Typography variant="body1" sx={{ mt: 1 }}>
                {item.summary}
              </Typography>
            </CardContent>
          </Card>
        ))
      )}
    </Container>
  );
}

export default History;
