// client/src/components/EditInterests.tsx
import { useState } from "react";
import { Trash2 } from "lucide-react";


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

      await fetch(`http://localhost:8000/user/${user.id}/interests/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(trimmed),
      });

      setNewInterest("");
    }
  };

  const handleRemove = async (interest: string) => {
    const updated = interests.filter((i) => i !== interest);
    setInterests(updated);
    localStorage.setItem("user", JSON.stringify({ ...user, interests: updated }));

    await fetch(`http://localhost:8000/user/${user.id}/interests/remove`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(interest),
    });
  };

  return (
    <div className="fixed inset-0 z-50 flex justify-start">
      <div className="bg-zinc-900 w-full max-w-md h-full shadow-lg p-6 border-r border-zinc-700 overflow-y-auto">
        <div className="mb-6 flex justify-between items-center">
          <h2 className="text-xl font-bold text-white">Edit Interests</h2>
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
            className="flex-1 px-3 py-2 rounded bg-zinc-800 text-white border border-zinc-600"
          />
          <button
            onClick={handleAdd}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Add
          </button>
        </div>

        <ul className="space-y-2 mt-8 mb-4">
          {interests.map((interest, idx) => (
            <li
              key={idx}
              className="flex justify-between items-center bg-zinc-800 px-4 py-2 rounded"
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
    </div>
  );
}
