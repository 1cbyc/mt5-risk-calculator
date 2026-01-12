# The Recovery Roadmap

A trading utility that calculates exactly how many trades it takes to grow an account from a starting balance to a target balance using a fixed Risk-Reward strategy.

## Features

- **Perfect Execution Simulation**: Shows the best-case scenario assuming all trades are winners
- **Flexible Configuration**: Customize starting balance, target balance, risk percentage, and risk-reward ratio
- **Multiple Interfaces**: 
  - Command-line interface (CLI)
  - Web interface with modern UI
- **Detailed Output**: Formatted tables showing each trade with balance, risk, and profit

## Installation

### Python Dependencies

```bash
pip install -r requirements.txt
```

### Frontend Dependencies

```bash
cd frontend
npm install
```

## Usage

### CLI Usage

Run the CLI script with default values:

```bash
python cli.py
```

Or customize the parameters:

```bash
python cli.py --balance 500 --target 5000 --risk 2.5 --reward 3.0
```

**CLI Options:**
- `--balance`: Current account balance (default: $200)
- `--target`: Target account balance (default: $2000)
- `--risk`: Risk per trade as percentage (default: 2%)
- `--reward`: Risk-to-Reward ratio (default: 3.0 for 1:3)

### Web Interface

1. Start the FastAPI backend:

```bash
python api.py
```

The API will be available at `http://localhost:8000`

2. Start the Next.js frontend:

```bash
cd frontend
npm run dev
```

The web interface will be available at `http://localhost:3000`

## How It Works

The Recovery Roadmap simulates perfect execution trading:

1. For each trade iteration:
   - Calculates the dollar risk based on current balance and risk percentage
   - Calculates the dollar profit based on risk-reward ratio
   - Adds profit to the account balance (assuming a win)

2. Continues until the target balance is reached

3. Displays all trades in a formatted table

4. Provides a summary with:
   - Total trades needed
   - Maximum risk taken
   - Reality check reminder

## Important Notes

**This simulation assumes perfect execution (100% win rate).**

In reality, with a 50% win rate, you would need approximately **double** the number of trades shown. Always consider:
- Actual win rate
- Market conditions
- Psychological factors
- Risk management

## Project Structure

```
mt5-risk-calculator/
├── recovery_roadmap/      # Core calculation module
│   ├── __init__.py
│   └── core.py
├── cli.py                  # Command-line interface
├── api.py                  # FastAPI backend
├── frontend/               # Next.js web interface
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── README.md
```

## License

MIT
