/**
 * 계약 등록/수정 폼 컴포넌트
 */
import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Typography,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  FormHelperText
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { ko } from 'date-fns/locale';
import { Contract, ContractCreate, ContractUpdate, ContractStatus } from '../../types/contract';

// 타입 정의
interface ContractFormData {
  name: string;
  contract_number: string;
  contract_amount: number;
  contract_date: Date | null;
  start_date: Date | null;
  end_date: Date | null;
  client_name: string;
  client_contact: string;
  status: string;
  description: string;
  vendor_id: string;
}

interface ContractFormProps {
  contract?: Contract | null;
  onSave: (data: ContractCreate | ContractUpdate) => Promise<void>;
  onCancel: () => void;
}

// 유효성 검증 스키마
const contractSchema = yup.object({
  name: yup.string().required('계약명을 입력해주세요').max(255, '계약명은 255자 이하여야 합니다'),
  contract_number: yup.string().required('계약번호를 입력해주세요').max(50, '계약번호는 50자 이하여야 합니다'),
  contract_amount: yup.number().required('계약금액을 입력해주세요').positive('계약금액은 0보다 커야 합니다'),
  contract_date: yup.date().required('계약일을 선택해주세요'),
  start_date: yup.date().nullable(),
  end_date: yup.date().nullable().test(
    'end-date-after-start',
    '종료일은 시작일보다 늦어야 합니다',
    function(value) {
      const { start_date } = this.parent;
      if (value && start_date && value <= start_date) {
        return false;
      }
      return true;
    }
  ),
  client_name: yup.string().required('발주처명을 입력해주세요').max(255, '발주처명은 255자 이하여야 합니다'),
  client_contact: yup.string().max(100, '연락처는 100자 이하여야 합니다'),
  status: yup.string().required('상태를 선택해주세요'),
  description: yup.string(),
  vendor_id: yup.string().required('거래처를 선택해주세요')
});

