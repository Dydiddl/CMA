import React, { createContext, useContext, useReducer, ReactNode } from 'react';
import { User, UserState, UserFormData, LoginFormData } from '../types';
import * as userService from '../services/userService';

interface UserContextType extends UserState {
  login: (credentials: LoginFormData) => Promise<void>;
  register: (userData: UserFormData) => Promise<void>;
  logout: () => Promise<void>;
  getCurrentUser: () => Promise<void>;
  updateUser: (id: number, userData: UserFormData) => Promise<void>;
}

const initialState: UserState = {
  user: null,
  loading: false,
  error: null,
  isAuthenticated: false,
};

type UserAction =
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string | null }
  | { type: 'SET_USER'; payload: User | null }
  | { type: 'SET_AUTHENTICATED'; payload: boolean };

const userReducer = (state: UserState, action: UserAction): UserState => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_ERROR':
      return { ...state, error: action.payload };
    case 'SET_USER':
      return { ...state, user: action.payload };
    case 'SET_AUTHENTICATED':
      return { ...state, isAuthenticated: action.payload };
    default:
      return state;
  }
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(userReducer, initialState);

  const login = async (credentials: LoginFormData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const user = await userService.login(credentials);
      dispatch({ type: 'SET_USER', payload: user });
      dispatch({ type: 'SET_AUTHENTICATED', payload: true });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '로그인에 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const register = async (userData: UserFormData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const user = await userService.register(userData);
      dispatch({ type: 'SET_USER', payload: user });
      dispatch({ type: 'SET_AUTHENTICATED', payload: true });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '회원가입에 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const logout = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      await userService.logout();
      dispatch({ type: 'SET_USER', payload: null });
      dispatch({ type: 'SET_AUTHENTICATED', payload: false });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '로그아웃에 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const getCurrentUser = async () => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const user = await userService.getCurrentUser();
      dispatch({ type: 'SET_USER', payload: user });
      dispatch({ type: 'SET_AUTHENTICATED', payload: true });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '사용자 정보를 가져오는데 실패했습니다',
      });
      dispatch({ type: 'SET_AUTHENTICATED', payload: false });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  const updateUser = async (id: number, userData: UserFormData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      const updatedUser = await userService.updateUser(id, userData);
      dispatch({ type: 'SET_USER', payload: updatedUser });
    } catch (error) {
      dispatch({
        type: 'SET_ERROR',
        payload: error instanceof Error ? error.message : '사용자 정보 수정에 실패했습니다',
      });
    } finally {
      dispatch({ type: 'SET_LOADING', payload: false });
    }
  };

  return (
    <UserContext.Provider
      value={{
        ...state,
        login,
        register,
        logout,
        getCurrentUser,
        updateUser,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}; 