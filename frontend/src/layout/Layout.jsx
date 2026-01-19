import { Link, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div>
      {/* 상단 메뉴바 */}
      <header
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          height: "64px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 20px",
          borderBottom: "1px solid #eee",
          background: "white",
          zIndex: 1000,
        }}
      >
        <div style={{ fontWeight: "bold" }}>
          <Link to="/" style={{ textDecoration: "none", color: "black" }}>
            LocalVibe
          </Link>
        </div>

        <nav style={{ display: "flex", gap: "16px" }}>
          <Link to="/">AI 검색</Link>
          <Link to="/collect">전시 수집</Link>
        </nav>
      </header>

      {/* 페이지 콘텐츠 */}
      <main style={{ paddingTop: "80px" }}>
        <Outlet />
      </main>
    </div>
  );
}
