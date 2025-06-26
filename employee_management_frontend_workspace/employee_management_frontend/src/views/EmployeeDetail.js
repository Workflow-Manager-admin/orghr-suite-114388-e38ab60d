import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchEmployee } from "../api";

export default function EmployeeDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [emp, setEmp] = useState(null);
  const [err, setErr] = useState(null);

  useEffect(() => {
    fetchEmployee(id)
      .then(setEmp)
      .catch(() => setErr("Not found"));
  }, [id]);

  if (err) return <div className="form-error">{err}</div>;
  if (!emp) return <div>Loading...</div>;

  return (
    <div style={{ maxWidth: 460, margin: "0 auto" }}>
      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between" }}>
          <div>
            <h2>
              {emp.first_name} {emp.last_name}
            </h2>
            <div>
              <strong>Email:</strong> {emp.email}
            </div>
            <div>
              <strong>Department:</strong> {emp.department?.name}
            </div>
            <div>
              <strong>Role:</strong> {emp.role?.name}
            </div>
            <div>
              <strong>Status:</strong> {emp.is_active ? "Active" : "Inactive"}
            </div>
          </div>
        </div>
        <div style={{ marginTop: 24 }}>
          <button className="btn btn-accent" onClick={() => navigate(`/employees/${emp.id}/edit`)}>Edit</button>
          <button className="btn" onClick={() => navigate("/")}>Back</button>
        </div>
      </div>
    </div>
  );
}
