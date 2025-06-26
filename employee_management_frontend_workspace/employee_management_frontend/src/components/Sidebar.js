import React from "react";
import { NavLink, useLocation } from "react-router-dom";
import { COLORS } from "../theme";

const NAV_ITEMS = [
  { path: "/", text: "Employees", exact: true },
  { path: "/roles-departments", text: "Roles & Departments" }
];

export default function Sidebar() {
  const { pathname } = useLocation();
  return (
    <aside className="sidebar">
      {NAV_ITEMS.map(item => (
        <NavLink
          key={item.path}
          to={item.path}
          className={({ isActive }) =>
            "nav-link" + ((isActive || (item.exact && pathname === "/")) ? " active" : "")
          }
          end={item.exact || undefined}
          style={({ isActive }) =>
            isActive ? { color: COLORS.primary, borderLeft: `4px solid ${COLORS.primary}` } : {}
          }
        >
          {item.text}
        </NavLink>
      ))}
    </aside>
  );
}
