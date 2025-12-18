export default function ItineraryDay({ day }: any) {
  return (
    <div className="card p-4 mb-4 border rounded-lg bg-white shadow">
      <h4>Day {day.day}</h4>

      {day.schedule.length === 0 ? (
        <p>No activities planned for this day.</p>
      ) : (
        <ul>
          {day.schedule.map((a: any, idx: number) => (
            <li key={idx}>
              {a.start} - {a.end}: {a.activity} (${a.cost})
            </li>
          ))}
        </ul>
      )}

      <p>Activity Cost: ${day.costs.activities}</p>
      <p>Meals: ${day.costs.meals}</p>
      <p>Transport: ${day.costs.transport}</p>
      <p>Total: ${day.costs.total}</p>
    </div>
  );
}
