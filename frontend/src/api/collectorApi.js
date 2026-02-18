const BASE_URL = "http://localhost:8000";

/* 1️⃣ 수동 수집 실행 */
export async function collectExhibitions() {
  const res = await fetch(`${BASE_URL}/collect`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("수집 요청 실패");
  }

  return res.json();
}

/* 2️⃣ 최근 수집 상태 조회 */
export async function getCollectStatus() {
  const res = await fetch(`${BASE_URL}/admin/status`);

  if (!res.ok) {
    throw new Error("상태 조회 실패");
  }

  return res.json();
}

/* 3️⃣ DB 저장 데이터 조회 */
export async function getSavedExhibitions() {
  const res = await fetch(`${BASE_URL}/admin/exhibitions`);

  if (!res.ok) {
    throw new Error("데이터 조회 실패");
  }

  return res.json();
}
