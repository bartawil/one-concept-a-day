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
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <div className="bg-white shadow-xl rounded-2xl p-8 max-w-xl w-full space-y-6">
        <h1 className="text-3xl font-bold text-center">One Concept a Day</h1>
        <p className="text-center text-gray-600">
          Discover a new idea every day – no account needed.
        </p>

        <input
          type="text"
          placeholder="Try a topic (e.g. 'AI')"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded"
        />

        <button
          onClick={fetchConcept}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          {loading ? "Loading..." : "Get Concept"}
        </button>

        {concept && (
          <div className="bg-gray-100 p-4 rounded">
            <strong className="block mb-2 text-gray-700">Concept:</strong>
            <p className="text-gray-800">{concept}</p>
          </div>
        )}

        <div className="flex justify-between">
          <button
            onClick={() => navigate("/login")}
            className="text-blue-600 hover:underline"
          >
            Login
          </button>
          <button
            onClick={() => navigate("/signup")}
            className="text-blue-600 hover:underline"
          >
            Sign Up
          </button>
        </div>
      </div>
    </div>
  );
}
