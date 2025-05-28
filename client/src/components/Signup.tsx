// client/src/components/Signup.tsx
import { useState } from "react";
import { createUser } from "../api/user";

export default function Signup() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [interests, setInterests] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const parsedInterests = interests
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean); // removes empty strings

    const user = {
      username,
      email,
      interests: parsedInterests,
    };

    console.log("Sending user:", user); // DEBUG

    try {
      const result = await createUser(user);
      console.log("User created:", result);
      alert("User created successfully");
    } catch (error) {
      console.error("Signup failed", error);
      alert("Failed to create user");
    }
  };

  return (
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
        type="text"
        placeholder="Interests (comma separated)"
        value={interests}
        onChange={(e) => setInterests(e.target.value)}
      />
      <button type="submit">Sign Up</button>
    </form>
  );
}
