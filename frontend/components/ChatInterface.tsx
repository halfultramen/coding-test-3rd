"use client";
import { useState, useRef, useEffect } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, AlertCircle } from "lucide-react";
import { getFunds, sendChatMessage } from "@/lib/api";

interface Message {
  sender: "user" | "bot";
  text: string;
}

interface Fund {
  id: number;
  name: string;
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    { sender: "bot", text: "Hello! How can I assist you today?" },
  ]);
  const [input, setInput] = useState("");
  const [funds, setFunds] = useState<Fund[]>([]);
  const [selectedFund, setSelectedFund] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await getFunds();
        setFunds(data);
      } catch (error) {
        console.error("Failed to load funds:", error);
        setFunds([]);
      }
    })();
  }, []);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg] as Message[]);
    setInput("");
    setIsLoading(true);

    try {
      const res = await sendChatMessage(input, selectedFund);
      const botMsg = {
        sender: "bot",
        text: res.answer || res.message || "No response from the server.",
      };
      setMessages((prev) => [...prev, botMsg] as Message[]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "An error occurred while processing your message." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <Card className="p-4 bg-white shadow-md rounded-xl">
      {/* Fund Dropdown */}
      <div className="mb-3">
        <label className="text-sm text-gray-600 font-medium mb-1 block">
          Select Target Fund:
        </label>
        <select
          value={selectedFund ?? ""}
          onChange={(e) =>
            setSelectedFund(e.target.value ? Number(e.target.value) : null)
          }
          className="border rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-blue-300 outline-none"
        >
          <option value="">All Funds (Global)</option>
          {funds.map((f) => (
            <option key={f.id} value={f.id}>
              {f.name}
            </option>
          ))}
        </select>
      </div>

      {/* Chat Box */}
      <div className="h-80 overflow-y-auto border rounded-md p-4 space-y-3 bg-gray-50">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"} animate-fadeIn`}
          >
            <div
              className={`px-4 py-2 rounded-2xl text-sm max-w-[75%] break-words ${
                msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input and Send Button */}
      <div className="flex mt-4 gap-2">
        <Input
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          className="rounded-xl px-4 py-2 shadow-sm focus:ring-2 focus:ring-blue-300 focus:outline-none transition-all"
        />
        <Button
          onClick={handleSend}
          disabled={isLoading}
          className="rounded-xl flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white transition-colors duration-300"
        >
          {isLoading ? "..." : <>Send <Send className="w-4 h-4" /></>}
        </Button>
      </div>
    </Card>
  );
}
