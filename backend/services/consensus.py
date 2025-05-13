"""
Academic consensus service with improved reliability and metrics
"""
from typing import Dict, Any, List, Optional, TypedDict
from datetime import datetime
from functools import lru_cache
import logging
from backend.api.client import SonarAPIClient

class ConsensusMetrics(TypedDict):
    support_count: int
    oppose_count: int 
    neutral_count: int
    confidence_score: float
    total_sources: int
    recency_factor: float

class AcademicSource(TypedDict):
    id: str
    title: str
    journal: str
    year: int
    sentiment: float
    url: Optional[str]

class ConsensusResult(TypedDict):
    metrics: ConsensusMetrics
    journals: List[str]
    sources: List[AcademicSource]

class ConsensusService:
    """Service for gathering and analyzing academic consensus"""
    
    def __init__(self, api_client: SonarAPIClient):
        self.api_client = api_client
        self.logger = logging.getLogger(__name__)
        
    @lru_cache(maxsize=100)
    async def get_academic_consensus(self, policy_text: str) -> ConsensusResult:
        """
        Get academic consensus with caching and robust error handling
        
        Args:
            policy_text: Policy text to analyze (minimum 50 chars)
            
        Returns:
            Structured consensus data with metrics and sources
            
        Raises:
            ValueError: If policy text is too short
            APIError: If Sonar API request fails
        """
        if len(policy_text.strip()) < 50:
            raise ValueError("Policy text must be at least 50 characters")
            
        try:
            response = await self.api_client.analyze_policy(
                policy_text=policy_text,
                focus="academic"
            )
            return self._process_response(response)
        except Exception as e:
            self.logger.error(f"Consensus analysis failed: {str(e)}")
            raise
            
    def _process_response(self, response: Dict[str, Any]) -> ConsensusResult:
        """Process API response into structured consensus data"""
        sources: List[AcademicSource] = response.get("sources", [])
        
        # Calculate metrics
        support, oppose, neutral = self._count_positions(sources)
        total = len(sources)
        recent = sum(1 for s in sources if self._is_recent(s))
        
        confidence = self._calculate_confidence(
            support, 
            oppose,
            recent,
            total
        )
        
        return {
            "metrics": {
                "support_count": support,
                "oppose_count": oppose,
                "neutral_count": neutral,
                "confidence_score": confidence,
                "total_sources": total,
                "recency_factor": recent / total if total > 0 else 0
            },
            "journals": self._extract_journals(sources),
            "sources": sources
        }
        
    def _count_positions(self, sources: List[AcademicSource]) -> tuple[int, int, int]:
        """Count supporting, opposing and neutral sources"""
        support = oppose = neutral = 0
        for source in sources:
            sentiment = source.get("sentiment", 0.5)
            if sentiment > 0.7:
                support += 1
            elif sentiment < 0.3:
                oppose += 1
            else:
                neutral += 1
        return support, oppose, neutral
        
    def _calculate_confidence(
        self,
        support: int,
        oppose: int,
        recent: int,
        total: int
    ) -> float:
        """Calculate weighted confidence score"""
        if total == 0:
            return 0.0
            
        base_score = (support - oppose) / total
        recency_boost = 1 + (recent / total * 0.5)  # Up to 50% boost
        
        # Apply diminishing returns for very high counts
        confidence = base_score * min(1, recency_boost)
        return round(confidence, 2)
        
    def _extract_journals(self, sources: List[AcademicSource]) -> List[str]:
        """Extract unique journal names"""
        return sorted({
            s["journal"] for s in sources 
            if s.get("journal")
        })
        
    def _is_recent(self, source: AcademicSource) -> bool:
        """Check if source was published in last 5 years"""
        current_year = datetime.now().year
        return source.get("year", 0) >= (current_year - 5)
