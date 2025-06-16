export interface ExcelData {
  headers: string[];
  rows: Record<string, any>[];
  metadata?: {
    fileName: string;
    sheetName: string;
    totalRows: number;
    totalColumns: number;
  };
}

export interface ExcelValidationResult {
  isValid: boolean;
  errors: string[];
  warnings?: string[];
}

export interface ExcelUploadResponse {
  success: boolean;
  data?: ExcelData;
  error?: string;
  validationResult?: ExcelValidationResult;
}

export interface ExcelPreviewProps {
  data: ExcelData;
  onEdit?: (rowIndex: number, column: string, value: any) => void;
  onDelete?: (rowIndex: number) => void;
}

export interface ExcelProcessorOptions {
  skipEmptyRows?: boolean;
  skipHeaderRow?: boolean;
  dateFormat?: string;
  numberFormat?: string;
}
