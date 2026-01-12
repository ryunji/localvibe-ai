import { useState } from "react";
import { collectExhibitions } from "../api/collectorApi";
import ResultList from "../components/ResultList";

export default function CollectPage() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const handleCollect = async () => {
    setLoading(true);
    setError(null);

    try {
      const data = await collectExhibitions();
      setResults(data.data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        paddingTop: "120px",
      }}
    >
      {/* 콘텐츠 영역 */}
      <div
        style={{
          width: "100%",
          maxWidth: "900px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* 제목 */}
        <h1 style={{ textAlign: "center", marginBottom: "40px" }}>
          LocalVibe 전시 수집
        </h1>

        {/* 버튼 영역 (오른쪽 정렬) */}
        <button
          onClick={handleCollect}
          disabled={loading}
          style={{
            alignSelf: "flex-end",
            marginBottom: "40px",
          }}
        >
          {loading ? "수집 중..." : "전시 수집하기"}
        </button>

        {/* 에러 */}
        {error && (
          <p style={{ color: "red", textAlign: "center" }}>{error}</p>
        )}

        {/* 결과 영역 */}
        {results.length === 0 ? (
          <p style={{ textAlign: "center", opacity: 0.7 }}>
            결과가 없습니다.
          </p>
        ) : (
          <ResultList items={results} />
        )}
      </div>
    </div>
  );
}
