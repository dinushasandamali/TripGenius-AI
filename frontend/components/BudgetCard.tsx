export default function BudgetCard({ analysis }: any) {
  return (
    <div className="card">
      <h3>💰 Budget</h3>
      <p>Total Budget: ${analysis.budget}</p>
      <p>Total Spent: ${analysis.total_cost}</p>
      <p>Remaining: ${analysis.difference}</p>
    </div>
  );
}
