"""
Repository for simulation operations using SQLAlchemy
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from backend.models.simulation import Simulation

class SimulationRepository:
    """Repository for simulation operations using SQLAlchemy"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def save(self, simulation_data: Dict[str, Any]) -> Simulation:
        """Save a simulation to the database"""
        simulation = Simulation(
            policy_id=simulation_data["policy_id"],
            parameters=simulation_data["parameters"],
            results=simulation_data["results"]
        )
        self.db.add(simulation)
        self.db.commit()
        self.db.refresh(simulation)
        return simulation
    
    def find_by_policy(self, policy_id: int) -> List[Simulation]:
        """Find simulations for a given policy"""
        return self.db.query(Simulation)\
            .filter(Simulation.policy_id == policy_id)\
            .order_by(Simulation.created_at.desc())\
            .all()
            
    def find_by_id(self, simulation_id: int) -> Optional[Simulation]:
        """Find a simulation by ID"""
        return self.db.query(Simulation)\
            .filter(Simulation.id == simulation_id)\
            .first()
