import { useState } from "react";
import { Link, Outlet } from "react-router-dom";
import "./Layout.css";

const MOCK_HISTORY = [
  { id: 1, q: "홍대 이번 주 전시 뭐 있어?", model: "gpt" },
  { id: 2, q: "성수동 팝업 일정 알려줘", model: "local" },
  { id: 3, q: "서울숲 근처 주말 행사", model: "gpt" },
  { id: 4, q: "마포구 갤러리 추천", model: "local" },
];

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [history, setHistory] = useState(MOCK_HISTORY);
  const [activeId, setActiveId] = useState(null);

  // 외부(AiChatPage)에서 히스토리 추가할 수 있도록 함수 노출
  const addHistory = (item) => {
    setHistory((prev) => [item, ...prev]);
    setActiveId(item.id);
  };

  return (
    <div className="layout-container">

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
          <Link to="/" className="sidebar-new-btn" onClick={() => setActiveId(null)}>
            <span className="sidebar-new-btn-icon">+</span> 새 검색
          </Link>
        </div>

        <div className="sidebar-history-list">
          {history.length === 0 && (
            <div className="sidebar-empty">아직 검색 기록이 없어요</div>
          )}
          {history.map((item) => (
            <div
              key={item.id}
              className={`history-item ${activeId === item.id ? "active" : ""}`}
              onClick={() => setActiveId(item.id)}
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

      {/* ── 오른쪽 영역 ── */}
      <div className="main-area">

        {/* 상단 네비 */}
        <header className="navbar">
          <div className="navbar-left">
            <button
              className="sidebar-toggle-btn"
              onClick={() => setSidebarOpen((o) => !o)}
              title="히스토리 사이드바"
            >
              ☰
            </button>
            <Link to="/" className="navbar-logo">LocalVibe AI</Link>
          </div>
          <nav className="navbar-right">
            <Link to="/">AI 검색</Link>
            <span className="navbar-divider">|</span>
            <Link to="/collect">전시 수집</Link>
          </nav>
        </header>

        {/* 페이지 컨텐츠 */}
        <main className="content-area">
          <Outlet context={{ addHistory }} />
        </main>

      </div>
    </div>
  );
}