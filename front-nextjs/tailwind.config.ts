import type { Config } from "tailwindcss";
import colors from "tailwindcss/colors";

export default {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        noir: colors.black,
        blanc: colors.white,
        bleu: colors.blue,
        vert: colors.green,
        jaune: colors.yellow,
        depart: colors.pink,
        objectif: colors.red,
      },
    },
  },
  plugins: [],
} satisfies Config;
