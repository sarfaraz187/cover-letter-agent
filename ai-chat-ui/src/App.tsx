import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ChatWindow />} />
      </Routes>
    </Router>
  );
}

export default App;
