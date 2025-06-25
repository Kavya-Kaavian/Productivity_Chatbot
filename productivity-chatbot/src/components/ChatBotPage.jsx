import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import Image from "../assets/chatbotimgs.png";
import Imageinfo from "../assets/paragraph.png";
import headerImage from "../assets/K3.png";
import "./ChatBotPage.css";
import { IoSend } from "react-icons/io5";

const ChatLayout = () => {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hello! How can I help you?" },
  ]);
  const [input, setInput] = useState("");

  const chatBodyRef = useRef(null);

  useEffect(() => {
    if (chatBodyRef.current) {
      chatBodyRef.current.scrollTop = chatBodyRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
  const trimmedInput = input.trim();
  if (!trimmedInput) return;

  // Add user message first (without delay)
  setMessages((prev) => [...prev, { from: "user", text: trimmedInput }]);
  setInput(""); // Clear input immediately for smooth UX

  try {
    const response = await axios.post("http://127.0.0.1:8000/api/assistant/ask", {
      question: trimmedInput,
    });

    setMessages((prev) => [...prev, { from: "bot", text: response.data.reply }]);
  } catch (error) {
    console.error("Error sending message:", error);
    setMessages((prev) => [...prev, { from: "bot", text: "Error getting response" }]);
  }
};

  return (
    <>
      <div className="chat-header">
        <img src={headerImage} alt="Header" className="side-image" />
        Productivity Chatbot
      </div>

      <div className="chat-container">
        <div className="left-panel">
          <img src={Imageinfo} alt="Info" className="side-main-image" />
          <div className="image-area">
            <img src={Image} alt="Bot" className="side-image" />
          </div>
        </div>

        <div className="right-panel">
          <div className="chat-body" ref={chatBodyRef}>
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.from}`}>
                {msg.text}
              </div>
            ))}
          </div>

          <div className="chat-footer">
            <input
              type="text"
              placeholder="Type a message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
            />
            <button onClick={handleSend}>
              <IoSend />
            </button>
          </div>

          <div className="window-footer">© 2025 K³ Chatbot Created by KKK</div>
        </div>
      </div>
    </>
  );
};

export default ChatLayout;
