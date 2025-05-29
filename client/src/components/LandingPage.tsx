// client/src/pages/LandingPage.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LandingPage() {
  const [category, setCategory] = useState("");
  const [concept, setConcept] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const fetchConcept = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/daily-concept?category=${encodeURIComponent(category)}`);
      if (!response.ok) {
        throw new Error("Failed to fetch concept");
      }
      const data = await response.json();
      setConcept(data.concept);
    } catch (error) {
      setConcept("Error fetching concept");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white p-6">
      <div className="bg-gray-800 shadow-2xl rounded-2xl p-8 max-w-xl w-full space-y-6 border border-gray-700">
        <h1 className="text-4xl font-extrabold text-center text-white">One Concept a Day</h1>
        <p className="text-center text-gray-300">
          Discover a new idea every day – no account needed.
        </p>

        <input
          type="text"
          placeholder="Try a topic (e.g. 'AI')"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="w-full p-2 border border-gray-600 bg-gray-900 text-white rounded placeholder-gray-400"
        />

        <button
          onClick={fetchConcept}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded font-semibold transition"
        >
          {loading ? "Loading..." : "Get Concept"}
        </button>

        {concept && (
          <div className="bg-gray-700 p-4 rounded border border-gray-600">
            <strong className="block mb-2 text-white">Concept:</strong>
            <p className="text-gray-200">{concept}</p>
          </div>
        )}

        <div className="flex justify-between pt-2">
          <button
            onClick={() => navigate("/login")}
            className="text-teal-400 hover:underline"
          >
            Login
          </button>
          <button
            onClick={() => navigate("/signup")}
            className="text-teal-400 hover:underline"
          >
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}
