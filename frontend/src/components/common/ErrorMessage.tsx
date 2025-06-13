import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { Error as ErrorIcon } from '@mui/icons-material';

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onRetry }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '200px',
        p: 3,
        textAlign: 'center',
      }}
    >
      <ErrorIcon color="error" sx={{ fontSize: 48, mb: 2 }} />
      <Typography variant="h6" color="error" gutterBottom>
        오류가 발생했습니다
      </Typography>
      <Typography color="textSecondary" paragraph>
        {message}
      </Typography>
      {onRetry && (
        <Button
          variant="contained"
          color="primary"
          onClick={onRetry}
          sx={{ mt: 2 }}
        >
          다시 시도
        </Button>
      )}
    </Box>
  );
};

export default ErrorMessage; 