export const ContractForm: React.FC<ContractFormProps> = ({
  contract,
  onSave,
  onCancel,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<Partial<ContractCreate>>({
    name: '',
    contractNumber: '',
    contractAmount: 0,
    contractDate: new Date(),
    startDate: null,
    endDate: null,
    clientName: '',
    clientContact: '',
    status: '진행중',
    description: '',
    vendorId: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const isEditMode = !!contract;

  // 초기 데이터 설정
  useEffect(() => {
    if (contract) {
      setFormData({
        name: contract.name,
        contractNumber: contract.contractNumber,
        contractAmount: contract.contractAmount,
        contractDate: new Date(contract.contractDate),
        startDate: contract.startDate ? new Date(contract.startDate) : null,
        endDate: contract.endDate ? new Date(contract.endDate) : null,
        clientName: contract.clientName,
        clientContact: contract.clientContact || '',
        status: contract.status,
        description: contract.description || '',
        vendorId: contract.vendorId,
      });
    }
  }, [contract]);

  // 폼 검증
  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.name?.trim()) {
      newErrors.name = '계약명을 입력해주세요.';
    }

    if (!formData.contractNumber?.trim()) {
      newErrors.contractNumber = '계약번호를 입력해주세요.';
    }

    if (!formData.contractAmount || formData.contractAmount <= 0) {
      newErrors.contractAmount = '계약금액을 입력해주세요.';
    }

    if (!formData.contractDate) {
      newErrors.contractDate = '계약일을 선택해주세요.';
    }

    if (!formData.clientName?.trim()) {
      newErrors.clientName = '발주처명을 입력해주세요.';
    }

    if (!formData.vendorId?.trim()) {
      newErrors.vendorId = '거래처를 선택해주세요.';
    }

    // 종료일 검증
    if (formData.endDate && formData.startDate && formData.endDate <= formData.startDate) {
      newErrors.endDate = '종료일은 시작일보다 늦어야 합니다.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 폼 제출
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const submitData = {
        ...formData,
        contractDate: formData.contractDate?.toISOString(),
        startDate: formData.startDate?.toISOString(),
        endDate: formData.endDate?.toISOString(),
      };

      await onSave(submitData);
    } catch (err: any) {
      setError(err.message || '계약 저장에 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // 입력 필드 변경
  const handleInputChange = (field: keyof ContractCreate, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // 에러 초기화
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  // 금액 포맷팅
  const formatAmount = (value: string) => {
    const numericValue = value.replace(/[^\d]/g, '');
    return numericValue ? parseInt(numericValue, 10) : 0;
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
      <Paper elevation={3} sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
        <Typography variant="h5" component="h2" gutterBottom>
          {isEditMode ? '계약 수정' : '새 계약 등록'}
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
          <Grid container spacing={2}>
            {/* 계약명 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="계약명 *"
                value={formData.name || ''}
                onChange={(e) => handleInputChange('name', e.target.value)}
                error={!!errors.name}
                helperText={errors.name}
                required
              />
            </Grid>
            
            {/* 계약번호 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="계약번호 *"
                value={formData.contractNumber || ''}
                onChange={(e) => handleInputChange('contractNumber', e.target.value)}
                error={!!errors.contractNumber}
                helperText={errors.contractNumber}
                required
              />
            </Grid>

            {/* 계약금액 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="계약금액 *"
                type="number"
                value={formData.contractAmount || ''}
                onChange={(e) => handleInputChange('contractAmount', parseFloat(e.target.value))}
                error={!!errors.contractAmount}
                helperText={errors.contractAmount}
                required
                InputProps={{
                  endAdornment: <Typography variant="caption">원</Typography>,
                }}
              />
            </Grid>

            {/* 계약일 */}
            <Grid item xs={12} sm={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
                <DatePicker
                  label="계약일 *"
                  value={formData.contractDate}
                  onChange={(date) => handleInputChange('contractDate', date)}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      fullWidth
                      error={!!errors.contractDate}
                      helperText={errors.contractDate}
                      required
                    />
                  )}
                />
              </LocalizationProvider>
            </Grid>

            {/* 시작일 */}
            <Grid item xs={12} sm={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
                <DatePicker
                  label="시작일"
                  value={formData.startDate}
                  onChange={(date) => handleInputChange('startDate', date)}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      fullWidth
                      helperText="선택사항"
                    />
                  )}
                />
              </LocalizationProvider>
            </Grid>

            {/* 종료일 */}
            <Grid item xs={12} sm={6}>
              <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
                <DatePicker
                  label="종료일"
                  value={formData.endDate}
                  onChange={(date) => handleInputChange('endDate', date)}
                  renderInput={(params) => (
                    <TextField
                      {...params}
                      fullWidth
                      error={!!errors.endDate}
                      helperText={errors.endDate || "선택사항"}
                    />
                  )}
                />
              </LocalizationProvider>
            </Grid>

            {/* 발주처명 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="발주처명 *"
                value={formData.clientName || ''}
                onChange={(e) => handleInputChange('clientName', e.target.value)}
                error={!!errors.clientName}
                helperText={errors.clientName}
                required
              />
            </Grid>

            {/* 발주처 연락처 */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="발주처 연락처"
                value={formData.clientContact || ''}
                onChange={(e) => handleInputChange('clientContact', e.target.value)}
                helperText="선택사항"
              />
            </Grid>

            {/* 상태 */}
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>상태</InputLabel>
                <Select
                  value={formData.status || '진행중'}
                  label="상태"
                  onChange={(e) => handleInputChange('status', e.target.value)}
                >
                  <MenuItem value="진행중">진행중</MenuItem>
                  <MenuItem value="완료">완료</MenuItem>
                  <MenuItem value="중단">중단</MenuItem>
                  <MenuItem value="취소">취소</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* 거래처 ID */}
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="거래처 ID *"
                value={formData.vendorId || ''}
                onChange={(e) => handleInputChange('vendorId', e.target.value)}
                error={!!errors.vendorId}
                helperText={errors.vendorId}
                required
              />
            </Grid>

            {/* 설명 */}
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="설명"
                multiline
                rows={3}
                value={formData.description || ''}
                onChange={(e) => handleInputChange('description', e.target.value)}
                helperText="선택사항"
              />
            </Grid>
          </Grid>

          <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
            <Button
              type="submit"
              variant="contained"
              disabled={loading}
              startIcon={loading ? <CircularProgress size={20} /> : null}
            >
              {isEditMode ? '수정' : '등록'}
            </Button>
            <Button variant="outlined" onClick={onCancel} disabled={loading}>
              취소
            </Button>
          </Box>
        </Box>
      </Paper>
    </LocalizationProvider>
  );
}; 