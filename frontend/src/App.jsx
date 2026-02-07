import React, { useState } from 'react';
import Home from './pages/Home';
import Result from './pages/Result';

function App() {
  const [view, setView] = useState('home'); // 'home' | 'result'
  const [data, setData] = useState(null);

  const handleAnalyze = (resultData) => {
    setData(resultData);
    setView('result');
  };

  const handleBack = () => {
    setView('home');
    setData(null);
  };

  return (
    <>
      {view === 'home' ? (
        <Home onAnalyze={handleAnalyze} />
      ) : (
        <Result data={data} onBack={handleBack} />
      )}
    </>
  );
}

export default App;
