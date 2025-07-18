// components/AnimatedText.jsx
import React from "react";
import "./AnimatedText.css";

const AnimatedText = ({ lines = [], delay = 1, tag = "p", className = "" }) => {
  const Tag = tag;

  return (
    <div className={`animated-text-wrapper ${className}`}>
      {lines.map((line, index) => (
        <Tag
          key={index}
          className="animated-line"
          style={{ animationDelay: `${index * delay}s` }}
        >
          {line}
        </Tag>
      ))}
    </div>
  );
};

export default AnimatedText;
