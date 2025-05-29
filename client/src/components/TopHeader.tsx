import { useNavigate } from "react-router-dom";

export default function TopHeader() {
  const navigate = useNavigate();

  return (
    <header className="w-full flex justify-between items-center px-6 py-4 bg-transparent absolute top-0 left-0">
      <h1 className="text-xl font-bold text-white"></h1>
      <div className="space-x-4">
        <button
          onClick={() => navigate("/login")}
          className="px-4 py-2 border border-white text-white rounded hover:bg-white hover:text-black transition"
        >
          Login
        </button>
        <button
          onClick={() => navigate("/signup")}
          className="px-4 py-2 border border-white text-white rounded hover:bg-white hover:text-black transition"
        >
          Sign Up
        </button>
      </div>
    </header>
  );
}