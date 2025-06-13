import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Assignment as ProjectIcon,
  Task as TaskIcon,
  TrendingUp as ProgressIcon,
  Warning as AlertIcon,
} from '@mui/icons-material';

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
  // 임시 데이터
  const stats = {
    totalProjects: 12,
    activeTasks: 45,
    completedTasks: 78,
    alerts: 3,
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        대시보드
      </Typography>
      <Grid container spacing={3}>
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
              <ProgressIcon />
              <Box>
                <Typography variant="h6">완료된 작업</Typography>
                <Typography variant="h4">{stats.completedTasks}</Typography>
              </Box>
            </StatBox>
          </StyledPaper>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper>
            <StatBox>
              <AlertIcon />
              <Box>
                <Typography variant="h6">알림</Typography>
                <Typography variant="h4">{stats.alerts}</Typography>
              </Box>
            </StatBox>
          </StyledPaper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard; 