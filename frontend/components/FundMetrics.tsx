"use client";

import React from "react";
import { Card } from "@/components/ui/card";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import dayjs from "dayjs";

interface FundMetricsProps {
  roi: string;         // IRR (return)
  volatility: string;  // PIC (invested capital)
  sharpe: string;      // DPI (distribution ratio)
  chartData?: { date: string; value: number; label: string }[];
}

// Function to shorten numbers: 1_000_000 → 1M, 10_000 → 10K
const formatCurrencyShort = (num: number): string => {
  if (Math.abs(num) >= 1_000_000_000) return `${(num / 1_000_000_000).toFixed(1)}B`;
  if (Math.abs(num) >= 1_000_000) return `${(num / 1_000_000).toFixed(1)}M`;
  if (Math.abs(num) >= 1_000) return `${(num / 1_000).toFixed(1)}K`;
  return num.toString();
};

// Format date short
const formatDateShort = (dateStr: string): string => {
  const d = dayjs(dateStr);
  return d.format("MMM YY");
};

export default function FundMetrics({ roi, volatility, sharpe, chartData = [] }: FundMetricsProps) {
  return (
    <div className="space-y-8">
      {/* Metrics Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="p-4 text-center hover:scale-105 transition-transform duration-200">
          <p className="text-sm text-gray-500">IRR (Internal Rate of Return)</p>
          <p className="text-xl font-semibold text-green-600">{roi}%</p>
        </Card>
        <Card className="p-4 text-center hover:scale-105 transition-transform duration-200">
          <p className="text-sm text-gray-500">PIC (Invested Capital)</p>
          <p className="text-xl font-semibold text-yellow-600">${volatility}</p>
        </Card>
        <Card className="p-4 text-center hover:scale-105 transition-transform duration-200">
          <p className="text-sm text-gray-500">DPI (Distributions to Paid-In Capital)</p>
          <p className="text-xl font-semibold text-blue-600">{sharpe}</p>
        </Card>
      </div>

      {/* Fund Cashflow Chart */}
      <Card className="p-6">
        <h3 className="text-lg font-semibold mb-4">Fund Cashflow Trend</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tickFormatter={formatDateShort}
                interval="preserveStartEnd"
                minTickGap={30}
                angle={-30}
                textAnchor="end"
                height={60}
              />
              <YAxis
                tickFormatter={formatCurrencyShort}
                width={80}
              />
              <Tooltip
                formatter={(v: number) => `$${v.toLocaleString()}`}
                labelFormatter={(label) => `Date: ${dayjs(label).format("DD MMM YYYY")}`}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke="#2563eb"
                strokeWidth={2}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
}
