from typing import Dict, Any, List
import json
from pathlib import Path
from datetime import datetime

class EstimatorUpdater:
    """연도별 품셈 변경사항 관리 클래스"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent / 'templates' / 'updates'
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.updates_file = self.data_dir / 'yearly_updates.json'
    
    def add_update(self, year: int, updates: Dict[str, Any]):
        """
        연도별 변경사항 추가
        
        Args:
            year (int): 연도
            updates (Dict[str, Any]): 변경사항 데이터
        """
        current_updates = self._load_updates()
        current_updates[str(year)] = {
            'year': year,
            'updates': updates,
            'created_at': datetime.now().isoformat()
        }
        self._save_updates(current_updates)
    
    def get_updates(self, year: int = None) -> Dict[str, Any]:
        """
        연도별 변경사항 조회
        
        Args:
            year (int, optional): 조회할 연도
            
        Returns:
            Dict[str, Any]: 변경사항 데이터
        """
        updates = self._load_updates()
        if year:
            return updates.get(str(year), {})
        return updates
    
    def apply_updates(self, work_items: List[Dict[str, Any]], year: int) -> List[Dict[str, Any]]:
        """
        공사 항목에 연도별 변경사항 적용
        
        Args:
            work_items (List[Dict[str, Any]]): 공사 항목 목록
            year (int): 적용할 연도
            
        Returns:
            List[Dict[str, Any]]: 변경사항이 적용된 공사 항목 목록
        """
        updates = self.get_updates(year)
        if not updates:
            return work_items
            
        # TODO: 변경사항 적용 로직 구현
        return work_items
    
    def _load_updates(self) -> Dict[str, Any]:
        """저장된 변경사항 로드"""
        if not self.updates_file.exists():
            return {}
            
        with open(self.updates_file, 'r', encoding='utf-8', newline='') as f:
            return json.load(f)
    
    def _save_updates(self, updates: Dict[str, Any]):
        """변경사항 저장"""
        with open(self.updates_file, 'w', encoding='utf-8', newline='') as f:
            json.dump(updates, f, ensure_ascii=False, indent=2)
