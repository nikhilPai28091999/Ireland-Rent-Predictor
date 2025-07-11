import { useEffect, useState } from "react";
import axios from "axios";
import "./RentInfluence.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { useNavigate } from "react-router-dom";

function RentInfluence() {
  const [data, setData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    console.log("In Use Effect");
    axios
      .get("http://localhost:8000/feature-importance")
      .then((res) => setData(res.data))
      .catch(console.error);
  }, []);

  return (
    <>
      <div className="chart-container">
        {console.log("in return")}
        <h3>📊 What Influences Rent the Most?</h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data.slice(0, 10)} layout="vertical">
            <XAxis type="number" stroke="#888" tick={{ fill: "#444" }} />
            <YAxis
              dataKey="feature"
              type="category"
              stroke="#888"
              tick={{ fill: "#333", fontSize: 10, fontWeight: 700 }}
            />
            <Tooltip />
            <Bar
              dataKey="importance"
              fill="#8884d8"
              isAnimationActive={true}
              animationDuration={1000}
            />
            <defs>
              <linearGradient id="barGradient" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#84fab0" />
                <stop offset="100%" stopColor="#8fd3f4" />
              </linearGradient>
            </defs>
          </BarChart>
        </ResponsiveContainer>
        <button onClick={() => navigate("/")}>Back</button>
      </div>
    </>
  );
}

export default RentInfluence;
