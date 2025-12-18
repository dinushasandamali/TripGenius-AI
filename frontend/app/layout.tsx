import "../styles/main.css";
import Navbar from "@/components/Navbar";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <div style={{ maxWidth: "1200px", margin: "0 auto", padding: "20px" }}>
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}
