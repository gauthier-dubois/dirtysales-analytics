import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom"
import TablePage from "@/pages/TablePage"
import ChartPage from "@/pages/ChartPage"

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <header className="border-b bg-white">
          <div className="mx-auto max-w-6xl px-4 py-3 flex items-center gap-3">
            <div className="font-semibold">DirtySales Analytics</div>
            <nav className="ml-auto flex gap-2">
              <NavLink className={({ isActive }) => `px-3 py-1 rounded-lg ${isActive ? "bg-gray-100" : ""}`} to="/table">
                Table
              </NavLink>
              <NavLink className={({ isActive }) => `px-3 py-1 rounded-lg ${isActive ? "bg-gray-100" : ""}`} to="/charts">
                Charts
              </NavLink>
            </nav>
          </div>
        </header>

        <main className="mx-auto max-w-6xl px-4 py-6">
          <Routes>
            <Route path="/" element={<TablePage />} />
            <Route path="/table" element={<TablePage />} />
            <Route path="/charts" element={<ChartPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}