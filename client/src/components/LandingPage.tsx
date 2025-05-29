// client/src/pages/LandingPage.tsx
import { useEffect, useState } from "react";
import TopHeader from "./TopHeader";

export default function LandingPage() {
  const [category, setCategory] = useState("");
  const [concept, setConcept] = useState("");
  const [displayedConcept, setDisplayedConcept] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchConcept = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/daily-concept?category=${encodeURIComponent(category)}`);
      if (!response.ok) throw new Error("Failed to fetch concept");
      const data = await response.json();
      setConcept(data.concept);
    } catch {
      setConcept("Error fetching concept");
    } finally {
      setLoading(false);
    }
  };

  // אפקט כתיבה חי
  useEffect(() => {
    if (!concept) return;

    setDisplayedConcept(""); // נתחיל ריק
    let i = 0;
    const interval = setInterval(() => {
      setDisplayedConcept(prev => prev + concept[i]);
      i++;
      if (i >= concept.length) clearInterval(interval);
    }, 15); // מהירות הקלדה

    return () => clearInterval(interval);
  }, [concept]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white px-4">
      <TopHeader />
      <div className="bg-white/5 backdrop-blur-xl border border-white/10 shadow-xl rounded-2xl p-10 max-w-xl w-full space-y-6">
        <div>
          <h1 className="text-4xl font-extrabold text-center text-white leading-tight">
            One Concept a Day
          </h1>
          <p className="text-center text-gray-300 text-lg mt-2">
            What's on your mind ?
          </p>
        </div>

        <input
          type="text"
          placeholder="Try a topic (e.g. 'AI')"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="w-full p-3 border border-gray-700 bg-gray-900 text-white rounded-md placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500"
        />

        <button
          onClick={fetchConcept}
          className="w-full bg-gradient-to-r from-purple-600 via-pink-500 to-red-500 hover:opacity-90 text-white py-3 px-6 rounded-xl text-lg font-semibold shadow-lg transition duration-200"
        >
          {loading ? "Loading..." : "Get Concept"}
        </button>

        {concept && (
          <div className="bg-gray-800/80 p-4 rounded-lg border border-gray-600">
            <strong className="block mb-2 text-white text-lg">Concept:</strong>
            <p className="text-gray-300 whitespace-pre-line">{displayedConcept}</p>
          </div>
        )}
      </div>
    </div>
  );
}
