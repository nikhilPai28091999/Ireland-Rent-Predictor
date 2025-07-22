import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./App.css";

function App() {
  const [bed, setBed] = useState("");
  const [bath, setBath] = useState("");
  const [location, setLocation] = useState("");
  const [utilities, setUtilities] = useState([]);
  const [showDropdown, setShowDropdown] = useState(false);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const utilityOptions = [
    "Parking",
    "Gym",
    "Pets Allowed",
    "Microwave",
    "Central Heating",
    "Washing Machine",
    "Dryer",
    "Dishwasher",
    "Internet",
    "Garden / Patio / Balcony",
  ];

  const handleUtilityChange = (utility) => {
    setUtilities((prev) =>
      prev.includes(utility)
        ? prev.filter((u) => u !== utility)
        : [...prev, utility]
    );
  };

  const handleBack = () => {
    navigate("/");
  };

  const handlePredict = async () => {
    if (!bed || !bath || !location) {
      setError("All fields are required.");
      setPrediction(null);
      return;
    }

    try {
      const response = await axios.post("http://localhost:8000/predict", {
        bed: parseFloat(bed),
        bath: parseFloat(bath),
        location,
        utilities,
      });

      setPrediction(response.data.predicted_rent);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Could not connect to the API. Make sure FastAPI is running.");
    }
  };

  const handleInfluenceRent = () => {};

  return (
    <>
      <button className="back-button" onClick={handleBack}>
        Back to Homepage
      </button>
      <div className="container">
        <h2>🏡 Ireland Rent Predictor</h2>
        <div className="form-group">
          <label>Bedrooms</label>
          <input
            type="number"
            value={bed}
            onChange={(e) => setBed(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Bathrooms</label>
          <input
            type="number"
            value={bath}
            onChange={(e) => setBath(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Location (e.g., Dublin 8)</label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Utilities (can choose more than 1)</label>
          <div className="multi-select-wrapper">
            <div
              className="multi-select-display"
              onClick={() => setShowDropdown(!showDropdown)}
            >
              <div className="selected-display">
                {utilities.length > 0 ? (
                  <span>
                    {utilities.length} selected: {utilities.join(", ")}
                  </span>
                ) : (
                  <span className="placeholder">Select utilities...</span>
                )}
              </div>
              <span className="dropdown-arrow">▼</span>
            </div>
            {showDropdown && (
              <div className="dropdown-options">
                {utilityOptions.map((utility) => (
                  <div
                    key={utility}
                    className={`option-item ${
                      utilities.includes(utility) ? "selected" : ""
                    }`}
                    onClick={() => handleUtilityChange(utility)}
                  >
                    <span className="checkbox-custom">
                      {utilities.includes(utility) && "✓"}
                    </span>
                    {utility}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
        <button onClick={handlePredict}>Predict Rent</button>
        <button onClick={() => navigate("/influences")}>
          What influences rent?{" "}
        </button>
        ;
        {prediction && (
          <div className="result">
            💶 Estimated Rent: <strong>€{prediction}</strong>
          </div>
        )}
        {error && <div className="error">{error}</div>}
      </div>
    </>
  );
}

export default App;
