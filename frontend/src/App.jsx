import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./layout/Layout";
import HomePage from "./pages/HomePage";
import AiChatPage from "./pages/AiChatPage";
import CollectPage from "./pages/CollectPage";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />        {/* 나중에 만들 홈 */}
          <Route path="/search" element={<AiChatPage />} /> {/* AI 채팅 */}
          <Route path="/collect" element={<CollectPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}