"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { TrendingUp, Calculator, AlertTriangle } from "lucide-react"

interface Trade {
  trade_number: number
  account_balance: number
  risk_amount: number
  profit_amount: number
}

interface SimulationResponse {
  trades: Trade[]
  summary: {
    total_trades: number
    max_risk_taken: number
    final_balance: number
    starting_balance: number
    target_balance: number
  }
}

export default function Home() {
  const [currentBalance, setCurrentBalance] = useState("200")
  const [targetBalance, setTargetBalance] = useState("2000")
  const [riskPercent, setRiskPercent] = useState("2")
  const [rewardRatio, setRewardRatio] = useState("3")
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<SimulationResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(amount)
  }

  const handleSimulate = async () => {
    setLoading(true)
    setError(null)
    setResults(null)

    try {
      const response = await fetch("http://localhost:8000/api/simulate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          current_balance: parseFloat(currentBalance),
          target_balance: parseFloat(targetBalance),
          risk_per_trade_percent: parseFloat(riskPercent),
          risk_reward_ratio: parseFloat(rewardRatio),
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || "Failed to simulate")
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen p-4 md:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-4">
          <div className="flex items-center justify-center gap-3">
            <TrendingUp className="h-8 w-8 text-primary" />
            <h1 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              The Recovery Roadmap
            </h1>
          </div>
          <p className="text-muted-foreground text-lg">
            Calculate trades needed to grow your account using Risk-Reward strategy
          </p>
        </div>

        {/* Input Form */}
        <Card className="border-primary/20 shadow-lg">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calculator className="h-5 w-5" />
              Simulation Parameters
            </CardTitle>
            <CardDescription>
              Configure your trading parameters to calculate the recovery roadmap
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <Label htmlFor="balance">Current Balance ($)</Label>
                <Input
                  id="balance"
                  type="number"
                  step="0.01"
                  value={currentBalance}
                  onChange={(e) => setCurrentBalance(e.target.value)}
                  placeholder="200"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="target">Target Balance ($)</Label>
                <Input
                  id="target"
                  type="number"
                  step="0.01"
                  value={targetBalance}
                  onChange={(e) => setTargetBalance(e.target.value)}
                  placeholder="2000"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="risk">Risk per Trade (%)</Label>
                <Input
                  id="risk"
                  type="number"
                  step="0.1"
                  value={riskPercent}
                  onChange={(e) => setRiskPercent(e.target.value)}
                  placeholder="2"
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="reward">Risk-to-Reward Ratio</Label>
                <Input
                  id="reward"
                  type="number"
                  step="0.1"
                  value={rewardRatio}
                  onChange={(e) => setRewardRatio(e.target.value)}
                  placeholder="3"
                />
              </div>
            </div>
            <Button
              onClick={handleSimulate}
              disabled={loading}
              className="w-full mt-6"
              size="lg"
            >
              {loading ? "Calculating..." : "Calculate Recovery Roadmap"}
            </Button>
          </CardContent>
        </Card>

        {/* Error Message */}
        {error && (
          <Card className="border-destructive/50 bg-destructive/10">
            <CardContent className="pt-6">
              <div className="flex items-center gap-2 text-destructive">
                <AlertTriangle className="h-5 w-5" />
                <p>{error}</p>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Results */}
        {results && (
          <>
            {/* Summary Card */}
            <Card className="border-primary/20 shadow-lg">
              <CardHeader>
                <CardTitle>Summary</CardTitle>
                <CardDescription>Recovery roadmap overview</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Total Trades Needed</p>
                    <p className="text-2xl font-bold text-primary">
                      {results.summary.total_trades}
                    </p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Max Risk Taken</p>
                    <p className="text-2xl font-bold">
                      {formatCurrency(results.summary.max_risk_taken)}
                    </p>
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm text-muted-foreground">Final Balance</p>
                    <p className="text-2xl font-bold text-green-500">
                      {formatCurrency(results.summary.final_balance)}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Reality Check */}
            <Card className="border-yellow-500/20 bg-yellow-500/5">
              <CardContent className="pt-6">
                <div className="flex items-start gap-3">
                  <AlertTriangle className="h-5 w-5 text-yellow-500 mt-0.5" />
                  <div className="space-y-1">
                    <p className="font-semibold text-yellow-500">Reality Check</p>
                    <p className="text-sm text-muted-foreground">
                      This simulation assumes zero losses (perfect execution). With a 50% win rate,
                      you would need approximately{" "}
                      <span className="font-bold text-foreground">
                        {results.summary.total_trades * 2} trades
                      </span>
                      .
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Trades Table */}
            <Card className="border-primary/20 shadow-lg">
              <CardHeader>
                <CardTitle>Trade Simulation Results</CardTitle>
                <CardDescription>
                  Detailed breakdown of each trade in the recovery roadmap
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="rounded-md border overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Trade #</TableHead>
                        <TableHead>Account Balance</TableHead>
                        <TableHead>Risk Amount</TableHead>
                        <TableHead>Profit Amount</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {results.trades.map((trade) => (
                        <TableRow key={trade.trade_number}>
                          <TableCell className="font-medium">
                            {trade.trade_number}
                          </TableCell>
                          <TableCell>{formatCurrency(trade.account_balance)}</TableCell>
                          <TableCell className="text-yellow-500">
                            {formatCurrency(trade.risk_amount)}
                          </TableCell>
                          <TableCell className="text-green-500">
                            {formatCurrency(trade.profit_amount)}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </>
        )}
      </div>
    </div>
  )
}
