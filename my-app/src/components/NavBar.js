// src/components/NavBar.js
import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton } from '@mui/material';
import { Audiotrack } from '@mui/icons-material';
import { Link } from 'react-router-dom';

function NavBar() {
  return (
    <AppBar position="static">
      <Toolbar>
        <Audiotrack sx={{ mr: 2 }} />
        <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, textDecoration: 'none', color: 'inherit' }}>
          Audio Analyzer
        </Typography>
        <Button color="inherit" component={Link} to="/transcription">
          Transcribe
        </Button>
        <Button color="inherit" component={Link} to="/history">
          History
        </Button>
        <Button color="inherit" component={Link} to="/login">
          Login
        </Button>
        <Button color="inherit" component={Link} to="/signup">
          Sign Up
        </Button>
      </Toolbar>
    </AppBar>
  );
}

export default NavBar;
