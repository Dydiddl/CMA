import React, { useState, useEffect, useMemo, useCallback } from 'react';
import {
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Box,
  TextField,
  InputAdornment,
  Chip,
  Stack,
  IconButton,
  LinearProgress,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  FilterList as FilterListIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { Task } from '../types/task';
import { getTasks } from '../services/taskService';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorMessage from '../components/common/ErrorMessage';
import { styled } from '@mui/material/styles';

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  transition: 'transform 0.2s',
  '&:hover': {
    transform: 'translateY(-4px)',
    cursor: 'pointer',
  },
}));

const StatusChip = styled(Chip)(({ theme }) => ({
  marginRight: theme.spacing(1),
}));

// 메모이제이션된 태스크 카드 컴포넌트
const TaskCard = React.memo(({ task, onClick }: { task: Task; onClick: () => void }) => {
  const formatDate = useCallback((dateString: string | undefined): string => {
    if (!dateString) return '날짜 미정';
    const date = new Date(dateString);
    return date.toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'IN_PROGRESS':
        return 'primary';
      case 'DONE':
        return 'success';
      case 'TODO':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'IN_PROGRESS':
        return '진행중';
      case 'DONE':
        return '완료';
      case 'TODO':
        return '대기중';
      default:
        return status;
    }
  };

  return (
    <StyledCard onClick={onClick}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" component="div">
            {task.name}
          </Typography>
          <Box>
            <IconButton size="small" onClick={(e) => {
              e.stopPropagation();
              // 수정 로직
            }}>
              <EditIcon />
            </IconButton>
            <IconButton size="small" onClick={(e) => {
              e.stopPropagation();
              // 삭제 로직
            }}>
              <DeleteIcon />
            </IconButton>
          </Box>
        </Box>
        <Typography color="text.secondary" gutterBottom>
          {task.description}
        </Typography>
        <Box sx={{ mt: 2 }}>
          <StatusChip
            label={getStatusLabel(task.status)}
            color={getStatusColor(task.status)}
            size="small"
          />
          <Typography variant="body2" color="text.secondary">
            진행률: {task.progress}%
          </Typography>
          <LinearProgress
            variant="determinate"
            value={task.progress}
            sx={{ mt: 1 }}
          />
        </Box>
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" color="text.secondary">
            시작일: {formatDate(task.startDate)}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            종료일: {formatDate(task.endDate)}
          </Typography>
        </Box>
      </CardContent>
    </StyledCard>
  );
});

TaskCard.displayName = 'TaskCard';

interface TaskListProps {
  projectId?: number;
}

const TaskList: React.FC<TaskListProps> = ({ projectId }) => {
  const navigate = useNavigate();
  const { projectId: urlProjectId } = useParams<{ projectId: string }>();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterOpen, setFilterOpen] = useState(false);

  const effectiveProjectId = useMemo(() => {
    return projectId || (urlProjectId ? parseInt(urlProjectId, 10) : undefined);
  }, [projectId, urlProjectId]);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        setLoading(true);
        const data = await getTasks(effectiveProjectId);
        setTasks(data);
      } catch (err) {
        setError('태스크 목록을 불러오는데 실패했습니다');
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [effectiveProjectId]);

  const handleTaskClick = useCallback((taskId: number) => {
    navigate(`/tasks/${taskId}`);
  }, [navigate]);

  const handleSearch = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  }, []);

  const filteredTasks = useMemo(() => {
    return tasks.filter((task) =>
      task.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [tasks, searchTerm]);

  if (loading) {
    return <LoadingSpinner message="태스크 목록을 불러오는 중..." />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        <Typography variant="h4" component="h1">
          태스크 목록
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => navigate('/tasks/new')}
        >
          새 태스크
        </Button>
      </Box>

      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              placeholder="태스크 검색..."
              value={searchTerm}
              onChange={handleSearch}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon />
                  </InputAdornment>
                ),
              }}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Button
                startIcon={<FilterListIcon />}
                onClick={() => setFilterOpen(!filterOpen)}
              >
                필터
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Box>

      <Box sx={{ display: 'grid', gap: 3, gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)', lg: 'repeat(3, 1fr)' } }}>
        {filteredTasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onClick={() => handleTaskClick(task.id)}
          />
        ))}
      </Box>
    </Container>
  );
};

export default TaskList; 