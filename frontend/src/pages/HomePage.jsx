import { useState } from "react";

export default function HomePage() {
  const [q, setQ] = useState("");
  const [result, setResult] = useState("");
  const [elapsedSec, setElapsedSec] = useState(null);
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!q.trim()) return;

    setLoading(true);
    setResult("");
    setElapsedSec(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ q }),
      });

      const data = await res.json();

      if (data.answer) {
        setResult(data.answer);

        if (typeof data.elapsed_ms === "number") {
          setElapsedSec((data.elapsed_ms / 1000).toFixed(2));
        }
      } else if (data.error) {
        setResult("❌ ERROR: " + data.error);
      } else {
        setResult("❌ 응답이 이상함: " + JSON.stringify(data));
      }
    } catch (e) {
      setResult("❌ 요청 실패: " + e.message);
    } finally {
      setLoading(false);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter") send();
  };

  return (
    <div style={{ maxWidth: 900, margin: "0 auto", padding: 40 }}>
      <h1>LocalVibe AI</h1>

      <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
        <input
          style={{ flex: 1, padding: 10 }}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="전시나 일정 질문해봐"
          disabled={loading}
        />

        <button onClick={send} disabled={loading}>
          {loading ? "검색중..." : "검색하기"}
        </button>

        {/* ✅ 동그라미 로딩 */}
        {loading && (
          <div
            style={{
              width: 18,
              height: 18,
              border: "3px solid #ccc",
              borderTop: "3px solid #333",
              borderRadius: "50%",
              animation: "spin 0.8s linear infinite",
            }}
          />
        )}
      </div>

      {/* ✅ 걸린 시간 표시 */}
      {elapsedSec !== null && (
        <div style={{ marginTop: 12, fontSize: 14, color: "#555" }}>
          ⏱ 응답 시간: {elapsedSec}초
        </div>
      )}

      <pre style={{ whiteSpace: "pre-wrap", marginTop: 20 }}>
        {result}
      </pre>

      {/* ✅ 스피너 애니메이션 */}
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
    </div>
  );
}
