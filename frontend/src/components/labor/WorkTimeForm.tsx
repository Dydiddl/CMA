import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Grid,
  Typography,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Divider,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { ko } from 'date-fns/locale';
import { Labor, WorkTimeCreate } from '../../types/labor';

interface WorkTimeFormProps {
  labor: Labor;
  onSave: (data: WorkTimeCreate) => Promise<void>;
  onCancel: () => void;
}

export const WorkTimeForm: React.FC<WorkTimeFormProps> = ({
  labor,
  onSave,
  onCancel,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState<Partial<WorkTimeCreate>>({
    laborId: labor.id,
    date: new Date().toISOString().split('T')[0],
    startTime: '09:00',
    endTime: '18:00',
    breakTime: 60, // 1시간
    notes: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.date || !formData.startTime || !formData.endTime) {
      setError('필수 항목을 모두 입력해주세요.');
      return;
    }

    // 시작 시간과 종료 시간 검증
    const startTime = new Date(`2000-01-01T${formData.startTime}`);
    const endTime = new Date(`2000-01-01T${formData.endTime}`);
    
    if (startTime >= endTime) {
      setError('종료 시간은 시작 시간보다 늦어야 합니다.');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      await onSave(formData as WorkTimeCreate);
    } catch (err: any) {
      setError(err.message || '저장 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (field: keyof WorkTimeCreate, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleDateChange = (date: Date | null) => {
    if (date) {
      setFormData(prev => ({ 
        ...prev, 
        date: date.toISOString().split('T')[0] 
      }));
    }
  };

  const handleTimeChange = (field: 'startTime' | 'endTime', time: Date | null) => {
    if (time) {
      const timeString = time.toTimeString().slice(0, 5); // HH:MM 형식
      setFormData(prev => ({ ...prev, [field]: timeString }));
    }
  };

  // 총 작업 시간 계산
  const calculateTotalHours = () => {
    if (!formData.startTime || !formData.endTime) return 0;
    
    const startTime = new Date(`2000-01-01T${formData.startTime}`);
    const endTime = new Date(`2000-01-01T${formData.endTime}`);
    const breakTimeMinutes = formData.breakTime || 0;
    
    const totalMinutes = (endTime.getTime() - startTime.getTime()) / (1000 * 60) - breakTimeMinutes;
    return Math.max(0, totalMinutes / 60); // 시간 단위로 변환
  };

  // 총 금액 계산
  const calculateTotalAmount = () => {
    const totalHours = calculateTotalHours();
    return totalHours * labor.hourlyRate;
  };

  // 금액 포맷팅
  const formatAmount = (amount: number) => {
    return new Intl.NumberFormat('ko-KR').format(amount);
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
      <Typography variant="h6" gutterBottom>
        작업 시간 기록
      </Typography>

      {/* 작업자 정보 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            작업자 정보
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                작업자명: {labor.workerName}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                직종: {labor.position}
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                시급: {formatAmount(labor.hourlyRate)}원
              </Typography>
            </Grid>
            <Grid item xs={12} sm={6}>
              <Typography variant="body2" color="text.secondary">
                일급: {formatAmount(labor.dailyRate)}원
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
            <DatePicker
              label="작업일 *"
              value={formData.date ? new Date(formData.date) : null}
              onChange={handleDateChange}
              renderInput={(params) => <TextField {...params} fullWidth required />}
            />
          </LocalizationProvider>
        </Grid>

        <Grid item xs={12} sm={6}>
          <TextField
            fullWidth
            label="휴식 시간 (분)"
            type="number"
            value={formData.breakTime || 0}
            onChange={(e) => handleInputChange('breakTime', parseInt(e.target.value) || 0)}
            inputProps={{ min: 0, max: 480 }} // 최대 8시간
            helperText="기본값: 60분 (1시간)"
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
            <TimePicker
              label="시작 시간 *"
              value={formData.startTime ? new Date(`2000-01-01T${formData.startTime}`) : null}
              onChange={(time) => handleTimeChange('startTime', time)}
              renderInput={(params) => <TextField {...params} fullWidth required />}
            />
          </LocalizationProvider>
        </Grid>

        <Grid item xs={12} sm={6}>
          <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
            <TimePicker
              label="종료 시간 *"
              value={formData.endTime ? new Date(`2000-01-01T${formData.endTime}`) : null}
              onChange={(time) => handleTimeChange('endTime', time)}
              renderInput={(params) => <TextField {...params} fullWidth required />}
            />
          </LocalizationProvider>
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="메모"
            multiline
            rows={3}
            value={formData.notes || ''}
            onChange={(e) => handleInputChange('notes', e.target.value)}
            placeholder="작업 내용이나 특이사항을 기록하세요"
          />
        </Grid>
      </Grid>

      {/* 계산 결과 */}
      <Card sx={{ mt: 3, mb: 3 }}>
        <CardContent>
          <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
            계산 결과
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <Typography variant="body2" color="text.secondary">
                총 작업 시간
              </Typography>
              <Typography variant="h6">
                {calculateTotalHours().toFixed(1)}시간
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="body2" color="text.secondary">
                시급
              </Typography>
              <Typography variant="h6">
                {formatAmount(labor.hourlyRate)}원
              </Typography>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Typography variant="body2" color="text.secondary">
                총 금액
              </Typography>
              <Typography variant="h6" color="primary">
                {formatAmount(calculateTotalAmount())}원
              </Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button
          type="submit"
          variant="contained"
          disabled={loading}
          startIcon={loading ? <CircularProgress size={20} /> : null}
        >
          저장
        </Button>
        <Button variant="outlined" onClick={onCancel}>
          취소
        </Button>
      </Box>
    </Box>
  );
}; 