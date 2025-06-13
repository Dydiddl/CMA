import React from 'react';
import { List, ListItem, ListItemIcon, ListItemText, ListItemButton, Divider } from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Dashboard as DashboardIcon,
  Assignment as ProjectIcon,
  Task as TaskIcon,
  Assessment as ReportIcon,
  Settings as SettingsIcon,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const StyledListItem = styled(ListItemButton)(({ theme }) => ({
  '&.Mui-selected': {
    backgroundColor: theme.palette.primary.main,
    '&:hover': {
      backgroundColor: theme.palette.primary.dark,
    },
    '& .MuiListItemIcon-root': {
      color: theme.palette.common.white,
    },
    '& .MuiListItemText-primary': {
      color: theme.palette.common.white,
    },
  },
  '&:hover': {
    backgroundColor: theme.palette.action.hover,
  },
}));

const menuItems = [
  { text: '대시보드', icon: <DashboardIcon />, path: '/' },
  { text: '프로젝트', icon: <ProjectIcon />, path: '/projects' },
  { text: '작업', icon: <TaskIcon />, path: '/tasks' },
  { text: '보고서', icon: <ReportIcon />, path: '/reports' },
];

export const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <List>
      {menuItems.map((item) => (
        <ListItem key={item.text} disablePadding>
          <StyledListItem
            selected={location.pathname === item.path}
            onClick={() => navigate(item.path)}
          >
            <ListItemIcon sx={{ minWidth: 40 }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} />
          </StyledListItem>
        </ListItem>
      ))}
      <Divider sx={{ my: 1 }} />
      <ListItem disablePadding>
        <StyledListItem
          selected={location.pathname === '/settings'}
          onClick={() => navigate('/settings')}
        >
          <ListItemIcon sx={{ minWidth: 40 }}>
            <SettingsIcon />
          </ListItemIcon>
          <ListItemText primary="설정" />
        </StyledListItem>
      </ListItem>
    </List>
  );
}; 