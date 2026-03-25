import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(
    !!localStorage.getItem("token") || !!localStorage.getItem("idToken")
  );
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("user");
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch (error) {
        console.error("Failed to parse stored user:", error);
      }
    }
    return null;
  });

  const login = (token, userInfo) => {
    // Store JWT token
    localStorage.setItem("token", token);
    localStorage.setItem("idToken", token); // For API interceptor compatibility
    
    // Store user info
    const finalUserInfo = userInfo || { email: "" };
    localStorage.setItem("user", JSON.stringify(finalUserInfo));
    
    setIsAuthenticated(true);
    setUser(finalUserInfo);
  };

  const logout = () => {
    // Clear all auth-related storage
    localStorage.removeItem("token");
    localStorage.removeItem("idToken");
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("user");
    
    setIsAuthenticated(false);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);