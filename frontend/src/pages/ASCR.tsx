import React, { useState } from 'react';
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
} from '@mui/material';
import { Upload as UploadIcon, Download as DownloadIcon, CheckCircle as CheckCircleIcon } from '@mui/icons-material';
import ascrService, { TOCStructure, PDFExtractionResult, StandardPriceResult, ValidationResult } from '../services/ascrService';

const ASCR: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [year, setYear] = useState<number>(2025);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleExtractTOC = async () => {
    if (!selectedFile) {
      setError('파일을 선택해주세요.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const tocResult = await ascrService.extractTOC(selectedFile, year);
      setResult({ type: 'toc', data: tocResult });
    } catch (err) {
      setError('목차 추출에 실패했습니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleExtractText = async () => {
    if (!selectedFile) {
      setError('파일을 선택해주세요.');
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const textResult = await ascrService.extractText(selectedFile);
      setResult({ type: 'text', data: textResult });
    } catch (err) {
      setError('텍스트 추출에 실패했습니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadStandardPrice = async () => {
    setLoading(true);
    setError(null);
    try {
      const priceResult = await ascrService.downloadStandardPrice(year);
      setResult({ type: 'standard_price', data: priceResult });
    } catch (err) {
      setError('표준 가격 목록 다운로드에 실패했습니다.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleValidatePriceList = async () => {
    setLoading(true);
    setError(null);
    try {
      const validationResult = await ascrService.validatePriceList(year);
      setResult({ type: 'validation', data: validationResult });
    } catch (err) {
      setError('표준 가격 목록 검증에 실패했습니다.');
      console.error(err);
    } finally {
      setLoading(false);
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