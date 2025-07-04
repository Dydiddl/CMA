import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Avatar,
  Divider,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import {
  Person as PersonIcon,
  Work as WorkIcon,
  Phone as PhoneIcon,
  Email as EmailIcon,
  LocationOn as LocationIcon,
  Edit as EditIcon,
  Schedule as ScheduleIcon,
  AttachMoney as MoneyIcon,
  CalendarToday as CalendarIcon,
  Badge as BadgeIcon,
} from '@mui/icons-material';
import { Labor, LaborStatus } from '../../types/labor';

interface LaborDetailProps {
  labor: Labor;
  onEdit: () => void;
}

export const LaborDetail: React.FC<LaborDetailProps> = ({ labor, onEdit }) => {
  // 상태별 색상
  const getStatusColor = (status: LaborStatus) => {
    switch (status) {
      case '활성':
        return 'success';
      case '비활성':
        return 'default';
      case '퇴사':
        return 'error';
      case '휴직':
        return 'warning';
      default:
        return 'default';
    }
  };

  // 금액 포맷팅
  const formatAmount = (amount: number) => {
    return new Intl.NumberFormat('ko-KR').format(amount);
  };

  // 날짜 포맷팅
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR');
  };

  // 시간 포맷팅
  const formatTime = (timeString: string) => {
    return new Date(`2000-01-01T${timeString}`).toLocaleTimeString('ko-KR', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <Box>
      {/* 헤더 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Avatar sx={{ mr: 2, width: 64, height: 64, bgcolor: 'primary.main' }}>
            {labor.workerName.charAt(0)}
          </Avatar>
          <Box>
            <Typography variant="h5" fontWeight="bold">
              {labor.workerName}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {labor.workerId}
            </Typography>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Chip
            label={labor.status}
            color={getStatusColor(labor.status) as any}
            size="medium"
          />
          <Button
            variant="outlined"
            startIcon={<EditIcon />}
            onClick={onEdit}
          >
            수정
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {/* 기본 정보 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <PersonIcon sx={{ mr: 1 }} />
                기본 정보
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemIcon>
                    <BadgeIcon />
                  </ListItemIcon>
                  <ListItemText
                    primary="직종"
                    secondary={labor.position}
                  />
                </ListItem>
                <ListItem>
                  <ListItemIcon>
                    <CalendarIcon />
                  </ListItemIcon>
                  <ListItemText
                    primary="시작일"
                    secondary={formatDate(labor.startDate)}
                  />
                </ListItem>
                {labor.endDate && (
                  <ListItem>
                    <ListItemIcon>
                      <CalendarIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="종료일"
                      secondary={formatDate(labor.endDate)}
                    />
                  </ListItem>
                )}
                <ListItem>
                  <ListItemIcon>
                    <WorkIcon />
                  </ListItemIcon>
                  <ListItemText
                    primary="계약 ID"
                    secondary={labor.contractId}
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* 급여 정보 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <MoneyIcon sx={{ mr: 1 }} />
                급여 정보
              </Typography>
              <List dense>
                <ListItem>
                  <ListItemText
                    primary="시급"
                    secondary={`${formatAmount(labor.hourlyRate)}원`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="일급"
                    secondary={`${formatAmount(labor.dailyRate)}원`}
                  />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="일일 근무 시간"
                    secondary="8시간"
                  />
                </ListItem>
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* 연락처 정보 */}
        {(labor.phoneNumber || labor.email || labor.address) && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <PhoneIcon sx={{ mr: 1 }} />
                  연락처 정보
                </Typography>
                <List dense>
                  {labor.phoneNumber && (
                    <ListItem>
                      <ListItemIcon>
                        <PhoneIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary="전화번호"
                        secondary={labor.phoneNumber}
                      />
                    </ListItem>
                  )}
                  {labor.email && (
                    <ListItem>
                      <ListItemIcon>
                        <EmailIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary="이메일"
                        secondary={labor.email}
                      />
                    </ListItem>
                  )}
                  {labor.address && (
                    <ListItem>
                      <ListItemIcon>
                        <LocationIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary="주소"
                        secondary={labor.address}
                      />
                    </ListItem>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* 메모 */}
        {labor.notes && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  메모
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {labor.notes}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* 시스템 정보 */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                시스템 정보
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    생성일: {formatDate(labor.createdAt)}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="body2" color="text.secondary">
                    수정일: {formatDate(labor.updatedAt)}
                  </Typography>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 작업 시간 기록 섹션 */}
      <Box sx={{ mt: 3 }}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <ScheduleIcon sx={{ mr: 1 }} />
              작업 시간 기록
            </Typography>
            <Typography variant="body2" color="text.secondary">
              작업 시간 기록 기능은 별도 페이지에서 관리됩니다.
            </Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
}; 