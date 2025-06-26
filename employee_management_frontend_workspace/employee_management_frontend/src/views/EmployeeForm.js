import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchRoles, fetchDepartments, createEmployee, updateEmployee, fetchEmployee } from "../api";

export default function EmployeeForm({ editMode = false }) {
  const params = useParams();
  const navigate = useNavigate();
  const [roles, setRoles] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    email: "",
    is_active: true,
    role_id: "",
    department_id: "",
    password: ""
  });
  const [err, setErr] = useState(null);
  const [loading, setLoading] = useState(false);

  // Get dropdown options
  useEffect(() => {
    fetchRoles().then(setRoles);
    fetchDepartments().then(setDepartments);
  }, []);

  // If edit, load the record
  useEffect(() => {
    if (params.id && editMode) {
      fetchEmployee(params.id)
        .then(emp =>
          setForm({
            ...form,
            ...emp,
            password: ""
          })
        )
        .catch(() => setErr("Not found"));
    }
    // eslint-disable-next-line
  }, [params.id]);

  function handleChange(e) {
    const { name, value, type, checked } = e.target;
    setForm(f => ({
      ...f,
      [name]: type === "checkbox" ? checked : value
    }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErr(null);
    setLoading(true);
    try {
      if (editMode) {
        await updateEmployee(params.id, form);
      } else {
        await createEmployee(form);
      }
      navigate("/");
    } catch (e) {
      setErr("Error saving employee");
    }
    setLoading(false);
  }

  return (
    <div style={{ maxWidth: 520, margin: "0 auto" }}>
      <form className="card" onSubmit={handleSubmit}>
        <h2 style={{ marginBottom: 10 }}>{editMode ? "Edit Employee" : "New Employee"}</h2>
        <label className="form-label">First Name</label>
        <input required name="first_name" value={form.first_name} onChange={handleChange} />
        <label className="form-label">Last Name</label>
        <input required name="last_name" value={form.last_name} onChange={handleChange} />
        <label className="form-label">Email</label>
        <input required type="email" name="email" value={form.email} onChange={handleChange} />
        {!editMode && (
          <>
            <label className="form-label">Password</label>
            <input required type="password" name="password" value={form.password} onChange={handleChange} />
          </>
        )}
        <label className="form-label">Role</label>
        <select required name="role_id" value={form.role_id} onChange={handleChange}>
          <option value="">Select role</option>
          {roles.map(r => (
            <option key={r.id} value={r.id}>{r.name}</option>
          ))}
        </select>
        <label className="form-label">Department</label>
        <select required name="department_id" value={form.department_id} onChange={handleChange}>
          <option value="">Select department</option>
          {departments.map(d => (
            <option key={d.id} value={d.id}>{d.name}</option>
          ))}
        </select>
        <label className="form-label">
          <input type="checkbox" style={{ marginRight: 6 }} name="is_active" checked={!!form.is_active} onChange={handleChange} /> Active
        </label>
        {err && <div className="form-error">{err}</div>}
        <button className="btn btn-accent" type="submit" disabled={loading}>
          {loading ? "Saving..." : editMode ? "Save Changes" : "Create Employee"}
        </button>
        <button className="btn" type="button" onClick={() => navigate("/")}>
          Cancel
        </button>
      </form>
    </div>
  );
}
