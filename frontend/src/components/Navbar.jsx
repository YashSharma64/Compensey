import React from 'react';

const Navbar = () => {
  return (
    <nav className="w-full flex justify-between items-center py-6 px-12 bg-transparent">
      <div className="text-[#E89F4C] text-xl font-medium tracking-wide">
        CompenseyAI
      </div>
      <div className="text-[#E89F4C] text-sm font-medium tracking-wide cursor-pointer hover:opacity-80 transition-opacity">
        ABOUT US
      </div>
    </nav>
  );
};

export default Navbar;
