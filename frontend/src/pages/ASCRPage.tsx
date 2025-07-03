import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Typography,
  Tabs,
  Tab,
  Paper,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Alert,
  Chip,
  LinearProgress
} from '@mui/material';
import { ASCRUpload } from '../components/ascr/ASCRUpload';
import { ASCRService, ASCRTaskStatus } from '../services/ascrService';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`ascr-tabpanel-${index}`}
      aria-labelledby={`ascr-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export const ASCRPage: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [tasks, setTasks] = useState<ASCRTaskStatus[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    loadTasks();
    loadStats();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const taskList = await ASCRService.getAllTasks();
      setTasks(taskList);
    } catch (err: any) {
      setError('작업 목록을 불러오는 중 오류가 발생했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await ASCRService.getProcessingStats();
      setStats(statsData);
    } catch (err: any) {
      console.error('통계 로드 실패:', err);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleProcessingSuccess = (result: any) => {
    console.log('처리 완료:', result);
    // 작업 목록 새로고침
    loadTasks();
  };

  const handleProcessingError = (error: string) => {
    setError(error);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'success';
      case 'processing':
        return 'warning';
      case 'error':
        return 'error';
      default:
        return 'default';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return '완료';
      case 'processing':
        return '처리중';
      case 'pending':
        return '대기중';
      case 'error':
        return '오류';
      default:
        return status;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        ASCR - 건설공사 내역서 자동화
      </Typography>
      
      <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
        PDF 문서를 업로드하여 자동으로 데이터를 추출하고 엑셀 문서를 생성합니다.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ width: '100%' }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          aria-label="ASCR 기능 탭"
          sx={{ borderBottom: 1, borderColor: 'divider' }}
        >
          <Tab label="PDF 처리" />
          <Tab label="작업 현황" />
          <Tab label="통계" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <ASCRUpload
            onSuccess={handleProcessingSuccess}
            onError={handleProcessingError}
          />
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Typography variant="h6" gutterBottom>
            처리 작업 현황
          </Typography>
          
          {loading ? (
            <LinearProgress />
          ) : tasks.length === 0 ? (
            <Alert severity="info">
              아직 처리된 작업이 없습니다.
            </Alert>
          ) : (
            <Grid container spacing={2}>
              {tasks.map((task) => (
                <Grid item xs={12} key={task.task_id}>
                  <Card>
                    <CardHeader
                      title={`작업 ${task.task_id}`}
                      subheader={new Date(task.created_at).toLocaleString()}
                      action={
                        <Chip
                          label={getStatusText(task.status)}
                          color={getStatusColor(task.status) as any}
                          size="small"
                        />
                      }
                    />
                    <CardContent>
                      {task.status === 'processing' && (
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2" gutterBottom>
                            진행률: {Math.round(task.progress * 100)}%
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={task.progress * 100} 
                          />
                        </Box>
                      )}
                      
                      {task.error && (
                        <Alert severity="error" sx={{ mb: 2 }}>
                          {task.error}
                        </Alert>
                      )}
                      
                      {task.result && (
                        <Typography variant="body2" color="text.secondary">
                          결과: {JSON.stringify(task.result, null, 2)}
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Typography variant="h6" gutterBottom>
            처리 통계
          </Typography>
          
          {stats ? (
            <Grid container spacing={3}>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      총 처리 파일
                    </Typography>
                    <Typography variant="h4">
                      {stats.total_files || 0}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      성공한 처리
                    </Typography>
                    <Typography variant="h4" color="success.main">
                      {stats.successful_processing || 0}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      실패한 처리
                    </Typography>
                    <Typography variant="h4" color="error.main">
                      {stats.failed_processing || 0}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="textSecondary" gutterBottom>
                      평균 처리 시간
                    </Typography>
                    <Typography variant="h4">
                      {stats.avg_processing_time || 0}s
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          ) : (
            <Alert severity="info">
              통계 정보를 불러오는 중입니다.
            </Alert>
          )}
        </TabPanel>
      </Paper>
    </Container>
  );
}; 