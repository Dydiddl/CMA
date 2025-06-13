import { create } from 'zustand';
import { Project, ProjectFormData } from '../types/project';
import { projectService } from '../services/projectService';

interface ProjectState {
  projects: Project[];
  selectedProject: Project | null;
  loading: boolean;
  error: string | null;
  fetchProjects: () => Promise<void>;
  fetchProject: (id: number) => Promise<void>;
  createProject: (project: ProjectFormData) => Promise<void>;
  updateProject: (id: number, project: ProjectFormData) => Promise<void>;
  deleteProject: (id: number) => Promise<void>;
  setSelectedProject: (project: Project | null) => void;
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  projects: [],
  selectedProject: null,
  loading: false,
  error: null,

  fetchProjects: async () => {
    try {
      set({ loading: true, error: null });
      const projects = await projectService.getProjects();
      set({ projects, loading: false });
    } catch (error) {
      set({ error: '프로젝트 목록을 불러오는데 실패했습니다', loading: false });
    }
  },

  fetchProject: async (id: number) => {
    try {
      set({ loading: true, error: null });
      const project = await projectService.getProject(id);
      set({ selectedProject: project, loading: false });
    } catch (error) {
      set({ error: '프로젝트를 불러오는데 실패했습니다', loading: false });
    }
  },

  createProject: async (projectData: ProjectFormData) => {
    try {
      set({ loading: true, error: null });
      const newProject = await projectService.createProject(projectData);
      set((state) => ({
        projects: [...state.projects, newProject],
        loading: false,
      }));
    } catch (error) {
      set({ error: '프로젝트 생성에 실패했습니다', loading: false });
    }
  },

  updateProject: async (id: number, projectData: ProjectFormData) => {
    try {
      set({ loading: true, error: null });
      const updatedProject = await projectService.updateProject(id, projectData);
      set((state) => ({
        projects: state.projects.map((p) =>
          p.id === id ? updatedProject : p
        ),
        selectedProject: state.selectedProject?.id === id ? updatedProject : state.selectedProject,
        loading: false,
      }));
    } catch (error) {
      set({ error: '프로젝트 수정에 실패했습니다', loading: false });
    }
  },

  deleteProject: async (id: number) => {
    try {
      set({ loading: true, error: null });
      await projectService.deleteProject(id);
      set((state) => ({
        projects: state.projects.filter((p) => p.id !== id),
        selectedProject: state.selectedProject?.id === id ? null : state.selectedProject,
        loading: false,
      }));
    } catch (error) {
      set({ error: '프로젝트 삭제에 실패했습니다', loading: false });
    }
  },

  setSelectedProject: (project: Project | null) => {
    set({ selectedProject: project });
  },
})); 