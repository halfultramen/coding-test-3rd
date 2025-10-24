"use client";

import FileUpload from "@/components/FileUpload";
import { UploadCloud } from "lucide-react";

export default function UploadPage() {
  return (
    <div className="max-w-3xl mx-auto space-y-8 p-8">
      {/* Header */}
      <div className="flex items-center gap-3 animate-fadeIn">
        <UploadCloud className="w-7 h-7 text-blue-600" />
        <h2 className="text-3xl font-bold text-gray-900">Upload Fund Documents</h2>
      </div>

      <p className="text-gray-600 text-lg animate-fadeIn delay-75">
        Upload <strong>PDF</strong> reports for the selected fund. The system will automatically process and extract key data.
      </p>

      {/* Upload Card */}
      <FileUpload />
    </div>
  );
}
