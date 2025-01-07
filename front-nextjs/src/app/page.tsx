import Head from "next/head";
import HexagonGrid from "@/components/HexagonGrid";
import ColorButtons from "@/components/ColorButtons";
import Toolbar from "@/components/Toolbar";

export default function Home() {
  return (
    <>
      <Head>
        <title>Chiffre deux</title>
      </Head>
      <div className="flex flex-col h-screen bg-gray-50 p-6 space-y-6">
        {/* Barre d'outils */}
        <Toolbar />

        {/* Contenu principal */}
        <div className="flex flex-grow space-x-6">
          {/* Barre latérale */}
          <ColorButtons />

          {/* Grille hexagonale */}
          <div className="flex-grow flex justify-center items-center bg-white rounded-lg shadow-lg p-6">
            <HexagonGrid />
          </div>
        </div>
      </div>
    </>
  );
}
