// src/components/ResultDisplay.js
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Box,
  Fade,
} from '@mui/material';
import {
  SentimentSatisfiedAlt,
  SentimentDissatisfied,
  SentimentNeutral,
} from '@mui/icons-material';

function ResultDisplay({ results, setResults }) {
  const { transcript, summary, hashtags, sentiment } = results;

  const getSentimentIcon = () => {
    switch (sentiment.label) {
      case 'POSITIVE':
        return <SentimentSatisfiedAlt color="success" />;
      case 'NEGATIVE':
        return <SentimentDissatisfied color="error" />;
      default:
        return <SentimentNeutral color="action" />;
    }
  };

  return (
    <Fade in={true} timeout={500}>
      <Box sx={{ mt: 4 }}>
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Transcript
            </Typography>
            <Typography variant="body1">{transcript}</Typography>
          </CardContent>
        </Card>

        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Summary
            </Typography>
            <Typography variant="body1">{summary}</Typography>
          </CardContent>
        </Card>

        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Hashtags
            </Typography>
            <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {hashtags.map((tag, index) => (
                <Chip key={index} label={tag} color="primary" />
              ))}
            </Box>
          </CardContent>
        </Card>

        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Sentiment Analysis
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {getSentimentIcon()}
              <Typography variant="body1" sx={{ ml: 1 }}>
                Sentiment: {sentiment.label} (Score: {sentiment.score.toFixed(2)})
              </Typography>
            </Box>
          </CardContent>
        </Card>

        <Button
          variant="contained"
          color="secondary"
          onClick={() => setResults(null)}
        >
          Analyze Another File
        </Button>
      </Box>
    </Fade>
  );
}

export default ResultDisplay;
