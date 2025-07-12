import { useMutation } from "convex/react";
import { api } from "../../convex/_generated/api";
import { Id } from "../../convex/_generated/dataModel";

interface Assignment {
  _id: Id<"assignments">;
  title: string;
  subject: string;
  description?: string;
  dueDate: number;
  difficulty: "easy" | "medium" | "hard";
  status: "pending" | "in_progress" | "completed";
  priority: "low" | "medium" | "high";
  questionCount: number;
  answeredCount: number;
  timeSpent: number;
  isOverdue: boolean;
}

interface AssignmentListProps {
  assignments: Assignment[];
  onSelectAssignment: (id: Id<"assignments">) => void;
}

export function AssignmentList({ assignments, onSelectAssignment }: AssignmentListProps) {
  const updateStatus = useMutation(api.assignments.updateStatus);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case "easy": return "bg-green-100 text-green-800";
      case "medium": return "bg-yellow-100 text-yellow-800";
      case "hard": return "bg-red-100 text-red-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "pending": return "bg-gray-100 text-gray-800";
      case "in_progress": return "bg-blue-100 text-blue-800";
      case "completed": return "bg-green-100 text-green-800";
      default: return "bg-gray-100 text-gray-800";
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case "high": return "🔴";
      case "medium": return "🟡";
      case "low": return "🟢";
      default: return "";
    }
  };

  if (assignments.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-6xl mb-4">📚</div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">No assignments yet</h3>
        <p className="text-gray-500">Create your first assignment to get started!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {assignments.map((assignment) => (
        <div
          key={assignment._id}
          className={`bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow ${
            assignment.isOverdue ? "border-red-200 bg-red-50" : ""
          }`}
        >
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-lg">{getPriorityIcon(assignment.priority)}</span>
                <h3 className="text-lg font-semibold text-gray-900">{assignment.title}</h3>
                {assignment.isOverdue && (
                  <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-800 rounded-full">
                    Overdue
                  </span>
                )}
              </div>
              
              <div className="flex items-center gap-4 mb-3">
                <span className="text-sm text-gray-600">📖 {assignment.subject}</span>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(assignment.difficulty)}`}>
                  {assignment.difficulty}
                </span>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(assignment.status)}`}>
                  {assignment.status.replace('_', ' ')}
                </span>
              </div>

              {assignment.description && (
                <p className="text-gray-600 text-sm mb-3">{assignment.description}</p>
              )}

              <div className="flex items-center gap-6 text-sm text-gray-500">
                <span>📅 Due: {new Date(assignment.dueDate).toLocaleDateString()}</span>
                <span>❓ Questions: {assignment.answeredCount}/{assignment.questionCount}</span>
                <span>⏱️ Time: {Math.round(assignment.timeSpent)}min</span>
              </div>

              {assignment.questionCount > 0 && (
                <div className="mt-3">
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full transition-all"
                      style={{
                        width: `${(assignment.answeredCount / assignment.questionCount) * 100}%`
                      }}
                    ></div>
                  </div>
                  <span className="text-xs text-gray-500 mt-1">
                    {Math.round((assignment.answeredCount / assignment.questionCount) * 100)}% complete
                  </span>
                </div>
              )}
            </div>

            <div className="flex flex-col gap-2 ml-4">
              <button
                onClick={() => onSelectAssignment(assignment._id)}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors text-sm font-medium"
              >
                Work on it
              </button>
              
              {assignment.status !== "completed" && (
                <select
                  value={assignment.status}
                  onChange={(e) => updateStatus({
                    assignmentId: assignment._id,
                    status: e.target.value as "pending" | "in_progress" | "completed"
                  })}
                  className="px-3 py-1 border border-gray-300 rounded text-sm"
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
