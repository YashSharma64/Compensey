import React, { useState, useEffect } from 'react';

const LoadingOverlay = ({ messages = ["Loading..."], progressData }) => {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [simulatedProgress, setSimulatedProgress] = useState(0);

  useEffect(() => {
    // If we've started receiving actual backend progress, stop simulating
    if (progressData) return;

    // Cycle through messages with just enough time to read
    const messageInterval = setInterval(() => {
      setCurrentMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
    }, 1500); // Slightly longer reading time
    
    // Simulate slow progress for cold starts (Render free tier spin-up)
    const progressInterval = setInterval(() => {
        setSimulatedProgress((prev) => {
            if (prev >= 95) return 95;
            const increment = (95 - prev) * 0.02; 
            return prev + (increment > 0.1 ? increment : 0.1);
        });
    }, 500);

    return () => {
        clearInterval(messageInterval);
        clearInterval(progressInterval);
    };
  }, [messages, progressData]);

  const displayProgress = progressData ? progressData.progress : simulatedProgress;
  const displayMessage = progressData ? progressData.message : messages[currentMessageIndex];

  return (
    <div className="fixed inset-0 bg-[#FFF9EF]/95 backdrop-blur-md z-50 flex flex-col items-center justify-center transition-all duration-500">
      
      <div className="w-full max-w-sm px-6">
        {/* Animated Message - Pure Text */}
        <div className="mb-4 min-h-[3rem] flex items-center justify-center text-center">
            <span className="text-xl md:text-2xl font-light text-[#5A4A3A] tracking-wide animate-fade-in-up key={displayMessage}">
            {displayMessage}
            </span>
        </div>
        
        {/* Clean, Elegant Progress Line */}
        <div className="w-full h-[3px] bg-[#E89F4C]/10 relative overflow-hidden rounded-full mb-3">
            <div 
                className="absolute inset-y-0 left-0 bg-[#E89F4C] shadow-[0_0_10px_rgba(232,159,76,0.5)] transition-all ease-linear"
                style={{ width: `${displayProgress}%`, transitionDuration: '500ms' }}
            ></div>
        </div>
        <div className="text-right text-xs font-mono text-[#E89F4C] font-semibold mb-6">
            {Math.round(displayProgress)}%
        </div>
        
        {!progressData && (
          <p className="text-xs text-center text-[#8B6E4E] opacity-70 mb-6 bg-white/50 p-3 rounded-lg border border-[#E89F4C]/20 shadow-sm leading-relaxed">
              <span className="font-semibold block mb-1">First Time Loading?</span>
              Our backend runs on a free tier service and may take <span className="font-bold text-[#E89F4C]">2-3 minutes</span> to spin up on your first request. Please be patient!
          </p>
        )}
        
        {/* Professional Footer Metadata */}
        <div className="mt-2 flex justify-between text-[10px] uppercase tracking-[0.2em] text-[#8B6E4E] opacity-60 font-mono">
            <span>Compensey AI</span>
            <span>Processing...</span>
        </div>
      </div>

    </div>
  );
};

export default LoadingOverlay;
