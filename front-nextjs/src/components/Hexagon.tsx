import React from "react";

type HexagonProps = {
  x: number;
  y: number;
  size: number;
  color: string;
  id: string;
  onClick: (id: string) => void;
};

const Hexagon: React.FC<HexagonProps> = ({ x, y, size, color, id, onClick }) => {
  const angle = (i: number) => (Math.PI / 180) * (60 * i);
  const points = Array.from({ length: 6 }).map((_, i) => {
    const px = x + size * Math.cos(angle(i));
    const py = y + size * Math.sin(angle(i));
    return `${px},${py}`;
  });

  return (
    <polygon
      points={points.join(" ")}
      fill={color}
      stroke="gray"
      strokeWidth={1}
      onClick={() => onClick(id)}
      className="cursor-pointer"
    />
  );
};

export default Hexagon;
