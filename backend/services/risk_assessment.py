"""
Risk assessment service using standard library
"""
from typing import Dict, Any, List

class RiskAssessmentService:
    """Service for assessing policy risks based on historical analogs"""
    
    def assess_risk(self, analogs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess risk based on historical policy analogs
        
        Args:
            analogs: List of historical analogs with similarity scores and outcomes
            
        Returns:
            Risk assessment with level, confidence, factors and recommendations
        """
        if not analogs:
            return {
                "risk_level": "Insufficient Data",
                "confidence": 0.0,
                "factors": [],
                "recommendations": ["No historical analogs found for assessment"]
            }
        
        # Calculate weighted risk score
        weighted_scores = []
        risk_factors = []
        
        for analog in analogs:
            similarity = analog["similarity"]
            outcome_type = self._classify_outcome(analog["policy"]["outcome_analysis"])
            risk_score = self._calculate_risk_score(similarity, outcome_type)
            
            weighted_scores.append(risk_score * similarity)
            
            # Collect risk factors
            if outcome_type != "positive":
                risk_factors.append({
                    "policy": analog["policy"]["text"],
                    "year": analog["policy"]["year"],
                    "type": analog["policy"]["policy_type"],
                    "outcome": analog["policy"]["outcome_analysis"],
                    "similarity": similarity
                })
        
        # Calculate final risk score (weighted average)
        total_similarity = sum(a["similarity"] for a in analogs)
        final_score = sum(weighted_scores) / total_similarity if total_similarity > 0 else 0
        
        # Determine risk level based on matrix
        risk_level = self._determine_risk_level(final_score)
        
        return {
            "risk_level": risk_level,
            "score": final_score,
            "confidence": min(total_similarity / len(analogs), 1.0),
            "factors": risk_factors,
            "recommendations": self._generate_recommendations(risk_level, risk_factors)
        }
    
    def _classify_outcome(self, outcome: str) -> str:
        """Classify historical outcome as positive, negative or mixed"""
        outcome_lower = outcome.lower()
        if "increase" in outcome_lower and "decrease" in outcome_lower:
            return "mixed"
        elif any(word in outcome_lower for word in ["increase", "growth", "improve"]):
            return "positive"
        elif any(word in outcome_lower for word in ["decrease", "reduction", "decline"]):
            return "negative"
        return "mixed"
    
    def _calculate_risk_score(self, similarity: float, outcome: str) -> float:
        """Calculate risk score based on similarity and outcome type"""
        # Base scores from matrix
        if outcome == "negative":
            if similarity > 0.85: return 0.9
            elif similarity > 0.7: return 0.7
            else: return 0.5
        elif outcome == "mixed":
            if similarity > 0.85: return 0.6
            elif similarity > 0.7: return 0.4
            else: return 0.3
        else:  # positive
            if similarity > 0.85: return 0.2
            elif similarity > 0.7: return 0.1
            else: return 0.05
    
    def _determine_risk_level(self, score: float) -> str:
        """Convert score to risk level with emoji indicators"""
        if score > 0.7: return "🔴 High"
        elif score > 0.5: return "🟠 Medium"
        elif score > 0.3: return "🟡 Low-Medium"
        elif score > 0.1: return "🟢 Low"
        else: return "⚪ Insufficient Data"
    
    def _generate_recommendations(self, risk_level: str, factors: List[Dict[str, Any]]) -> List[str]:
        """Generate context-aware recommendations"""
        recommendations = []
        
        # General recommendations
        if "🔴" in risk_level:
            recommendations.append("Strongly consider policy redesign or mitigation strategies")
            recommendations.append("Implement phased rollout with monitoring checkpoints")
        elif "🟠" in risk_level:
            recommendations.append("Consider targeted adjustments to high-risk aspects")
            recommendations.append("Establish monitoring framework for key indicators")
        
        # Factor-specific recommendations
        for factor in factors:
            if "trade" in factor["type"].lower():
                recommendations.append(f"Review trade agreements from {factor['year']} for lessons")
            if "employment" in factor["outcome"].lower() and "reduction" in factor["outcome"].lower():
                recommendations.append("Develop workforce transition programs")
            if "price" in factor["outcome"].lower() and "increase" in factor["outcome"].lower():
                recommendations.append("Consider price stabilization measures")
        
        if not recommendations:
            recommendations.append("No significant risks identified based on historical analogs")
        
        return recommendations
