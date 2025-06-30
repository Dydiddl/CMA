from supabase import create_client, Client
from ..core.config import settings

class SupabaseClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance.client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
        return cls._instance
    
    @property
    def client(self) -> Client:
        return self._client
    
    @client.setter
    def client(self, value):
        self._client = value

# 싱글톤 인스턴스 생성
supabase = SupabaseClient().client 