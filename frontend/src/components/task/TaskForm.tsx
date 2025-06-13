import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
} from '@mui/material';
import { useTask } from '../../contexts/TaskContext';

interface TaskFormProps {
  open: boolean;
  onClose: () => void;
  projectId: string;
  task?: Task;
}

const TaskForm: React.FC<TaskFormProps> = ({ open, onClose, projectId, task }) => {
  const { createTask, updateTask } = useTask();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: '대기중',
    assignee: '',
    dueDate: '',
  });

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description,
        status: task.status,
        assignee: task.assignee,
        dueDate: task.dueDate,
      });
    } else {
      setFormData({
        title: '',
        description: '',
        status: '대기중',
        assignee: '',
        dueDate: '',
      });
    }
  }, [task]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name as string]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (task) {
        await updateTask(task.id, formData);
      } else {
        await createTask({ ...formData, projectId });
      }
      onClose();
    } catch (error) {
      console.error('작업 저장 중 오류 발생:', error);
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit}>
        <DialogTitle>{task ? '작업 수정' : '새 작업 추가'}</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, pt: 1 }}>
            <TextField
              name="title"
              label="제목"
              value={formData.title}
              onChange={handleChange}
              required
              fullWidth
            />
            <TextField
              name="description"
              label="설명"
              value={formData.description}
              onChange={handleChange}
              multiline
              rows={4}
              fullWidth
            />
            <FormControl fullWidth>
              <InputLabel>상태</InputLabel>
              <Select
                name="status"
                value={formData.status}
                onChange={handleChange}
                label="상태"
              >
                <MenuItem value="대기중">대기중</MenuItem>
                <MenuItem value="진행중">진행중</MenuItem>
                <MenuItem value="완료">완료</MenuItem>
              </Select>
            </FormControl>
            <TextField
              name="assignee"
              label="담당자"
              value={formData.assignee}
              onChange={handleChange}
              required
              fullWidth
            />
            <TextField
              name="dueDate"
              label="기한"
              type="date"
              value={formData.dueDate}
              onChange={handleChange}
              required
              fullWidth
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>취소</Button>
          <Button type="submit" variant="contained">
            {task ? '수정' : '추가'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default TaskForm; 