import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Button,
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  IconButton,
  LinearProgress,
} from '@mui/material';
import { Add as AddIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useProject } from '../contexts/ProjectContext';
import LoadingSpinner from '../components/common/LoadingSpinner';
import TaskList from '../components/task/TaskList';
import TaskForm from '../components/task/TaskForm';
import { styled } from '@mui/material/styles';
import { Task } from '../types/task';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
}));

const TaskCard = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
  '&:hover': {
    backgroundColor: theme.palette.action.hover,
    cursor: 'pointer',
  },
}));

const ProjectDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { state, getProject, updateProject, deleteProject } = useProject();
  const [isTaskFormOpen, setIsTaskFormOpen] = useState(false);

  useEffect(() => {
    if (id) {
      getProject(id);
    }
  }, [id, getProject]);

  if (state.loading) {
    return <LoadingSpinner message="프로젝트 정보를 불러오는 중..." />;
  }

  const project = state.currentProject;
  if (!project) {
    return <Typography>프로젝트를 찾을 수 없습니다.</Typography>;
  }

  const handleDelete = async () => {
    if (window.confirm('정말로 이 프로젝트를 삭제하시겠습니까?')) {
      await deleteProject(project.id);
      navigate('/projects');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case '진행중':
        return 'primary';
      case '완료':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case '진행중':
        return '진행중';
      case '완료':
        return '완료';
      default:
        return status;
    }
  };

  const tasks: Task[] = [
    {
      id: 1,
      name: '기초 공사',
      description: '건물 기초 공사 진행',
      status: 'IN_PROGRESS',
      progress: 75,
      startDate: '2024-01-01',
      endDate: '2024-02-28',
      projectId: 1,
    },
    {
      id: 2,
      name: '철근 작업',
      description: '철근 배치 및 설치',
      status: 'TODO',
      progress: 0,
      startDate: '2024-03-01',
      endDate: '2024-03-15',
      projectId: 1,
    },
  ];

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h4">{project.name}</Typography>
            <Box>
              <Button
                variant="outlined"
                startIcon={<EditIcon />}
                onClick={() => navigate(`/projects/${id}/edit`)}
                sx={{ mr: 1 }}
              >
                수정
              </Button>
              <Button
                variant="outlined"
                color="error"
                startIcon={<DeleteIcon />}
                onClick={handleDelete}
              >
                삭제
              </Button>
            </Box>
          </Box>
          <Chip
            label={getStatusLabel(project.status)}
            color={getStatusColor(project.status)}
            sx={{ mb: 2 }}
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              프로젝트 정보
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="시작일"
                  secondary={new Date(project.startDate).toLocaleDateString()}
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="종료일"
                  secondary={new Date(project.endDate).toLocaleDateString()}
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="담당자"
                  secondary={project.manager}
                />
              </ListItem>
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              프로젝트 설명
            </Typography>
            <Typography>{project.description}</Typography>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">작업 목록</Typography>
              <Button
                variant="contained"
                startIcon={<AddIcon />}
                onClick={() => setIsTaskFormOpen(true)}
              >
                작업 추가
              </Button>
            </Box>
            <TaskList projectId={project.id} />
          </Paper>
        </Grid>
      </Grid>

      <TaskForm
        open={isTaskFormOpen}
        onClose={() => setIsTaskFormOpen(false)}
        projectId={project.id}
      />
    </Box>
  );
};

export default ProjectDetail; 