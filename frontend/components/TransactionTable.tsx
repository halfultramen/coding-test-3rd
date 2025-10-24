"use client";

import React, { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { getTransactions, getFunds } from "@/lib/api";

interface Transaction {
  id: number;
  date: string;
  type: string;
  amount: number;
  description: string;
  source: string;
}

interface Fund {
  id: number;
  name: string;
}

export default function TransactionTable() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [funds, setFunds] = useState<Fund[]>([]);
  const [selectedFundId, setSelectedFundId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [progress, setProgress] = useState(0);

  // Fetch fund list on mount
  useEffect(() => {
    getFunds()
      .then((data) => {
        setFunds(data);
        if (data.length > 0) setSelectedFundId(data[0].id);
      })
      .catch((err) => console.error("Failed to fetch funds:", err));
  }, []);

  // Fetch transactions when selectedFundId changes
  useEffect(() => {
    if (!selectedFundId) return;

    setLoading(true);
    setProgress(0);

    const interval = setInterval(() => {
      setProgress((prev) => Math.min(prev + 10, 90));
    }, 100);

    getTransactions(selectedFundId)
      .then((data) => {
        if (Array.isArray(data.transactions)) {
          setTransactions(data.transactions);
        } else {
          console.error("Invalid transaction data format:", data);
          setTransactions([]);
        }
      })
      .catch((err) => {
        console.error("Error fetching transactions:", err);
        setTransactions([]);
      })
      .finally(() => {
        clearInterval(interval);
        setProgress(100);
        setTimeout(() => setLoading(false), 300);
      });
  }, [selectedFundId]);

  const renderTable = (title: string, filteredTx: Transaction[], color: string) => (
    <Card className="p-4 bg-white rounded-xl shadow-lg space-y-4">
      <h3 className={`text-xl font-semibold text-center text-white p-2 rounded-md ${color}`}>
        {title}
      </h3>

      {filteredTx.length === 0 ? (
        <p className="text-gray-500 text-center">No transactions available for this category.</p>
      ) : (
        <Table className="min-w-full border-collapse text-center">
          <TableHeader>
            <TableRow className="bg-gray-100">
              <TableHead className="text-center">No.</TableHead>
              <TableHead className="text-center">Date</TableHead>
              <TableHead className="text-center">Type</TableHead>
              <TableHead className="text-center">Amount</TableHead>
              <TableHead className="text-center">Description</TableHead>
            </TableRow>
          </TableHeader>

          <TableBody>
            {filteredTx.map((tx, index) => (
              <TableRow key={`${tx.source}-${tx.id}`} className="hover:bg-gray-50 transition-colors">
                <TableCell>{index + 1}</TableCell>
                <TableCell>{tx.date}</TableCell>
                <TableCell>{tx.type}</TableCell>
                <TableCell>{tx.amount}</TableCell>
                <TableCell>{tx.description}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
    </Card>
  );

  const capitalCalls = transactions.filter((tx) => tx.source === "capital_call");
  const distributions = transactions.filter((tx) => tx.source === "distribution");
  const adjustments = transactions.filter((tx) => tx.source === "adjustment");

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold text-center text-gray-900 mb-4">
        Transaction History
      </h2>

      <div className="flex justify-center mb-6">
        <select
          value={selectedFundId ?? ""}
          onChange={(e) => setSelectedFundId(parseInt(e.target.value))}
          className="border rounded-md p-2"
        >
          {funds.map((f) => (
            <option key={f.id} value={f.id}>
              {f.name}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <div className="text-center">
          <p className="text-gray-600 mb-2">Loading transactions... {progress}%</p>
          <div className="w-3/4 mx-auto h-2 bg-gray-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
      ) : (
        <>
          {renderTable("Capital Calls", capitalCalls, "bg-blue-500")}
          {renderTable("Distributions", distributions, "bg-green-500")}
          {renderTable("Adjustments", adjustments, "bg-orange-500")}
        </>
      )}
    </div>
  );
}
