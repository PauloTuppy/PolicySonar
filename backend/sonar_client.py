"""
Sonar API Client using only Python standard library
"""
import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from typing import Dict, Any

class SonarAPIClient:
    """Client for interacting with policy analysis APIs using standard library only"""
    
    def __init__(self):
        self.api_key = os.getenv("SONAR_API_KEY")
        self.base_url = "https://api.policysonar.com/v1"
        
    def analyze_policy(self, policy_text: str, focus: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze policy text using the Sonar API
        
        Args:
            policy_text: The policy text to analyze
            focus: Analysis focus (comprehensive, economic, social, environmental)
            
        Returns:
            Dict containing analysis results
            
        Raises:
            Exception: If API request fails
        """
        url = f"{self.base_url}/analyze"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = json.dumps({
            "text": policy_text,
            "focus": focus,
            "include_historical": True
        }).encode('utf-8')
        
        try:
            req = Request(url, data=payload, headers=headers, method='POST')
            with urlopen(req) as response:
                return json.loads(response.read().decode('utf-8'))
        except HTTPError as e:
            error_body = e.read().decode('utf-8')
            raise Exception(f"API request failed: {e.code} - {error_body}")
