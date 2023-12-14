// Title.js
import Image from "next/image";
import { useRef } from "react";

export default function Title({ scrollTargetRef }) {
  const handleScrollToSection = () => {
    // Scroll to the section below the title
    if (scrollTargetRef.current) {
      scrollTargetRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  return (
    <div className="bg-gradient-to-b from-purple-500 via-pink-500 to-orange-400 h-screen flex items-center justify-center">
      <div className="text-white text-center">
        <h1 className="text-6xl font-bold mb-4">Mid-Moments</h1>
        <p className="text-lg">By Jack and the Elastic Beanstalk.</p>
        <p className="text-4xl mt-8" ref={scrollTargetRef}>
          <button
            onClick={handleScrollToSection}
            className="cursor-pointer focus:outline-none hover:border-2 border-white rounded-lg p-1"
          >
            ↓
          </button>
        </p>
      </div>
    </div>
  );
}
