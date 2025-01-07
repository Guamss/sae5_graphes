export default function ColorButtons() {
  const items = [
    { color: "bg-noir", label: "Noir" },
    { color: "bg-blanc", label: "Blanc" },
    { color: "bg-bleu-500", label: "Bleu" },
    { color: "bg-vert-500", label: "Vert" },
    { color: "bg-jaune-500", label: "Jaune" },
    { color: "bg-pink-500", label: "Depart" },
    { color: "bg-red-500", label: "Objectif" },
  ];

  return (
    <div className="flex flex-col bg-gray-100 p-6 rounded-lg shadow-lg space-y-4">
      {items.map(({ color, label }) => (
        <div
          key={label}
          className="flex items-center space-x-3 cursor-pointer hover:opacity-80 transition-all duration-200 ease-in-out"
        >
          <div className={`w-8 h-8 rounded-full ${color} border border-gray-300`} />
          <span className="text-gray-700 font-medium">{label}</span>
        </div>
      ))}
    </div>
  );
}
