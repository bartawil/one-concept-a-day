import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Settings } from "lucide-react";

import "../styles/Animations.css";
import "../styles/Fonts.css";

import useTypewriter from '../features/useTypewriter';
import EditInterests from './EditInterests';
import { getDailyConcept } from '../../api/dashboard';

function Dashboard() {
  const [category, setCategory] = useState('');
  const [concept, setConcept] = useState('');
  const [term, setTerm] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalVisible, setModalVisible] = useState(false); // for animation class

  const displayedConcept = useTypewriter(concept);

  const getStoredUser = () => {
    const raw = localStorage.getItem("user");
    return raw ? JSON.parse(raw) : null;
  };

  const storedUser = getStoredUser();
  const username = storedUser?.username ?? "";
  const interests = storedUser?.interests ?? [];

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
      const data = await getDailyConcept(userId, category);
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

  const openModal = () => {
    setIsModalOpen(true);
    setTimeout(() => setModalVisible(true), 10);
  };

  const closeModal = () => {
    setModalVisible(false);
    setTimeout(() => setIsModalOpen(false), 300); // must match animation duration
  };

  return (
    <div className="min-h-screen bg-black text-white font-sans px-4 pb-8 pt-24 flex flex-col">
      <header className="w-full px-4 sm:px-6 py-4 flex flex-wrap justify-between items-center fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-black/70 border-b border-zinc-800">
        <div className="flex justify-between w-full">
          <button
            onClick={openModal}
            className="flex-1 sm:flex-none px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded hover:text-white hover:border-white transition"
            aria-label="Edit Interests"
          >
            <Settings className="w-5 h-5" />
          </button>
          <button
            onClick={() => {
              localStorage.removeItem("user");
              window.location.href = "/";
            }}
            className="flex-1 sm:flex-none px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded hover:text-white hover:border-white transition"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-center w-full">
        <div className="w-full max-w-xl text-center mb-10 animate-fade-in">
          <h2 className="text-4xl md:text-5xl font-bold mt-8 mb-4 text-white averia-serif-libre-bold">
            Hi {username}!
          </h2>
          <p className="text-gray-400 text-lg mt-4 averia-serif-libre-bold">
            Here's your concept for today based on your interests.
          </p>
        </div>
        {displayedConcept && (
          <div className="w-full max-w-xl mt-4 bg-zinc-900 p-6 rounded-2xl shadow-lg animate-fade-in z-10">
            <h4 className="text-md italic text-zinc-400 mb-3 averia-serif-libre-bold">{term}:</h4>
            <p className="whitespace-pre-wrap leading-relaxed text-gray-300 ">
              {displayedConcept}<span className="blinking-cursor"></span>
            </p>
          </div>
        )}
      </main>
      <img
        src="/app_icon.svg"
        className="h-50 w-50 filter invert absolute bottom-15 right-4 z-0"
      />
      {isModalOpen && (
        <div className="modal-backdrop" onClick={closeModal}>
          <div
            className={modalVisible ? "modal-slide-in-left animate-in" : "modal-slide-in-left animate-out"}
            onClick={(e) => e.stopPropagation()}
          >
            <EditInterests isOpen={true} onClose={closeModal} />
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
