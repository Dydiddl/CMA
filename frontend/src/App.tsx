import React, { Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import theme from './theme';
import { UserProvider } from './contexts/UserContext';
import { ProjectProvider } from './contexts/ProjectContext';
import { TaskProvider } from './contexts/TaskContext';
import LoadingSpinner from './components/common/LoadingSpinner';
import { Layout } from './components/layout/Layout';
import { useState } from 'react'
import { MantineProvider, AppShell, Text, Button } from '@mantine/core'

// Lazy load components
const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const ProjectList = React.lazy(() => import('./pages/ProjectList'));
const ProjectDetail = React.lazy(() => import('./pages/ProjectDetail'));
const TaskList = React.lazy(() => import('./pages/TaskList'));
const TaskDetail = React.lazy(() => import('./pages/TaskDetail'));
const Login = React.lazy(() => import('./pages/Login'));
const Register = React.lazy(() => import('./pages/Register'));
const NotFound = React.lazy(() => import('./pages/NotFound'));

const App: React.FC = () => {
  const [count, setCount] = useState(0)

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <UserProvider>
        <ProjectProvider>
          <TaskProvider>
            <Suspense fallback={<LoadingSpinner message="페이지를 불러오는 중..." />}>
              <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route element={<Layout />}>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/projects" element={<ProjectList />} />
                  <Route path="/projects/:id" element={<ProjectDetail />} />
                  <Route path="/tasks" element={<TaskList />} />
                  <Route path="/tasks/:id" element={<TaskDetail />} />
                  <Route path="*" element={<NotFound />} />
                </Route>
              </Routes>
            </Suspense>
          </TaskProvider>
        </ProjectProvider>
      </UserProvider>
      <MantineProvider>
        <AppShell
          padding="md"
          header={{ height: 60, collapsed: false }}
        >
          <AppShell.Header>
            <Text size="xl" fw={700}>건설 관리 시스템</Text>
          </AppShell.Header>
          <AppShell.Main>
            <div style={{ padding: 20 }}>
              <h1>실시간 미리보기 테스트</h1>
              <Button onClick={() => setCount(count + 1)} color="blue" style={{ marginTop: 20 }}>
                카운트: {count}
              </Button>
              <Text mt="md">
                이 텍스트를 수정하면 실시간으로 변경사항을 확인할 수 있습니다!
              </Text>
            </div>
          </AppShell.Main>
        </AppShell>
      </MantineProvider>
    </ThemeProvider>
  );
};

export default App;
