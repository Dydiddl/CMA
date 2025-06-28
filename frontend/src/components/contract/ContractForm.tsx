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
  CircularProgress
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import { ko } from 'date-fns/locale';

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
  initialData?: Partial<ContractFormData>;
  onSubmit: (data: ContractFormData) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
  vendors: Array<{ id: string; name: string }>;
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

const ContractForm: React.FC<ContractFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  isLoading = false,
  vendors
}) => {
  const [error, setError] = useState<string | null>(null);

  const {
    control,
    handleSubmit,
    formState: { errors, isValid },
    reset,
    watch
  } = useForm<ContractFormData>({
    resolver: yupResolver(contractSchema),
    mode: 'onChange',
    defaultValues: {
      name: initialData?.name || '',
      contract_number: initialData?.contract_number || '',
      contract_amount: initialData?.contract_amount || 0,
      contract_date: initialData?.contract_date || null,
      start_date: initialData?.start_date || null,
      end_date: initialData?.end_date || null,
      client_name: initialData?.client_name || '',
      client_contact: initialData?.client_contact || '',
      status: initialData?.status || '진행중',
      description: initialData?.description || '',
      vendor_id: initialData?.vendor_id || ''
    }
  });

  const watchStartDate = watch('start_date');

  // 초기 데이터가 변경되면 폼 리셋
  useEffect(() => {
    if (initialData) {
      reset({
        name: initialData.name || '',
        contract_number: initialData.contract_number || '',
        contract_amount: initialData.contract_amount || 0,
        contract_date: initialData.contract_date || null,
        start_date: initialData.start_date || null,
        end_date: initialData.end_date || null,
        client_name: initialData.client_name || '',
        client_contact: initialData.client_contact || '',
        status: initialData.status || '진행중',
        description: initialData.description || '',
        vendor_id: initialData.vendor_id || ''
      });
    }
  }, [initialData, reset]);

  const handleFormSubmit = async (data: ContractFormData) => {
    try {
      setError(null);
      await onSubmit(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : '계약 저장 중 오류가 발생했습니다');
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
      <Paper elevation={3} sx={{ p: 3, maxWidth: 800, mx: 'auto' }}>
        <Typography variant="h5" component="h2" gutterBottom>
          {initialData ? '계약 수정' : '새 계약 등록'}
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit(handleFormSubmit)}>
          <Grid container spacing={3}>
            {/* 기본 정보 */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                기본 정보
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="name"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="계약명"
                    fullWidth
                    required
                    error={!!errors.name}
                    helperText={errors.name?.message}
                    disabled={isLoading}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="contract_number"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="계약번호"
                    fullWidth
                    required
                    error={!!errors.contract_number}
                    helperText={errors.contract_number?.message}
                    disabled={isLoading}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="contract_amount"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="계약금액"
                    type="number"
                    fullWidth
                    required
                    error={!!errors.contract_amount}
                    helperText={errors.contract_amount?.message}
                    disabled={isLoading}
                    InputProps={{
                      startAdornment: <span>₩</span>
                    }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="vendor_id"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth required error={!!errors.vendor_id} disabled={isLoading}>
                    <InputLabel>거래처</InputLabel>
                    <Select {...field} label="거래처">
                      {vendors.map((vendor) => (
                        <MenuItem key={vendor.id} value={vendor.id}>
                          {vendor.name}
                        </MenuItem>
                      ))}
                    </Select>
                    {errors.vendor_id && (
                      <Typography variant="caption" color="error">
                        {errors.vendor_id.message}
                      </Typography>
                    )}
                  </FormControl>
                )}
              />
            </Grid>

            {/* 날짜 정보 */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                날짜 정보
              </Typography>
            </Grid>

            <Grid item xs={12} md={4}>
              <Controller
                name="contract_date"
                control={control}
                render={({ field }) => (
                  <DatePicker
                    label="계약일"
                    value={field.value}
                    onChange={field.onChange}
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        required: true,
                        error: !!errors.contract_date,
                        helperText: errors.contract_date?.message,
                        disabled: isLoading
                      }
                    }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <Controller
                name="start_date"
                control={control}
                render={({ field }) => (
                  <DatePicker
                    label="시작일"
                    value={field.value}
                    onChange={field.onChange}
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        error: !!errors.start_date,
                        helperText: errors.start_date?.message,
                        disabled: isLoading
                      }
                    }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <Controller
                name="end_date"
                control={control}
                render={({ field }) => (
                  <DatePicker
                    label="종료일"
                    value={field.value}
                    onChange={field.onChange}
                    minDate={watchStartDate || undefined}
                    slotProps={{
                      textField: {
                        fullWidth: true,
                        error: !!errors.end_date,
                        helperText: errors.end_date?.message,
                        disabled: isLoading
                      }
                    }}
                  />
                )}
              />
            </Grid>

            {/* 발주처 정보 */}
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                발주처 정보
              </Typography>
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="client_name"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="발주처명"
                    fullWidth
                    required
                    error={!!errors.client_name}
                    helperText={errors.client_name?.message}
                    disabled={isLoading}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12} md={6}>
              <Controller
                name="client_contact"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="발주처 연락처"
                    fullWidth
                    error={!!errors.client_contact}
                    helperText={errors.client_contact?.message}
                    disabled={isLoading}
                  />
                )}
              />
            </Grid>

            {/* 상태 및 설명 */}
            <Grid item xs={12} md={6}>
              <Controller
                name="status"
                control={control}
                render={({ field }) => (
                  <FormControl fullWidth required error={!!errors.status} disabled={isLoading}>
                    <InputLabel>상태</InputLabel>
                    <Select {...field} label="상태">
                      <MenuItem value="진행중">진행중</MenuItem>
                      <MenuItem value="완료">완료</MenuItem>
                      <MenuItem value="중단">중단</MenuItem>
                      <MenuItem value="취소">취소</MenuItem>
                    </Select>
                    {errors.status && (
                      <Typography variant="caption" color="error">
                        {errors.status.message}
                      </Typography>
                    )}
                  </FormControl>
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="description"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="계약 설명"
                    multiline
                    rows={4}
                    fullWidth
                    error={!!errors.description}
                    helperText={errors.description?.message}
                    disabled={isLoading}
                  />
                )}
              />
            </Grid>

            {/* 버튼 */}
            <Grid item xs={12}>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                <Button
                  variant="outlined"
                  onClick={onCancel}
                  disabled={isLoading}
                >
                  취소
                </Button>
                <Button
                  type="submit"
                  variant="contained"
                  disabled={isLoading || !isValid}
                  startIcon={isLoading ? <CircularProgress size={20} /> : null}
                >
                  {isLoading ? '저장 중...' : (initialData ? '수정' : '등록')}
                </Button>
              </Box>
            </Grid>
          </Grid>
        </Box>
      </Paper>
    </LocalizationProvider>
  );
};

export default ContractForm; 