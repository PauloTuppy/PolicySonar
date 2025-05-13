"""
Updated Simulation Service with SQLAlchemy integration
"""
from typing import Dict, Any
from backend.models.simulation import Simulation
from backend.repositories.simulation_repository import SimulationRepository

class SimulationService:
    """Service for running policy impact simulations with SQLAlchemy"""
    
    def __init__(self, db_session):
        self.repository = SimulationRepository(db_session)
        
    def run_simulation(self, 
                     policy_id: int, 
                     parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run simulation and return results (updated for SQLAlchemy)
        """
        # ... (rest of existing implementation remains the same)
        
        # Store simulation using SQLAlchemy
        simulation = self.repository.save({
            "policy_id": policy_id,
            "parameters": parameters,
            "results": results
        })
        
        return simulation.to_dict()
