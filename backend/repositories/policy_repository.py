"""
Policy Repository implementation using standard library only
"""
import os
import json
from typing import List, Dict, Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from datetime import datetime

class PolicyRepository:
    """Repository for policy analog operations using Supabase REST API"""
    
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        self.table_name = "policy_analogs"
        
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make authenticated request to Supabase API"""
        url = f"{self.supabase_url}/rest/v1/{endpoint}"
        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        
        try:
            req = Request(
                url,
                data=json.dumps(data).encode('utf-8') if data else None,
                headers=headers,
                method=method
            )
            with urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"Supabase request failed: {e.code} - {error_body}")
    
    def save(self, policy_data: Dict) -> Dict:
        """Save a policy analog to the database"""
        return self._make_request("POST", self.table_name, policy_data)
    
    def find_by_policy_text(self, policy_text: str) -> List[Dict]:
        """Find historical analogs for a given policy text"""
        params = {
            "policy_text": f"eq.{policy_text}",
            "select": "*",
            "order": "similarity_score.desc"
        }
        return self._make_request("GET", f"{self.table_name}?{self._build_query(params)}")
    
    def find_top_matches(self, policy_text: str, limit: int = 5) -> List[Dict]:
        """Find top historical matches for a policy text"""
        params = {
            "policy_text": f"eq.{policy_text}",
            "select": "*",
            "order": "similarity_score.desc",
            "limit": str(limit)
        }
        return self._make_request("GET", f"{self.table_name}?{self._build_query(params)}")
    
    def _build_query(self, params: Dict) -> str:
        """Build URL query string from params"""
        return "&".join(f"{k}={v}" for k, v in params.items())

    def to_model(self, data: Dict) -> Dict:
        """Convert raw data to policy analog model"""
        return {
            "id": data.get("id"),
            "policy_text": data.get("policy_text"),
            "historical_match": data.get("historical_match"),
            "similarity_score": data.get("similarity_score"),
            "risk_factors": data.get("risk_factors", []),
            "outcome_analysis": data.get("outcome_analysis"),
            "policy_type": data.get("policy_type"),
            "jurisdiction": data.get("jurisdiction"),
            "time_period": data.get("time_period"),
            "created_at": data.get("created_at")
        }
