"""
Historical policy analog service using standard library
"""
from typing import List, Dict, Any
from backend.services.similarity_engine import SimilarityEngine
from backend.repositories.policy_repository import PolicyRepository

class AnalogService:
    """Service for historical policy analog operations"""
    
    def __init__(self):
        self.similarity_engine = SimilarityEngine()
        self.repository = PolicyRepository()
        # Initialize with sample historical policies
        self.historical_policies = self._get_historical_policies()
        # Train the similarity engine
        self.similarity_engine.train([p["text"] for p in self.historical_policies])
    
    def find_historical_analogs(self, policy_text: str, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Find historical policy analogs for a given policy text
        
        Args:
            policy_text: The policy text to analyze
            threshold: Minimum similarity threshold (0-1)
            
        Returns:
            List of historical analogs with similarity scores
        """
        # Find similar policies using similarity engine
        similar_policies = self.similarity_engine.find_similar_policies(
            policy_text, 
            self.historical_policies,
            threshold
        )
        
        # Store matches in database
        for match in similar_policies:
            policy_analog = {
                "policy_text": policy_text,
                "historical_match": match["policy"]["text"],
                "similarity_score": match["similarity"],
                "risk_factors": match["policy"].get("risk_factors", []),
                "outcome_analysis": match["policy"].get("outcome_analysis", "")
            }
            self.repository.save(policy_analog)
        
        return similar_policies
    
    def _get_historical_policies(self) -> List[Dict[str, Any]]:
        """
        Get historical policies from database or external source
        
        Returns:
            List of historical policies with metadata
        """
        return [
            {
                "id": 1,
                "text": "Tariff increase of 25% on imported steel and aluminum",
                "year": 2018,
                "policy_type": "Trade",
                "jurisdiction": "National",
                "risk_factors": ["trade retaliation", "price inflation"],
                "outcome_analysis": "2.6% price increase in construction sector, -0.2% employment in manufacturing"
            },
            {
                "id": 2,
                "text": "Tax credit of 30% for renewable energy investments",
                "year": 2009,
                "policy_type": "Energy",
                "jurisdiction": "National",
                "risk_factors": ["budget deficit", "market distortion"],
                "outcome_analysis": "12% growth in renewable sector, +3.1% in green energy jobs"
            },
            {
                "id": 3,
                "text": "Minimum wage increase to $15 per hour",
                "year": 2021,
                "policy_type": "Labor",
                "jurisdiction": "State",
                "risk_factors": ["small business impact", "inflation"],
                "outcome_analysis": "10% wage increase for bottom quartile, 2% reduction in low-wage employment"
            }
        ]
