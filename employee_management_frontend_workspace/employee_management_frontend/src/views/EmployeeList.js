import React, { useState, useEffect } from "react";
import { fetchEmployees, deleteEmployee } from "../api";
import { useNavigate } from "react-router-dom";

export default function EmployeeList() {
  const [list, setList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [delId, setDelId] = useState(null);
  const [err, setErr] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchEmployees()
      .then(setList)
      .catch(() => setErr("Failed to fetch"))
      .finally(() => setLoading(false));
  }, []);

  async function handleDelete(id) {
    if (!window.confirm("Are you sure to delete employee?")) return;
    setDelId(id);
    try {
      await deleteEmployee(id);
      setList(list.filter(emp => emp.id !== id));
    } catch (e) {
      alert("Failed to delete");
    }
    setDelId(null);
  }

  if (loading) return <div>Loading employees...</div>;
  if (err) return <div className="form-error">{err}</div>;

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 22 }}>
        <h2>Employees</h2>
        <button className="btn btn-accent" onClick={() => navigate("/employees/new")}>
          + Add Employee
        </button>
      </div>
      <div style={{ overflowX: "auto" }}>
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Department</th>
              <th>Role</th>
              <th>Status</th>
              <th style={{ textAlign: "center" }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {list.length === 0 && (
              <tr>
                <td colSpan={6} style={{ textAlign: "center" }}>No employees found</td>
              </tr>
            )}
            {list.map(emp => (
              <tr key={emp.id}>
                <td>{emp.first_name} {emp.last_name}</td>
                <td>{emp.email}</td>
                <td>{emp.department?.name}</td>
                <td>{emp.role?.name}</td>
                <td>{emp.is_active ? "Active" : "Inactive"}</td>
                <td style={{ textAlign: "center" }}>
                  <button className="btn" onClick={() => navigate(`/employees/${emp.id}`)}>View</button>
                  <button className="btn" onClick={() => navigate(`/employees/${emp.id}/edit`)}>Edit</button>
                  <button className="btn btn-danger" disabled={delId === emp.id} onClick={() => handleDelete(emp.id)}>
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
