"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import FundMetrics from "@/components/FundMetrics";
import { getFundById, getFundMetrics } from "@/lib/api";

export default function FundDetailPage() {
  const { id } = useParams();
  const [fund, setFund] = useState<any | null>(null);
  const [metrics, setMetrics] = useState<any | null>(null);
  const [chartData, setChartData] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [fundData, metricsData] = await Promise.all([
          getFundById(Number(id)),
          getFundMetrics(Number(id)),
        ]);

        setFund(fundData);
        setMetrics(metricsData.metrics);

        // Merge all transactions
        const allTransactions = [
          ...(metricsData.capital_calls || []).map((t: any) => ({
            date: t.date,
            label: t.type || "Capital Call",
            amount: -Math.abs(t.amount),
          })),
          ...(metricsData.distributions || []).map((t: any) => ({
            date: t.date,
            label: t.type || "Distribution",
            amount: Math.abs(t.amount),
          })),
          ...(metricsData.adjustments || []).map((t: any) => ({
            date: t.date,
            label: t.type || "Adjustment",
            amount: t.amount,
          })),
        ];

        allTransactions.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

        let cumulative = 0;
        const formattedChart = allTransactions.map((t) => {
          cumulative += t.amount;
          return {
            date: t.date,
            value: cumulative,
            label: t.label,
          };
        });

        setChartData(formattedChart);
      } catch (err) {
        console.error("Failed to fetch fund data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  if (loading)
    return <p className="text-center mt-8 text-gray-500">Loading fund data...</p>;
  if (!fund)
    return (
      <div className="p-8 text-center text-gray-500">
        Fund data not found.
      </div>
    );

  return (
    <div className="p-8 space-y-8">
      <h1 className="text-3xl font-bold text-gray-800">{fund.name}</h1>
      <p className="text-gray-600">{fund.fund_type || "No fund description available"}</p>

      {metrics ? (
        <FundMetrics
          roi={metrics.IRR ? (metrics.IRR * 100).toFixed(2) : "0"}
          volatility={metrics.PIC?.toLocaleString() || "0"}
          sharpe={metrics.DPI?.toFixed(3) || "0"}
          chartData={chartData}
        />
      ) : (
        <p className="text-gray-500">No metrics data available for this fund.</p>
      )}

      <Button
        variant="default"
        className="rounded-full mt-6 bg-blue-600 text-white hover:bg-blue-700 shadow-md transition-all duration-200"
        onClick={() => history.back()}
      >
        Back
      </Button>
    </div>
  );
}
