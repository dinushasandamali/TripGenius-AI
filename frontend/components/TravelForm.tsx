"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function TravelForm() {
  const router = useRouter();

  const [form, setForm] = useState({
    destination: "",
    budget: 1000,
    num_days: 0,
    interests: [] as string[],
    travel_style: "mid-range"
  });

  const handleSubmit = async () => {
    localStorage.setItem("travelData", JSON.stringify(form));
    router.push("/plan");
  };

  return (
    <div className="card">
      <h2>Plan Your Trip 🌍</h2>

      <input
        placeholder="Destination (Paris, Tokyo...)"
        onChange={e => setForm({ ...form, destination: e.target.value })}
      />

      <input
        type="number"
        placeholder="Budget ($)"
        onChange={e => setForm({ ...form, budget: Number(e.target.value) })}
      />

        <input
        type="number"
        placeholder="Number of Days"
        
        onChange={e => setForm({ ...form, num_days: Number(e.target.value) })}
      />

        <input
        type="text"
        placeholder="Interests (comma separated)"
        value={form.interests.join(", ")}
        onChange={e =>
          setForm({ ...form, interests: e.target.value.split(",").map(i => i.trim()) })
        }
      />

      <select
        onChange={e => setForm({ ...form, travel_style: e.target.value })}
      >
        <option value="budget">Budget</option>
        <option value="mid-range">Mid-range</option>
        <option value="luxury">Luxury</option>
      </select>

      <button onClick={handleSubmit}>
        ✨ Generate Plan
      </button>
    </div>
  );
}
