import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, getCurrentUser } from "../api";

// Util: checks if input is "admin" or a valid email
function isValidUsernameOrEmail(val) {
  if (val === "admin") return true;
  // simple email regex
  // eslint-disable-next-line
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);
}

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);
  const [touched, setTouched] = useState(false);

  const navigate = useNavigate();

  function onUsernameChange(e) {
    setUsername(e.target.value);
    if (!touched) setTouched(true);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErr(null);
    setLoading(true);

    if (!isValidUsernameOrEmail(username)) {
      setErr("Please enter a valid email address or use 'admin'.");
      setLoading(false);
      return;
    }

    try {
      await login(username, password);
      // Optionally fetch user profile to test token
      await getCurrentUser();
      navigate("/");
    } catch (e) {
      setErr("Invalid username/email or password");
    }
    setLoading(false);
  }

  const showFormatHelper =
    touched && username && !isValidUsernameOrEmail(username);

  return (
    <div className="main-content" style={{ maxWidth: 420, margin: "70px auto" }}>
      <form className="card" style={{ width: "100%" }} onSubmit={handleSubmit} autoComplete="on">
        <h2 style={{ marginBottom: 10 }}>Login</h2>
        <label className="form-label" htmlFor="username">
          Username or Email
        </label>
        <input
          required
          id="username"
          name="username"
          autoComplete="username"
          type="text"
          value={username}
          onChange={onUsernameChange}
          placeholder="user@company.com or admin"
          aria-describedby="user-login-helper"
        />
        <div id="user-login-helper" style={{ color: "#888", fontSize: 13, marginTop: -10, marginBottom: 12 }}>
          Use your email address <b>or</b> enter <b>admin</b> to sign in as admin.
        </div>
        {showFormatHelper && (
          <div className="form-error" style={{ marginTop: -12 }}>
            Enter a valid email or <b>admin</b> to login.
          </div>
        )}
        <label className="form-label" htmlFor="password">
          Password
        </label>
        <input
          required
          type="password"
          id="password"
          autoComplete="current-password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          placeholder="Password"
        />
        {err && <div className="form-error">{err}</div>}
        <button className="btn btn-accent" type="submit" disabled={loading || !isValidUsernameOrEmail(username)}>
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}
