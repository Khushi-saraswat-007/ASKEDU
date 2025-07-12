import { useState } from "react";
import { useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { AssignmentList } from "./AssignmentList";
import { CreateAssignment } from "./CreateAssignment";
import { QuestionView } from "./QuestionView";
import { StatsPanel } from "./StatsPanel";
import { Id } from "../../convex/_generated/dataModel";

export function HomeworkDashboard() {
  const [activeTab, setActiveTab] = useState<"assignments" | "create" | "stats">("assignments");
  const [selectedAssignment, setSelectedAssignment] = useState<Id<"assignments"> | null>(null);
  const [statusFilter, setStatusFilter] = useState<"all" | "pending" | "in_progress" | "completed">("all");

  const assignments = useQuery(api.assignments.list, {
    status: statusFilter === "all" ? undefined : statusFilter,
  });
  const upcomingAssignments = useQuery(api.assignments.getUpcoming);
  const stats = useQuery(api.progress.getStats);

  if (selectedAssignment) {
    return (
      <QuestionView
        assignmentId={selectedAssignment}
        onBack={() => setSelectedAssignment(null)}
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* Quick Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white p-4 rounded-lg shadow-sm border">
            <div className="text-2xl font-bold text-blue-600">{stats.completedAssignments}</div>
            <div className="text-sm text-gray-600">Completed</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border">
            <div className="text-2xl font-bold text-orange-600">{stats.totalAssignments - stats.completedAssignments}</div>
            <div className="text-sm text-gray-600">Pending</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border">
            <div className="text-2xl font-bold text-green-600">{Math.round(stats.totalTimeSpent / 60)}h</div>
            <div className="text-sm text-gray-600">Study Time</div>
          </div>
          <div className="bg-white p-4 rounded-lg shadow-sm border">
            <div className="text-2xl font-bold text-purple-600">{stats.answeredQuestions}</div>
            <div className="text-sm text-gray-600">Questions Solved</div>
          </div>
        </div>
      )}

      {/* Upcoming Assignments Alert */}
      {upcomingAssignments && upcomingAssignments.length > 0 && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <h3 className="font-semibold text-yellow-800 mb-2">⏰ Upcoming Deadlines</h3>
          <div className="space-y-1">
            {upcomingAssignments.slice(0, 3).map((assignment) => (
              <div key={assignment._id} className="text-sm text-yellow-700">
                <span className="font-medium">{assignment.title}</span> - 
                <span className="ml-1">
                  {new Date(assignment.dueDate).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Navigation Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: "assignments", label: "Assignments", icon: "📝" },
            { id: "create", label: "Add New", icon: "➕" },
            { id: "stats", label: "Progress", icon: "📊" },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeTab === tab.id
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      {activeTab === "assignments" && (
        <div>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Your Assignments</h2>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as any)}
              className="px-3 py-2 border border-gray-300 rounded-md text-sm"
            >
              <option value="all">All Assignments</option>
              <option value="pending">Pending</option>
              <option value="in_progress">In Progress</option>
              <option value="completed">Completed</option>
            </select>
          </div>
          <AssignmentList
            assignments={assignments || []}
            onSelectAssignment={setSelectedAssignment}
          />
        </div>
      )}

      {activeTab === "create" && <CreateAssignment />}

      {activeTab === "stats" && <StatsPanel stats={stats} />}
    </div>
  );
}
