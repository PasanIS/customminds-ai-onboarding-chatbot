import React, { useState, useEffect } from "react";
import axios from "axios";
import { RiChatSmile3Fill } from "react-icons/ri";
import ReactMarkdown from "react-markdown";

interface ChatMessage {
  sender: "user" | "bot";
  content: string;
}

const ChatPopup: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string>("");
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    getSessionId();
    // const existingSession = localStorage.getItem("chatSessionId");
    // const newSessionId = existingSession || `session_${Date.now()}`;
    // setSessionId(newSessionId);
    // localStorage.setItem("chatSessionId", newSessionId);

    // Add welcome message
    setMessages([
      {
        sender: "bot",
        content:
          "👋 **Hi there!** I’m your AI assistant.\n\nHow can I help you today?",
      },
    ]);
  }, []);

  const getSessionId = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/session/create"
      );
      setSessionId(response.data.session_id);
      localStorage.setItem("chatSessionId", response.data.session_id);
      console.log("Session created:", response.data);
    } catch (error) {
      console.error("Error creating session:", error);
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await axios.post(
        "http://localhost:8000/api/chat/start/message/",
        {
          message: input,
          session_id: sessionId,
        }
      );

      let botReply =
        response.data.reply || "🤖 Sorry, I didn’t understand that.";

      // Markdown auto-formatting for lists and paragraphs
      botReply = botReply
        .replace(/\n/g, "\n\n") // Add paragraph breaks
        .replace(/(\d+)\)\s/g, "- ") // Convert numbered parentheses lists
        .replace(/(\d+)\.\s/g, "- ") // Convert numbered lists
        .replace(/•\s/g, "- "); // Standardize bullets

      const botMessage: ChatMessage = {
        sender: "bot",
        content: botReply.trim(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", content: "⚠️ Sorry, something went wrong." },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  // Start new chat session
  const handleNewChat = () => {
    const newSessionId = `session_${Date.now()}`;
    setSessionId(newSessionId);
    localStorage.setItem("chatSessionId", newSessionId);

    // Reset messages
    setMessages([
      {
        sender: "bot",
        content: "👋 Hello again! What would you like to talk about?",
      },
    ]);
  };

  return (
    <>
      {/* Floating Chat Icon */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 w-16 h-16 rounded-full 
                     bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600 
                     text-white flex items-center justify-center shadow-lg 
                     hover:scale-110 transition-transform duration-300 animate-bounce"
        >
          <RiChatSmile3Fill size={30} />
        </button>
      )}

      {/* Chat Interface */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 w-[500px] h-[700px] bg-white shadow-2xl rounded-2xl flex flex-col overflow-hidden border border-gray-200">
          {/* Header */}
          <div
            className="bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600 
                        text-white flex items-center justify-between p-4"
          >
            <span className="font-semibold text-lg flex items-center gap-2">
              <RiChatSmile3Fill size={22} /> Chat Assistant
            </span>
            <div className="flex gap-3">
              <button
                onClick={handleNewChat}
                className="bg-white/20 hover:bg-white/30 rounded-full px-3 py-1 text-sm"
              >
                New
              </button>
              <button
                onClick={() => setIsOpen(false)}
                className="bg-white/20 hover:bg-white/30 rounded-full px-3 py-1 text-sm"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-gray-50">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${
                  msg.sender === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`px-4 py-2 rounded-2xl max-w-[70%] break-words ${
                    msg.sender === "user"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-50 text-gray-900"
                  }`}
                >
                  <ReactMarkdown>{msg.content}</ReactMarkdown>
                </div>
              </div>
            ))}

            {/* Typing Indicator */}
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-gray-200 text-gray-700 px-4 py-2 rounded-2xl text-sm animate-pulse">
                  🤖 Typing...
                </div>
              </div>
            )}
          </div>

          {/* Input */}
          <div className="p-3 border-t flex gap-2 bg-white">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
              placeholder="Type a message..."
              className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleSendMessage}
              className="bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600 
                         text-white px-4 py-2 rounded-lg hover:scale-105 transition-transform duration-200"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatPopup;
