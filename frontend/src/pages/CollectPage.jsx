import { useState, useEffect } from "react";
import {
  collectExhibitions,
  getCollectStatus,
  getSavedExhibitions,
} from "../api/collectorApi";

export default function CollectPage() {
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [exhibitions, setExhibitions] = useState([]);
  const [error, setError] = useState(null);

  // 최초 로딩 시 상태 + 저장 데이터 불러오기
  useEffect(() => {
    fetchStatus();
    fetchExhibitions();
  }, []);

  const fetchStatus = async () => {
    try {
      const res = await getCollectStatus();
      setStatus(res);
    } catch (e) {
      console.error(e);
    }
  };

  const fetchExhibitions = async () => {
    try {
      const res = await getSavedExhibitions();
      setExhibitions(res);
    } catch (e) {
      console.error(e);
    }
  };

  const handleCollect = async () => {
    setLoading(true);
    setError(null);

    try {
      await collectExhibitions();
      await fetchStatus();
      await fetchExhibitions();
    } catch (e) {
      setError("수집 중 오류 발생");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "60px", maxWidth: "1200px", margin: "0 auto" }}>
      <h1 style={{ marginBottom: "40px" }}>LocalVibe 전시 수집 관리자</h1>

      {/* ================= 상태 카드 ================= */}
      <div
        style={{
          border: "1px solid #ddd",
          padding: "20px",
          borderRadius: "8px",
          marginBottom: "40px",
        }}
      >
        <h3>최근 수집 상태</h3>
        {status ? (
          <>
            <p>실행 시간: {status.last_run_time}</p>
            <p>
              상태:{" "}
              <span
                style={{
                  color:
                    status.status === "SUCCESS" ? "green" : "red",
                  fontWeight: "bold",
                }}
              >
                {status.status}
              </span>
            </p>
            <p>저장 건수: {status.saved_count}</p>
          </>
        ) : (
          <p>수집 이력이 없습니다.</p>
        )}


      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          marginTop: "20px",
        }}
      >        
        <button
          onClick={handleCollect}
          disabled={loading}
          style={{ marginTop: "20px" }}
        >
          {loading ? "수집 중..." : "수동 수집 실행"}
        </button>
      </div>
        {error && (
          <p style={{ color: "red", marginTop: "10px" }}>{error}</p>
        )}
      </div>

      {/* ================= 저장 데이터 그리드 ================= */}
      <h3 style={{ marginBottom: "20px" }}>
        저장된 전시 데이터 ({exhibitions.length}건)
      </h3>

      <table
        style={{
          width: "100%",
          borderCollapse: "collapse",
        }}
      >
        <thead>
          <tr style={{ background: "#f5f5f5" }}>
            <th style={thStyle}>제목</th>
            <th style={thStyle}>장소</th>
            <th style={thStyle}>시작일</th>
            <th style={thStyle}>종료일</th>
            <th style={thStyle}>등록일</th>
          </tr>
        </thead>
        <tbody>
          {exhibitions.map((item, index) => (
            <tr key={index}>
              <td style={tdStyle}>{item.title}</td>
              <td style={tdStyle}>{item.place_name}</td>
              <td style={tdStyle}>{item.start_date}</td>
              <td style={tdStyle}>{item.end_date}</td>
              <td style={tdStyle}>{item.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const thStyle = {
  border: "1px solid #ddd",
  padding: "10px",
  textAlign: "left",
};

const tdStyle = {
  border: "1px solid #ddd",
  padding: "10px",
};
