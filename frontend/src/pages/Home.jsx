import React from 'react';
import Navbar from '../components/Navbar';

const Home = () => {
  return (
    <div className="h-screen w-screen bg-[#FFF9EF] text-[#2A2A2A] font-sans selection:bg-[#E89F4C] selection:text-white flex flex-col overflow-hidden">
      <Navbar />

      <main className="flex-grow flex flex-col items-center justify-center px-6 w-full max-w-7xl mx-auto">
        
        {/* Hero Text */}
        <div className="text-center mb-12">
          <h1 className="text-7xl md:text-8xl font-bold text-[#E89F4C] mb-4 tracking-tight drop-shadow-sm">
            Compensey
          </h1>
          
          <h2 className="text-3xl md:text-4xl text-[#5A4A3A] font-medium mb-4">
            AI-powered Competitor Intelligence
          </h2>
          
          <p className="text-[#E89F4C] text-sm md:text-base tracking-[0.2em] uppercase font-semibold">
            Compare competitors. Discover growth signals.
          </p>
        </div>

        {/* Input Section */}
        <div className="w-full max-w-5xl bg-white/40 backdrop-blur-sm border border-[#E89F4C]/20 rounded-2xl p-12 shadow-xl mb-12">
          <p className="text-[#D48C3C] text-center text-lg font-medium mb-10">
            Compare two companies using data-driven ML insights.
          </p>

          <div className="flex flex-col md:flex-row gap-12 items-center justify-between w-full px-8">
            {/* Company A Input */}
            <div className="relative group w-full">
              <input 
                type="text" 
                placeholder="Company A" 
                className="w-full text-center text-3xl md:text-4xl font-bold text-[#5A4A3A] placeholder-[#E89F4C]/40 bg-transparent border-b-2 border-[#E89F4C]/20 focus:border-[#E89F4C] outline-none pb-4 transition-all duration-300"
              />
            </div>

            {/* Separator - Vertical Line */}
            <div className="hidden md:block h-24 w-[1px] bg-[#E89F4C]/30"></div>

            {/* Company B Input */}
            <div className="relative group w-full">
              <input 
                type="text" 
                placeholder="Company B" 
                className="w-full text-center text-3xl md:text-4xl font-bold text-[#5A4A3A] placeholder-[#E89F4C]/40 bg-transparent border-b-2 border-[#E89F4C]/20 focus:border-[#E89F4C] outline-none pb-4 transition-all duration-300"
              />
            </div>
          </div>

          <div className="flex justify-center mt-12">
            <button className="bg-[#8B6E4E] hover:bg-[#7A5E3F] text-white text-xl font-semibold py-4 px-16 rounded-xl shadow-lg hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 focus:ring-4 focus:ring-[#8B6E4E]/30 cursor-pointer">
              Analyze
            </button>
          </div>
        </div>
      </main>

      <footer className="w-full text-center py-6">
        <p className="text-[#D48C3C] text-sm font-medium opacity-90">
          Uses sentiment analysis, growth modeling & explainable ML.
        </p>
      </footer>
    </div>
  );
};

export default Home;
