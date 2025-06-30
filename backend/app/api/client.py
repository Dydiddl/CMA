from typing import Dict, Any, Optional, List

class Client:
    def get_labor_records(
        self, 
        skip: int = 0, 
        limit: int = 50,
        search: Optional[str] = None,
        job_type: Optional[str] = None,
        status: Optional[str] = None,
        worker_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """노무자 목록 조회"""
        params = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        if job_type:
            params["job_type"] = job_type
        if status:
            params["status"] = status
        if worker_id:
            params["worker_id"] = worker_id
        
        response = self.session.get(f"{self.base_url}/labor/", params=params)
        response.raise_for_status()
        return response.json()
    
    def get_labor_by_id(self, labor_id: str) -> Dict[str, Any]:
        """노무자 상세 조회"""
        response = self.session.get(f"{self.base_url}/labor/{labor_id}")
        response.raise_for_status()
        return response.json()
    
    def create_labor_record(self, labor_data: Dict[str, Any]) -> Dict[str, Any]:
        """노무자 생성"""
        response = self.session.post(f"{self.base_url}/labor/", json=labor_data)
        response.raise_for_status()
        return response.json()
    
    def update_labor_record(self, labor_id: str, labor_data: Dict[str, Any]) -> Dict[str, Any]:
        """노무자 수정"""
        response = self.session.put(f"{self.base_url}/labor/{labor_id}", json=labor_data)
        response.raise_for_status()
        return response.json()
    
    def delete_labor_record(self, labor_id: str) -> Dict[str, Any]:
        """노무자 삭제"""
        response = self.session.delete(f"{self.base_url}/labor/{labor_id}")
        response.raise_for_status()
        return response.json()
    
    def get_labor_summary(self) -> Dict[str, Any]:
        """노무 요약 통계 조회"""
        response = self.session.get(f"{self.base_url}/labor/summary")
        response.raise_for_status()
        return response.json()
    
    def get_labor_statistics(
        self, 
        start_date: str, 
        end_date: str
    ) -> Dict[str, Any]:
        """기간별 노무 통계 조회"""
        params = {"start_date": start_date, "end_date": end_date}
        response = self.session.get(f"{self.base_url}/labor/statistics", params=params)
        response.raise_for_status()
        return response.json()
    
    def batch_create_labor_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """노무 기록 배치 생성"""
        response = self.session.post(f"{self.base_url}/labor/batch", json={"records": records})
        response.raise_for_status()
        return response.json()
    
    def get_workers(
        self, 
        skip: int = 0, 
        limit: int = 100,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        """근로자 목록 조회"""
        params = {"skip": skip, "limit": limit}
        if search:
            params["search"] = search
        
        response = self.session.get(f"{self.base_url}/workers/", params=params)
        response.raise_for_status()
        return response.json() 