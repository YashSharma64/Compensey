import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import { getStrategy } from '../api/compare';

const Result = ({ data, onBack }) => {
  const [question, setQuestion] = useState('');
  const [strategyResponse, setStrategyResponse] = useState(null);
  const [isAsking, setIsAsking] = useState(false);

  if (!data) return null;

  const { winner, loser, companyA, companyB, metrics, reasons, insight } = data;

  const getCompanyColor = (company) => company === winner ? 'text-[#5A4A3A]' : 'text-[#E89F4C]';
  const getBarColor = (company) => company === winner ? 'bg-[#5A4A3A]' : 'bg-[#E89F4C]/60';
  
  const maxScale = 1.0;
  const sentH_A = (metrics.sentiment.a / maxScale) * 100;
  const sentH_B = (metrics.sentiment.b / maxScale) * 100;
  const growthH_A = (metrics.growth.a / maxScale) * 100;
  const growthH_B = (metrics.growth.b / maxScale) * 100;

  const handleAskStrategy = async () => {
    if (!question) return;
    setIsAsking(true);
    setStrategyResponse(null);

    try {
      const winnerIsA = winner === companyA;
      const winnerMetrics = winnerIsA
        ? { sentiment: metrics.sentiment.a, growth: metrics.growth.a, risk: metrics.risk.a }
        : { sentiment: metrics.sentiment.b, growth: metrics.growth.b, risk: metrics.risk.b };
      const loserMetrics = winnerIsA
        ? { sentiment: metrics.sentiment.b, growth: metrics.growth.b, risk: metrics.risk.b }
        : { sentiment: metrics.sentiment.a, growth: metrics.growth.a, risk: metrics.risk.a };

      const strategyData = await getStrategy(winner, loser, winnerMetrics, loserMetrics, question, data.raw_drivers);
      setStrategyResponse(strategyData.answer);
    } catch (err) {
      setStrategyResponse("Strategic analysis subsystem is currently offline. Please try again.");
    } finally {
      setIsAsking(false);
    }
  };


  return (
    <div className="h-screen w-screen bg-[#FFF9EF] text-[#2A2A2A] font-sans selection:bg-[#E89F4C] selection:text-white flex flex-col overflow-y-auto">
      <Navbar />

      <main className="flex-grow flex flex-col items-center justify-center px-6 w-full max-w-6xl mx-auto pb-10">
        <div className="text-center mb-10 w-full animate-fade-in-up">
          <h1 className="text-5xl md:text-6xl font-bold text-[#5A4A3A] mb-3 tracking-tight">
            Winner: <span className="text-[#E89F4C]">{winner}</span>
          </h1>
          <p className="text-[#8B6E4E] text-lg font-medium opacity-80">
            Based on customer sentiment and growth indicators.
          </p>
        </div>

        <div className="w-full flex flex-col md:flex-row gap-8 items-stretch justify-center h-auto min-h-[400px]">
          <div className="flex-1 w-full flex flex-col items-center gap-10">
            <div className="flex w-full justify-center gap-16 md:gap-24">
              <div className="text-center">
                <p className="text-[#8B6E4E] text-sm uppercase font-bold tracking-wider mb-2">Sentiment Score</p>
                <div className="flex items-baseline justify-center gap-1">
                  <span className={`text-5xl font-bold ${getCompanyColor(companyA)}`}>{metrics.sentiment.a}</span>
                  <span className={`text-lg font-medium ${getCompanyColor(companyB)}`}>/ {metrics.sentiment.b}</span>
                </div>
              </div>
              <div className="text-center">
                <p className="text-[#8B6E4E] text-sm uppercase font-bold tracking-wider mb-2">Growth Score</p>
                <div className="flex items-baseline justify-center gap-1">
                  <span className={`text-5xl font-bold ${getCompanyColor(companyA)}`}>{metrics.growth.a}</span>
                  <span className={`text-lg font-medium ${getCompanyColor(companyB)}`}>/ {metrics.growth.b}</span>
                </div>
              </div>
            </div>

            <div className="w-full max-w-md mt-auto pt-8">
              <div className="flex items-end justify-center h-48 gap-16 border-b border-[#E89F4C]/30 pb-0 relative">
                <div className="absolute -top-6 left-0 text-xs text-[#8B6E4E] font-medium">1.0</div>
                <div className="absolute -top-6 right-0 text-xs text-[#8B6E4E] font-medium">0.0</div>
                
                <div className="flex gap-1 h-full items-end group relative w-16 justify-center">
                  <div className={`w-6 rounded-t-sm ${getBarColor(companyA)}`} style={{ height: `${sentH_A}%` }}></div>
                  <div className={`w-6 rounded-t-sm ${getBarColor(companyB)}`} style={{ height: `${sentH_B}%` }}></div>
                  <div className="absolute -bottom-8 whitespace-nowrap text-xs font-bold text-[#8B6E4E] tracking-wider uppercase">Sentiment</div>
                </div>

                <div className="flex gap-1 h-full items-end group relative w-16 justify-center">
                  <div className={`w-6 rounded-t-sm ${getBarColor(companyA)}`} style={{ height: `${growthH_A}%` }}></div>
                  <div className={`w-6 rounded-t-sm ${getBarColor(companyB)}`} style={{ height: `${growthH_B}%` }}></div>
                  <div className="absolute -bottom-8 whitespace-nowrap text-xs font-bold text-[#8B6E4E] tracking-wider uppercase">Growth</div>
                </div>
              </div>
              
              <div className="flex justify-center gap-8 mt-12">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-[#5A4A3A]"></div>
                  <span className="text-sm text-[#5A4A3A] font-medium">{winner}</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-[#E89F4C]/60"></div>
                  <span className="text-sm text-[#5A4A3A] font-medium">{loser}</span>
                </div>
              </div>
            </div>
          </div>

          <div className="hidden md:block w-[1px] bg-[#E89F4C]/20 self-stretch my-4"></div>

          <div className="flex-1 w-full max-w-md flex flex-col justify-center py-4 px-8">
            <div className="mb-10">
              <h3 className="text-lg uppercase tracking-widest font-bold text-[#E89F4C] mb-6">Key Drivers</h3>
              <ul className="space-y-6">
                {reasons.map((reason, idx) => (
                  <li key={idx} className="flex items-start gap-4 text-[#5A4A3A] text-lg leading-relaxed font-light">
                    <span className="mt-2 w-1.5 h-1.5 rounded-full bg-[#E89F4C] shrink-0"></span>
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>
            </div>

            {insight && (
              <div className="mb-12">
                <p className="text-[#8B6E4E] font-medium italic border-l-2 border-[#E89F4C] pl-4 py-1">
                  "{insight}"
                </p>
              </div>
            )}

            <div className="mt-auto">
              <button 
                onClick={onBack}
                className="group flex items-center gap-2 text-[#5A4A3A] hover:text-[#E89F4C] font-semibold text-sm tracking-widest uppercase transition-colors"
              >
                <span className="group-hover:-translate-x-1 transition-transform duration-300">&larr;</span> Compare Another Pair
              </button>
            </div>
          </div>
        </div>

        <div className="w-full max-w-4xl mt-16 border-t border-[#E89F4C]/20 pt-12 animate-fade-in-up mb-12">
          <h3 className="text-2xl font-serif text-[#5A4A3A] mb-2">Strategic Outlook</h3>
          <p className="text-[#8B6E4E] text-sm mb-6 opacity-80">
            Ask scenario-based questions to generate consulting-grade reasoning. 
            <span className="italic"> (e.g., "What if growth slows?", "Key risks ahead?")</span>
          </p>

          <div className="flex gap-4 mb-8">
            <input 
              type="text" value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask about future scenarios..."
              className="flex-1 bg-white/50 border border-[#E89F4C]/30 rounded-lg px-4 py-3 text-[#5A4A3A] placeholder-[#8B6E4E]/40 focus:outline-none focus:border-[#E89F4C] transition-colors"
              onKeyDown={(e) => e.key === 'Enter' && handleAskStrategy()}
            />
            <button 
              onClick={handleAskStrategy}
              disabled={!question || isAsking}
              className={`bg-[#5A4A3A] text-white px-8 py-3 rounded-lg font-medium tracking-wide hover:bg-[#4A3A2A] transition-colors ${(!question || isAsking) ? 'opacity-50 cursor-not-allowed' : ''}`}
            >
              {isAsking ? 'Analyzing...' : 'Ask'}
            </button>
          </div>

          {strategyResponse && (
            <div className="bg-white/60 border-l-4 border-[#5A4A3A] p-6 rounded-r-lg shadow-sm animate-fade-in-up">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-xs font-bold tracking-widest text-[#8B6E4E] uppercase">Strategic Memo</span>
                <div className="h-px flex-1 bg-[#E89F4C]/20"></div>
              </div>
              <p className="text-[#2A2A2A] font-serif text-lg leading-relaxed antialiased">
                {strategyResponse}
              </p>
              <p className="text-xs text-[#8B6E4E] mt-4 italic opacity-70">
                * Scenario-based reasoning based on current signals. Not a financial prediction.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Result;
