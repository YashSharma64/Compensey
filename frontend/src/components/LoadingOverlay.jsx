import React, { useState, useEffect } from 'react';

const LoadingOverlay = ({ messages = ["Loading..."] }) => {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

  useEffect(() => {
    // Cycle through messages with just enough time to read
    const interval = setInterval(() => {
      setCurrentMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
    }, 1200);

    return () => clearInterval(interval);
  }, [messages]);

  return (
    <div className="fixed inset-0 bg-[#FFF9EF]/95 backdrop-blur-md z-50 flex flex-col items-center justify-center transition-all duration-500">
      
      <div className="w-full max-w-sm px-6">
        {/* Animated Message - Pure Text */}
        <div className="mb-8 min-h-[3rem] flex items-center justify-center text-center">
            <span className="text-xl md:text-2xl font-light text-[#5A4A3A] tracking-wide animate-fade-in-up key={currentMessageIndex}">
            {messages[currentMessageIndex]}
            </span>
        </div>
        
        {/* Clean, Elegant Progress Line */}
        <div className="w-full h-[2px] bg-[#E89F4C]/10 relative overflow-hidden rounded-full">
            <div className="absolute inset-y-0 left-0 bg-[#E89F4C] w-1/3 animate-progress-indeterminate shadow-[0_0_10px_rgba(232,159,76,0.5)]"></div>
        </div>
        
        {/* Professional Footer Metadata */}
        <div className="mt-6 flex justify-between text-[10px] uppercase tracking-[0.2em] text-[#8B6E4E] opacity-60 font-mono">
            <span>Compensey AI</span>
            <span>Processing...</span>
        </div>
      </div>

    </div>
  );
};

export default LoadingOverlay;
