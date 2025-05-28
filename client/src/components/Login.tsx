import { useState } from "react";
import { loginUser } from "../api/user";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await loginUser({ email, password });
      console.log("Login successful:", result);
      alert(`Welcome back, ${result.username}!`);
    } catch (error) {
      console.error("Login failed", error);
      alert("Login failed: Invalid email or password");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-2 max-w-sm">
      <h2 className="text-xl font-bold mb-2">Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
      />
      <button type="submit">Login</button>
    </form>
  );
}
