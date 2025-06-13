import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { Task, TaskState, TaskFormData } from '../types';
import * as taskService from '../services/taskService';

interface TaskContextType extends TaskState {
  fetchTasks: (projectId?: number) => Promise<void>;
  fetchTask: (id: number) => Promise<void>;
  createTask: (task: TaskFormData) => Promise<void>;
  updateTask: (id: number, task: TaskFormData) => Promise<void>;
  deleteTask: (id: number) => Promise<void>;
  setSelectedTask: (task: Task | null) => void;
}

const initialState: TaskState = {
  tasks: [],
  loading: false,
  error: null,
  selectedTask: null,
};

type TaskAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_TASKS'; payload: Task[] }
  | { type: 'SET_SELECTED_TASK'; payload: Task | null }
  | { type: 'ADD_TASK'; payload: Task }
  | { type: 'UPDATE_TASK'; payload: Task }
  | { type: 'DELETE_TASK'; payload: number };

const taskReducer = (state: TaskState, action: TaskAction): TaskState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_TASKS':
      return { ...state, tasks: action.payload };
    case 'SET_SELECTED_TASK':
      return { ...state, selectedTask: action.payload };
    case 'ADD_TASK':
      return { ...state, tasks: [...state.tasks, action.payload] };
    case 'UPDATE_TASK':
      return {
        ...state,
        tasks: state.tasks.map((task) =>
          task.id === action.payload.id ? action.payload : task
        ),
      };
    case 'DELETE_TASK':
      return {
        ...state,
        tasks: state.tasks.filter((task) => task.id !== action.payload),
      };
    default:
      return state;
  }
};

const TaskContext = createContext<TaskContextType | undefined>(undefined);

export const TaskProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(taskReducer, initialState);

  const fetchTasks = async (projectId?: number) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const tasks = await taskService.getTasks(projectId);
      dispatch({ type: 'SET_TASKS', payload: tasks });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '작업 목록을 가져오는데 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const fetchTask = async (id: number) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const task = await taskService.getTask(id);
      dispatch({ type: 'SET_SELECTED_TASK', payload: task });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '작업을 가져오는데 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const createTask = async (taskData: TaskFormData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const newTask = await taskService.createTask(taskData);
      dispatch({ type: 'ADD_TASK', payload: newTask });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '작업 생성에 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const updateTask = async (id: number, taskData: TaskFormData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const updatedTask = await taskService.updateTask(id, taskData);
      dispatch({ type: 'UPDATE_TASK', payload: updatedTask });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '작업 수정에 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const deleteTask = async (id: number) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      await taskService.deleteTask(id);
      dispatch({ type: 'DELETE_TASK', payload: id });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '작업 삭제에 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const setSelectedTask = (task: Task | null) => {
    dispatch({ type: 'SET_SELECTED_TASK', payload: task });
  };

  return (
    <TaskContext.Provider
      value={{
        ...state,
        fetchTasks,
        fetchTask,
        createTask,
        updateTask,
        deleteTask,
        setSelectedTask,
      }}
    >
      {children}
    </TaskContext.Provider>
  );
};

export const useTask = () => {
  const context = useContext(TaskContext);
  if (context === undefined) {
    throw new Error('useTask must be used within a TaskProvider');
  }
  return context;
}; 