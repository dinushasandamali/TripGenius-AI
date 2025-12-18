"use client";

import { useEffect, useState } from "react";
import api from "@/services/api";
import Loader from "@/components/Loader";
// import BudgetCard from "@/components/BudgetCard";
// import ItineraryDay from "@/components/ItineraryDay";
import FinalPlan from "@/components/FinalPlan";

export default function PlanPage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const travelData = JSON.parse(localStorage.getItem("travelData") || "{}");

    if (Object.keys(travelData).length === 0) return;

    api
      .post("/create-plan", travelData)
      .then(res => {
        setData(res.data);
      })
      .catch(err => {
        console.error("Error fetching plan:", err);
      });
  }, []);

  if (!data) return <Loader />;

  return (
    <div className="container mx-auto p-6">
      {/* Budget Overview */}
      {/* <BudgetCard analysis={data.budget_analysis} /> */}

      {/* Daily Itineraries */}
      {/* <div className="mt-6">
        {data.daily_itineraries.map((d: any) => (
        ))}
      </div> */}

      {/* Final AI Plan */}
      <div style={{ marginTop: "24px" }}>
        <FinalPlan plan={data.final_plan} />
      </div>
    </div>
  );
}
