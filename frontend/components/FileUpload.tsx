"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { UploadCloud, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { uploadDocument, getFunds } from "@/lib/api";
import { Card } from "@/components/ui/card";

export default function FileUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [funds, setFunds] = useState<any[]>([]);
  const [fundId, setFundId] = useState<number | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  useEffect(() => {
    getFunds().then(setFunds).catch(console.error);
  }, []);

  const handleUpload = async () => {
    if (!file || !fundId) {
      setStatus("error");
      return;
    }

    setIsUploading(true);
    setStatus("idle");

    try {
      await uploadDocument(file, fundId);
      setStatus("success");
      setFile(null);
    } catch (err) {
      console.error(err);
      setStatus("error");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Card className="border border-dashed border-gray-300 p-8 rounded-2xl bg-white shadow-md space-y-6 hover:shadow-lg transition-all duration-300 animate-fadeIn">
      {/* Select Fund */}
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          Select Target Fund
        </label>
        <select
          onChange={(e) => setFundId(Number(e.target.value))}
          className="w-full border rounded-lg p-2 focus:ring-2 focus:ring-blue-400"
        >
          <option value="">-- Select Fund --</option>
          {funds.map((fund) => (
            <option key={fund.id} value={fund.id}>
              {fund.name}
            </option>
          ))}
        </select>
      </div>

      {/* File Upload */}
      <label className="flex flex-col items-center justify-center border-2 border-dashed border-blue-300 rounded-xl p-8 cursor-pointer hover:bg-blue-50 transition-colors duration-300">
        <UploadCloud className="w-10 h-10 text-blue-500 mb-2" />
        <span className="text-gray-700 font-medium">
          Click or drag PDF file here
        </span>
        <span className="text-xs text-gray-500 mt-1">(PDF format only)</span>
        <Input
          type="file"
          accept=".pdf"
          className="hidden"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
      </label>

      {/* File Info */}
      {file && (
        <p className="text-sm text-gray-700 flex items-center gap-2">
          {file.name}
        </p>
      )}

      {/* Upload Button */}
      <Button
        onClick={handleUpload}
        disabled={!file || !fundId || isUploading}
        className={`w-full flex justify-center items-center gap-2 text-white ${
          isUploading ? "bg-gray-400" : "bg-blue-600 hover:bg-blue-700"
        }`}
      >
        {isUploading ? (
          <>
            <Loader2 className="animate-spin w-4 h-4" /> Uploading...
          </>
        ) : (
          "Upload File"
        )}
      </Button>

      {/* Status Pop-up */}
      {status === "success" && (
        <Card className="flex items-center justify-center gap-2 text-green-600 text-sm font-medium p-2 border border-green-300 rounded-md">
          <CheckCircle2 className="w-5 h-5" /> File uploaded successfully!
        </Card>
      )}

      {status === "error" && (
        <Card className="flex items-center justify-center gap-2 text-red-500 text-sm font-medium p-2 border border-red-300 rounded-md">
          <AlertCircle className="w-5 h-5" /> Upload failed. Please select a fund and a valid PDF file.
        </Card>
      )}
    </Card>
  );
}
