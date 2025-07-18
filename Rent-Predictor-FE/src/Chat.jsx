import { useState } from "react";
import "./Chat.css";
import axios from "axios";

function Chat() {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! Welcome to the Ireland Rent Predictor. What are you looking for?",
    },
  ]);
  const [awaitingPropertyConfirmation, setAwaitingPropertyConfirmation] =
    useState(false);

  const handleSend = async () => {
    debugger;
    if (!userInput.trim()) return;

    const newMessages = [...messages, { sender: "user", text: userInput }];
    setMessages(newMessages);

    if (awaitingPropertyConfirmation) {
      if (userInput.toLowerCase().includes("yes")) {
        setMessages((prev) => [
          ...prev,
          { type: "bot", text: "The user replied Yes" },
        ]);
        setAwaitingPropertyConfirmation(false);
        return;
      } else {
        setMessages((prev) => [
          ...prev,
          { type: "bot", text: "Okay, let me know if you change your mind!" },
        ]);
        setAwaitingPropertyConfirmation(false);
        return;
      }
    }

    try {
      const res = await axios.post("http://localhost:8000/parse-query", {
        text: userInput,
      });

      const prediction = res.data;

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `${prediction}
          `,
        },
      ]);

      if (
        prediction.includes(
          "Would you like to see the properties associated with this?"
        )
      ) {
        setAwaitingPropertyConfirmation(true);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "❌ Sorry, I couldn't process your request." },
      ]);
    }

    setUserInput("");
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`chat-bubble ${msg.sender === "user" ? "user" : "bot"}`}
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
            placeholder="Type your request..."
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
