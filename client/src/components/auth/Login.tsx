import { useState } from "react";
import { useNavigate } from "react-router-dom";
import AuthHeader from "./AuthHeader";
import { loginUser } from "../../api/user";

import "../styles/Animations.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Shared input styling to avoid code duplication
  const inputClassName =
    "w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0 disabled:opacity-50 disabled:cursor-not-allowed";

  const validateInputs = () => {
    if (!email.trim()) {
      setError("Please enter your email address");
      return false;
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
      setError("Please enter a valid email address");
      return false;
    }
    if (!password.trim()) {
      setError("Please enter your password");
      return false;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters long");
      return false;
    }
    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!validateInputs()) {
      return;
    }

    setIsLoading(true);

    try {
      const result = await loginUser({ email, password });
      localStorage.setItem("user", JSON.stringify(result));
      navigate("/dashboard");
    } catch (error: any) {
      // Handle different types of errors with specific messages
      if (
        error.message?.includes("Failed to fetch") ||
        error.message?.includes("NetworkError")
      ) {
        setError("Connection error. Please try again.");
      } else if (error.message?.includes("401") || error.message?.includes("Invalid")) {
        setError("Invalid email or password");
      } else if (error.message?.includes("429")) {
        setError("Too many login attempts. Please wait and try again");
      } else {
        setError("Login failed. Please try again");
      }
    } finally {
      setIsLoading(false);
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
          {/* Error Message Display */}
          {error && (
            <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-xl text-sm animate-fade-in">
              {error}
            </div>
          )}

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={inputClassName}
            disabled={isLoading}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className={inputClassName}
            disabled={isLoading}
            required
          />
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed transition text-white font-semibold py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0 flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Signing in...
              </>
            ) : (
              "Sign In"
            )}
          </button>
        </form>
        {/* Right Side Quote */}
        <div className="flex-1 text-center px-4">
          <h2 className="text-4xl md:text-5xl font-bold mt-8 mb-2 text-white text-center">
            Welcome back
          </h2>
          <p className="text-gray-400 text-lg">Good to see you again</p>
        </div>
      </div>
    </div>
  );
}
