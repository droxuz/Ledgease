import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import LandingPage from './pages/Landing-Page/LandingPage.tsx'
import { BrowserRouter, RouterProvider } from 'react-router-dom'
import App from './App.tsx'
import React from 'react'

createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <App/>
    </BrowserRouter>
  </React.StrictMode>
)
