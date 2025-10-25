import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { RiChatSmile3Fill } from "react-icons/ri";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

interface ChatMessage {
  sender: "user" | "bot";
  content: string;
  interrupt?: boolean;
}

interface ApiMessage {
  sender: string;
  content: string;
}

const ChatPopup: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string>("");
  const [isTyping, setIsTyping] = useState(false);
  const [isPaused, setIsPaused] = useState(false); // Human in the loop interrupt

  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const abortController = useRef<AbortController | null>(null);

  // Load chat history
  useEffect(() => {
    const storedSession = localStorage.getItem("chatSessionId");
    if (storedSession) {
      setSessionId(storedSession);
      loadChatHistory(storedSession); // Load past 10 messages
    } else {
      getSessionId();
    }
  }, []);

  // Scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  // Initialize session and welcome message
  // useEffect(() => {
  //   getSessionId();

  //   setMessages([
  //     {
  //       sender: "bot",
  //       content:
  //         "👋 **Hi there!** I’m your AI assistant.\n\nHow can I help you today?",
  //     },
  //   ]);
  // }, []);

  // const getSessionId = async () => {
  //   try {
  //     const response = await axios.post(
  //       "http://localhost:8000/api/session/create"
  //     );
  //     setSessionId(response.data.session_id);
  //     localStorage.setItem("chatSessionId", response.data.session_id);
  //     console.log("Session created:", response.data);
  //   } catch (error) {
  //     console.error("Error creating session:", error);
  //   }
  // };

  const getSessionId = async () => {
    try {
      const response = await axios.post(
        "http://localhost:8000/api/session/create"
      );
      const newId = response.data.session_id;
      setSessionId(newId);
      localStorage.setItem("chatSessionId", response.data.session_id);

      // Welcome on first chat
      setMessages([
        {
          sender: "bot",
          content:
            "👋 **Hi there!** I’m your AI assistant.\n\nHow can I help you today?",
        },
      ]);
    } catch (error) {
      console.error("Error creating session:", error);
    }
  };

  // Load chat history->BcEnd
  const loadChatHistory = async (id: string) => {
    try {
      const res = await axios.get(
        `http://localhost:8000/api/chat/start/history/${id}`
      );
      if (res.data && res.data.length > 0) {
        const formatted = res.data.map((m: ApiMessage) => ({
          sender: m.sender as "user" | "bot",
          content: m.content,
        }));
        setMessages(formatted);
      } else {
        setMessages([
          {
            sender: "bot",
            content:
              "👋 **Hi there!** I’m your AI assistant.\n\nHow can I help you today?",
          },
        ]);
      }
    } catch (err) {
      console.error("Error loading chat history:", err);
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() || isPaused) return;

    const userMessage: ChatMessage = { sender: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    const controller = new AbortController();
    abortController.current = controller;

    try {
      const response = await axios.post(
        "http://localhost:8000/api/chat/start/message",
        { message: input, session_id: sessionId }
      );

      if (response.data.session_id) {
        setSessionId(response.data.session_id);
        localStorage.setItem("chatSessionId", response.data.session_id);
      }

      let botReply =
        response.data.reply || "🤖 Sorry, I didn’t understand that.";
      const isInterrupt = response.data.interrupt || false;

      botReply = botReply
        .replace(/\n/g, "\n\n")
        .replace(/(\d+)\)\s/g, "- ")
        .replace(/(\d+)\.\s/g, "- ")
        .replace(/•\s/g, "- ");

      const botMessage: ChatMessage = {
        sender: "bot",
        content: botReply.trim(),
        interrupt: isInterrupt,
      };

      setMessages((prev) => [...prev, botMessage]);

      // Pause chat
      if (isInterrupt) {
        setIsPaused(true);
      }
    } catch (error: unknown) {
      if (error instanceof DOMException && error.name === "AbortError") {
        setMessages((prev) => [
          ...prev,
          { sender: "bot", content: "⏸️ Reply stopped." },
        ]);
      } else {
        console.error("Chat error:", error);
        setMessages((prev) => [
          ...prev,
          { sender: "bot", content: "⚠️ Sorry, something went wrong." },
        ]);
      }
    } finally {
      setIsTyping(false);
    }
  };

  const handleStop = () => {
    abortController.current?.abort();
  };

  const handleNewChat = async () => {
    await getSessionId();

    setMessages([
      {
        sender: "bot",
        content: "👋 Hello again! What would you like to talk about?",
      },
    ]);
  };

  const togglePause = () => {
    setIsPaused((prev) => !prev);
    if (!isPaused) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          content: "👤 Conversation paused for human review...",
        },
      ]);
    } else {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", content: "✅ Resuming automated conversation..." },
      ]);
    }
  };

  return (
    <>
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

      {isOpen && (
        <div className="fixed bottom-6 right-6 w-[400px] h-[500px] bg-white shadow-2xl rounded-2xl flex flex-col overflow-hidden border border-gray-200">
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
                onClick={togglePause}
                className="bg-white/20 hover:bg-white/30 rounded-full px-3 py-1 text-sm"
              >
                {isPaused ? "Resume" : "Pause"}
              </button>
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
                  className={`px-4 py-2 rounded-2xl max-w-[70%] break-words transition-all duration-300
                    ${
                      msg.sender === "user"
                        ? "bg-blue-500 text-white"
                        : msg.interrupt
                        ? "bg-yellow-100 text-gray-800 border border-yellow-300 shadow-md"
                        : "bg-gray-200 text-gray-900"
                    }`}
                >
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeRaw]}
                  >
                    {msg.content}
                  </ReactMarkdown>
                  {msg.interrupt && (
                    <div className="text-xs text-gray-600 mt-1">
                      ⏸️ (Bot is waiting for your answer to continue...)
                    </div>
                  )}
                </div>
              </div>
            ))}

            <div ref={messagesEndRef} />

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
              placeholder={
                isPaused ? "Paused for human review..." : "Type a message..."
              }
              disabled={isPaused}
              className="flex-1 border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-60"
            />
            <button
              onClick={isTyping ? handleStop : handleSendMessage}
              className={`${
                isTyping
                  ? "bg-red-500 hover:bg-red-600"
                  : "bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600"
              } text-white px-4 py-2 rounded-lg hover:scale-105 transition-transform duration-200`}
              disabled={isPaused}
            >
              {isTyping ? "Stop" : "Send"}
            </button>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatPopup;
