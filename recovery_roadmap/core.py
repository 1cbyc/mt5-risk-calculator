"""
Core calculation module for The Recovery Roadmap.

This module contains the logic for simulating account growth
using a fixed Risk-Reward trading strategy.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class TradeResult:
    """Represents a single trade result."""
    trade_number: int
    account_balance: float
    risk_amount: float
    profit_amount: float


@dataclass
class SimulationConfig:
    """Configuration for the recovery roadmap simulation."""
    current_balance: float
    target_balance: float
    risk_per_trade_percent: float
    risk_reward_ratio: float  # e.g., 3.0 means 1:3


class RecoveryRoadmapCalculator:
    """Calculates the recovery roadmap using perfect execution simulation."""
    
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.trades: List[TradeResult] = []
    
    def calculate(self) -> List[TradeResult]:
        """
        Simulate perfect execution trades until target balance is reached.
        
        Returns:
            List of TradeResult objects representing each trade
        """
        self.trades = []
        current_balance = self.config.current_balance
        trade_number = 1
        
        while current_balance < self.config.target_balance:
            # Calculate risk amount based on current balance
            risk_amount = current_balance * (self.config.risk_per_trade_percent / 100)
            
            # Calculate profit amount based on risk-reward ratio
            profit_amount = risk_amount * self.config.risk_reward_ratio
            
            # Add profit to balance (assuming win)
            new_balance = current_balance + profit_amount
            
            # Create trade result
            trade = TradeResult(
                trade_number=trade_number,
                account_balance=current_balance,
                risk_amount=risk_amount,
                profit_amount=profit_amount
            )
            self.trades.append(trade)
            
            # Update for next iteration
            current_balance = new_balance
            trade_number += 1
        
        return self.trades
    
    def get_summary(self) -> dict:
        """
        Generate summary statistics from the simulation.
        
        Returns:
            Dictionary with summary statistics
        """
        if not self.trades:
            return {
                "total_trades": 0,
                "max_risk_taken": 0.0,
                "final_balance": self.config.current_balance
            }
        
        max_risk = max(trade.risk_amount for trade in self.trades)
        final_balance = self.trades[-1].account_balance + self.trades[-1].profit_amount
        
        return {
            "total_trades": len(self.trades),
            "max_risk_taken": max_risk,
            "final_balance": final_balance,
            "starting_balance": self.config.current_balance,
            "target_balance": self.config.target_balance
        }
