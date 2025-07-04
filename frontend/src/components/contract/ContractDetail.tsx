import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  Button,
  Divider,
  Paper,
} from '@mui/material';
import {
  Edit as EditIcon,
  Business as BusinessIcon,
  Person as PersonIcon,
  CalendarToday as CalendarIcon,
  AttachMoney as MoneyIcon,
  Description as DescriptionIcon,
} from '@mui/icons-material';
import { Contract } from '../../types/contract';

interface ContractDetailProps {
  contract: Contract;
  onEdit?: () => void;
}

export const ContractDetail: React.FC<ContractDetailProps> = ({
  contract,
  onEdit,
}) => {
  // 금액 포맷팅
  const formatAmount = (amount: number) => {
    return new Intl.NumberFormat('ko-KR').format(amount);
  };

  // 날짜 포맷팅
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR');
  };

  // 상태별 색상
  const getStatusColor = (status: string) => {
    switch (status) {
      case '진행중':
        return 'primary';
      case '완료':
        return 'success';
      case '중단':
        return 'warning';
      case '취소':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box sx={{ p: 2 }}>
      {/* 헤더 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h5" component="h2">
          계약 상세 정보
        </Typography>
        {onEdit && (
          <Button
            variant="outlined"
            startIcon={<EditIcon />}
            onClick={onEdit}
          >
            수정
          </Button>
        )}
      </Box>

      <Grid container spacing={3}>
        {/* 기본 정보 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <BusinessIcon sx={{ mr: 1 }} />
                기본 정보
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  계약명
                </Typography>
                <Typography variant="body1">
                  {contract.name}
                </Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  계약번호
                </Typography>
                <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                  {contract.contractNumber}
                </Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  계약금액
                </Typography>
                <Typography variant="h6" color="primary" sx={{ display: 'flex', alignItems: 'center' }}>
                  <MoneyIcon sx={{ mr: 0.5, fontSize: '1.2em' }} />
                  {formatAmount(contract.contractAmount)}원
                </Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  상태
                </Typography>
                <Chip
                  label={contract.status}
                  color={getStatusColor(contract.status) as any}
                  size="small"
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* 날짜 정보 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <CalendarIcon sx={{ mr: 1 }} />
                날짜 정보
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  계약일
                </Typography>
                <Typography variant="body1">
                  {formatDate(contract.contractDate)}
                </Typography>
              </Box>

              {contract.startDate && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    시작일
                  </Typography>
                  <Typography variant="body1">
                    {formatDate(contract.startDate)}
                  </Typography>
                </Box>
              )}

              {contract.endDate && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    종료일
                  </Typography>
                  <Typography variant="body1">
                    {formatDate(contract.endDate)}
                  </Typography>
                </Box>
              )}

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  생성일
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {formatDate(contract.createdAt)}
                </Typography>
              </Box>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  수정일
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {formatDate(contract.updatedAt)}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* 발주처 정보 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <PersonIcon sx={{ mr: 1 }} />
                발주처 정보
              </Typography>
              <Divider sx={{ mb: 2 }} />
              
              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  발주처명
                </Typography>
                <Typography variant="body1">
                  {contract.clientName}
                </Typography>
              </Box>

              {contract.clientContact && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" color="text.secondary">
                    연락처
                  </Typography>
                  <Typography variant="body1">
                    {contract.clientContact}
                  </Typography>
                </Box>
              )}

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="text.secondary">
                  거래처 ID
                </Typography>
                <Typography variant="body1" sx={{ fontFamily: 'monospace' }}>
                  {contract.vendorId}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* 설명 */}
        {contract.description && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <DescriptionIcon sx={{ mr: 1 }} />
                  설명
                </Typography>
                <Divider sx={{ mb: 2 }} />
                
                <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
                  {contract.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      {/* 요약 정보 */}
      <Paper sx={{ mt: 3, p: 2, backgroundColor: 'grey.50' }}>
        <Typography variant="h6" gutterBottom>
          계약 요약
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <Typography variant="subtitle2" color="text.secondary">
              계약 기간
            </Typography>
            <Typography variant="body1">
              {contract.startDate && contract.endDate
                ? `${formatDate(contract.startDate)} ~ ${formatDate(contract.endDate)}`
                : '미정'
              }
            </Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="subtitle2" color="text.secondary">
              진행 상태
            </Typography>
            <Chip
              label={contract.status}
              color={getStatusColor(contract.status) as any}
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="subtitle2" color="text.secondary">
              총 계약금액
            </Typography>
            <Typography variant="h6" color="primary">
              {formatAmount(contract.contractAmount)}원
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
}; 