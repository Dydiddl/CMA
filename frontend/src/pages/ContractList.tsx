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
} from '@mui/material';
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as ViewIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Refresh as RefreshIcon,
} from '@mui/icons-material';
import { ContractForm } from '../components/contract/ContractForm';
import { ContractDetail } from '../components/contract/ContractDetail';
import { ContractService } from '../services/contractService';
import { Contract, ContractStatus } from '../types/contract';

const ContractList: React.FC = () => {
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  
  // 다이얼로그 상태
  const [openForm, setOpenForm] = useState(false);
  const [openDetail, setOpenDetail] = useState(false);
  const [openDelete, setOpenDelete] = useState(false);
  const [selectedContract, setSelectedContract] = useState<Contract | null>(null);
  const [editingContract, setEditingContract] = useState<Contract | null>(null);

  // 계약 목록 조회
  const fetchContracts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await ContractService.getContracts({
        page,
        size,
        search: search || undefined,
        status: statusFilter || undefined,
      });
      
      if (response.status === 'success') {
        setContracts(response.data);
        setTotal(response.total);
      } else {
        setError(response.message || '계약 목록을 불러오는데 실패했습니다.');
      }
    } catch (err: any) {
      setError(err.message || '계약 목록을 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  }, [page, size, search, statusFilter]);

  // 초기 로드
  useEffect(() => {
    fetchContracts();
  }, [fetchContracts]);

  // 검색 처리
  const handleSearch = (event: React.FormEvent) => {
    event.preventDefault();
    setPage(1);
    fetchContracts();
  };

  // 필터 초기화
  const handleClearFilters = () => {
    setSearch('');
    setStatusFilter('');
    setPage(1);
  };

  // 계약 생성/수정
  const handleSaveContract = async (contractData: any) => {
    try {
      if (editingContract) {
        await ContractService.updateContract(editingContract.id, contractData);
      } else {
        await ContractService.createContract(contractData);
      }
      
      setOpenForm(false);
      setEditingContract(null);
      fetchContracts();
    } catch (err: any) {
      setError(err.message || '계약 저장에 실패했습니다.');
    }
  };

  // 계약 삭제
  const handleDeleteContract = async () => {
    if (!selectedContract) return;
    
    try {
      await ContractService.deleteContract(selectedContract.id);
      setOpenDelete(false);
      setSelectedContract(null);
      fetchContracts();
    } catch (err: any) {
      setError(err.message || '계약 삭제에 실패했습니다.');
    }
  };

  // 계약 상세 보기
  const handleViewContract = (contract: Contract) => {
    setSelectedContract(contract);
    setOpenDetail(true);
  };

  // 계약 수정
  const handleEditContract = (contract: Contract) => {
    setEditingContract(contract);
    setOpenForm(true);
  };

  // 계약 삭제 확인
  const handleDeleteClick = (contract: Contract) => {
    setSelectedContract(contract);
    setOpenDelete(true);
  };

  // 상태별 색상
  const getStatusColor = (status: ContractStatus) => {
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

  // 금액 포맷팅
  const formatAmount = (amount: number) => {
    return new Intl.NumberFormat('ko-KR').format(amount);
  };

  return (
    <Box sx={{ p: 3 }}>
      {/* 헤더 */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          계약 관리
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setOpenForm(true)}
        >
          새 계약
        </Button>
      </Box>

      {/* 검색 및 필터 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <form onSubmit={handleSearch}>
            <Grid container spacing={2} alignItems="center">
              <Grid item xs={12} md={4}>
                <TextField
                  fullWidth
                  label="검색"
                  placeholder="계약명, 계약번호, 발주처명으로 검색"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  InputProps={{
                    startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
                  }}
                />
              </Grid>
              <Grid item xs={12} md={3}>
                <FormControl fullWidth>
                  <InputLabel>상태</InputLabel>
                  <Select
                    value={statusFilter}
                    label="상태"
                    onChange={(e) => setStatusFilter(e.target.value)}
                  >
                    <MenuItem value="">전체</MenuItem>
                    <MenuItem value="진행중">진행중</MenuItem>
                    <MenuItem value="완료">완료</MenuItem>
                    <MenuItem value="중단">중단</MenuItem>
                    <MenuItem value="취소">취소</MenuItem>
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
                  onClick={fetchContracts}
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

      {/* 계약 목록 테이블 */}
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
                      <TableCell>계약번호</TableCell>
                      <TableCell>계약명</TableCell>
                      <TableCell>발주처</TableCell>
                      <TableCell align="right">계약금액</TableCell>
                      <TableCell>계약일</TableCell>
                      <TableCell>상태</TableCell>
                      <TableCell align="center">작업</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {contracts.map((contract) => (
                      <TableRow key={contract.id} hover>
                        <TableCell>{contract.contractNumber}</TableCell>
                        <TableCell>{contract.name}</TableCell>
                        <TableCell>{contract.clientName}</TableCell>
                        <TableCell align="right">
                          {formatAmount(contract.contractAmount)}원
                        </TableCell>
                        <TableCell>
                          {new Date(contract.contractDate).toLocaleDateString('ko-KR')}
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={contract.status}
                            color={getStatusColor(contract.status) as any}
                            size="small"
                          />
                        </TableCell>
                        <TableCell align="center">
                          <IconButton
                            size="small"
                            onClick={() => handleViewContract(contract)}
                            title="상세보기"
                          >
                            <ViewIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleEditContract(contract)}
                            title="수정"
                          >
                            <EditIcon />
                          </IconButton>
                          <IconButton
                            size="small"
                            onClick={() => handleDeleteClick(contract)}
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
              {contracts.length === 0 && !loading && (
                <Box sx={{ textAlign: 'center', p: 3 }}>
                  <Typography variant="body2" color="text.secondary">
                    계약이 없습니다.
                  </Typography>
                </Box>
              )}
            </>
          )}
        </CardContent>
      </Card>

      {/* 계약 생성/수정 폼 다이얼로그 */}
      <Dialog
        open={openForm}
        onClose={() => {
          setOpenForm(false);
          setEditingContract(null);
        }}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {editingContract ? '계약 수정' : '새 계약 등록'}
        </DialogTitle>
        <DialogContent>
          <ContractForm
            contract={editingContract}
            onSave={handleSaveContract}
            onCancel={() => {
              setOpenForm(false);
              setEditingContract(null);
            }}
          />
        </DialogContent>
      </Dialog>

      {/* 계약 상세 보기 다이얼로그 */}
      <Dialog
        open={openDetail}
        onClose={() => setOpenDetail(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>계약 상세 정보</DialogTitle>
        <DialogContent>
          {selectedContract && (
            <ContractDetail
              contract={selectedContract}
              onEdit={() => {
                setOpenDetail(false);
                handleEditContract(selectedContract);
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
        <DialogTitle>계약 삭제</DialogTitle>
        <DialogContent>
          <Typography>
            정말로 "{selectedContract?.name}" 계약을 삭제하시겠습니까?
            <br />
            이 작업은 되돌릴 수 없습니다.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDelete(false)}>취소</Button>
          <Button onClick={handleDeleteContract} color="error" variant="contained">
            삭제
          </Button>
        </DialogActions>
      </Dialog>

      {/* 플로팅 액션 버튼 */}
      <Tooltip title="새 계약 등록">
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

export default ContractList; 