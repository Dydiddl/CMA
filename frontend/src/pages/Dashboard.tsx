import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography, Box, Card, CardContent, Button } from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Assignment as ProjectIcon,
  Task as TaskIcon,
  TrendingUp as ProgressIcon,
  Warning as AlertIcon,
  Business as ContractIcon,
  AttachMoney as FinancialIcon,
  Description as DocumentIcon,
  People as LaborIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  display: 'flex',
  flexDirection: 'column',
  height: '100%',
  backgroundColor: theme.palette.background.paper,
  border: `1px solid ${theme.palette.divider}`,
}));

const StatBox = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  marginBottom: theme.spacing(2),
  '& .MuiSvgIcon-root': {
    marginRight: theme.spacing(2),
    color: theme.palette.primary.main,
  },
}));

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  
  // 임시 데이터
  const stats = {
    totalProjects: 12,
    activeTasks: 45,
    completedTasks: 78,
    totalContracts: 8,
    totalFinancial: 156,
    totalLabor: 24,
    totalDocuments: 23,
    alerts: 3,
  };

  const quickActions = [
    {
      title: '계약 관리',
      description: '계약 생성, 수정, 조회',
      icon: <ContractIcon />,
      path: '/contracts',
      color: 'primary',
    },
    {
      title: '재무 관리',
      description: '수입/지출 관리',
      icon: <FinancialIcon />,
      path: '/financial',
      color: 'success',
    },
    {
      title: '노무 관리',
      description: '작업자 및 시간 관리',
      icon: <LaborIcon />,
      path: '/labor',
      color: 'warning',
    },
    {
      title: 'ASCR 처리',
      description: 'PDF 문서 자동화',
      icon: <DocumentIcon />,
      path: '/ascr',
      color: 'info',
    },
  ];

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        건설 관리 시스템 대시보드
      </Typography>
      
      {/* 통계 카드 */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper>
            <StatBox>
              <ContractIcon />
              <Box>
                <Typography variant="h6">전체 계약</Typography>
                <Typography variant="h4">{stats.totalContracts}</Typography>
              </Box>
            </StatBox>
          </StyledPaper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper>
            <StatBox>
              <FinancialIcon />
              <Box>
                <Typography variant="h6">재무 기록</Typography>
                <Typography variant="h4">{stats.totalFinancial}</Typography>
              </Box>
            </StatBox>
          </StyledPaper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper>
            <StatBox>
              <ProjectIcon />
              <Box>
                <Typography variant="h6">전체 프로젝트</Typography>
                <Typography variant="h4">{stats.totalProjects}</Typography>
              </Box>
            </StatBox>
          </StyledPaper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper>
            <StatBox>
              <TaskIcon />
              <Box>
                <Typography variant="h6">진행중인 작업</Typography>
                <Typography variant="h4">{stats.activeTasks}</Typography>
              </Box>
            </StatBox>
          </StyledPaper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper>
            <StatBox>
              <LaborIcon />
              <Box>
                <Typography variant="h6">전체 작업자</Typography>
                <Typography variant="h4">{stats.totalLabor}</Typography>
              </Box>
            </StatBox>
          </StyledPaper>
        </Grid>
      </Grid>

      {/* 빠른 액션 */}
      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        빠른 액션
      </Typography>
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {quickActions.map((action, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card 
              sx={{ 
                height: '100%', 
                cursor: 'pointer',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                }
              }}
              onClick={() => navigate(action.path)}
            >
              <CardContent sx={{ textAlign: 'center', p: 3 }}>
                <Box sx={{ color: `${action.color}.main`, mb: 2 }}>
                  {action.icon}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {action.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {action.description}
                </Typography>
                <Button 
                  variant="outlined" 
                  color={action.color as any}
                  fullWidth
                >
                  바로가기
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* 최근 활동 */}
      <Typography variant="h5" gutterBottom>
        최근 활동
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                최근 계약
              </Typography>
              <Typography variant="body2" color="text.secondary">
                아직 등록된 계약이 없습니다.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                최근 재무 기록
              </Typography>
              <Typography variant="body2" color="text.secondary">
                아직 등록된 재무 기록이 없습니다.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                최근 노무 기록
              </Typography>
              <Typography variant="body2" color="text.secondary">
                아직 등록된 노무 기록이 없습니다.
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 