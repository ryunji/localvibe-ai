const BASE_URL = "http://localhost:8000";

export async function collectExhibitions() {
  const res = await fetch(`${BASE_URL}/collect`, {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error("수집 요청 실패");
  }

  return res.json();
}