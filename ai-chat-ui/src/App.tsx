import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CoverLetterGenerator from './components/CoverLetterGenerator';
import './App.css';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-100 text-gray-800">
        <nav className="bg-gray-800 text-white p-4">
          <div className="container mx-auto max-w-6xl px-4 flex justify-between items-center">
            <div className="font-bold text-xl">AI Cover Letter Generator</div>
          </div>
        </nav>
        
        <main className="flex-grow px-6 py-6">
          <Routes>
            <Route path="/" element={<CoverLetterGenerator />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
