import { extendTheme } from "@chakra-ui/react";

// Cyber-punk neon color palette
const theme = extendTheme({
  colors: {
    // Primary neon colors
    neonPink: {
      50: "#fef7ff",
      100: "#feeaff",
      200: "#fdd5ff",
      300: "#fcb0ff",
      400: "#f97bff",
      500: "#f146ff",
      600: "#e011ff",
      700: "#c700e0",
      800: "#a500b8",
      900: "#850094",
    },
    neonBlue: {
      50: "#f0f9ff",
      100: "#e0f2fe",
      200: "#bae6fd",
      300: "#7dd3fc",
      400: "#38bdf8",
      500: "#0ea5e9",
      600: "#0284c7",
      700: "#0369a1",
      800: "#075985",
      900: "#0c4a6e",
    },
    neonGreen: {
      50: "#f0fdf4",
      100: "#dcfce7",
      200: "#bbf7d0",
      300: "#86efac",
      400: "#4ade80",
      500: "#22c55e",
      600: "#16a34a",
      700: "#15803d",
      800: "#166534",
      900: "#14532d",
    },
    neonPurple: {
      50: "#faf5ff",
      100: "#f3e8ff",
      200: "#e9d5ff",
      300: "#d8b4fe",
      400: "#c084fc",
      500: "#a855f7",
      600: "#9333ea",
      700: "#7c3aed",
      800: "#6b21a8",
      900: "#581c87",
    },
    neonOrange: {
      50: "#fff7ed",
      100: "#ffedd5",
      200: "#fed7aa",
      300: "#fdba74",
      400: "#fb923c",
      500: "#f97316",
      600: "#ea580c",
      700: "#c2410c",
      800: "#9a3412",
      900: "#7c2d12",
    },
    // Dark background colors
    darkBg: {
      50: "#1a1a1a",
      100: "#0f0f0f",
      200: "#0a0a0a",
      300: "#050505",
      400: "#000000",
      500: "#000000",
      600: "#000000",
      700: "#000000",
      800: "#000000",
      900: "#000000",
    },
    // Override default colors for cyber-punk theme
    brand: {
      50: "#fef7ff",
      100: "#feeaff",
      200: "#fdd5ff",
      300: "#fcb0ff",
      400: "#f97bff",
      500: "#f146ff",
      600: "#e011ff",
      700: "#c700e0",
      800: "#a500b8",
      900: "#850094",
    },
  },
  config: {
    initialColorMode: "dark",
    useSystemColorMode: false,
  },
  styles: {
    global: (props) => ({
      body: {
        bg: props.colorMode === "dark" ? "darkBg.100" : "white",
        color: props.colorMode === "dark" ? "neonPink.300" : "gray.800",
        fontFamily: "'Orbitron', 'Courier New', monospace",
      },
      "*": {
        borderColor: props.colorMode === "dark" ? "neonBlue.500" : "gray.200",
      },
    }),
  },
  fonts: {
    heading: "'Orbitron', 'Arial Black', sans-serif",
    body: "'Roboto Mono', 'Courier New', monospace",
  },
  components: {
    Button: {
      baseStyle: {
        fontWeight: "bold",
        textTransform: "uppercase",
        letterSpacing: "0.1em",
      },
      variants: {
        solid: (props) => ({
          bg: props.colorMode === "dark" ? "neonPink.500" : "brand.500",
          color: "darkBg.100",
          _hover: {
            bg: props.colorMode === "dark" ? "neonPink.400" : "brand.400",
            boxShadow: "0 0 20px rgba(241, 70, 255, 0.6)",
            transform: "translateY(-2px)",
          },
          _active: {
            bg: props.colorMode === "dark" ? "neonPink.600" : "brand.600",
          },
          transition: "all 0.3s ease",
        }),
        outline: (props) => ({
          borderColor:
            props.colorMode === "dark" ? "neonBlue.500" : "brand.500",
          color: props.colorMode === "dark" ? "neonBlue.300" : "brand.500",
          _hover: {
            bg: props.colorMode === "dark" ? "neonBlue.500" : "brand.500",
            color: "darkBg.100",
            boxShadow: "0 0 15px rgba(14, 165, 233, 0.5)",
          },
        }),
        ghost: (props) => ({
          color: props.colorMode === "dark" ? "neonGreen.400" : "brand.500",
          _hover: {
            bg: props.colorMode === "dark" ? "neonGreen.900" : "brand.50",
            boxShadow: "0 0 10px rgba(34, 197, 94, 0.3)",
          },
        }),
      },
    },
    Input: {
      variants: {
        outline: (props) => ({
          field: {
            borderColor:
              props.colorMode === "dark" ? "neonBlue.500" : "gray.300",
            bg: props.colorMode === "dark" ? "darkBg.200" : "white",
            color: props.colorMode === "dark" ? "neonPink.200" : "gray.800",
            _hover: {
              borderColor:
                props.colorMode === "dark" ? "neonBlue.400" : "brand.400",
            },
            _focus: {
              borderColor:
                props.colorMode === "dark" ? "neonPink.500" : "brand.500",
              boxShadow:
                props.colorMode === "dark"
                  ? "0 0 0 1px rgba(241, 70, 255, 0.6)"
                  : "0 0 0 1px rgba(165, 85, 247, 0.6)",
            },
          },
        }),
      },
    },
    Card: {
      baseStyle: (props) => ({
        container: {
          bg: props.colorMode === "dark" ? "darkBg.200" : "white",
          borderColor: props.colorMode === "dark" ? "neonBlue.600" : "gray.200",
          borderWidth: "1px",
          boxShadow:
            props.colorMode === "dark"
              ? "0 4px 12px rgba(14, 165, 233, 0.15)"
              : "lg",
          _hover: {
            boxShadow:
              props.colorMode === "dark"
                ? "0 8px 25px rgba(14, 165, 233, 0.25)"
                : "xl",
            transform: "translateY(-2px)",
          },
          transition: "all 0.3s ease",
        },
      }),
    },
    Heading: {
      baseStyle: (props) => ({
        color: props.colorMode === "dark" ? "neonPink.300" : "gray.800",
        textShadow:
          props.colorMode === "dark"
            ? "0 0 10px rgba(241, 70, 255, 0.5)"
            : "none",
      }),
    },
    Text: {
      baseStyle: (props) => ({
        color: props.colorMode === "dark" ? "neonBlue.200" : "gray.600",
      }),
    },
  },
});

export default theme;
