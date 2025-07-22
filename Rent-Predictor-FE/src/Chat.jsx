import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import "./Chat.css";
import axios from "axios";

function Chat() {
  const buttonRef = useRef();
  const navigate = useNavigate();

  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! Welcome to the Ireland Rent Predictor. What are you looking for?",
    },
  ]);
  const [lastPrediction, setLastPrediction] = useState(null); // Save prediction object
  const [lastBotMessage, setLastBotMessage] = useState(""); // Save last bot response

  const handleBack = () => {
    navigate("/");
  };

  const handleSend = async () => {
    if (!userInput.trim()) return;

    // Add user message to chat
    const newMessages = [...messages, { sender: "user", text: userInput }];
    setMessages(newMessages);

    if (
      lastBotMessage.startsWith("The estimated rent would be around €") &&
      userInput.trim().toLowerCase() === "yes" &&
      typeof lastPrediction === "number"
    ) {
      try {
        const res = await axios.post("http://localhost:8000/listings", {
          predicted_rent: lastPrediction,
        });

        const { predicted_rent, matching_properties } = res.data;

        if (!matching_properties || matching_properties.length === 0) {
          setMessages((prev) => [
            ...prev,
            { sender: "bot", text: "No properties found in this price range." },
          ]);
        } else {
          navigate("/listings", {
            state: {
              predicted_rent,
              matching_properties,
            },
          });
        }
      } catch (err) {
        console.error("Error:", err);
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: "❌ Failed to fetch properties." },
        ]);
      }

      setUserInput("");
      return;
    }

    try {
      const res = await axios.post("http://localhost:8000/analyze-message", {
        text: userInput,
      });

      const { reply, prediction } = res.data;

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: reply,
        },
      ]);

      if (
        reply.startsWith("The estimated rent would be around €") &&
        prediction
      ) {
        setLastPrediction(parseFloat(prediction));
        setLastBotMessage(reply);
      } else {
        setLastPrediction(null);
        setLastBotMessage(reply);
      }
    } catch (err) {
      console.error("Error:", err);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "❌ Sorry, I couldn't process your request." },
      ]);
    }

    setUserInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      buttonRef.current.click(); // Simulates button click
    }
  };

  return (
    <>
      <button className="back-button" onClick={handleBack}>
        Back to Homepage
      </button>
      <div className="chat-container">
        <div className="chat-box">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-bubble ${
                msg.sender === "user" ? "user" : "bot"
              }`}
            >
              {msg.text}
            </div>
          ))}
        </div>

        <div className="chat-input">
          <div className="chat-input-wrapper">
            <input
              type="text"
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your request..."
            />
            <button ref={buttonRef} onClick={handleSend}>
              Send
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

export default Chat;
