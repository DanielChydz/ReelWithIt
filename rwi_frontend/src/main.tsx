import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import './index.css'
import HomePage from './pages/HomePage.tsx'
import LoginPage from './pages/LoginPage.tsx';
import RegisterPage from './pages/RegisterPage.tsx';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage/>} />
        <Route path="/auth/login" element={<LoginPage/>} />
        <Route path="/auth/register" element={<RegisterPage/>} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)