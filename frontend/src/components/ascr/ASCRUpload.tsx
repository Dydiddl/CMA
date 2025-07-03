import React, { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Grid,
  Chip,
  LinearProgress
} from '@mui/material';
import { CloudUpload, Description, CheckCircle, Error } from '@mui/icons-material';
import { ASCRService } from '../../services/ascrService';

interface ASCRUploadProps {
  onSuccess?: (result: any) => void;
  onError?: (error: string) => void;
}

export const ASCRUpload: React.FC<ASCRUploadProps> = ({ onSuccess, onError }) => {
  const [file, setFile] = useState<File | null>(null);
  const [processingType, setProcessingType] = useState<string>('standard');
  const [year, setYear] = useState<number>(2025);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('PDF 파일만 업로드 가능합니다.');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('파일을 선택해주세요.');
      return;
    }

    try {
      setLoading(true);
      setProgress(0);
      setStatus('파일 업로드 중...');
      setError(null);

      // 파일 업로드
      const formData = new FormData();
      formData.append('file', file);

      setProgress(20);
      setStatus('PDF 처리 중...');

      // ASCR 처리 요청
      const response = await ASCRService.uploadAndProcess(formData, {
        processingType,
        year,
        options: {}
      });

      setProgress(80);
      setStatus('결과 생성 중...');

      // 결과 처리
      setResult(response.data);
      setProgress(100);
      setStatus('처리 완료!');

      onSuccess?.(response.data);

    } catch (err: any) {
      setError(err.response?.data?.message || '처리 중 오류가 발생했습니다.');
      onError?.(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleExtractTOC = async () => {
    if (!file) {
      setError('파일을 선택해주세요.');
      return;
    }

    try {
      setLoading(true);
      setProgress(0);
      setStatus('목차 추출 중...');
      setError(null);

      const formData = new FormData();
      formData.append('file', file);

      const response = await ASCRService.extractTOC(formData, year);

      setResult(response.data);
      setProgress(100);
      setStatus('목차 추출 완료!');

      onSuccess?.(response.data);

    } catch (err: any) {
      setError(err.response?.data?.message || '목차 추출 중 오류가 발생했습니다.');
      onError?.(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card sx={{ maxWidth: 800, mx: 'auto', mt: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          ASCR PDF 처리
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          건설공사 표준품셈 PDF를 업로드하여 자동으로 데이터를 추출하고 엑셀 문서를 생성합니다.
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Box
              sx={{
                border: '2px dashed #ccc',
                borderRadius: 2,
                p: 3,
                textAlign: 'center',
                cursor: 'pointer',
                '&:hover': {
                  borderColor: 'primary.main',
                  backgroundColor: 'action.hover'
                }
              }}
              onClick={() => document.getElementById('file-input')?.click()}
            >
              <input
                id="file-input"
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              
              {file ? (
                <Box>
                  <CheckCircle color="success" sx={{ fontSize: 48, mb: 1 }} />
                  <Typography variant="h6" gutterBottom>
                    {file.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </Typography>
                </Box>
              ) : (
                <Box>
                  <CloudUpload sx={{ fontSize: 48, mb: 1, color: 'text.secondary' }} />
                  <Typography variant="h6" gutterBottom>
                    PDF 파일을 선택하거나 드래그하세요
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    건설공사 표준품셈 PDF 파일
                  </Typography>
                </Box>
              )}
            </Box>
          </Grid>

          <Grid item xs={12} sm={6}>
            <FormControl fullWidth>
              <InputLabel>처리 타입</InputLabel>
              <Select
                value={processingType}
                onChange={(e) => setProcessingType(e.target.value)}
                label="처리 타입"
              >
                <MenuItem value="standard">표준 처리</MenuItem>
                <MenuItem value="optimized">최적화 처리</MenuItem>
                <MenuItem value="ml_enhanced">ML 강화 처리</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              label="연도"
              type="number"
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              inputProps={{ min: 2020, max: 2030 }}
            />
          </Grid>

          <Grid item xs={12}>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                variant="contained"
                onClick={handleUpload}
                disabled={!file || loading}
                startIcon={loading ? <CircularProgress size={20} /> : <Description />}
              >
                전체 처리
              </Button>
              
              <Button
                variant="outlined"
                onClick={handleExtractTOC}
                disabled={!file || loading}
                startIcon={loading ? <CircularProgress size={20} /> : <Description />}
              >
                목차만 추출
              </Button>
            </Box>
          </Grid>

          {loading && (
            <Grid item xs={12}>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" gutterBottom>
                  {status}
                </Typography>
                <LinearProgress 
                  variant="determinate" 
                  value={progress} 
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
            </Grid>
          )}

          {result && (
            <Grid item xs={12}>
              <Alert severity="success" sx={{ mt: 2 }}>
                <Typography variant="h6" gutterBottom>
                  처리 완료!
                </Typography>
                <Typography variant="body2">
                  파일: {result.output_file || '생성됨'}
                </Typography>
                {result.year && (
                  <Typography variant="body2">
                    연도: {result.year}
                  </Typography>
                )}
              </Alert>
            </Grid>
          )}
        </Grid>
      </CardContent>
    </Card>
  );
}; 