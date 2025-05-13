"""
Policy monitoring alert service with economic indicators
"""
from typing import Dict, Any, List, Optional, TypedDict
from datetime import datetime, timedelta
from enum import Enum
import logging
from backend.api.client import SonarAPIClient
from backend.services.economic_indicators import EconomicIndicatorService

class AlertSeverity(Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    SENTIMENT = "sentiment"
    INFLATION = "inflation"
    GDP = "gdp"
    EMPLOYMENT = "employment"
    TRADE = "trade"

class Alert(TypedDict):
    id: str
    policy_id: int
    type: AlertType
    metric: str
    current_value: float
    threshold: float
    timestamp: str
    severity: AlertSeverity
    message: str
    related_indicators: List[str]

class AlertService:
    """Service for monitoring policy impacts with economic indicators"""
    
    def __init__(
        self,
        api_client: SonarAPIClient,
        economic_service: EconomicIndicatorService
    ):
        self.api_client = api_client
        self.economic_service = economic_service
        self.logger = logging.getLogger(__name__)
        
        # Configurable thresholds with severity bands
        self.thresholds = {
            AlertType.SENTIMENT: {
                "warning": -0.15,
                "alert": -0.25,
                "critical": -0.4
            },
            AlertType.INFLATION: {
                "warning": 0.01,  # 1% monthly
                "alert": 0.02,
                "critical": 0.03
            },
            AlertType.GDP: {
                "warning": -0.003,  # -0.3% quarterly
                "alert": -0.006,
                "critical": -0.01
            }
        }
        
        # Alert message templates
        self.message_templates = {
            AlertType.SENTIMENT: (
                "Policy sentiment changed by {value:.1%} "
                "(threshold: {threshold:.1%})"
            ),
            AlertType.INFLATION: (
                "Inflation impact detected: {value:.1%} "
                "(threshold: {threshold:.1%})"
            )
        }

    async def monitor_policy(
        self,
        policy_id: int,
        policy_text: str,
        policy_type: str
    ) -> List[Alert]:
        """
        Comprehensive policy monitoring with economic indicators
        
        Args:
            policy_id: Policy database ID
            policy_text: Policy content to analyze
            policy_type: Policy category (e.g., "trade", "labor")
            
        Returns:
            List of generated alerts
        """
        alerts: List[Alert] = []
        
        try:
            # Sentiment analysis from news
            news_response = await self.api_client.analyze_policy(
                policy_text=policy_text,
                focus="news"
            )
            alerts.extend(self._check_sentiment(policy_id, news_response))
            
            # Economic impact analysis
            economic_data = await self.economic_service.get_indicators(
                policy_type=policy_type,
                timeframe="30d"
            )
            alerts.extend(self._check_economic_indicators(policy_id, economic_data))
            
        except Exception as e:
            self.logger.error(f"Policy monitoring failed: {str(e)}")
            
        return alerts

    def _check_sentiment(
        self,
        policy_id: int,
        news_data: Dict[str, Any]
    ) -> List[Alert]:
        """Analyze sentiment changes from news sources"""
        sources = news_data.get("sources", [])
        if not sources:
            return []
            
        # Calculate weighted sentiment (recent sources have more weight)
        total_weight = 0.0
        weighted_sentiment = 0.0
        
        for source in sources:
            days_old = (datetime.now() - datetime.fromisoformat(source["date"])).days
            weight = max(0, 1 - (days_old / 30))  # Linear decay over 30 days
            weighted_sentiment += source.get("sentiment", 0.5) * weight
            total_weight += weight
            
        if total_weight == 0:
            return []
            
        avg_sentiment = weighted_sentiment / total_weight
        baseline = 0.5  # Neutral sentiment baseline
        
        return self._generate_alert_if_threshold(
            policy_id=policy_id,
            alert_type=AlertType.SENTIMENT,
            metric="sentiment_change",
            value=avg_sentiment - baseline,
            positive_is_good=False
        )

    def _check_economic_indicators(
        self,
        policy_id: int,
        economic_data: Dict[str, Any]
    ) -> List[Alert]:
        """Check economic indicators against thresholds"""
        alerts: List[Alert] = []
        
        # Inflation check
        if "inflation" in economic_data:
            alerts.extend(self._generate_alert_if_threshold(
                policy_id=policy_id,
                alert_type=AlertType.INFLATION,
                metric="inflation_rate",
                value=economic_data["inflation"]["change"],
                positive_is_good=False
            ))
            
        # GDP check
        if "gdp" in economic_data:
            alerts.extend(self._generate_alert_if_threshold(
                policy_id=policy_id,
                alert_type=AlertType.GDP,
                metric="gdp_change",
                value=economic_data["gdp"]["change"],
                positive_is_good=False
            ))
            
        return alerts

    def _generate_alert_if_threshold(
        self,
        policy_id: int,
        alert_type: AlertType,
        metric: str,
        value: float,
        positive_is_good: bool
    ) -> List[Alert]:
        """
        Generate alert if value crosses configured thresholds
        
        Args:
            positive_is_good: Whether positive values indicate good outcomes
        """
        thresholds = self.thresholds.get(alert_type, {})
        if not thresholds:
            return []
            
        # Determine if value crosses any thresholds
        severity = None
        abs_value = abs(value)
        
        if positive_is_good:
            test_value = -value  # Flip for positive-is-good metrics
        else:
            test_value = value
            
        if test_value <= thresholds.get("critical", 0):
            severity = AlertSeverity.CRITICAL
        elif test_value <= thresholds.get("alert", 0):
            severity = AlertSeverity.HIGH
        elif test_value <= thresholds.get("warning", 0):
            severity = AlertSeverity.MEDIUM
            
        if not severity:
            return []
            
        return [self._create_alert(
            policy_id=policy_id,
            alert_type=alert_type,
            metric=metric,
            value=value,
            threshold=thresholds["warning"],  # Use warning as reference
            severity=severity
        )]

    def _create_alert(
        self,
        policy_id: int,
        alert_type: AlertType,
        metric: str,
        value: float,
        threshold: float,
        severity: AlertSeverity
    ) -> Alert:
        """Create structured alert object"""
        alert_id = f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{alert_type.value}"
        
        return {
            "id": alert_id,
            "policy_id": policy_id,
            "type": alert_type,
            "metric": metric,
            "current_value": value,
            "threshold": threshold,
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "message": self._generate_alert_message(
                alert_type,
                value,
                threshold
            ),
            "related_indicators": self._get_related_indicators(alert_type)
        }

    def _generate_alert_message(
        self,
        alert_type: AlertType,
        value: float,
        threshold: float
    ) -> str:
        """Generate human-readable alert message"""
        template = self.message_templates.get(
            alert_type,
            "{metric} changed by {value:.1%} (threshold: {threshold:.1%})"
        )
        return template.format(
            metric=alert_type.value,
            value=value,
            threshold=threshold
        )

    def _get_related_indicators(self, alert_type: AlertType) -> List[str]:
        """Get related economic indicators for alert type"""
        indicator_map = {
            AlertType.SENTIMENT: ["consumer_confidence", "business_sentiment"],
            AlertType.INFLATION: ["cpi", "ppi", "wages"],
            AlertType.GDP: ["industrial_production", "retail_sales"]
        }
        return indicator_map.get(alert_type, [])
