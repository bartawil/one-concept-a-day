// DailyConcept.tsx
import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './DailyConcept.css';
import useTypewriter from './useTypewriter';
import EditInterests from './EditInterests';
import { Settings } from "lucide-react";


function DailyConcept() {
  const [category, setCategory] = useState('');
  const [concept, setConcept] = useState('');
  const [term, setTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  const displayedConcept = useTypewriter(concept);
  const storedUser = localStorage.getItem("user");
  const username = storedUser ? JSON.parse(storedUser).username : "";
  const interests = storedUser ? JSON.parse(storedUser).interests : [];
  const navigate = useNavigate();

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (!user) {
      navigate("/login");
    } else if (interests.length > 0 && category === '') {
      setCategory(interests[0]);
    }
  }, []);

  const fetchConcept = async () => {
    setConcept("");
    try {
      const storedUser = localStorage.getItem("user");
      if (!storedUser) return;
      const user = JSON.parse(storedUser);
      const userId = user.id;
      const response = await fetch(
        `http://localhost:8000/daily-concept?category=${encodeURIComponent(category)}&user_id=${userId}`
      );
      if (!response.ok) throw new Error("Failed to fetch concept");
      const data = await response.json();
      setConcept(data.explanation);
      setTerm(data.term);
    } catch {
      setConcept("Error fetching concept");
    }
  };

  useEffect(() => {
    if (category && !concept) {
      fetchConcept();
    }
  }, [category]);

  return (
    <div className="min-h-screen bg-black text-white font-sans px-4 pb-8 pt-24 flex flex-col">
      <header className="w-full px-4 sm:px-6 py-4 flex flex-wrap justify-between items-center fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-black/70 border-b border-zinc-800">
        <div className="flex justify-between w-full">
          <button
            onClick={() => setIsModalOpen(true)}
            className="p-2 text-gray-300 border border-gray-600 rounded hover:text-white hover:border-white transition"
            aria-label="Edit Interests"
          >
            <Settings className="w-5 h-5" />
          </button>


          <button
            onClick={() => {
              localStorage.removeItem("user");
              window.location.href = "/";
            }}
            className="px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded hover:text-white hover:border-white transition"
          >
            Logout
          </button>
        </div>

      </header>

      <main className="flex-1 flex flex-col items-center justify-center w-full">
        <div className="w-full max-w-xl text-center mb-10 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mt-8 mb-4 text-white">
            Hi {username}!
          </h2>
          <p className="text-gray-400 text-lg">
            Here's your concept for today based on your interests.
          </p>
        </div>

        {displayedConcept && (
          <div className="w-full max-w-xl mt-4 bg-zinc-900 p-6 rounded-2xl shadow-lg animate-fade-in">
            <h4 className="text-md italic text-zinc-400 mb-3">Today’s Concept about {term}:</h4>
            <p className="whitespace-pre-wrap leading-relaxed text-gray-300">
              {displayedConcept}<span className="blinking-cursor"></span>
            </p>
          </div>
        )}
      </main>

      {isModalOpen && (
        <div className="modal-backdrop" onClick={() => setIsModalOpen(false)}>
          <div className="modal-slide-in-left" onClick={(e) => e.stopPropagation()}>
            <EditInterests isOpen={true} onClose={() => setIsModalOpen(false)} />
          </div>
        </div>
      )}

      <style>{`
        .blinking-cursor {
          display: inline-block;
          width: 1px;
          background-color: white;
          animation: blink 1s step-start infinite;
        }
        @keyframes blink {
          50% { opacity: 0; }
        }
        @keyframes fade-in {
          0% { opacity: 0; transform: translateY(10px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in {
          animation: fade-in 0.8s ease-out both;
        }
        .modal-backdrop {
          position: fixed;
          inset: 0;
          z-index: 50;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          justify-content: flex-start;
          align-items: stretch;
          animation: backdrop-fade-in 0.2s ease-out forwards;
        }
        @keyframes backdrop-fade-in {
          from { background-color: rgba(0, 0, 0, 0); }
          to { background-color: rgba(0, 0, 0, 0.5); }
        }
        .modal-slide-in-left {
          width: 100%;
          max-width: 400px;
          height: 100%;
          background: #18181b;
          border-right: 1px solid #3f3f46;
          animation: slide-in-left 0.3s ease-out forwards;
        }
        @keyframes slide-in-left {
          from { transform: translateX(-100%); }
          to { transform: translateX(0); }
        }
      `}</style>
    </div>
  );
}

export default DailyConcept;