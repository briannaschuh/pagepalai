import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App.jsx';
import Home from './pages/Home.jsx';
import Reader from './pages/Reader.jsx';
import BookViewer from './components/BookViewer.jsx'; // or put it in pages/

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/reader" element={<Reader />} />
        <Route path="/reader/:gutenberg_id" element={<BookViewer />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
