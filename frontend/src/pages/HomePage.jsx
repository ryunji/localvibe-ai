import { useState } from "react";
import "./AiChatPage.css";

const MOCK_HISTORY = [
  { id: 1, q: "홍대 이번 주 전시 뭐 있어?", model: "gpt" },
  { id: 2, q: "성수동 팝업 일정 알려줘", model: "local" },
  { id: 3, q: "서울숲 근처 주말 행사", model: "gpt" },
  { id: 4, q: "마포구 갤러리 추천", model: "local" },
];

export default function HomePage() {
  const [q, setQ] = useState("");
  const [result, setResult] = useState("");
  const [elapsedSec, setElapsedSec] = useState(null);
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState("local"); // "local" | "gpt"
  const [history, setHistory] = useState(MOCK_HISTORY);
  const [activeId, setActiveId] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const send = async () => {
    if (!q.trim()) return;
    setLoading(true);
    setResult("");
    setElapsedSec(null);

    const newItem = { id: Date.now(), q: q.trim(), model };
    setHistory((prev) => [newItem, ...prev]);
    setActiveId(newItem.id);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ q, model }),
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

  const loadHistory = (item) => {
    setQ(item.q);
    setModel(item.model);
    setActiveId(item.id);
    setResult("");
    setElapsedSec(null);
  };

  const getModelToggleClass = (m) => {
    if (model !== m) return "model-toggle-btn inactive";
    return m === "gpt" ? "model-toggle-btn active-gpt" : "model-toggle-btn active-local";
  };

  return (
    <div className="app-container">

      {/* ── 사이드바 ── */}
      <div
        className="sidebar"
        style={{ width: sidebarOpen ? 260 : 0, minWidth: sidebarOpen ? 260 : 0 }}
      >
        <div className="sidebar-header">
          <div className="sidebar-title">LocalVibe</div>
          <div className="sidebar-subtitle">검색 히스토리</div>
        </div>

        <div className="sidebar-new-btn-wrap">
          <button
            className="sidebar-new-btn"
            onClick={() => { setQ(""); setResult(""); setElapsedSec(null); setActiveId(null); }}
          >
            <span className="sidebar-new-btn-icon">+</span> 새 검색
          </button>
        </div>

        <div className="sidebar-history-list">
          {history.length === 0 && (
            <div className="sidebar-empty">아직 검색 기록이 없어요</div>
          )}
          {history.map((item) => (
            <div
              key={item.id}
              className={`history-item ${activeId === item.id ? "active" : ""}`}
              onClick={() => loadHistory(item)}
            >
              <div className="history-item-text">{item.q}</div>
              <div className="history-item-meta">
                <span className={`model-badge ${item.model}`}>
                  {item.model === "gpt" ? "GPT" : "내부"}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── 메인 영역 ── */}
      <div className="main-area">

        {/* 상단 네비 */}
        <div className="navbar">
          <div className="navbar-left">
            <button
              className="sidebar-toggle-btn"
              onClick={() => setSidebarOpen((o) => !o)}
              title="히스토리 사이드바"
            >
              ☰
            </button>
            <span className="navbar-logo">LocalVibe AI</span>
          </div>
          <div className="navbar-right">
            <span>AI 검색</span>
            <span className="navbar-divider">|</span>
            <span>전시 수집</span>
          </div>
        </div>

        {/* 컨텐츠 */}
        <div className="content-area">
          <div className="content-inner">

            {/* 타이틀 */}
            {!result && !loading && (
              <div className="page-title-wrap">
                <h1 className="page-title">무엇이 궁금한가요?</h1>
                <p className="page-subtitle">전시, 팝업, 행사 일정을 AI로 검색해보세요</p>
              </div>
            )}

            {/* 모델 선택 토글 */}
            <div className="model-toggle-row">
              {["local", "gpt"].map((m) => (
                <button
                  key={m}
                  className={getModelToggleClass(m)}
                  onClick={() => setModel(m)}
                >
                  {m === "local" ? "🧠 내부 모델" : "✨ GPT"}
                </button>
              ))}
              <span className="model-toggle-label">
                {model === "local" ? "로컬 LLM 사용 중" : "OpenAI GPT 사용 중"}
              </span>
            </div>

            {/* 검색 인풋 */}
            <div className="search-row">
              <input
                className="search-input"
                value={q}
                onChange={(e) => setQ(e.target.value)}
                onKeyDown={onKeyDown}
                placeholder="전시나 일정 질문해봐"
                disabled={loading}
              />
              <button
                className={`search-btn ${loading ? "loading" : "idle"}`}
                onClick={send}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <div className="spinner" />
                    검색중
                  </>
                ) : "검색하기 →"}
              </button>
            </div>

            {/* 응답 시간 */}
            {elapsedSec !== null && (
              <div className="elapsed-time">
                ⏱ 응답 시간: {elapsedSec}초 · {model === "gpt" ? "GPT" : "내부 모델"} 사용
              </div>
            )}

            {/* 결과 */}
            {result && (
              <div className="result-box">
                <div className="result-header">
                  <span className={`result-model-badge ${model}`}>
                    {model === "gpt" ? "GPT 답변" : "내부 모델 답변"}
                  </span>
                  <span className="result-query-label">{q}</span>
                </div>
                <pre className="result-text">{result}</pre>
              </div>
            )}

            {/* 힌트 버튼들 */}
            {!result && !loading && (
              <div className="hint-row">
                {["홍대 이번 주 전시", "성수동 팝업 언제야?", "이번 주말 행사 추천"].map((hint) => (
                  <button
                    key={hint}
                    className="hint-btn"
                    onClick={() => setQ(hint)}
                  >
                    {hint}
                  </button>
                ))}
              </div>
            )}

          </div>
        </div>
      </div>

    </div>
  );
}