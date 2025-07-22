import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import RentInfluence from "./RentInfluence";
import Chat from "./Chat";
import LandingPage from "./LandingPage";
import Listings from "./listings.jsx";

createRoot(document.getElementById("root")).render(
  <Router>
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/chat" element={<Chat />} />
      <Route path="/app" element={<App />} />
      <Route path="/influences" element={<RentInfluence />} />
      <Route path="/listings" element={<Listings />} />
    </Routes>
  </Router>
);
