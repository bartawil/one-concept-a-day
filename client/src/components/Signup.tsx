import { useState, useEffect } from "react";
import { createUser } from "../api/user";
import { useNavigate } from "react-router-dom";
import AuthHeader from "./AuthHeader";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [interests, setInterests] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) navigate("/daily");
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const user = {
      username,
      email,
      password,
      interests: interests.split(",").map((s) => s.trim()),
    };
    try {
      const result = await createUser(user);
      localStorage.setItem("user", JSON.stringify(result));
      navigate("/daily");
    } catch (error) {
      alert("Failed to create user");
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-4">
      <AuthHeader />

      <div className="flex flex-col md:flex-row items-center justify-center gap-12 w-full max-w-6xl mt-12 animate-fade-in">
        {/* Registration Form */}
        <form
          onSubmit={handleSubmit}
          className="flex-1 w-full max-w-md space-y-4 bg-zinc-900 p-10 rounded-2xl shadow-lg"
        >

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0"
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0"
            required
          />
          <input
            type="text"
            placeholder="Interests (comma separated)"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
            className="w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0"
          />
          <button
            type="submit"
            className="w-full bg-zinc-700 hover:bg-zinc-600 transition text-white font-semibold py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0"
          >
            Sign Up
          </button>
        </form>

        {/* Right Side Quote */}
        <div className="flex-1 text-center px-4">
          <h2 className="text-4xl md:text-5xl font-bold mt-8 mb-2 text-white text-center">Join the journey</h2>
          <p className="text-gray-400 text-lg">Start learning one concept a day</p>
        </div>
      </div>

      <style>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-in {
          animation: fade-in 0.6s ease-out both;
        }
      `}</style>
    </div>
  );
}