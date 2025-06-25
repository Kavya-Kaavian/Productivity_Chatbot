import React, { useState } from "react";
import axios from "axios";
import Image from '../assets/chatbotimgs.png'
import Imageinfo from '../assets/paragraph.png'
import headerImage from '../assets/K3.png'
import "./ChatBotPage.css";
import { IoSend } from "react-icons/io5";


const ChatLayout = () => {
  const [messages, setMessages] = useState([
    { from: "bot", text: "Hello! How can I help you?" },
  ]);
  const [input, setInput] = useState("");

 const handleSend = async () => {
  if (input.trim()) {
    console.log(input); 
    setMessages([...messages, { from: "user", text: input }]);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/assistant/ask", {
        question: input, 
      });

      console.log("Backend response:", response.data);

      setMessages((prev) => [...prev, { from: "bot", text: response.data.reply }]);

    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prev) => [...prev, { from: "bot", text: "Error getting response" }]);
    }
    setInput("");
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
          <img src={Imageinfo} alt="user visual" className="side-main-image" />
          <div className="image-area">
            <img src={Image} alt="User visual" className="side-image" />
          </div>
        </div>

        <div className="right-panel">
          <div className="chat-body">
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
          <button onClick={handleSend}><IoSend /></button>
          </div>
        <div className="window-footer"> &copy; 2025 K³ Chatbot </div>
        </div>
      </div>
    </>
  );
};

export default ChatLayout;
