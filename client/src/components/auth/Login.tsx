import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthHeader from "./AuthHeader";
import { loginUser } from "../../api/user";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await loginUser({ email, password });
      localStorage.setItem("user", JSON.stringify(result));
      navigate("/dashboard");
    } catch (error) {
      alert("Login failed: Invalid email or password");
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-4">
      <AuthHeader />

      <div className="flex flex-col md:flex-row items-center justify-center gap-12 w-full max-w-6xl mt-12 animate-fade-in">
        {/* Login Form */}
        <form
          onSubmit={handleSubmit}
          className="flex-1 w-full max-w-md space-y-4 bg-zinc-900 p-10 rounded-2xl shadow-lg"
        >

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
          <button
            type="submit"
            className="w-full bg-zinc-700 hover:bg-zinc-600 transition text-white font-semibold py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0"
          >
            Sign In
          </button>
        </form>

        {/* Right Side Quote */}
        <div className="flex-1 text-center px-4">
          <h2 className="text-4xl md:text-5xl font-bold mt-8 mb-2 text-white text-center">Welcome back</h2>
          <p className="text-gray-400 text-lg">Good to see you again</p>
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
