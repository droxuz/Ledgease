import { Routes, Route } from 'react-router-dom'
import LandingPage from './pages/Landing-Page/LandingPage.tsx'
import LoginPage from './pages/Login-Page/LoginPage.tsx'
import SignupPage from './pages/Signup-Page/SignupPage.tsx'
import DashboardPage from './pages/Dashboard-Page/DashboardPage.tsx'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/dashboard" element={<DashboardPage />} />
    </Routes>
  )
}


