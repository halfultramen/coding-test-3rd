"use client";

import Link from "next/link";
import { ChartPie, UploadCloud, MessageCircle } from "lucide-react";
import TransactionTable from "@/components/TransactionTable";

export default function HomePage() {
  const menuItems = [
    {
      title: "Fund Dashboard",
      desc: "View performance metrics and key indicators for each fund.",
      href: "/funds",
      icon: <ChartPie className="w-6 h-6 text-blue-500" />,
    },
    {
      title: "Upload Documents",
      desc: "Upload fund reports to be processed automatically by our AI system.",
      href: "/upload",
      icon: <UploadCloud className="w-6 h-6 text-green-500" />,
    },
    {
      title: "Chat Assistant",
      desc: "Ask questions about uploaded fund data and receive instant insights.",
      href: "/chat",
      icon: <MessageCircle className="w-6 h-6 text-purple-500" />,
    },
  ];

  return (
    <div className="space-y-12 px-4 md:px-8 lg:px-16">
      {/* Hero Section */}
      <div className="text-center space-y-4 mt-8">
        <h1 className="text-4xl md:text-5xl font-extrabold text-gray-900">
          Welcome to the Fund Analysis Platform
        </h1>
        <p className="text-gray-600 text-lg md:text-xl max-w-3xl mx-auto">
          This platform helps you analyze fund data and documents automatically
          using advanced AI models. Navigate to the Upload section to start processing your reports.
        </p>
      </div>

      {/* Menu Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-10">
        {menuItems.map((item, index) => (
          <Link key={index} href={item.href}>
            <div className="p-6 bg-white rounded-xl shadow-md hover:shadow-xl transform hover:-translate-y-1 transition-all cursor-pointer flex flex-col gap-4 h-full">
              <div className="flex items-center gap-3">
                {item.icon}
                <h3 className="font-semibold text-gray-800 text-lg">{item.title}</h3>
              </div>
              <p className="text-gray-500 text-sm md:text-base">{item.desc}</p>
            </div>
          </Link>
        ))}
      </div>

      {/* Transaction Table */}
      <div className="mt-12">
        <TransactionTable />
      </div>
    </div>
  );
}
