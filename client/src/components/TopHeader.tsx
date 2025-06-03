import { useNavigate } from "react-router-dom";

export default function TopHeader() {
  const navigate = useNavigate();

  return (
    <header className="w-full px-4 sm:px-6 py-4 flex flex-wrap justify-between items-center fixed top-0 left-0 right-0 z-50 backdrop-blur-md bg-black/70 border-b border-zinc-800">
      <h1 className="text-lg font-semibold text-white tracking-wide mb-2 sm:mb-0" style={{ fontFamily: 'Poppins, sans-serif' }}>

      </h1>
      <div className="flex space-x-2 sm:space-x-4 w-full sm:w-auto justify-end">
        <button
          onClick={() => navigate("/login")}
          className="flex-1 sm:flex-none px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded hover:text-white hover:border-white transition"
        >
          Login
        </button>
        <button
          onClick={() => navigate("/signup")}
          className="flex-1 sm:flex-none px-4 py-2 text-sm text-gray-300 border border-gray-600 rounded hover:text-white hover:border-white transition"
        >
          Sign Up
        </button>
      </div>
    </header>
  );
}
