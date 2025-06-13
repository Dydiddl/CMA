import axios from 'axios';
import { Project, ProjectFormData } from '../types/project';

const API_URL = 'http://localhost:8000/api';

const projectService = {
  getProjects: async (): Promise<Project[]> => {
    try {
      const response = await axios.get(`${API_URL}/projects`);
      return response.data;
    } catch (error) {
      console.error('프로젝트 목록을 가져오는데 실패했습니다:', error);
      throw error;
    }
  },

  getProject: async (id: number): Promise<Project> => {
    try {
      const response = await axios.get(`${API_URL}/projects/${id}`);
      return response.data;
    } catch (error) {
      console.error('프로젝트 정보를 가져오는데 실패했습니다:', error);
      throw error;
    }
  },

  createProject: async (projectData: ProjectFormData): Promise<Project> => {
    try {
      const response = await axios.post(`${API_URL}/projects`, projectData);
      return response.data;
    } catch (error) {
      console.error('프로젝트 생성에 실패했습니다:', error);
      throw error;
    }
  },

  updateProject: async (id: number, projectData: ProjectFormData): Promise<Project> => {
    try {
      const response = await axios.put(`${API_URL}/projects/${id}`, projectData);
      return response.data;
    } catch (error) {
      console.error('프로젝트 수정에 실패했습니다:', error);
      throw error;
    }
  },

  deleteProject: async (id: number): Promise<void> => {
    try {
      await axios.delete(`${API_URL}/projects/${id}`);
    } catch (error) {
      console.error('프로젝트 삭제에 실패했습니다:', error);
      throw error;
    }
  },
};

export default projectService; 