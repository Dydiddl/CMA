import React, { useEffect, useState } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Box,
  Typography,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon } from '@mui/icons-material';
import { useTask } from '../../contexts/TaskContext';
import LoadingSpinner from '../common/LoadingSpinner';

interface TaskListProps {
  projectId: string;
}

const TaskList: React.FC<TaskListProps> = ({ projectId }) => {
  const { state, fetchTasks, deleteTask } = useTask();
  const [tasks, setTasks] = useState<Task[]>([]);

  useEffect(() => {
    fetchTasks(projectId);
  }, [projectId, fetchTasks]);

  useEffect(() => {
    setTasks(state.tasks);
  }, [state.tasks]);

  if (state.loading) {
    return <LoadingSpinner message="작업 목록을 불러오는 중..." />;
  }

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

  const handleDelete = async (taskId: string) => {
    if (window.confirm('정말로 이 작업을 삭제하시겠습니까?')) {
      await deleteTask(taskId);
    }
  };

  if (tasks.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 3 }}>
        <Typography color="textSecondary">등록된 작업이 없습니다.</Typography>
      </Box>
    );
  }

  return (
    <List>
      {tasks.map((task) => (
        <ListItem
          key={task.id}
          sx={{
            border: '1px solid',
            borderColor: 'divider',
            borderRadius: 1,
            mb: 1,
          }}
        >
          <ListItemText
            primary={task.title}
            secondary={
              <Box sx={{ mt: 1 }}>
                <Typography variant="body2" color="textSecondary">
                  {task.description}
                </Typography>
                <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                  <Chip
                    label={task.status}
                    size="small"
                    color={getStatusColor(task.status)}
                  />
                  <Chip
                    label={`담당자: ${task.assignee}`}
                    size="small"
                    variant="outlined"
                  />
                  <Chip
                    label={`기한: ${new Date(task.dueDate).toLocaleDateString()}`}
                    size="small"
                    variant="outlined"
                  />
                </Box>
              </Box>
            }
          />
          <ListItemSecondaryAction>
            <IconButton
              edge="end"
              aria-label="edit"
              onClick={() => {/* TODO: 작업 수정 기능 구현 */}}
              sx={{ mr: 1 }}
            >
              <EditIcon />
            </IconButton>
            <IconButton
              edge="end"
              aria-label="delete"
              onClick={() => handleDelete(task.id)}
            >
              <DeleteIcon />
            </IconButton>
          </ListItemSecondaryAction>
        </ListItem>
      ))}
    </List>
  );
};

export default TaskList; 