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
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Refresh as RefreshIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
} from '@mui/icons-material';
import { FinancialForm } from '../components/financial/FinancialForm';
import { FinancialDetail } from '../components/financial/FinancialDetail';
import { FinancialService } from '../services/financialService';
import { FinancialRecord, FinancialType } from '../types/financial';

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
      id={`financial-tabpanel-${index}`}
      aria-labelledby={`financial-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const FinancialList: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [records, setRecords] = useState<FinancialRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  
  // 다이얼로그 상태
  const [openForm, setOpenForm] = useState(false);
  const [openDetail, setOpenDetail] = useState(false);
  const [openDelete, setOpenDelete] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState<FinancialRecord | null>(null);
  const [editingRecord, setEditingRecord] = useState<FinancialRecord | null>(null);

  // 현재 탭에 따른 타입
  const currentType = tabValue === 0 ? '수입' : '지출';

  // 재무 기록 목록 조회
  const fetchRecords = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await FinancialService.getFinancialRecords({
        page,
        size,
        type: currentType,
        search: search || undefined,
        category: categoryFilter || undefined,
      });
      
      if (response.status === 'success') {
        setRecords(response.data);
        setTotal(response.total);
      } else {
        setError(response.message || '재무 기록을 불러오는데 실패했습니다.');
      }
    } catch (err: any) {
      setError(err.message || '재무 기록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  }, [page, size, currentType, search, categoryFilter]);

  // 초기 로드
  useEffect(() => {
    fetchRecords();
  }, [fetchRecords]);

  // 탭 변경 처리
  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
    setPage(1);
    setSearch('');
    setCategoryFilter('');
  };

  // 검색 처리
  const handleSearch = (event: React.FormEvent) => {
    event.preventDefault();
    setPage(1);
    fetchRecords();
  };

  // 필터 초기화
  const handleClearFilters = () => {
    setSearch('');
    setCategoryFilter('');
    setPage(1);
  };

  // 재무 기록 생성/수정
  const handleSaveRecord = async (recordData: any) => {
    try {
      if (editingRecord) {
        await FinancialService.updateFinancialRecord(editingRecord.id, recordData);
      } else {
        await FinancialService.createFinancialRecord(recordData);
      }
      
      setOpenForm(false);
      setEditingRecord(null);
      fetchRecords();
    } catch (err: any) {
      setError(err.message || '재무 기록 저장에 실패했습니다.');
    }
  };

  // 재무 기록 삭제
  const handleDeleteRecord = async () => {
    if (!selectedRecord) return;
    
    try {
      await FinancialService.deleteFinancialRecord(selectedRecord.id);
      setOpenDelete(false);
      setSelectedRecord(null);
      fetchRecords();
    } catch (err: any) {
      setError(err.message || '재무 기록 삭제에 실패했습니다.');
    }
  };

  // 재무 기록 상세 보기
  const handleViewRecord = (record: FinancialRecord) => {
    setSelectedRecord(record);
    setOpenDetail(true);
  };

  // 재무 기록 수정
  const handleEditRecord = (record: FinancialRecord) => {
    setEditingRecord(record);
    setOpenForm(true);
  };

  // 재무 기록 삭제 확인
  const handleDeleteClick = (record: FinancialRecord) => {
    setSelectedRecord(record);
    setOpenDelete(true);
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
          재무 관리
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenForm(true)}
        >
          새 {currentType} 등록
        </Button>
      </Box>

      {/* 탭 */}
      <Card sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="재무 관리 탭">
          <Tab 
            icon={<TrendingUpIcon />} 
            label="수입" 
            iconPosition="start"
          />
          <Tab 
            icon={<TrendingDownIcon />} 
            label="지출" 
            iconPosition="start"
          />
        </Tabs>
      </Card>

      {/* 검색 및 필터 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <form onSubmit={handleSearch}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="검색"
                  placeholder="설명, 카테고리로 검색"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  InputProps={{
                    startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                  }}
                />
              </Grid>
              <Grid item xs={12} md={3}>
                <FormControl fullWidth>
                  <InputLabel>카테고리</InputLabel>
                  <Select
                    value={categoryFilter}
                    label="카테고리"
                    onChange={(e) => setCategoryFilter(e.target.value)}
                  >
                    <MenuItem value="">전체</MenuItem>
                    <MenuItem value="자재비">자재비</MenuItem>
                    <MenuItem value="노무비">노무비</MenuItem>
                    <MenuItem value="경비">경비</MenuItem>
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
                  onClick={fetchRecords}
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

      {/* 재무 기록 목록 테이블 */}
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
                      <TableCell>날짜</TableCell>
                      <TableCell>카테고리</TableCell>
                      <TableCell>설명</TableCell>
                      <TableCell align="right">금액</TableCell>
                      <TableCell>결제방식</TableCell>
                      <TableCell align="center">작업</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {records.map((record) => (
                      <TableRow key={record.id} hover>
                        <TableCell>{formatDate(record.date)}</TableCell>
                        <TableCell>
                          <Chip
                            label={record.category}
                            size="small"
                            color="primary"
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell>{record.description}</TableCell>
                        <TableCell align="right">
                          <Typography
                            color={record.type === '수입' ? 'success.main' : 'error.main'}
                            fontWeight="bold"
                          >
                            {record.type === '수입' ? '+' : '-'}
                            {formatAmount(record.amount)}원
                          </Typography>
                        </TableCell>
                        <TableCell>{record.paymentMethod}</TableCell>
                        <TableCell align="center">
                          <IconButton
                            size="small"
                            onClick={() => handleViewRecord(record)}
                            title="상세보기"
                          >
                            <ViewIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleEditRecord(record)}
                            title="수정"
                          >
                            <EditIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDeleteClick(record)}
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
              {records.length === 0 && !loading && (
                <Box sx={{ textAlign: 'center', p: 3 }}>
                  <Typography variant="body2" color="text.secondary">
                    {currentType} 기록이 없습니다.
                  </Typography>
                </Box>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {/* 재무 기록 생성/수정 폼 다이얼로그 */}
      <Dialog
        open={openForm}
        onClose={() => {
          setOpenForm(false);
          setEditingRecord(null);
        }}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {editingRecord ? `${currentType} 수정` : `새 ${currentType} 등록`}
        </DialogTitle>
        <DialogContent>
          <FinancialForm
            record={editingRecord}
            type={currentType as FinancialType}
            onSave={handleSaveRecord}
            onCancel={() => {
              setOpenForm(false);
              setEditingRecord(null);
            }}
          />
        </DialogContent>
      </Dialog>

      {/* 재무 기록 상세 보기 다이얼로그 */}
      <Dialog
        open={openDetail}
        onClose={() => setOpenDetail(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>{currentType} 상세 정보</DialogTitle>
        <DialogContent>
          {selectedRecord && (
            <FinancialDetail
              record={selectedRecord}
              onEdit={() => {
                setOpenDetail(false);
                handleEditRecord(selectedRecord);
              }}
            />
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDetail(false)}>닫기</Button>
        </DialogActions>
      </Dialog>

      {/* 삭제 확인 다이얼로그 */}
      <Dialog open={openDelete} onClose={() => setOpenDelete(false)}>
        <DialogTitle>{currentType} 삭제</DialogTitle>
        <DialogContent>
          <Typography>
            정말로 "{selectedRecord?.description}" {currentType}을 삭제하시겠습니까?
            <br />
            이 작업은 되돌릴 수 없습니다.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDelete(false)}>취소</Button>
          <Button onClick={handleDeleteRecord} color="error" variant="contained">
            삭제
          </Button>
        </DialogActions>
      </Dialog>

      {/* 플로팅 액션 버튼 */}
      <Tooltip title={`새 ${currentType} 등록`}>
        <Fab
          color="primary"
          sx={{ position: 'fixed', bottom: 16, right: 16 }}
          onClick={() => setOpenForm(true)}
        >
          <AddIcon />
        </Fab>
      </Tooltip>
    </Box>
  );
};

export default FinancialList; 