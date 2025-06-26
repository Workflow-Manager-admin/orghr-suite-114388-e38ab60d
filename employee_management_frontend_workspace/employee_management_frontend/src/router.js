import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./views/Dashboard";
import EmployeeList from "./views/EmployeeList";
import EmployeeDetail from "./views/EmployeeDetail";
import EmployeeForm from "./views/EmployeeForm";
import RoleDepartmentMgmt from "./views/RoleDepartmentMgmt";
import Login from "./views/Login";

function ProtectedRoute({ children }) {
  const token = window.localStorage.getItem("authToken");
  return token ? children : <Navigate to="/login" replace />;
}

// PUBLIC_INTERFACE
export default function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>}>
        <Route index element={<EmployeeList />} />
        <Route path="employees/new" element={<EmployeeForm />} />
        <Route path="employees/:id/edit" element={<EmployeeForm editMode />} />
        <Route path="employees/:id" element={<EmployeeDetail />} />
        <Route path="roles-departments" element={<RoleDepartmentMgmt />} />
      </Route>
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
}
