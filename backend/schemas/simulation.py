"""
Simulation API schemas and response models
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from enum import Enum

class SimulationScenario(str, Enum):
    BASELINE = "baseline"
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"
    CUSTOM = "custom"

class SimulationParameters(BaseModel):
    """Parameters for running a simulation"""
    economic_model: str = Field(
        ...,
        description="Economic model to use for simulation"
    )
    time_horizon: int = Field(
        5,
        description="Number of years to simulate",
        ge=1,
        le=20
    )
    assumptions: Dict[str, Any] = Field(
        {},
        description="Model-specific assumptions"
    )

    @validator('economic_model')
    def validate_economic_model(cls, v):
        valid_models = ["keynesian", "neoclassical", "behavioral"]
        if v.lower() not in valid_models:
            raise ValueError(
                f"Invalid economic model. Must be one of: {valid_models}"
            )
        return v.lower()

class SimulationRequest(BaseModel):
    """Request body for running a simulation"""
    parameters: SimulationParameters
    scenario_name: Optional[str] = Field(
        None,
        max_length=100,
        description="Name for this simulation scenario"
    )
    notes: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional notes about this simulation"
    )

class EconomicImpact(BaseModel):
    """Economic impact metrics from simulation"""
    gdp_change: float = Field(
        ...,
        description="Percentage change in GDP",
        example=0.025
    )
    employment_impact: float = Field(
        ...,
        description="Change in employment rate (percentage points)",
        example=-0.5
    )
    inflation_effect: float = Field(
        ...,
        description="Effect on inflation rate (percentage points)",
        example=0.3
    )

class SimulationResult(BaseModel):
    """Detailed simulation results"""
    economic_impact: EconomicImpact
    sector_impacts: Dict[str, float] = Field(
        ...,
        description="Impact by economic sector"
    )
    risk_assessment: Dict[str, float] = Field(
        ...,
        description="Risk probability assessments"
    )
    sensitivity_analysis: Dict[str, Any] = Field(
        ...,
        description="Sensitivity analysis results"
    )

class SimulationSummary(BaseModel):
    """Summary of a simulation run"""
    id: int
    policy_id: int
    scenario_name: str
    created_at: datetime
    economic_impact: EconomicImpact
    notes: Optional[str]

class SimulationResponse(SimulationSummary):
    """Complete simulation response including all results"""
    parameters: SimulationParameters
    results: SimulationResult
    execution_time_ms: int = Field(
        ...,
        description="Simulation execution time in milliseconds"
    )
