import React, { useState, useEffect, useCallback } from 'react';
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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Chip,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Pagination,
  Grid,
  Fab,
  Tooltip,
  Tabs,
  Tab,
  Avatar,
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Refresh as RefreshIcon,
  Schedule as ScheduleIcon,
  Person as PersonIcon,
  Work as WorkIcon,
} from '@mui/icons-material';
import { LaborForm } from '../components/labor/LaborForm';
import { LaborDetail } from '../components/labor/LaborDetail';
import { WorkTimeForm } from '../components/labor/WorkTimeForm';
import { LaborService } from '../services/laborService';
import { Labor, LaborStatus } from '../types/labor';

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
      id={`labor-tabpanel-${index}`}
      aria-labelledby={`labor-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const LaborList: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [laborList, setLaborList] = useState<Labor[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [positionFilter, setPositionFilter] = useState<string>('');
  
  // 다이얼로그 상태
  const [openLaborForm, setOpenLaborForm] = useState(false);
  const [openLaborDetail, setOpenLaborDetail] = useState(false);
  const [openWorkTimeForm, setOpenWorkTimeForm] = useState(false);
  const [openDelete, setOpenDelete] = useState(false);
  const [selectedLabor, setSelectedLabor] = useState<Labor | null>(null);
  const [editingLabor, setEditingLabor] = useState<Labor | null>(null);

  // 노무 목록 조회
  const fetchLaborList = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await LaborService.getLaborList({
        page,
        size,
        search: search || undefined,
        status: statusFilter as LaborStatus || undefined,
        position: positionFilter || undefined,
      });
      
      if (response.status === 'success') {
        setLaborList(response.data);
        setTotal(response.total);
      } else {
        setError(response.message || '노무 목록을 불러오는데 실패했습니다.');
      }
    } catch (err: any) {
      setError(err.message || '노무 목록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  }, [page, size, search, statusFilter, positionFilter]);

  // 초기 로드
  useEffect(() => {
    fetchLaborList();
  }, [fetchLaborList]);

  // 탭 변경 처리
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setPage(1);
    setSearch('');
    setStatusFilter('');
    setPositionFilter('');
  };

  // 검색 처리
  const handleSearch = (event: React.FormEvent) => {
    event.preventDefault();
    setPage(1);
    fetchLaborList();
  };

  // 필터 초기화
  const handleClearFilters = () => {
    setSearch('');
    setStatusFilter('');
    setPositionFilter('');
    setPage(1);
  };

  // 노무 생성/수정
  const handleSaveLabor = async (laborData: any) => {
    try {
      if (editingLabor) {
        await LaborService.updateLabor(editingLabor.id, laborData);
      } else {
        await LaborService.createLabor(laborData);
      }
      
      setOpenLaborForm(false);
      setEditingLabor(null);
      fetchLaborList();
    } catch (err: any) {
      setError(err.message || '노무 정보 저장에 실패했습니다.');
    }
  };

  // 노무 삭제
  const handleDeleteLabor = async () => {
    if (!selectedLabor) return;
    
    try {
      await LaborService.deleteLabor(selectedLabor.id);
      setOpenDelete(false);
      setSelectedLabor(null);
      fetchLaborList();
    } catch (err: any) {
      setError(err.message || '노무 삭제에 실패했습니다.');
    }
  };

  // 노무 상세 보기
  const handleViewLabor = (labor: Labor) => {
    setSelectedLabor(labor);
    setOpenLaborDetail(true);
  };

  // 노무 수정
  const handleEditLabor = (labor: Labor) => {
    setEditingLabor(labor);
    setOpenLaborForm(true);
  };

  // 노무 삭제 확인
  const handleDeleteClick = (labor: Labor) => {
    setSelectedLabor(labor);
    setOpenDelete(true);
  };

  // 작업 시간 기록
  const handleWorkTime = (labor: Labor) => {
    setSelectedLabor(labor);
    setOpenWorkTimeForm(true);
  };

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

  return (
    <Box sx={{ p: 3 }}>
      {/* 헤더 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          노무 관리
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenLaborForm(true)}
        >
          새 작업자 등록
        </Button>
      </Box>

      {/* 탭 */}
      <Card sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="노무 관리 탭">
          <Tab 
            icon={<PersonIcon />} 
            label="작업자 관리" 
            iconPosition="start"
          />
          <Tab 
            icon={<WorkIcon />} 
            label="작업 시간" 
            iconPosition="start"
          />
        </Tabs>
      </Card>

      {/* 검색 및 필터 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <form onSubmit={handleSearch}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={3}>
                <TextField
                  fullWidth
                  label="검색"
                  placeholder="작업자명, 작업자ID로 검색"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  InputProps={{
                    startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                  }}
                />
              </Grid>
              <Grid item xs={12} md={2}>
                <FormControl fullWidth>
                  <InputLabel>상태</InputLabel>
                  <Select
                    value={statusFilter}
                    label="상태"
                    onChange={(e) => setStatusFilter(e.target.value)}
                  >
                    <MenuItem value="">전체</MenuItem>
                    <MenuItem value="활성">활성</MenuItem>
                    <MenuItem value="비활성">비활성</MenuItem>
                    <MenuItem value="퇴사">퇴사</MenuItem>
                    <MenuItem value="휴직">휴직</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={2}>
                <FormControl fullWidth>
                  <InputLabel>직종</InputLabel>
                  <Select
                    value={positionFilter}
                    label="직종"
                    onChange={(e) => setPositionFilter(e.target.value)}
                  >
                    <MenuItem value="">전체</MenuItem>
                    <MenuItem value="기술자">기술자</MenuItem>
                    <MenuItem value="일반작업자">일반작업자</MenuItem>
                    <MenuItem value="관리자">관리자</MenuItem>
                    <MenuItem value="기타">기타</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={3}>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    type="submit"
                    variant="contained"
                    startIcon={<SearchIcon />}
                  >
                    검색
                  </Button>
                  <Button
                    variant="outlined"
                    startIcon={<FilterIcon />}
                    onClick={handleClearFilters}
                  >
                    초기화
                  </Button>
                </Box>
              </Grid>
              <Grid item xs={12} md={2}>
                <Button
                  variant="outlined"
                  startIcon={<RefreshIcon />}
                  onClick={fetchLaborList}
                  fullWidth
                >
                  새로고침
                </Button>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>

      {/* 에러 메시지 */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* 노무 목록 테이블 */}
      <Card>
        <CardContent>
          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
              <CircularProgress />
            </Box>
          ) : (
            <>
              <TableContainer component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>작업자</TableCell>
                      <TableCell>작업자ID</TableCell>
                      <TableCell>직종</TableCell>
                      <TableCell align="right">시급</TableCell>
                      <TableCell align="right">일급</TableCell>
                      <TableCell>시작일</TableCell>
                      <TableCell>상태</TableCell>
                      <TableCell align="center">작업</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {laborList.map((labor) => (
                      <TableRow key={labor.id} hover>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
                              {labor.workerName.charAt(0)}
                            </Avatar>
                            <Box>
                              <Typography variant="body1" fontWeight="bold">
                                {labor.workerName}
                              </Typography>
                              {labor.phoneNumber && (
                                <Typography variant="caption" color="text.secondary">
                                  {labor.phoneNumber}
                                </Typography>
                              )}
                            </Box>
                          </Box>
                        </TableCell>
                        <TableCell>{labor.workerId}</TableCell>
                        <TableCell>{labor.position}</TableCell>
                        <TableCell align="right">
                          {formatAmount(labor.hourlyRate)}원
                        </TableCell>
                        <TableCell align="right">
                          {formatAmount(labor.dailyRate)}원
                        </TableCell>
                        <TableCell>
                          {formatDate(labor.startDate)}
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={labor.status}
                            color={getStatusColor(labor.status) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell align="center">
                          <IconButton
                            size="small"
                            onClick={() => handleViewLabor(labor)}
                            title="상세보기"
                          >
                            <ViewIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleEditLabor(labor)}
                            title="수정"
                          >
                            <EditIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleWorkTime(labor)}
                            title="작업시간"
                            color="info"
                          >
                            <ScheduleIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDeleteClick(labor)}
                            title="삭제"
                            color="error"
                          >
                            <DeleteIcon />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>

              {/* 페이징 */}
              {total > 0 && (
                <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                  <Pagination
                    count={Math.ceil(total / size)}
                    page={page}
                    onChange={(_, newPage) => setPage(newPage)}
                    color="primary"
                  />
                </Box>
              )}

              {/* 결과 없음 */}
              {laborList.length === 0 && !loading && (
                <Box sx={{ textAlign: 'center', p: 3 }}>
                  <Typography variant="body2" color="text.secondary">
                    등록된 작업자가 없습니다.
                  </Typography>
                </Box>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {/* 노무 생성/수정 폼 다이얼로그 */}
      <Dialog
        open={openLaborForm}
        onClose={() => {
          setOpenLaborForm(false);
          setEditingLabor(null);
        }}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {editingLabor ? '작업자 정보 수정' : '새 작업자 등록'}
        </DialogTitle>
        <DialogContent>
          <LaborForm
            labor={editingLabor}
            onSave={handleSaveLabor}
            onCancel={() => {
              setOpenLaborForm(false);
              setEditingLabor(null);
            }}
          />
        </DialogContent>
      </Dialog>

      {/* 노무 상세 보기 다이얼로그 */}
      <Dialog
        open={openLaborDetail}
        onClose={() => setOpenLaborDetail(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>작업자 상세 정보</DialogTitle>
        <DialogContent>
          {selectedLabor && (
            <LaborDetail
              labor={selectedLabor}
              onEdit={() => {
                setOpenLaborDetail(false);
                handleEditLabor(selectedLabor);
              }}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenLaborDetail(false)}>닫기</Button>
        </DialogActions>
      </Dialog>

      {/* 작업 시간 기록 폼 다이얼로그 */}
      <Dialog
        open={openWorkTimeForm}
        onClose={() => setOpenWorkTimeForm(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>작업 시간 기록</DialogTitle>
        <DialogContent>
          {selectedLabor && (
            <WorkTimeForm
              labor={selectedLabor}
              onSave={async (workTimeData) => {
                try {
                  await LaborService.createWorkTime(selectedLabor.id, workTimeData);
                  setOpenWorkTimeForm(false);
                  setSelectedLabor(null);
                } catch (err: any) {
                  setError(err.message || '작업 시간 기록에 실패했습니다.');
                }
              }}
              onCancel={() => {
                setOpenWorkTimeForm(false);
                setSelectedLabor(null);
              }}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* 삭제 확인 다이얼로그 */}
      <Dialog open={openDelete} onClose={() => setOpenDelete(false)}>
        <DialogTitle>작업자 삭제</DialogTitle>
        <DialogContent>
          <Typography>
            정말로 "{selectedLabor?.workerName}" 작업자를 삭제하시겠습니까?
            <br />
            이 작업은 되돌릴 수 없습니다.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDelete(false)}>취소</Button>
          <Button onClick={handleDeleteLabor} color="error" variant="contained">
            삭제
          </Button>
        </DialogActions>
      </Dialog>

      {/* 플로팅 액션 버튼 */}
      <Tooltip title="새 작업자 등록">
        <Fab
          color="primary"
          sx={{ position: 'fixed', bottom: 16, right: 16 }}
          onClick={() => setOpenLaborForm(true)}
        >
          <AddIcon />
        </Fab>
      </Tooltip>
    </Box>
  );
};

export default LaborList; 