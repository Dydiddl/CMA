import React, { useState, useCallback } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Grid,
  Paper,
  LinearProgress,
  Snackbar,
  Chip,
} from '@mui/material';
import { 
  Upload as UploadIcon, 
  Download as DownloadIcon, 
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import ascrService, { TOCStructure, PDFExtractionResult, StandardPriceResult, ValidationResult } from '../services/ascrService';

const ASCR: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [year, setYear] = useState<number>(2025);
  const [loading, setLoading] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState<string>('');
  const [progress, setProgress] = useState<number>(0);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState<{open: boolean, message: string, severity: 'success' | 'error' | 'info'}>({
    open: false,
    message: '',
    severity: 'info'
  });

  const showSnackbar = useCallback((message: string, severity: 'success' | 'error' | 'info' = 'info') => {
    setSnackbar({ open: true, message, severity });
  }, []);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.size > 50 * 1024 * 1024) { // 50MB 제한
        setError('파일 크기가 50MB를 초과합니다.');
        showSnackbar('파일 크기 제한: 50MB', 'error');
        return;
      }
      setSelectedFile(file);
      setError(null);
      showSnackbar('파일이 선택되었습니다.', 'success');
    }
  };

  const startLoading = useCallback((message: string) => {
    setLoading(true);
    setLoadingMessage(message);
    setProgress(0);
    setError(null);
  }, []);

  const updateProgress = useCallback((progress: number) => {
    setProgress(progress);
  }, []);

  const stopLoading = useCallback(() => {
    setLoading(false);
    setLoadingMessage('');
    setProgress(0);
  }, []);

  const handleExtractTOC = async () => {
    if (!selectedFile) {
      setError('파일을 선택해주세요.');
      showSnackbar('파일을 선택해주세요.', 'error');
      return;
    }

    startLoading('목차 구조를 추출하는 중...');
    
    try {
      // 진행률 시뮬레이션
      const progressInterval = setInterval(() => {
        updateProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const tocResult = await ascrService.extractTOC(selectedFile, year);
      
      clearInterval(progressInterval);
      updateProgress(100);
      
      setResult({ type: 'toc', data: tocResult });
      showSnackbar('목차 추출이 완료되었습니다.', 'success');
    } catch (err) {
      setError('목차 추출에 실패했습니다.');
      showSnackbar('목차 추출 실패', 'error');
      console.error(err);
    } finally {
      stopLoading();
    }
  };

  const handleExtractText = async () => {
    if (!selectedFile) {
      setError('파일을 선택해주세요.');
      showSnackbar('파일을 선택해주세요.', 'error');
      return;
    }

    startLoading('텍스트를 추출하는 중...');
    
    try {
      const progressInterval = setInterval(() => {
        updateProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 15;
        });
      }, 150);

      const textResult = await ascrService.extractText(selectedFile);
      
      clearInterval(progressInterval);
      updateProgress(100);
      
      setResult({ type: 'text', data: textResult });
      showSnackbar('텍스트 추출이 완료되었습니다.', 'success');
    } catch (err) {
      setError('텍스트 추출에 실패했습니다.');
      showSnackbar('텍스트 추출 실패', 'error');
      console.error(err);
    } finally {
      stopLoading();
    }
  };

  const handleDownloadStandardPrice = async () => {
    startLoading('표준 가격 목록을 다운로드하는 중...');
    
    try {
      const progressInterval = setInterval(() => {
        updateProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 20;
        });
      }, 300);

      const priceResult = await ascrService.downloadStandardPrice(year);
      
      clearInterval(progressInterval);
      updateProgress(100);
      
      setResult({ type: 'standard_price', data: priceResult });
      showSnackbar('표준 가격 목록 다운로드가 완료되었습니다.', 'success');
    } catch (err) {
      setError('표준 가격 목록 다운로드에 실패했습니다.');
      showSnackbar('다운로드 실패', 'error');
      console.error(err);
    } finally {
      stopLoading();
    }
  };

  const handleValidatePriceList = async () => {
    startLoading('표준 가격 목록을 검증하는 중...');
    
    try {
      const progressInterval = setInterval(() => {
        updateProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 25;
        });
      }, 250);

      const validationResult = await ascrService.validatePriceList(year);
      
      clearInterval(progressInterval);
      updateProgress(100);
      
      setResult({ type: 'validation', data: validationResult });
      showSnackbar('검증이 완료되었습니다.', 'success');
    } catch (err) {
      setError('표준 가격 목록 검증에 실패했습니다.');
      showSnackbar('검증 실패', 'error');
      console.error(err);
    } finally {
      stopLoading();
    }
  };

  const handleSplitPDF = async () => {
    if (!selectedFile) {
      setError('파일을 선택해주세요.');
      showSnackbar('파일을 선택해주세요.', 'error');
      return;
    }

    // 목차 구조가 필요하므로 먼저 목차 추출
    if (!result || result.type !== 'toc') {
      setError('PDF 분할을 위해서는 먼저 목차를 추출해야 합니다.');
      showSnackbar('먼저 목차를 추출해주세요.', 'error');
      return;
    }

    startLoading('PDF를 분할하는 중...');
    
    try {
      const progressInterval = setInterval(() => {
        updateProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 20;
        });
      }, 200);

      const splitResult = await ascrService.splitPDF(selectedFile, result.data.structure);
      
      clearInterval(progressInterval);
      updateProgress(100);
      
      setResult({ type: 'split', data: splitResult });
      showSnackbar('PDF 분할이 완료되었습니다.', 'success');
    } catch (err) {
      setError('PDF 분할에 실패했습니다.');
      showSnackbar('PDF 분할 실패', 'error');
      console.error(err);
    } finally {
      stopLoading();
    }
  };

  const renderResult = () => {
    if (!result) return null;

    switch (result.type) {
      case 'toc':
        return (
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              목차 구조
            </Typography>
            <pre style={{ whiteSpace: 'pre-wrap', fontSize: '12px' }}>
              {JSON.stringify(result.data, null, 2)}
            </pre>
          </Paper>
        );
      case 'text':
        return (
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              추출된 텍스트 (처음 500자)
            </Typography>
            <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
              {result.data.text.substring(0, 500)}...
            </Typography>
          </Paper>
        );
      case 'standard_price':
        return (
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              표준 가격 목록 다운로드 결과
            </Typography>
            <Typography>연도: {result.data.year}</Typography>
            <Typography>상태: {result.data.status}</Typography>
            {result.data.file_path && (
              <Typography>파일 경로: {result.data.file_path}</Typography>
            )}
          </Paper>
        );
      case 'validation':
        return (
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              검증 결과
            </Typography>
            <Typography color={result.data.is_valid ? 'success.main' : 'error.main'}>
              유효성: {result.data.is_valid ? '통과' : '실패'}
            </Typography>
            {result.data.errors.length > 0 && (
              <Box>
                <Typography variant="subtitle2" color="error">오류:</Typography>
                {result.data.errors.map((err: string, index: number) => (
                  <Typography key={index} variant="body2" color="error">• {err}</Typography>
                ))}
              </Box>
            )}
            {result.data.warnings.length > 0 && (
              <Box>
                <Typography variant="subtitle2" color="warning.main">경고:</Typography>
                {result.data.warnings.map((warning: string, index: number) => (
                  <Typography key={index} variant="body2" color="warning.main">• {warning}</Typography>
                ))}
              </Box>
            )}
          </Paper>
        );
      case 'split':
        return (
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              PDF 분할 결과
            </Typography>
            <Typography>분할된 파일 개수: {result.data.length}</Typography>
            {result.data.map((file: string, index: number) => (
              <Typography key={index} variant="body2">• {file}</Typography>
            ))}
          </Paper>
        );
      default:
        return null;
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        ASCR (PDF 처리 및 검증)
      </Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        건설공사 표준품셈 PDF 처리 및 검증 시스템
      </Typography>

      <Grid container spacing={3}>
        {/* 파일 업로드 섹션 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                PDF 파일 업로드
              </Typography>
              <input
                accept=".pdf"
                style={{ display: 'none' }}
                id="pdf-file-input"
                type="file"
                onChange={handleFileChange}
              />
              <label htmlFor="pdf-file-input">
                <Button
                  variant="outlined"
                  component="span"
                  startIcon={<UploadIcon />}
                  sx={{ mb: 2 }}
                >
                  PDF 파일 선택
                </Button>
              </label>
              {selectedFile && (
                <Typography variant="body2" color="success.main">
                  선택된 파일: {selectedFile.name}
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* 연도 설정 섹션 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                연도 설정
              </Typography>
              <FormControl fullWidth>
                <InputLabel>연도</InputLabel>
                <Select
                  value={year}
                  label="연도"
                  onChange={(e) => setYear(e.target.value as number)}
                >
                  <MenuItem value={2023}>2023</MenuItem>
                  <MenuItem value={2024}>2024</MenuItem>
                  <MenuItem value={2025}>2025</MenuItem>
                </Select>
              </FormControl>
            </CardContent>
          </Card>
        </Grid>

        {/* 기능 버튼들 */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                PDF 처리 기능
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  onClick={handleExtractTOC}
                  disabled={!selectedFile || loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <CheckCircleIcon />}
                >
                  목차 추출
                </Button>
                <Button
                  variant="contained"
                  onClick={handleExtractText}
                  disabled={!selectedFile || loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <CheckCircleIcon />}
                >
                  텍스트 추출
                </Button>
                <Button
                  variant="contained"
                  onClick={handleDownloadStandardPrice}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <DownloadIcon />}
                >
                  표준 가격 목록 다운로드
                </Button>
                <Button
                  variant="contained"
                  onClick={handleValidatePriceList}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <CheckCircleIcon />}
                >
                  표준 가격 목록 검증
                </Button>
                <Button
                  variant="contained"
                  onClick={handleSplitPDF}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <CheckCircleIcon />}
                >
                  PDF 분할
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 오류 메시지 */}
      {error && (
        <Alert severity="error" sx={{ mt: 2 }}>
          {error}
        </Alert>
      )}

      {/* 결과 표시 */}
      {renderResult()}
    </Box>
  );
};

export default ASCR; 