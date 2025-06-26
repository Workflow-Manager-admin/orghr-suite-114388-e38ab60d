import React from "react";
import Sidebar from "../components/Sidebar";
import { Outlet } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="dashboard-layout">
      <Sidebar />
      <main className="main-content">
        <Outlet />
      </main>
    </div>
  );
}
