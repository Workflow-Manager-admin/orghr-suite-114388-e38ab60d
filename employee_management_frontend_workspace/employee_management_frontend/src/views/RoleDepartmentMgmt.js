import React, { useEffect, useState } from "react";
import { fetchDepartments, fetchRoles, createDepartment, createRole } from "../api";

export default function RoleDepartmentMgmt() {
  const [roles, setRoles] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [roleName, setRoleName] = useState("");
  const [roleId, setRoleId] = useState("");
  const [deptName, setDeptName] = useState("");
  const [deptId, setDeptId] = useState("");
  const [roleDesc, setRoleDesc] = useState("");
  const [deptDesc, setDeptDesc] = useState("");
  const [err, setErr] = useState(null);
  const [ok, setOk] = useState("");

  useEffect(() => {
    fetchRoles().then(setRoles);
    fetchDepartments().then(setDepartments);
  }, []);

  async function handleAddRole(e) {
    e.preventDefault();
    setErr(null);
    setOk("");
    try {
      const newRole = await createRole({ id: Number(roleId), name: roleName, description: roleDesc });
      setRoles([...roles, newRole]);
      setRoleName("");
      setRoleId("");
      setRoleDesc("");
      setOk("Role added");
    } catch {
      setErr("Failed to add role");
    }
  }

  async function handleAddDepartment(e) {
    e.preventDefault();
    setErr(null);
    setOk("");
    try {
      const newDept = await createDepartment({ id: Number(deptId), name: deptName, description: deptDesc });
      setDepartments([...departments, newDept]);
      setDeptName("");
      setDeptId("");
      setDeptDesc("");
      setOk("Department added");
    } catch {
      setErr("Failed to add department");
    }
  }

  return (
    <div className="card">
      <h2>Roles</h2>
      <ul>
        {roles.map(r => (
          <li key={r.id}>
            {r.name} <span style={{ color: "#666" }}>{r.description}</span> (ID: {r.id})
          </li>
        ))}
      </ul>
      <form style={{ marginTop: 20 }} onSubmit={handleAddRole}>
        <input required value={roleId} type="number" placeholder="Role ID" onChange={e => setRoleId(e.target.value)} style={{ maxWidth: 110 }} />
        <input required value={roleName} placeholder="Role Name" onChange={e => setRoleName(e.target.value)} style={{ maxWidth: 160 }} />
        <input value={roleDesc} placeholder="Description" onChange={e => setRoleDesc(e.target.value)} />
        <button className="btn btn-accent" type="submit">Add Role</button>
      </form>
      <h2 style={{ marginTop: 32 }}>Departments</h2>
      <ul>
        {departments.map(d => (
          <li key={d.id}>
            {d.name} <span style={{ color: "#666" }}>{d.description}</span> (ID: {d.id})
          </li>
        ))}
      </ul>
      <form style={{ marginTop: 20 }} onSubmit={handleAddDepartment}>
        <input required value={deptId} type="number" placeholder="Dept ID" onChange={e => setDeptId(e.target.value)} style={{ maxWidth: 110 }} />
        <input required value={deptName} placeholder="Dept Name" onChange={e => setDeptName(e.target.value)} style={{ maxWidth: 160 }} />
        <input value={deptDesc} placeholder="Description" onChange={e => setDeptDesc(e.target.value)} />
        <button className="btn btn-accent" type="submit">Add Dept</button>
      </form>
      {err && <div className="form-error">{err}</div>}
      {ok && <div style={{ color: "#388e3c" }}>{ok}</div>}
    </div>
  );
}
