import { useState } from 'react';
import './DailyConcept.css';


function DailyConcept() {
  const [category, setCategory] = useState('');
  const [concept, setConcept] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchConcept = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/daily-concept?category=${encodeURIComponent(category)}`);
      if (!response.ok) {
        throw new Error('Failed to fetch concept');
      }
      const data = await response.json();
      setConcept(data.concept);
    } catch (error) {
      setConcept('Error fetching concept');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="p-6 max-w-xl mx-auto bg-white rounded-2xl shadow-md space-y-4">
        <h2 className="text-2xl font-bold text-center">One Concept a Day</h2>

        <input
          type="text"
          placeholder="Enter a topic (e.g. AI)"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="w-full p-2 border border-gray-300 rounded"
        />

        <button
          onClick={fetchConcept}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
        >
          Get Concept
        </button>

        {loading ? (
          <p className="text-center text-gray-500">Loading...</p>
        ) : concept && (
          <div className="bg-gray-100 p-4 rounded">
            <strong className="block mb-2 text-gray-700">Concept:</strong>
            <p className="text-gray-800">{concept}</p>
          </div>
        )}
      </div>
    </div>


  );
}

export default DailyConcept;
