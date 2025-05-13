"""
API endpoint dependencies
"""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.simulation_service import SimulationService
from backend.repositories.simulation_repository import SimulationRepository

def get_simulation_repository(
    db: Annotated[Session, Depends(get_db)]
) -> SimulationRepository:
    """Dependency for SimulationRepository"""
    return SimulationRepository(db)

def get_simulation_service(
    repository: Annotated[SimulationRepository, Depends(get_simulation_repository)]
) -> SimulationService:
    """Dependency for SimulationService"""
    return SimulationService(repository)
