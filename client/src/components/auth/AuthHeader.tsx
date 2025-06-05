import { useNavigate } from "react-router-dom";

export default function TopHeader() {
  const navigate = useNavigate();

  return (
    <header className="w-full px-4 sm:px-6 py-4 flex flex-wrap justify-between items-center fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-black/70 border-b border-zinc-800">
      <div className="flex space-x-2 sm:space-x-4 w-full sm:w-auto justify-end">
        <button onClick={() => navigate(-1)} className="flex-1 sm:flex-none px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded hover:text-white hover:border-white transition">
            ← Back
        </button>
      </div>
    </header>
  );
}