import { useState } from "react";
import { PlusCircle, Trash2 } from "lucide-react";
import { addUserInterest, removeUserInterest } from "../../api/dashboard";

interface Props {
  isOpen: boolean;
  onClose: () => void;
}

export default function EditInterests({ isOpen, onClose }: Props) {
  const storedUser = localStorage.getItem("user");
  const user = storedUser ? JSON.parse(storedUser) : null;
  const [interests, setInterests] = useState<string[]>(user?.interests || []);
  const [newInterest, setNewInterest] = useState("");

  if (!isOpen) return null;

  const handleAdd = async () => {
    const trimmed = newInterest.trim();
    if (trimmed && !interests.includes(trimmed)) {
      const updated = [...interests, trimmed];
      setInterests(updated);
      localStorage.setItem("user", JSON.stringify({ ...user, interests: updated }));

      await addUserInterest(user.id, trimmed);

      setNewInterest("");
    }
  };

  const handleRemove = async (interest: string) => {
    const updated = interests.filter((i) => i !== interest);
    setInterests(updated);
    localStorage.setItem("user", JSON.stringify({ ...user, interests: updated }));

    await removeUserInterest(user.id, interest);
  };

  return (
    <div className="bg-zinc-900 w-full max-w-md h-full shadow-lg p-6 border-r border-zinc-700 overflow-y-auto">
      <div className="mb-6 flex justify-between items-center">
        <h2 className="text-xl font-bold text-white averia-serif-libre-bold">Edit Interests</h2>
        <button onClick={onClose} className="text-gray-400 hover:text-white text-sm">
          ✕
        </button>
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={newInterest}
          onChange={(e) => setNewInterest(e.target.value)}
          placeholder="Add interest"
          className="flex-1 px-3 py-2 rounded bg-zinc-800 text-white border-zinc-600 focus:outline-none focus:ring-2 focus:ring-zinc-500/40 focus:ring-offset-0"
        />
        <button
          onClick={handleAdd}
          className="flex-1 sm:flex-none px-3 py-2 text-sm text-gray-300 border border-gray-600 rounded hover:text-white hover:border-white transition"
          aria-label="Add Interest"
        >
          <PlusCircle size={20} />
        </button>
      </div>

      <ul className="space-y-2 mt-8 mb-4">
        {interests.map((interest, idx) => (
          <li
            key={idx}
            className="flex justify-between items-center bg-zinc-800 px-4 py-2 rounded averia-serif-libre-bold"
          >
            <span>{interest}</span>
            <button
              onClick={() => handleRemove(interest)}
              className="text-red-400 hover:text-red-600 text-sm"
            >
              <Trash2 size={16} />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
