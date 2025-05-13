"""
SQLAlchemy model for policy simulations
"""
from sqlalchemy import Column, Integer, ForeignKey, JSON, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from typing import Dict, Any

Base = declarative_base()

class Simulation(Base):
    """SQLAlchemy model for policy simulations"""
    __tablename__ = "simulations"
    
    id = Column(Integer, primary_key=True)
    policy_id = Column(Integer, ForeignKey("policy_analogs.id"))
    parameters = Column(JSON, nullable=False)
    results = Column(JSON, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __init__(self, policy_id: int, parameters: Dict[str, Any], results: Dict[str, Any]):
        self.policy_id = policy_id
        self.parameters = parameters
        self.results = results

    def __repr__(self):
        return f"<Simulation(id={self.id}, policy_id={self.policy_id})>"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "policy_id": self.policy_id,
            "parameters": self.parameters,
            "results": self.results,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
