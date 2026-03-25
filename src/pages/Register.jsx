import { useNavigate } from "react-router-dom";
import { registerUser } from "../services/cognitoAuth";
import { useState } from "react";

export default function Register() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    const email = e.target.email.value;
    const password = e.target.password.value;
    const confirmPassword = e.target.confirmPassword.value;

    // Basic validation
    if (password !== confirmPassword) {
      setError("Passwords do not match");
      setLoading(false);
      return;
    }

    try {
      await registerUser(email, password);
      // Redirect to login with success message
      navigate("/login", { state: { message: "Registration successful! Please login." } });
    } catch (error) {
      setError(error.message || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-md px-4 py-8">
      <form onSubmit={handleRegister} className="space-y-4 rounded-xl bg-white p-6 ring-1 ring-slate-200">
        <h2 className="text-2xl font-semibold text-slate-900">Register</h2>
        
        {error && <div className="p-3 bg-red-100 border border-red-400 text-red-700 rounded">{error}</div>}
        
        <input 
          name="email" 
          type="email"
          placeholder="Email" 
          required 
          className="w-full rounded-lg border border-slate-300 px-3 py-2" 
        />
        <input 
          name="password" 
          type="password" 
          placeholder="Password" 
          required 
          className="w-full rounded-lg border border-slate-300 px-3 py-2" 
        />
        <input 
          name="confirmPassword" 
          type="password" 
          placeholder="Confirm Password" 
          required 
          className="w-full rounded-lg border border-slate-300 px-3 py-2" 
        />
        <button 
          type="submit" 
          disabled={loading}
          className="w-full rounded-lg bg-blue-700 px-3 py-2 font-semibold text-white disabled:bg-blue-400"
        >
          {loading ? "Registering..." : "Register"}
        </button>

        <p className="text-sm text-slate-600 text-center">
          Already have an account?{" "}
          <a href="/login" className="text-blue-700 hover:underline">
            Login here
          </a>
        </p>
      </form>
    </main>
  );
}