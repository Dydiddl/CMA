import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Chip,
  Button,
  LinearProgress,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Add as AddIcon,
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  Person as PersonIcon,
} from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { Task } from '../types/task';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
}));

const CommentCard = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const TaskDetail: React.FC = () => {
  const navigate = useNavigate();
  const { taskId } = useParams<{ taskId: string }>();

  // 임시 데이터
  const task: Task = {
    id: 1,
    name: '기초 공사',
    description: '건물 기초 공사 진행',
    status: 'IN_PROGRESS',
    progress: 75,
    startDate: '2024-01-01',
    endDate: '2024-02-28',
    projectId: 1,
    assignee: '홍길동',
    priority: 'HIGH',
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-15T00:00:00Z',
  };

  const comments = [
    {
      id: 1,
      content: '기초 공사 시작했습니다.',
      author: '홍길동',
      createdAt: '2024-01-01T10:00:00Z',
    },
    {
      id: 2,
      content: '진행 상황을 확인했습니다.',
      author: '김철수',
      createdAt: '2024-01-02T14:30:00Z',
    },
  ];

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

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return 'error';
      case 'MEDIUM':
        return 'warning';
      case 'LOW':
        return 'success';
      default:
        return 'default';
    }
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return '높음';
      case 'MEDIUM':
        return '중간';
      case 'LOW':
        return '낮음';
      default:
        return priority;
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">{task.name}</Typography>
        <Box>
          <Button
            variant="outlined"
            startIcon={<EditIcon />}
            onClick={() => navigate(`/tasks/${taskId}/edit`)}
            sx={{ mr: 1 }}
          >
            수정
          </Button>
          <Button
            variant="outlined"
            color="error"
            startIcon={<DeleteIcon />}
            onClick={() => {
              // 삭제 로직
            }}
          >
            삭제
          </Button>
        </Box>
      </Box>

      <StyledPaper>
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Typography variant="h6" gutterBottom>
              작업 정보
            </Typography>
            <Typography color="text.secondary" paragraph>
              {task.description}
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Chip
                label={getStatusLabel(task.status)}
                color={getStatusColor(task.status)}
                sx={{ mr: 1 }}
              />
              <Chip
                label={getPriorityLabel(task.priority)}
                color={getPriorityColor(task.priority)}
              />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                진행률: {task.progress}%
              </Typography>
              <LinearProgress
                variant="determinate"
                value={task.progress}
                sx={{ mt: 1 }}
              />
            </Box>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom>
              기본 정보
            </Typography>
            <List>
              <ListItem>
                <ListItemIcon>
                  <ScheduleIcon />
                </ListItemIcon>
                <ListItemText
                  primary="시작일"
                  secondary={task.startDate}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <ScheduleIcon />
                </ListItemIcon>
                <ListItemText
                  primary="종료일"
                  secondary={task.endDate}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <PersonIcon />
                </ListItemIcon>
                <ListItemText
                  primary="담당자"
                  secondary={task.assignee}
                />
              </ListItem>
            </List>
          </Grid>
        </Grid>
      </StyledPaper>

      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h5">댓글</Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => {
            // 댓글 추가 로직
          }}
        >
          댓글 작성
        </Button>
      </Box>

      {comments.map((comment) => (
        <CommentCard key={comment.id}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="subtitle1">{comment.author}</Typography>
            <Typography variant="body2" color="text.secondary">
              {new Date(comment.createdAt).toLocaleString()}
            </Typography>
          </Box>
          <Typography color="text.secondary">
            {comment.content}
          </Typography>
        </CommentCard>
      ))}
    </Box>
  );
};

export default TaskDetail; 