"""
Simulation API endpoints with comprehensive features
"""
from fastapi import APIRouter, HTTPException, Depends, status, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi_pagination import Page, paginate, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.services.simulation_service import SimulationService
from backend.schemas.simulation import (
    SimulationRequest,
    SimulationResponse,
    SimulationSummary,
    SimulationParameters,
    SimulationResult
)
from backend.models.simulation import Simulation
from backend.repositories.simulation_repository import SimulationRepository
from backend.api.dependencies import get_simulation_service

router = APIRouter(
    prefix="/api/simulations",
    tags=["simulations"],
    responses={
        404: {"description": "Simulation not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"}
    }
)

@router.post(
    "/{policy_id}",
    response_model=SimulationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Run policy simulation",
    response_description="The created simulation results"
)
async def run_simulation(
    policy_id: int,
    request: SimulationRequest,
    service: SimulationService = Depends(get_simulation_service)
) -> SimulationResponse:
    """
    Run a new policy impact simulation with the specified parameters.

    - **policy_id**: ID of the policy being simulated
    - **parameters**: Dictionary of simulation parameters
    - **scenario_name**: Optional name for this simulation scenario
    - **notes**: Optional notes about this simulation run

    Returns complete simulation results including metadata.
    """
    try:
        # Validate parameters before running simulation
        if not request.parameters:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Simulation parameters cannot be empty"
            )

        result = await service.run_simulation(
            policy_id=policy_id,
            parameters=request.parameters,
            scenario_name=request.scenario_name,
            notes=request.notes
        )
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Simulation failed: {str(e)}"
        )

@router.get(
    "/{policy_id}",
    response_model=Page[SimulationSummary],
    summary="List policy simulations",
    response_description="Paginated list of simulations"
)
async def get_simulations(
    policy_id: int,
    time_range: Optional[str] = Query(
        None,
        description="Time range filter (e.g., '7d', '30d', '1y')"
    ),
    scenario_name: Optional[str] = Query(
        None,
        description="Filter by scenario name"
    ),
    db: Session = Depends(get_db),
    repository: SimulationRepository = Depends(SimulationRepository)
) -> Page[SimulationSummary]:
    """
    Get paginated list of simulations for a specific policy with filtering options.

    - **policy_id**: ID of the policy to get simulations for
    - **time_range**: Optional time range filter
    - **scenario_name**: Optional scenario name filter
    """
    try:
        query = repository.get_base_query(policy_id)

        # Apply time range filter if specified
        if time_range:
            time_map = {
                '7d': timedelta(days=7),
                '30d': timedelta(days=30),
                '1y': timedelta(days=365)
            }
            if time_range not in time_map:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid time range. Use '7d', '30d', or '1y'"
                )
            cutoff_date = datetime.now() - time_map[time_range]
            query = query.filter(Simulation.created_at >= cutoff_date)

        # Apply scenario name filter if specified
        if scenario_name:
            query = query.filter(Simulation.scenario_name.ilike(f"%{scenario_name}%"))

        return sqlalchemy_paginate(query)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve simulations: {str(e)}"
        )

@router.get(
    "/{policy_id}/{simulation_id}",
    response_model=SimulationResponse,
    summary="Get simulation details",
    response_description="Complete simulation details"
)
async def get_simulation(
    policy_id: int,
    simulation_id: int,
    repository: SimulationRepository = Depends(SimulationRepository)
) -> SimulationResponse:
    """
    Get detailed results for a specific simulation.

    - **policy_id**: ID of the associated policy
    - **simulation_id**: ID of the simulation to retrieve
    """
    try:
        simulation = repository.find_by_id(simulation_id)
        if not simulation or simulation.policy_id != policy_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Simulation not found"
            )
        return simulation.to_response()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve simulation: {str(e)}"
        )

@router.delete(
    "/{policy_id}/{simulation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete simulation",
    response_description="Simulation successfully deleted"
)
async def delete_simulation(
    policy_id: int,
    simulation_id: int,
    repository: SimulationRepository = Depends(SimulationRepository)
) -> None:
    """
    Delete a specific simulation.

    - **policy_id**: ID of the associated policy
    - **simulation_id**: ID of the simulation to delete
    """
    try:
        simulation = repository.find_by_id(simulation_id)
        if not simulation or simulation.policy_id != policy_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Simulation not found"
            )
        repository.delete(simulation)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete simulation: {str(e)}"
        )

# Add pagination support to the router
add_pagination(router)
