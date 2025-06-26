//
// Simple API wrapper for backend integration with JWT handling
//
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:3001";

let authToken = null;

export function setAuthToken(token) {
  authToken = token;
  if (token) window.localStorage.setItem("authToken", token);
  else window.localStorage.removeItem("authToken");
}

export function getAuthToken() {
  if (authToken) return authToken;
  return window.localStorage.getItem("authToken");
}

function apiHeaders(isJson = true) {
  const headers = {
    ...(isJson ? { "Content-Type": "application/json" } : {})
  };
  const token = getAuthToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  return headers;
}

// PUBLIC_INTERFACE
export async function login(email, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: apiHeaders(false),
    body: new URLSearchParams({ username: email, password })
  });
  if (!res.ok) throw new Error("Login failed");
  const data = await res.json();
  setAuthToken(data.access_token);
  return data;
}

// PUBLIC_INTERFACE
export async function getCurrentUser() {
  const res = await fetch(`${API_BASE}/auth/me`, { headers: apiHeaders() });
  if (!res.ok) throw new Error("Unauthorized");
  return await res.json();
}

//
// EMPLOYEE CRUD
//
export async function fetchEmployees() {
  const res = await fetch(`${API_BASE}/employees`, { headers: apiHeaders() });
  if (!res.ok) throw new Error("Failed to fetch employees");
  return await res.json();
}

export async function fetchEmployee(id) {
  const res = await fetch(`${API_BASE}/employees/${id}`, { headers: apiHeaders() });
  if (!res.ok) throw new Error("Not found");
  return await res.json();
}

export async function createEmployee(input) {
  const res = await fetch(`${API_BASE}/employees`, {
    method: "POST",
    headers: apiHeaders(),
    body: JSON.stringify(input)
  });
  if (!res.ok) throw new Error("Failed to create");
  return await res.json();
}

export async function updateEmployee(id, input) {
  const res = await fetch(`${API_BASE}/employees/${id}`, {
    method: "PUT",
    headers: apiHeaders(),
    body: JSON.stringify(input)
  });
  if (!res.ok) throw new Error("Failed to update");
  return await res.json();
}

export async function deleteEmployee(id) {
  const res = await fetch(`${API_BASE}/employees/${id}`, {
    method: "DELETE",
    headers: apiHeaders()
  });
  if (res.status !== 204) throw new Error("Failed to delete");
}

//
// DEPARTMENT
//
export async function fetchDepartments() {
  const res = await fetch(`${API_BASE}/departments`, { headers: apiHeaders() });
  if (!res.ok) throw new Error("Fail fetch departments");
  return await res.json();
}

export async function createDepartment(input) {
  const res = await fetch(`${API_BASE}/departments`, {
    method: "POST",
    headers: apiHeaders(),
    body: JSON.stringify(input)
  });
  if (!res.ok) throw new Error("Fail create department");
  return await res.json();
}

//
// ROLES
//
export async function fetchRoles() {
  const res = await fetch(`${API_BASE}/roles`, { headers: apiHeaders() });
  if (!res.ok) throw new Error("Fail fetch roles");
  return await res.json();
}

export async function createRole(input) {
  const res = await fetch(`${API_BASE}/roles`, {
    method: "POST",
    headers: apiHeaders(),
    body: JSON.stringify(input)
  });
  if (!res.ok) throw new Error("Fail create role");
  return await res.json();
}
