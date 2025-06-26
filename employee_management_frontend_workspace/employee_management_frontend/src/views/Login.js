import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, getCurrentUser } from "../api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setErr(null);
    try {
      await login(email, password);
      // Optionally fetch user profile to test token
      await getCurrentUser();
      navigate("/");
    } catch (e) {
      setErr("Invalid email or password");
    }
    setLoading(false);
  }

  return (
    <div className="main-content" style={{ maxWidth: 420, margin: "70px auto" }}>
      <form className="card" style={{ width: "100%" }} onSubmit={handleSubmit}>
        <h2 style={{ marginBottom: 10 }}>Login</h2>
        <label className="form-label" htmlFor="email">Email</label>
        <input required type="email" id="email" autoComplete="username"
          value={email} onChange={e => setEmail(e.target.value)} placeholder="user@company.com" />

        <label className="form-label" htmlFor="password">Password</label>
        <input required type="password" id="password" autoComplete="current-password"
          value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
        {err && <div className="form-error">{err}</div>}
        <button className="btn btn-accent" type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}
