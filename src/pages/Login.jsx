import { useAuth } from "../context/AuthContext";
import { loginUser } from "../services/cognitoAuth";
import { useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const email = e.target.email.value;
    const password = e.target.password.value;

    try {
      const response = await loginUser(email, password);
      const token = response?.AuthenticationResult?.IdToken;
      const user = response?.user;

      if (!token) {
        setError("Login succeeded but token is missing.");
        return;
      }

      // Store idToken and user
      login(token, user);

      // Redirect to intended page or home
      const from = location.state?.from?.pathname || "/";
      navigate(from);
    } catch (error) {
      setError(error.message || "Login failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-md px-4 py-8">
      <form onSubmit={handleLogin} className="space-y-4 rounded-xl bg-white p-6 ring-1 ring-slate-200">
        <h2 className="text-2xl font-semibold text-slate-900">Login</h2>
        
        {error && <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>}
        
        <input 
          name="email" 
          type="email"
          required 
          placeholder="Email" 
          className="w-full rounded-lg border border-slate-300 px-3 py-2" 
        />
        <input 
          name="password" 
          type="password" 
          required 
          placeholder="Password" 
          className="w-full rounded-lg border border-slate-300 px-3 py-2" 
        />
        <button 
          type="submit" 
          disabled={loading}
          className="w-full rounded-lg bg-blue-700 px-3 py-2 font-semibold text-white disabled:bg-blue-400"
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <p className="text-sm text-slate-600 text-center">
          Don't have an account?{" "}
          <a href="/register" className="text-blue-700 hover:underline">
            Register here
          </a>
        </p>
      </form>
    </main>
  );
}