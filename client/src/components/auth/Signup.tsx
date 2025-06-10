import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AuthHeader from "./AuthHeader";
import { createUser } from "../../api/user";

import "../styles/Animations.css";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [interests, setInterests] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  // Shared input styling to avoid code duplication
  const inputClassName =
    "w-full px-4 py-3 rounded-xl bg-zinc-800 border border-zinc-700 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0 disabled:opacity-50 disabled:cursor-not-allowed";

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) navigate("/dashboard");
  }, []);

  const validateInputs = () => {
    if (!username.trim()) {
      setError("Please enter a username");
      return false;
    }
    if (username.length < 3) {
      setError("Username must be at least 3 characters long");
      return false;
    }
    if (!email.trim()) {
      setError("Please enter your email address");
      return false;
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
      setError("Please enter a valid email address");
      return false;
    }
    if (!password.trim()) {
      setError("Please enter a password");
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

    const user = {
      username: username.trim(),
      email: email.trim(),
      password,
      interests: interests
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s.length > 0),
    };

    try {
      const result = await createUser(user);
      localStorage.setItem("user", JSON.stringify(result));
      navigate("/dashboard");
    } catch (error: any) {
      // Handle different types of errors with specific messages
      if (
        error.message?.includes("Failed to fetch") ||
        error.message?.includes("NetworkError")
      ) {
        setError("Connection error. Please try again.");
      } else if (error.message?.includes("already exists")) {
        setError("A user with this email already exists");
      } else if (error.message?.includes("400")) {
        setError("Invalid data. Please check your details");
      } else {
        setError("Failed to create account. Please try again");
      }
    } finally {
      setIsLoading(false);
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
          {/* Error Message Display */}
          {error && (
            <div className="bg-red-900/50 border border-red-700 text-red-300 px-4 py-3 rounded-xl text-sm animate-fade-in">
              {error}
            </div>
          )}

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className={inputClassName}
            disabled={isLoading}
            required
          />
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
          <input
            type="text"
            placeholder="Interests (comma separated)"
            value={interests}
            onChange={(e) => setInterests(e.target.value)}
            className={inputClassName}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-zinc-700 hover:bg-zinc-600 disabled:bg-zinc-800 disabled:cursor-not-allowed transition text-white font-semibold py-3 rounded-xl focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0 flex items-center justify-center gap-2"
          >
            {isLoading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Creating account...
              </>
            ) : (
              "Sign Up"
            )}
          </button>
        </form>
        {/* Right Side Quote */}
        <div className="flex-1 text-center px-4">
          <h2 className="text-4xl md:text-5xl font-bold mt-8 mb-2 text-white text-center">
            Join the journey
          </h2>
          <p className="text-gray-400 text-lg">
            Start learning one concept a day
          </p>
        </div>
      </div>
    </div>
  );
}