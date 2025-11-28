import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import LandingPage from './pages/Landing-Page/landingpage.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <LandingPage/>
  </StrictMode>,
)
