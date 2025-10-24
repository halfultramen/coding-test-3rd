"use client"; 

import "./globals.css";
import { ReactNode } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, UploadCloud, MessageCircle, BarChart2, PieChart } from "lucide-react";

interface MenuItem {
  href: string;
  label: string;
  icon: React.ReactNode;
}

export default function RootLayout({ children }: { children: ReactNode }) {
  const pathname = usePathname();

  const menuItems: MenuItem[] = [
    { href: "/", label: "Dashboard", icon: <Home className="w-5 h-5" /> },
    { href: "/upload", label: "Upload", icon: <UploadCloud className="w-5 h-5" /> },
    { href: "/chat", label: "Chat", icon: <MessageCircle className="w-5 h-5" /> },
    { href: "/funds", label: "Funds", icon: <BarChart2 className="w-5 h-5" /> },
  ];

  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900 min-h-screen font-sans">
        <header className="w-full bg-white/90 backdrop-blur-md shadow-md p-4 flex items-center justify-between sticky top-0 z-50 transition-all duration-300">
          
          <h1 className="flex items-center text-2xl font-bold text-blue-700">
            <PieChart className="w-6 h-6 mr-2 text-blue-500" />
            Fund Analysis System
          </h1>

          <nav className="flex gap-4 md:gap-6 text-gray-600">
            {menuItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`flex items-center gap-2 px-3 py-2 rounded-md font-medium transition-all
                    ${isActive ? "bg-blue-100 text-blue-700 shadow-md" : "hover:bg-blue-50 hover:text-blue-600"}`}
                >
                  {item.icon}
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </header>
        <main className="p-6 md:p-10">{children}</main>
      </body>
    </html>
  );
}
