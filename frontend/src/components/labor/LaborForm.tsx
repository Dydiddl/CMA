import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Typography,
  Alert,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ko } from 'date-fns/locale';
import { Labor, LaborCreate, LaborUpdate, LaborStatus } from '../../types/labor';

interface LaborFormProps {
  labor?: Labor | null;
  onSave: (data: LaborCreate | LaborUpdate) => Promise<void>;
  onCancel: () => void;
}

export const LaborForm: React.FC<LaborFormProps> = ({
  labor,
  onSave,
  onCancel,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<Partial<LaborCreate>>({
    workerName: '',
    workerId: '',
    position: '',
    hourlyRate: 0,
    dailyRate: 0,
    contractId: '',
    startDate: new Date().toISOString().split('T')[0],
    status: '활성',
    phoneNumber: '',
    email: '',
    address: '',
    notes: '',
  });

  const isEditMode = !!labor;

  useEffect(() => {
    if (isEditMode && labor) {
      setFormData({
        workerName: labor.workerName,
        workerId: labor.workerId,
        position: labor.position,
        hourlyRate: labor.hourlyRate,
        dailyRate: labor.dailyRate,
        contractId: labor.contractId,
        startDate: labor.startDate,
        endDate: labor.endDate,
        status: labor.status,
        phoneNumber: labor.phoneNumber,
        email: labor.email,
        address: labor.address,
        notes: labor.notes,
      });
    }
  }, [labor, isEditMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.workerName || !formData.workerId || !formData.position) {
      setError('필수 항목을 모두 입력해주세요.');
      return;
    }

    if (formData.hourlyRate <= 0 || formData.dailyRate <= 0) {
      setError('시급과 일급은 0보다 커야 합니다.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await onSave(formData);
    } catch (err: any) {
      setError(err.message || '저장 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof LaborCreate, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleDateChange = (field: 'startDate' | 'endDate', date: Date | null) => {
    if (date) {
      setFormData(prev => ({ 
        ...prev, 
        [field]: date.toISOString().split('T')[0] 
      }));
    } else {
      setFormData(prev => ({ ...prev, [field]: undefined }));
    }
  };

  // 일급 자동 계산
  const calculateDailyRate = (hourlyRate: number) => {
    return hourlyRate * 8; // 8시간 기준
  };

  const handleHourlyRateChange = (value: number) => {
    setFormData(prev => ({ 
      ...prev, 
      hourlyRate: value,
      dailyRate: calculateDailyRate(value)
    }));
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        {isEditMode ? '작업자 정보 수정' : '새 작업자 등록'}
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={2}>
        {/* 기본 정보 */}
        <Grid item xs={12}>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            기본 정보
          </Typography>
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="작업자명 *"
            value={formData.workerName || ''}
            onChange={(e) => handleInputChange('workerName', e.target.value)}
            required
          />
        </Grid>
        
        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="작업자 ID *"
            value={formData.workerId || ''}
            onChange={(e) => handleInputChange('workerId', e.target.value)}
            required
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <FormControl fullWidth required>
            <InputLabel>직종</InputLabel>
            <Select
              value={formData.position || ''}
              label="직종"
              onChange={(e) => handleInputChange('position', e.target.value)}
            >
              <MenuItem value="기술자">기술자</MenuItem>
              <MenuItem value="일반작업자">일반작업자</MenuItem>
              <MenuItem value="관리자">관리자</MenuItem>
              <MenuItem value="기타">기타</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6}>
          <FormControl fullWidth>
            <InputLabel>상태</InputLabel>
            <Select
              value={formData.status || '활성'}
              label="상태"
              onChange={(e) => handleInputChange('status', e.target.value)}
            >
              <MenuItem value="활성">활성</MenuItem>
              <MenuItem value="비활성">비활성</MenuItem>
              <MenuItem value="퇴사">퇴사</MenuItem>
              <MenuItem value="휴직">휴직</MenuItem>
            </Select>
          </FormControl>
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="계약 ID *"
            value={formData.contractId || ''}
            onChange={(e) => handleInputChange('contractId', e.target.value)}
            required
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
            <DatePicker
              label="시작일 *"
              value={formData.startDate ? new Date(formData.startDate) : null}
              onChange={(date) => handleDateChange('startDate', date)}
              renderInput={(params) => <TextField {...params} fullWidth required />}
            />
          </LocalizationProvider>
        </Grid>

        <Grid item xs={12} sm={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
            <DatePicker
              label="종료일"
              value={formData.endDate ? new Date(formData.endDate) : null}
              onChange={(date) => handleDateChange('endDate', date)}
              renderInput={(params) => <TextField {...params} fullWidth />}
            />
          </LocalizationProvider>
        </Grid>

        <Grid item xs={12}>
          <Divider sx={{ my: 2 }} />
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            급여 정보
          </Typography>
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="시급 (원) *"
            type="number"
            value={formData.hourlyRate || ''}
            onChange={(e) => handleHourlyRateChange(parseFloat(e.target.value) || 0)}
            required
            inputProps={{ min: 0 }}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="일급 (원) *"
            type="number"
            value={formData.dailyRate || ''}
            onChange={(e) => handleInputChange('dailyRate', parseFloat(e.target.value) || 0)}
            required
            inputProps={{ min: 0 }}
            helperText="8시간 기준으로 자동 계산됩니다"
          />
        </Grid>

        <Grid item xs={12}>
          <Divider sx={{ my: 2 }} />
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            연락처 정보
          </Typography>
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="전화번호"
            value={formData.phoneNumber || ''}
            onChange={(e) => handleInputChange('phoneNumber', e.target.value)}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="이메일"
            type="email"
            value={formData.email || ''}
            onChange={(e) => handleInputChange('email', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="주소"
            value={formData.address || ''}
            onChange={(e) => handleInputChange('address', e.target.value)}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="메모"
            multiline
            rows={3}
            value={formData.notes || ''}
            onChange={(e) => handleInputChange('notes', e.target.value)}
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
        <Button variant="outlined" onClick={onCancel}>
          취소
        </Button>
      </Box>
    </Box>
  );
}; 