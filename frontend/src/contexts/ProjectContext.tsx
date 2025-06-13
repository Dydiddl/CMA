import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { Project, CreateProjectDto, UpdateProjectDto } from '../services/projectService';
import projectService from '../services/projectService';

interface ProjectState {
  projects: Project[];
  loading: boolean;
  error: string | null;
}

type ProjectAction =
  | { type: 'SET_PROJECTS'; payload: Project[] }
  | { type: 'ADD_PROJECT'; payload: Project }
  | { type: 'UPDATE_PROJECT'; payload: Project }
  | { type: 'DELETE_PROJECT'; payload: number }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null };

const initialState: ProjectState = {
  projects: [],
  loading: false,
  error: null,
};

const ProjectContext = createContext<{
  state: ProjectState;
  fetchProjects: () => Promise<void>;
  createProject: (project: CreateProjectDto) => Promise<void>;
  updateProject: (id: number, project: UpdateProjectDto) => Promise<void>;
  deleteProject: (id: number) => Promise<void>;
} | null>(null);

const projectReducer = (state: ProjectState, action: ProjectAction): ProjectState => {
  switch (action.type) {
    case 'SET_PROJECTS':
      return { ...state, projects: action.payload, loading: false, error: null };
    case 'ADD_PROJECT':
      return { ...state, projects: [...state.projects, action.payload] };
    case 'UPDATE_PROJECT':
      return {
        ...state,
        projects: state.projects.map((project) =>
          project.id === action.payload.id ? action.payload : project
        ),
      };
    case 'DELETE_PROJECT':
      return {
        ...state,
        projects: state.projects.filter((project) => project.id !== action.payload),
      };
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
};

export const ProjectProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(projectReducer, initialState);

  const fetchProjects = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const projects = await projectService.getProjects();
      dispatch({ type: 'SET_PROJECTS', payload: projects });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '프로젝트 목록을 불러오는데 실패했습니다.' });
    }
  };

  const createProject = async (project: CreateProjectDto) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const newProject = await projectService.createProject(project);
      dispatch({ type: 'ADD_PROJECT', payload: newProject });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '프로젝트 생성에 실패했습니다.' });
    }
  };

  const updateProject = async (id: number, project: UpdateProjectDto) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const updatedProject = await projectService.updateProject(id, project);
      dispatch({ type: 'UPDATE_PROJECT', payload: updatedProject });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '프로젝트 수정에 실패했습니다.' });
    }
  };

  const deleteProject = async (id: number) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      await projectService.deleteProject(id);
      dispatch({ type: 'DELETE_PROJECT', payload: id });
    } catch (error) {
      dispatch({ type: 'SET_ERROR', payload: '프로젝트 삭제에 실패했습니다.' });
    }
  };

  return (
    <ProjectContext.Provider
      value={{
        state,
        fetchProjects,
        createProject,
        updateProject,
        deleteProject,
      }}
    >
      {children}
    </ProjectContext.Provider>
  );
};

export const useProject = () => {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error('useProject must be used within a ProjectProvider');
  }
  return context;
}; 