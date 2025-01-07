"use client";

import React, { useState } from "react";
import Hexagon from "./Hexagon";

const HexGrid = () => {
  const cols = 20;
  const rows = 12;
  const size = 30; // Taille d'un hexagone
  const [hexagons, setHexagons] = useState(() =>
    Array.from({ length: cols }, (_, col) =>
      Array.from({ length: rows }, (_, row) => ({
        id: `${col + 1}-${row + 1}`,
        color: "white",
      }))
    )
  );

  const hexWidth = size * 1.5;
  const hexHeight = size * Math.sqrt(3);

  const handleHexClick = (id: string) => {
    setHexagons((prevHexagons) =>
      prevHexagons.map((col) =>
        col.map((hex) =>
          hex.id === id ? { ...hex, color: hex.color === "white" ? "blue" : "white" } : hex
        )
      )
    );
  };

  return (
    <svg
      width={hexWidth * cols + hexWidth / 2}
      height={hexHeight * rows + hexHeight}
      className="bg-black mx-auto"
    >
      {hexagons.map((col, colIndex) =>
        col.map((hex, rowIndex) => {
          const x = colIndex * hexWidth + hexWidth / 2;
          const y =
            rowIndex * hexHeight +
            (colIndex % 2 ? hexHeight / 2 : 0) +
            hexHeight / 4;

          return (
            <Hexagon
              key={hex.id}
              x={x}
              y={y}
              size={size}
              color={hex.color}
              id={hex.id}
              onClick={handleHexClick}
            />
          );
        })
      )}
    </svg>
  );
};

export default HexGrid;
