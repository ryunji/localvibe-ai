import { useState } from "react";
import { useOutletContext } from "react-router-dom";
import "./AiChatPage.css";

export default function AiChatPage() {
  const [q, setQ] = useState("");
  const [result, setResult] = useState("");
  const [elapsedSec, setElapsedSec] = useState(null);
  const [loading, setLoading] = useState(false);
  const [model, setModel] = useState("local"); // "local" | "gpt"

  // Layout에서 넘겨준 히스토리 추가 함수
  const { addHistory } = useOutletContext();

  const send = async () => {
    if (!q.trim()) return;
    setLoading(true);
    setResult("");
    setElapsedSec(null);

    // 사이드바 히스토리에 추가
    addHistory({ id: Date.now(), q: q.trim(), model });

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

  const getModelToggleClass = (m) => {
    if (model !== m) return "model-toggle-btn inactive";
    return m === "gpt" ? "model-toggle-btn active-gpt" : "model-toggle-btn active-local";
  };

  return (
    <div className="aichat-content">
      <div className="aichat-inner">

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

        {/* 검색 인풋 - textarea로 자동 개행 */}
        <div className="search-row">
          <textarea
            className="search-input"
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            placeholder="전시나 일정 질문해봐 (Shift+Enter 줄바꿈)"
            disabled={loading}
            rows={1}
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
            ) : (
              <>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="22" y1="2" x2="11" y2="13" />
                  <polygon points="22 2 15 22 11 13 2 9 22 2" />
                </svg>
                검색하기
              </>
            )}
          </button>
        </div>

        {/* 질문 + 답변 영역 */}
        {(result || loading) && (
          <div className="result-box">

            {/* 사용자 질문 */}
            <div className="question-bubble">
              <span className="question-label">질문</span>
              <p className="question-text">{q}</p>
            </div>

            {/* 구분선 */}
            <div className="result-divider" />

            {/* AI 답변 */}
            <div className="answer-section">
              <div className="answer-header">
                <span className={`result-model-badge ${model}`}>
                  {model === "gpt" ? "GPT 답변" : "내부 모델 답변"}
                </span>
                {elapsedSec !== null && (
                  <span className="elapsed-time">⏱ {elapsedSec}초</span>
                )}
              </div>
              {loading ? (
                <div className="answer-loading">
                  <div className="spinner-dark" />
                  <span>답변 생성 중...</span>
                </div>
              ) : (
                <pre className="result-text">{result}</pre>
              )}
            </div>

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
  );
}