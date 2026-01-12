"""
FastAPI backend for The Recovery Roadmap web interface.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from recovery_roadmap import RecoveryRoadmapCalculator, SimulationConfig, TradeResult


app = FastAPI(title="The Recovery Roadmap API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SimulationRequest(BaseModel):
    """Request model for simulation."""
    current_balance: float = Field(default=200.0, gt=0, description="Current account balance")
    target_balance: float = Field(default=2000.0, gt=0, description="Target account balance")
    risk_per_trade_percent: float = Field(default=2.0, gt=0, le=100, description="Risk per trade as percentage")
    risk_reward_ratio: float = Field(default=3.0, gt=0, description="Risk-to-Reward ratio (e.g., 3.0 for 1:3)")


class TradeResponse(BaseModel):
    """Response model for a single trade."""
    trade_number: int
    account_balance: float
    risk_amount: float
    profit_amount: float


class SimulationResponse(BaseModel):
    """Response model for simulation results."""
    trades: List[TradeResponse]
    summary: dict


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "The Recovery Roadmap API"}


@app.post("/api/simulate", response_model=SimulationResponse)
async def simulate(request: SimulationRequest):
    """
    Run the recovery roadmap simulation.
    
    Returns:
        SimulationResponse with trades and summary
    """
    # Validate that target is greater than current balance
    if request.target_balance <= request.current_balance:
        raise ValueError("Target balance must be greater than current balance")
    
    # Create configuration
    config = SimulationConfig(
        current_balance=request.current_balance,
        target_balance=request.target_balance,
        risk_per_trade_percent=request.risk_per_trade_percent,
        risk_reward_ratio=request.risk_reward_ratio
    )
    
    # Run calculation
    calculator = RecoveryRoadmapCalculator(config)
    trades = calculator.calculate()
    summary = calculator.get_summary()
    
    # Convert trades to response format
    trade_responses = [
        TradeResponse(
            trade_number=trade.trade_number,
            account_balance=trade.account_balance,
            risk_amount=trade.risk_amount,
            profit_amount=trade.profit_amount
        )
        for trade in trades
    ]
    
    return SimulationResponse(trades=trade_responses, summary=summary)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
