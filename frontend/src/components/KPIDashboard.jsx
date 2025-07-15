import React, { useState } from "react";
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import "./KPIDashboard.css";

const monthlyData = [
  { name: "Jan", revenue: 4000, expenses: 2400, profit: 1600 },
  { name: "Feb", revenue: 3000, expenses: 1398, profit: 1602 },
  { name: "Mar", revenue: 2000, expenses: 9800, profit: -7800 },
  { name: "Apr", revenue: 2780, expenses: 3908, profit: -1128 },
  { name: "May", revenue: 1890, expenses: 4800, profit: -2910 },
  { name: "Jun", revenue: 2390, expenses: 3800, profit: -1410 },
  { name: "Jul", revenue: 3490, expenses: 4300, profit: -810 },
  { name: "Aug", revenue: 4000, expenses: 2400, profit: 1600 },
  { name: "Sep", revenue: 5000, expenses: 3000, profit: 2000 },
  { name: "Oct", revenue: 6000, expenses: 3500, profit: 2500 },
  { name: "Nov", revenue: 7000, expenses: 4000, profit: 3000 },
  { name: "Dec", revenue: 9000, expenses: 5000, profit: 4000 },
];

const projectCompletionData = [
  { name: "Completed", value: 75 },
  { name: "In Progress", value: 15 },
  { name: "Not Started", value: 10 },
];

const COLORS = ["#66fcf1", "#45a29e", "#ff2e63"];

const teamPerformanceData = [
  { name: "Team A", performance: 90 },
  { name: "Team B", performance: 75 },
  { name: "Team C", performance: 86 },
  { name: "Team D", performance: 65 },
  { name: "Team E", performance: 78 },
];

export default function KPIDashboard() {
  const [activeView, setActiveView] = useState("financial");

  const renderFinancialMetrics = () => {
    return (
      <div className="chart-container">
        <h3>Financial Performance - 2025</h3>
        <div className="chart-description">
          Monthly revenue, expenses, and profit trends for the current year.
        </div>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={monthlyData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2833" />
            <XAxis dataKey="name" tick={{ fill: "#c5c6c7" }} />
            <YAxis tick={{ fill: "#c5c6c7" }} />
            <Tooltip
              contentStyle={{
                backgroundColor: "#0b0c10",
                border: "1px solid #45a29e",
                borderRadius: "4px",
                color: "#c5c6c7",
              }}
            />
            <Legend wrapperStyle={{ color: "#c5c6c7" }} />
            <Line
              type="monotone"
              dataKey="revenue"
              stroke="#66fcf1"
              strokeWidth={2}
              dot={{ fill: "#66fcf1", r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="expenses"
              stroke="#ff2e63"
              strokeWidth={2}
              dot={{ fill: "#ff2e63", r: 4 }}
            />
            <Line
              type="monotone"
              dataKey="profit"
              stroke="#45a29e"
              strokeWidth={2}
              dot={{ fill: "#45a29e", r: 4 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderProjectMetrics = () => {
    return (
      <div className="chart-container">
        <h3>Project Completion Status</h3>
        <div className="chart-description">
          Current distribution of project statuses across the organization.
        </div>
        <div className="chart-row">
          <div className="chart-half">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={projectCompletionData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  outerRadius={90}
                  innerRadius={60}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                >
                  {projectCompletionData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value) => `${value}%`}
                  contentStyle={{
                    backgroundColor: "#0b0c10",
                    border: "1px solid #45a29e",
                    borderRadius: "4px",
                    color: "#c5c6c7",
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="chart-half">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={teamPerformanceData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f2833" />
                <XAxis dataKey="name" tick={{ fill: "#c5c6c7" }} />
                <YAxis tick={{ fill: "#c5c6c7" }} domain={[0, 100]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#0b0c10",
                    border: "1px solid #45a29e",
                    borderRadius: "4px",
                    color: "#c5c6c7",
                  }}
                />
                <Bar dataKey="performance" fill="#45a29e">
                  {teamPerformanceData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={
                        entry.performance >= 80
                          ? "#66fcf1"
                          : entry.performance >= 70
                            ? "#45a29e"
                            : "#ff2e63"
                      }
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="kpi-container cyberpunk-theme">
      <h1>Key Performance Indicators</h1>
      <p className="kpi-description">
        Real-time metrics and analytics tracking our company's performance
        across different departments.
      </p>

      <div className="view-selector">
        <button
          className={`view-button ${activeView === "financial" ? "active" : ""}`}
          onClick={() => setActiveView("financial")}
        >
          Financial Metrics
        </button>
        <button
          className={`view-button ${activeView === "projects" ? "active" : ""}`}
          onClick={() => setActiveView("projects")}
        >
          Project Metrics
        </button>
      </div>

      <div className="dashboard-content">
        {activeView === "financial"
          ? renderFinancialMetrics()
          : renderProjectMetrics()}
      </div>
    </div>
  );
}
