import React, { useState, useCallback } from 'react';
import { useExcelUpload } from '@/hooks/useExcelUpload';
import { ExcelPreview } from './ExcelPreview';
import { Box, Button, Typography, CircularProgress } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';

export const ExcelUploader: React.FC = () => {
  const { upload, preview, loading, error } = useExcelUpload();
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      upload(e.dataTransfer.files[0]);
    }
  }, [upload]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      upload(e.target.files[0]);
    }
  }, [upload]);

  return (
    <Box sx={{ width: '100%', maxWidth: 600, mx: 'auto', p: 3 }}>
      <Box
        sx={{
          border: '2px dashed',
          borderColor: dragActive ? 'primary.main' : 'grey.300',
          borderRadius: 2,
          p: 3,
          textAlign: 'center',
          bgcolor: dragActive ? 'action.hover' : 'background.paper',
          transition: 'all 0.2s ease',
          cursor: 'pointer',
        }}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".xlsx,.xls"
          onChange={handleFileInput}
          style={{ display: 'none' }}
          id="excel-upload"
        />
        <label htmlFor="excel-upload">
          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
            <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main' }} />
            <Typography variant="h6">
              Excel 파일을 드래그하거나 클릭하여 업로드
            </Typography>
            <Typography variant="body2" color="text.secondary">
              .xlsx 또는 .xls 파일만 지원됩니다
            </Typography>
          </Box>
        </label>
      </Box>

      {loading && (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
          <CircularProgress />
        </Box>
      )}

      {error && (
        <Typography color="error" sx={{ mt: 2, textAlign: 'center' }}>
          {error}
        </Typography>
      )}

      {preview && (
        <Box sx={{ mt: 3 }}>
          <ExcelPreview data={preview} />
        </Box>
      )}
    </Box>
  );
};
