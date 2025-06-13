import { invoke } from '@tauri-apps/api/tauri';
import { User, UserFormData, LoginFormData } from '../types';

export const login = async (credentials: LoginFormData): Promise<User> => {
  try {
    return await invoke<User>('login', { credentials });
  } catch (error) {
    console.error('로그인에 실패했습니다:', error);
    throw error;
  }
};

export const register = async (userData: UserFormData): Promise<User> => {
  try {
    return await invoke<User>('register', { userData });
  } catch (error) {
    console.error('회원가입에 실패했습니다:', error);
    throw error;
  }
};

export const getCurrentUser = async (): Promise<User> => {
  try {
    return await invoke<User>('get_current_user');
  } catch (error) {
    console.error('현재 사용자 정보를 가져오는데 실패했습니다:', error);
    throw error;
  }
};

export const updateUser = async (id: number, userData: UserFormData): Promise<User> => {
  try {
    return await invoke<User>('update_user', { id, userData });
  } catch (error) {
    console.error('사용자 정보 수정에 실패했습니다:', error);
    throw error;
  }
};

export const logout = async (): Promise<void> => {
  try {
    await invoke('logout');
  } catch (error) {
    console.error('로그아웃에 실패했습니다:', error);
    throw error;
  }
}; 