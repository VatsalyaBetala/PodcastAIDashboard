// src/components/UploadForm.js
import React, { useState } from 'react';
import axios from 'axios';
import { Button, Typography, Box, LinearProgress, Alert } from '@mui/material';
import { useDropzone } from 'react-dropzone';

function UploadForm({ setResults }) {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
    setError('');
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: 'audio/*',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file to upload.');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/upload', formData);
      setResults(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4, textAlign: 'center' }}>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed #1976d2',
          padding: '2rem',
          cursor: 'pointer',
          backgroundColor: isDragActive ? '#f0f0f0' : 'transparent',
        }}
      >
        <input {...getInputProps()} />
        {file ? (
          <Typography variant="body1">Selected File: {file.name}</Typography>
        ) : (
          <Typography variant="body1">
            {isDragActive ? 'Drop the file here...' : 'Drag & drop an audio file here, or click to select one'}
          </Typography>
        )}
      </Box>
      <Button
        variant="contained"
        color="primary"
        type="submit"
        disabled={loading || !file}
        sx={{ mt: 2 }}
      >
        {loading ? 'Processing...' : 'Upload and Analyze'}
      </Button>
      {loading && <LinearProgress sx={{ mt: 2 }} />}
    </Box>
  );
}

export default UploadForm;
