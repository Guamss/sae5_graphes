export default function Toolbar() {
  return (
    <div className="flex space-x-4 bg-white shadow-lg p-4 rounded-lg">
      {[
        "Effacer Tout",
        "Effacer Résultats",
        "Aléatoire",
        "Parcours en profondeur",
        "Parcours en largeur",
        "Bellman-Ford",
        "Dijkstra",
        "A*",
      ].map((label) => (
        <button
          key={label}
          className="bg-blue-500 hover:bg-blue-600 text-white text-sm px-4 py-2 rounded-lg transition-all duration-200 ease-in-out shadow-md hover:shadow-lg"
        >
          {label}
        </button>
      ))}
    </div>
  );
}
