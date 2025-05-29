import { useNavigate } from "react-router-dom";

export default function TopHeader() {
  const navigate = useNavigate();

  return (
    <header className="w-full flex justify-between items-center px-6 py-4 bg-transparent absolute top-0 left-0">
      <div className="space-x-4">
        <button onClick={() => navigate(-1)} className="text-blue-600 mb-4 hover:underline">
            ← Back
        </button>
      </div>
    </header>
  );
}