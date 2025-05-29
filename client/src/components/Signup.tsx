// client/src/components/Signup.tsx
import { useState } from "react";
import { createUser } from "../api/user";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import AuthHeader from "./AuthHeader";


export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [interests, setInterests] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const user = localStorage.getItem("user");
    if (user) {
      navigate("/daily");
    }
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const user = {
      username,
      email,
      password,
      interests: interests.split(",").map(s => s.trim()),
    };

    try {
      const result = await createUser(user);
      console.log("User created:", result);
      localStorage.setItem("user", JSON.stringify(result));
      alert("User created successfully");
      navigate("/daily");
    } catch (error) {
      console.error("Signup failed", error);
      alert("Failed to create user");
    }
  };

  return (
    <div className="p-4">
      <AuthHeader/>
      <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-sm">
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Interests (comma separated)"
          value={interests}
          onChange={(e) => setInterests(e.target.value)}
        />
        <button type="submit">Sign Up</button>
      </form>
    </div>
  );
}
