export default function ResultList({ items }) {
  if (!items.length) {
    return <p>결과가 없습니다.</p>;
  }

  return (
    <ul style={{ marginTop: 20 }}>
      {items.map((item, idx) => (
        <li key={idx} style={{ marginBottom: 12 }}>
          <strong>[{item.category}]</strong> {item.title}
          <div>📍 {item.place} ({item.address})</div>
          <div>📅 {item.start_date} ~ {item.end_date}</div>
        </li>
      ))}
    </ul>
  );
}