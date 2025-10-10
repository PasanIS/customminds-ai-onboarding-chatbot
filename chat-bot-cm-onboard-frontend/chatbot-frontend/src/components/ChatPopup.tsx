import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { FaRobot } from "react-icons/fa";

interface ChatMessage {
  sender: "user" | "bot";
  content: string;
}

const ChatPopup: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // -----Scroll to bottom (new message)
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: ChatMessage = { sender: "user", content: input };
    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/chat/", {
        message: input,
      });

      if (response.data.reply) {
        const botMessage: ChatMessage = { sender: "bot", content: response.data.reply };
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (error) {
      console.error(error);
      const errorMsg: ChatMessage = { sender: "bot", content: "Error: Could not reach server." };
      setMessages(prev => [...prev, errorMsg]);
    }

    setInput("");
  };

  return (
    <div className="fixed bottom-5 right-5 z-50">
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="w-16 h-16 rounded-full bg-blue-500 text-white flex items-center justify-center shadow-lg hover:bg-blue-600 transition"
        >
          <FaRobot size={24} />
        </button>
      )}

      {isOpen && (
        <div className="w-80 h-[500px] bg-white shadow-xl rounded-lg flex flex-col">
          {/* Header */}
          <div className="flex justify-between items-center p-2 bg-blue-500 text-white rounded-t-lg">
            <span>Chatbot</span>
            <button onClick={() => setIsOpen(false)} className="font-bold">X</button>
          </div>

          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto p-2 bg-gray-50">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`mb-2 flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div className={`px-4 py-2 rounded-lg max-w-xs ${msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-gray-800"}`}>
                  {msg.content}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="flex gap-2 p-2 border-t">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === "Enter" && sendMessage()}
              placeholder="Type your message..."
              className="flex-1 px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
            <button
              onClick={sendMessage}
              className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition"
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatPopup;
