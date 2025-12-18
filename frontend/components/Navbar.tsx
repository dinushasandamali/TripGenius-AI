"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  return (
    <nav style={{
      background: "#1e293b",
      padding: "16px 20px",
      marginBottom: "20px",
      borderRadius: "12px",
    }}>
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: "16px",
      }}>
        <Link href="/" style={{
          fontSize: "24px",
          fontWeight: "bold",
          color: "white",
          textDecoration: "none",
        }}>
          🌍 TripGenius AI
        </Link>
        
        <div style={{
          display: "flex",
          gap: "16px",
        }}>
          <Link 
            href="/"
            style={{
              padding: "8px 16px",
              borderRadius: "8px",
              textDecoration: "none",
              color: pathname === "/" ? "white" : "#94a3b8",
              background: pathname === "/" ? "#680809" : "transparent",
              transition: "all 0.2s",
            }}
          >
            Home
          </Link>
          <Link 
            href="/plan"
            style={{
              padding: "8px 16px",
              borderRadius: "8px",
              textDecoration: "none",
              color: pathname === "/plan" ? "white" : "#94a3b8",
              background: pathname === "/plan" ? "#680809" : "transparent",
              transition: "all 0.2s",
            }}
          >
            Plan
          </Link>
        </div>
      </div>
    </nav>
  );
}

