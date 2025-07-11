import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RentInfluence from "./RentInfluence";

createRoot(document.getElementById("root")).render(
  <Router>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/influences" element={<RentInfluence />} />
    </Routes>
  </Router>
);
