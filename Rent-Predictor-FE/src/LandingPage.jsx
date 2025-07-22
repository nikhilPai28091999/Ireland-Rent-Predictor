// components/LandingPage.jsx
import { useNavigate } from "react-router-dom";
import "./LandingPage.css";
import AnimatedText from "./AnimatedText";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="landing-card">
        <h1>
          <AnimatedText
            lines={["🏠 Welcome to the Ireland Rent Predictor"]}
            delay={0.9} // optional
            tag="h1" // optional
            className="my-custom-heading" // optional
          />
        </h1>
        <p>
          <AnimatedText
            lines={["Choose how you'd like to predict your rent:"]}
            delay={0.9} // optional
            tag="p" // optional
            className="my-custom-heading" // optional
          />
        </p>
        <div className="landing-buttons">
          <button onClick={() => navigate("/chat")}>💬 Chat with Bot</button>
          <button onClick={() => navigate("/app")}>
            📝 Enter Details Manually
          </button>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
