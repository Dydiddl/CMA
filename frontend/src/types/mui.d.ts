import { GridProps } from '@mui/material/Grid';

declare module '@mui/material/Grid' {
  interface GridProps {
    item?: boolean;
  }
} 