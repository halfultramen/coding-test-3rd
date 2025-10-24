"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { BarChart2, Plus, AlertCircle } from "lucide-react";
import { getFunds, createFund, deleteFund } from "@/lib/api";

export default function FundsPage() {
  const [funds, setFunds] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [openAdd, setOpenAdd] = useState(false);
  const [popupMessage, setPopupMessage] = useState<string | null>(null);
  const [confirmDelete, setConfirmDelete] = useState<{ id: number; name: string } | null>(null);

  const [form, setForm] = useState({
    name: "",
    gp_name: "",
    fund_type: "",
    vintage_year: "",
  });

  // Fetch initial fund data
  useEffect(() => {
    const fetchFunds = async () => {
      try {
        const data = await getFunds();
        setFunds(data);
      } catch (err) {
        console.error("Failed to fetch funds:", err);
        setPopupMessage("Failed to fetch fund data.");
      } finally {
        setLoading(false);
      }
    };
    fetchFunds();
  }, []);

  // Submit new fund
  const handleSubmit = async () => {
    if (!form.name.trim()) {
      setPopupMessage("Fund name is required!");
      return;
    }

    try {
      const newFund = await createFund({
        name: form.name,
        gp_name: form.gp_name || undefined,
        fund_type: form.fund_type || undefined,
        vintage_year: form.vintage_year ? parseInt(form.vintage_year) : undefined,
      });

      setFunds((prev) => [...prev, newFund]);
      setOpenAdd(false);
      setForm({ name: "", gp_name: "", fund_type: "", vintage_year: "" });
      setPopupMessage(`Fund "${newFund.name}" has been successfully created!`);
    } catch (err) {
      console.error(err);
      setPopupMessage("Failed to create a new fund.");
    }
  };

  // Delete fund
  const handleConfirmDelete = async () => {
    if (!confirmDelete) return;

    try {
      await deleteFund(confirmDelete.id);
      setFunds((prev) => prev.filter((f) => f.id !== confirmDelete.id));
      setPopupMessage(`Fund "${confirmDelete.name}" has been deleted successfully.`);
    } catch (err) {
      console.error(err);
      setPopupMessage(`Failed to delete fund "${confirmDelete.name}".`);
    } finally {
      setConfirmDelete(null);
    }
  };

  if (loading)
    return <p className="text-center mt-8 text-gray-500">Loading funds...</p>;

  return (
    <div className="p-8 space-y-8">
      <h1 className="text-3xl font-bold text-center text-gray-800">Fund List</h1>

      {/* Popup Message */}
      {popupMessage && (
        <Dialog open={true} onOpenChange={() => setPopupMessage(null)}>
          <DialogContent className="sm:max-w-[400px]">
            <DialogHeader>
              <DialogTitle>Notification</DialogTitle>
            </DialogHeader>
            <p>{popupMessage}</p>
            <div className="flex justify-end mt-4">
              <Button className="rounded-xl" onClick={() => setPopupMessage(null)}>Close</Button>
            </div>
          </DialogContent>
        </Dialog>
      )}

      {/* Delete Confirmation Dialog */}
      <Dialog open={!!confirmDelete} onOpenChange={() => setConfirmDelete(null)}>
        <DialogContent className="sm:max-w-[400px]">
          <DialogHeader>
            <DialogTitle>Confirm Deletion</DialogTitle>
          </DialogHeader>
          <p className="flex items-center gap-2">
            <AlertCircle className="w-5 h-5 text-red-500" />
            Are you sure you want to delete the fund "{confirmDelete?.name}" and all its data?
          </p>
          <div className="flex justify-end gap-3 mt-4">
            <Button className="rounded-xl" variant="outline" onClick={() => setConfirmDelete(null)}>
              Cancel
            </Button>
            <Button className="bg-red-600 text-white rounded-xl" onClick={handleConfirmDelete}>
              Delete
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Add Fund */}
      <div className="flex justify-end">
        <Dialog open={openAdd} onOpenChange={setOpenAdd}>
          <DialogTrigger asChild>
            <Button className="bg-blue-600 text-white flex gap-2 rounded-xl">
              <Plus className="w-4 h-4" /> Add Fund
            </Button>
          </DialogTrigger>

          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>Add New Fund</DialogTitle>
            </DialogHeader>

            <div className="space-y-4 py-2">
              <div>
                <Label>Fund Name</Label>
                <Input
                  placeholder="Example: Tech Growth Fund I"
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  className=""
                />
              </div>
              <div>
                <Label>GP Name (General Partner)</Label>
                <Input
                  placeholder="Example: Example Capital"
                  value={form.gp_name}
                  onChange={(e) => setForm({ ...form, gp_name: e.target.value })}
                />
              </div>
              <div>
                <Label>Fund Type</Label>
                <Input
                  placeholder="Example: Venture Capital"
                  value={form.fund_type}
                  onChange={(e) => setForm({ ...form, fund_type: e.target.value })}
                />
              </div>
              <div>
                <Label>Vintage Year</Label>
                <Input
                  type="number"
                  placeholder="Example: 2020"
                  value={form.vintage_year}
                  onChange={(e) => setForm({ ...form, vintage_year: e.target.value })}
                />
              </div>
            </div>

            <div className="flex justify-end gap-3 mt-4">
              <Button className="rounded-xl" variant="outline" onClick={() => setOpenAdd(false)}>
                Cancel
              </Button>
              <Button className="bg-blue-600 text-white rounded-xl" onClick={handleSubmit}>
                Save
              </Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {/* Fund Cards */}
      {funds.length === 0 ? (
        <p className="text-gray-500">No fund data available.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {funds.map((fund) => (
            <Card
              key={fund.id}
              className="p-6 border border-gray-200 rounded-2xl shadow-lg hover:shadow-2xl transform hover:-translate-y-2 transition-all duration-300 flex flex-col justify-between"
            >
              <div>
                <h2 className="text-xl font-semibold mb-1">{fund.name}</h2>
                <p className="text-gray-600 text-sm mb-2">
                  {fund.fund_type || "Fund type not available"}
                </p>
                <span className="px-3 py-1 text-sm rounded-full font-medium bg-blue-100 text-blue-700">
                  Vintage: {fund.vintage_year || "-"}
                </span>
              </div>

              <div className="flex justify-between items-center mt-4">
                <Link href={`/funds/${fund.id}`}>
                  <Button
                    variant="default"
                    className="flex items-center gap-2 rounded-full bg-blue-600 text-white hover:bg-blue-700 shadow-md transition-all duration-200"
                  >
                    <BarChart2 className="w-4 h-4" />
                    View Details
                  </Button>
                </Link>

                <Button
                  variant="destructive"
                  className="bg-red-600 text-white hover:bg-red-700 shadow-md rounded-full transition-all duration-200"
                  onClick={() => setConfirmDelete({ id: fund.id, name: fund.name })}
                >
                  Delete Fund
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
