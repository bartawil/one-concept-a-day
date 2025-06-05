import { useState } from "react";
import useTypewriter from "../features/useTypewriter";
import LandingHeader from "./LandingHeader";
import "../styles/Animations.css";
import "../styles/Fonts.css";


export default function LandingPage() {
  const [category, setCategory] = useState("");
  const [concept, setConcept] = useState("");
  const displayedConcept = useTypewriter(concept);
  const [loading, setLoading] = useState(false);


  const fetchConcept = async () => {
    setLoading(true);
    setConcept("");
    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/get-concept?category=${encodeURIComponent(category)}`);
      if (!response.ok) throw new Error("Failed to fetch concept");
      const data = await response.json();
      console.log(data)
      setConcept(data.concept);
    } catch {
      setConcept("Error fetching concept");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans px-4 pb-8 pt-24 flex flex-col items-center">
      <LandingHeader />
      <main className="flex-1 flex flex-col items-center justify-center w-full">
        <div className="flex justify-center items-center my-10">
          <img
            src="/app_icon.svg"
            className="h-32 w-32 animate-spin-slow-reverse filter invert"
          />
        </div>
        <div className="w-full max-w-xl text-center mb-10 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mt-8 mb-6 text-white averia-serif-libre-bold">
            Learn something new every day
          </h2>
          <p className="text-gray-400 text-lg averia-serif-libre-bold">
            Type a topic and get a short, AI-generated concept explanation.
          </p>
        </div>
        <div className="w-full max-w-xl bg-zinc-900 p-6 rounded-2xl shadow-lg animate-fade-in">
          <div className="w-full max-w-xl mx-auto flex flex-col items-center space-y-4">
            <input
              type="text"
              placeholder="Try: AI, Philosophy, Climate"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0"
            />
            <button
              onClick={fetchConcept}
              className="w-full bg-zinc-700 hover:bg-zinc-600 transition text-white font-semibold py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0 averia-serif-libre-bold"
            >
              {loading ? "Loading..." : "Get Concept"}
            </button>
          </div>
        </div>
        {displayedConcept && (
          <div className="w-full max-w-xl mt-8 bg-zinc-900 p-6 rounded-2xl shadow-lg animate-fade-in">
            <h3 className="text-xl font-semibold mb-3 averia-serif-libre-bold">Today’s Concept:</h3>
            <p className="whitespace-pre-wrap leading-relaxed text-gray-300">
              {displayedConcept}<span className="blinking-cursor"></span>
            </p>
          </div>
        )}
      </main>
    </div>
  );
}
