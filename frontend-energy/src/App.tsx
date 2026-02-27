import { Button } from "antd";
import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";
import EnergyPage from "@/pages/EnergyPage"

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <header className="border-b bg-white">
          <div className="mx-auto max-w-6xl px-4 py-3 flex items-center gap-3">
            <div className="font-semibold">Energy Analytics</div>
            <nav className="ml-auto flex gap-2">
              <NavLink
                to="/energy"
                className={({ isActive }) =>
                  `px-3 py-1 rounded-lg ${isActive ? "bg-gray-100" : ""}`
                }
              >
                Energy
              </NavLink>
            </nav>
          </div>
        </header>

        <main className="mx-auto max-w-6xl px-4 py-6">
          <Routes>
            <Route path="/" element={<EnergyPage />} />
            <Route path="/energy" element={<EnergyPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}