#!/usr/bin/env python3
"""
CLI interface for The Recovery Roadmap.

Run this script to calculate the recovery roadmap from the command line.
"""

import argparse
from tabulate import tabulate
from recovery_roadmap import RecoveryRoadmapCalculator, SimulationConfig


def format_currency(amount: float) -> str:
    """Format amount as currency."""
    return f"${amount:,.2f}"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="The Recovery Roadmap - Calculate trades needed to reach target balance"
    )
    
    parser.add_argument(
        "--balance",
        type=float,
        default=200.0,
        help="Current account balance (default: $200)"
    )
    
    parser.add_argument(
        "--target",
        type=float,
        default=2000.0,
        help="Target account balance (default: $2000)"
    )
    
    parser.add_argument(
        "--risk",
        type=float,
        default=2.0,
        help="Risk per trade as percentage (default: 2%%)"
    )
    
    parser.add_argument(
        "--reward",
        type=float,
        default=3.0,
        help="Risk-to-Reward ratio (default: 3.0 for 1:3)"
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    if args.balance <= 0:
        print("Error: Current balance must be greater than 0")
        return
    
    if args.target <= args.balance:
        print("Error: Target balance must be greater than current balance")
        return
    
    if args.risk <= 0 or args.risk > 100:
        print("Error: Risk percentage must be between 0 and 100")
        return
    
    if args.reward <= 0:
        print("Error: Risk-to-Reward ratio must be greater than 0")
        return
    
    # Create configuration
    config = SimulationConfig(
        current_balance=args.balance,
        target_balance=args.target,
        risk_per_trade_percent=args.risk,
        risk_reward_ratio=args.reward
    )
    
    # Run calculation
    calculator = RecoveryRoadmapCalculator(config)
    trades = calculator.calculate()
    summary = calculator.get_summary()
    
    # Prepare table data
    table_data = []
    for trade in trades:
        table_data.append([
            trade.trade_number,
            format_currency(trade.account_balance),
            format_currency(trade.risk_amount),
            format_currency(trade.profit_amount)
        ])
    
    # Display results
    print("\n" + "="*70)
    print("THE RECOVERY ROADMAP - Perfect Execution Simulation")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  Starting Balance: {format_currency(config.current_balance)}")
    print(f"  Target Balance: {format_currency(config.target_balance)}")
    print(f"  Risk per Trade: {config.risk_per_trade_percent}%")
    print(f"  Risk-to-Reward Ratio: 1:{config.risk_reward_ratio}")
    print("\n" + "-"*70)
    print("TRADE SIMULATION RESULTS")
    print("-"*70)
    
    if table_data:
        headers = ["Trade #", "Account Balance", "Risk Amount ($)", "Profit Amount ($)"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    else:
        print("No trades needed - target already reached!")
    
    # Display summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total Trades Needed: {summary['total_trades']}")
    print(f"Max Risk Taken: {format_currency(summary['max_risk_taken'])}")
    print(f"Final Balance: {format_currency(summary['final_balance'])}")
    print("\n" + "⚠️  REALITY CHECK:")
    print("This simulation assumes zero losses (perfect execution).")
    print("With a 50%% win rate, you would need approximately {:.0f} trades.".format(
        summary['total_trades'] * 2
    ))
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
