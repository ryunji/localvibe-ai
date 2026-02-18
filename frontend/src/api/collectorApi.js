const BASE_URL = "http://localhost:8000";

/* 1️⃣ 수동 수집 실행 */
export const collectExhibitions = async () => {
  const res = await fetch("http://localhost:8000/admin/collect/manual", {
    method: "POST",
  });

  if (!res.ok) throw new Error("수집 실패");
  return res.json();
};

/* 2️⃣ 최근 수집 상태 조회 */
export async function getCollectStatus() {
  const res = await fetch(`${BASE_URL}/admin/status`);

  if (!res.ok) {
    throw new Error("상태 조회 실패");
  }

  return res.json();
}

/* 3️⃣ DB 저장 데이터 조회 */
export const getSavedExhibitions = async () => {
  const res = await fetch("http://localhost:8000/admin/exhibitions");
  if (!res.ok) throw new Error("데이터 조회 실패");
  return res.json();
};

