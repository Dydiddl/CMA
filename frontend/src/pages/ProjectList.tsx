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
  IconButton,
  Chip,
  Stack,
} from '@mui/material';
import { Add as AddIcon, Search as SearchIcon, FilterList as FilterListIcon, Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { Project } from '../types';
import { getProjects } from '../services/api';
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

// 메모이제이션된 프로젝트 카드 컴포넌트
const ProjectCard = React.memo(({ project, onClick }: { project: Project; onClick: () => void }) => {
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
      case 'COMPLETED':
        return 'success';
      case 'PLANNING':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'IN_PROGRESS':
        return '진행중';
      case 'COMPLETED':
        return '완료';
      case 'PLANNING':
        return '계획';
      default:
        return status;
    }
  };

  return (
    <StyledCard onClick={onClick}>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" component="div">
            {project.name}
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
          {project.description}
        </Typography>
        <Box sx={{ mt: 2 }}>
          <StatusChip
            label={getStatusLabel(project.status)}
            color={getStatusColor(project.status)}
            size="small"
          />
          <Typography variant="body2" color="text.secondary">
            진행률: {project.progress}%
          </Typography>
        </Box>
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" color="text.secondary">
            시작일: {formatDate(project.startDate)}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            종료일: {formatDate(project.endDate)}
          </Typography>
        </Box>
      </CardContent>
    </StyledCard>
  );
});

ProjectCard.displayName = 'ProjectCard';

const ProjectList: React.FC = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterOpen, setFilterOpen] = useState(false);

  useEffect(() => {
    const fetchProjects = async () => {
      try {
        setLoading(true);
        const data = await getProjects();
        setProjects(data);
      } catch (err) {
        setError('프로젝트 목록을 불러오는데 실패했습니다');
      } finally {
        setLoading(false);
      }
    };

    fetchProjects();
  }, []);

  const handleProjectClick = useCallback((projectId: number) => {
    navigate(`/projects/${projectId}`);
  }, [navigate]);

  const handleSearch = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  }, []);

  const filteredProjects = useMemo(() => {
    return projects.filter((project) =>
      project.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [projects, searchTerm]);

  if (loading) {
    return <LoadingSpinner message="프로젝트 목록을 불러오는 중..." />;
  }

  if (error) {
    return <ErrorMessage message={error} />;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4 }}>
        <Typography variant="h4" component="h1">
          프로젝트 목록
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => navigate('/projects/new')}
        >
          새 프로젝트
        </Button>
      </Box>

      <Box sx={{ mb: 4 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6}>
            <TextField
              fullWidth
              placeholder="프로젝트 검색..."
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
        {filteredProjects.map((project) => (
          <ProjectCard
            key={project.id}
            project={project}
            onClick={() => handleProjectClick(project.id)}
          />
        ))}
      </Box>
    </Container>
  );
};

export default ProjectList; 