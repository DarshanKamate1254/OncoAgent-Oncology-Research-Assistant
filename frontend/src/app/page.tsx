"use client";

import React, { useEffect, useState } from "react";

export default function Home() {
  const [data, setData] = useState<{ message: string; status: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/message")
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then((jsonData) => {
        setData(jsonData);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        setError(err.message || "Failed to load message");
        setLoading(false);
      });
  }, []);

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      fontFamily: "system-ui, sans-serif",
      backgroundColor: "#0a0a0a",
      color: "#ffffff",
      gap: "1rem"
    }}>
      <h1 style={{ fontSize: "2.5rem", fontWeight: 600 }}>Hello World</h1>
      
      <div style={{
        padding: "1rem 2rem",
        borderRadius: "8px",
        backgroundColor: "rgba(255, 255, 255, 0.05)",
        border: "1px solid rgba(255, 255, 255, 0.1)",
        fontSize: "1.2rem",
        color: "#0df2c9",
        minHeight: "3rem",
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
      }}>
        {loading && <span style={{ color: "#8b5cf6" }}>Fetching message from backend...</span>}
        {error && <span style={{ color: "#ef4444" }}>Error: {error}</span>}
        {data && <span>{data.message}</span>}
      </div>
    </div>
  );
}
