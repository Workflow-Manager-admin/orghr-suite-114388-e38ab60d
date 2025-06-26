//
// Centralized theme and color definitions based on requirement
//
export const COLORS = {
  primary: "#1976d2",
  accent: "#fbc02d",
  secondary: "#424242",
  background: "#ffffff",
  sidebar: "#f8f9fa",
  text: "#282c34",
  border: "#e9ecef",
  error: "#d32f2f",
  success: "#388e3c"
};

export const THEME = {
  light: {
    background: COLORS.background,
    sidebar: COLORS.sidebar,
    text: COLORS.text,
    primary: COLORS.primary,
    accent: COLORS.accent,
    secondary: COLORS.secondary
  }
  // dark: { ... } // Optionally can extend in the future
};
