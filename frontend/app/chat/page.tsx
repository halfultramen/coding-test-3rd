"use client";

import ChatInterface from "@/components/ChatInterface";
import { MessageCircle } from "lucide-react";

export default function ChatPage() {
  return (
    <div className="max-w-3xl mx-auto p-8 space-y-6">
      <div className="flex items-center gap-3 animate-fadeIn">
        <MessageCircle className="w-6 h-6 text-purple-500" />
        <h1 className="text-3xl font-bold text-gray-900">Chat Assistant</h1>
      </div>
      <p className="text-gray-600 text-lg animate-fadeIn delay-75">
        Ask any questions about the uploaded fund data. The system will provide automated responses.
      </p>

      <ChatInterface />
    </div>
  );
}
