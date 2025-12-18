"use client";

export default function FinalPlan({ plan }: { plan: string }) {
  // Parse the plan text into sections
  const parsePlan = (text: string) => {
    const lines = text.split('\n').filter(line => line.trim());
    const sections: { type: 'header' | 'list' | 'paragraph'; content: string; items?: string[] }[] = [];
    let currentParagraph: string[] = [];

    lines.forEach((line) => {
      const trimmed = line.trim();
      
      // Check if it's a header (starts with # or is all caps or has specific patterns)
      if (trimmed.match(/^#{1,3}\s+/) || 
          (trimmed.length < 50 && trimmed.match(/^[A-Z][A-Za-z\s&:]+$/)) ||
          trimmed.match(/^[A-Z\s]+:$/) ||
          trimmed.match(/^Day \d+/i) ||
          trimmed.match(/^Overview|Summary|Tips|Important|Notes?:$/i)) {
        // Save current paragraph if exists
        if (currentParagraph.length > 0) {
          sections.push({
            type: 'paragraph',
            content: currentParagraph.join(' ')
          });
          currentParagraph = [];
        }
        
        // Add header
        sections.push({
          type: 'header',
          content: trimmed.replace(/^#+\s*/, '')
        });
      }
      // Check if it's a list item (starts with -, •, *, or numbers)
      else if (trimmed.match(/^[-•*]\s+/) || trimmed.match(/^\d+[\.\)]\s+/)) {
        // Save current paragraph if exists
        if (currentParagraph.length > 0) {
          sections.push({
            type: 'paragraph',
            content: currentParagraph.join(' ')
          });
          currentParagraph = [];
        }
        
        // Check if last section is a list, append to it
        if (sections.length > 0 && sections[sections.length - 1].type === 'list') {
          sections[sections.length - 1].items!.push(trimmed.replace(/^[-•*\d+\.\)]\s+/, ''));
        } else {
          sections.push({
            type: 'list',
            content: '',
            items: [trimmed.replace(/^[-•*\d+\.\)]\s+/, '')]
          });
        }
      }
      // Regular text line
      else {
        if (trimmed.length > 0) {
          currentParagraph.push(trimmed);
        }
      }
    });

    // Add remaining paragraph
    if (currentParagraph.length > 0) {
      sections.push({
        type: 'paragraph',
        content: currentParagraph.join(' ')
      });
    }

    return sections;
  };

  const sections = parsePlan(plan);

  return (
    <div className="card" style={{
      background: "linear-gradient(135deg, #1e293b 0%, #0f172a 100%)",
      border: "1px solid #334155",
      position: "relative",
      overflow: "hidden",
    }}>
      {/* Decorative gradient overlay */}
      <div style={{
        position: "absolute",
        top: 0,
        right: 0,
        width: "200px",
        height: "200px",
        background: "radial-gradient(circle, rgba(104, 8, 9, 0.3) 0%, transparent 70%)",
        pointerEvents: "none",
      }} />
      
      <div style={{ position: "relative", zIndex: 1 }}>
        <div style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          marginBottom: "24px",
          paddingBottom: "16px",
          borderBottom: "2px solid #334155",
        }}>
          <span style={{ fontSize: "32px" }}>🧠</span>
          <h3 style={{
            fontSize: "28px",
            fontWeight: "bold",
            color: "white",
            margin: 0,
            background: "linear-gradient(135deg, #fff 0%, #94a3b8 100%)",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}>
            Final AI Plan
          </h3>
        </div>

        <div style={{ lineHeight: "1.8", color: "#e2e8f0" }}>
          {sections.length > 0 ? (
            sections.map((section, idx) => {
              if (section.type === 'header') {
                return (
                  <h4 key={idx} style={{
                    fontSize: "20px",
                    fontWeight: "bold",
                    color: "#fbbf24",
                    marginTop: idx > 0 ? "28px" : "0",
                    marginBottom: "12px",
                    paddingBottom: "8px",
                    borderBottom: "1px solid #475569",
                  }}>
                    {section.content}
                  </h4>
                );
              } else if (section.type === 'list') {
                return (
                  <ul key={idx} style={{
                    listStyle: "none",
                    padding: 0,
                    margin: "16px 0",
                  }}>
                    {section.items!.map((item, itemIdx) => (
                      <li key={itemIdx} style={{
                        padding: "12px 16px",
                        marginBottom: "8px",
                        background: "rgba(51, 65, 85, 0.5)",
                        borderRadius: "8px",
                        borderLeft: "4px solid #680809",
                        display: "flex",
                        alignItems: "flex-start",
                        gap: "12px",
                      }}>
                        <span style={{
                          color: "#680809",
                          fontSize: "18px",
                          lineHeight: "1",
                          marginTop: "2px",
                        }}>•</span>
                        <span style={{ flex: 1 }}>{item}</span>
                      </li>
                    ))}
                  </ul>
                );
              } else {
                return (
                  <p key={idx} style={{
                    margin: "16px 0",
                    fontSize: "16px",
                    color: "#cbd5e1",
                    lineHeight: "1.8",
                  }}>
                    {section.content}
                  </p>
                );
              }
            })
          ) : (
            <div style={{
              whiteSpace: "pre-wrap",
              fontSize: "16px",
              color: "#cbd5e1",
              lineHeight: "1.8",
            }}>
              {plan}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

