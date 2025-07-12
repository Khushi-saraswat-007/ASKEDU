interface StatsData {
  totalTimeSpent: number;
  totalHintsUsed: number;
  completedAssignments: number;
  totalAssignments: number;
  answeredQuestions: number;
  totalQuestions: number;
  averageTimePerQuestion: number;
}

interface StatsPanelProps {
  stats: StatsData | undefined;
}

export function StatsPanel({ stats }: StatsPanelProps) {
  if (!stats) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const completionRate = stats.totalAssignments > 0 
    ? (stats.completedAssignments / stats.totalAssignments) * 100 
    : 0;

  const questionCompletionRate = stats.totalQuestions > 0
    ? (stats.answeredQuestions / stats.totalQuestions) * 100
    : 0;

  return (
    <div className="space-y-6">
      <h2 className="text-xl font-semibold">Your Progress</h2>
      
      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="text-3xl font-bold text-blue-600 mb-2">
            {Math.round(stats.totalTimeSpent / 60)}
          </div>
          <div className="text-sm text-gray-600">Hours Studied</div>
          <div className="text-xs text-gray-500 mt-1">
            {stats.totalTimeSpent} minutes total
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="text-3xl font-bold text-green-600 mb-2">
            {stats.completedAssignments}
          </div>
          <div className="text-sm text-gray-600">Assignments Done</div>
          <div className="text-xs text-gray-500 mt-1">
            out of {stats.totalAssignments} total
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="text-3xl font-bold text-purple-600 mb-2">
            {stats.answeredQuestions}
          </div>
          <div className="text-sm text-gray-600">Questions Solved</div>
          <div className="text-xs text-gray-500 mt-1">
            out of {stats.totalQuestions} total
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="text-3xl font-bold text-orange-600 mb-2">
            {stats.totalHintsUsed}
          </div>
          <div className="text-sm text-gray-600">Hints Used</div>
          <div className="text-xs text-gray-500 mt-1">
            {Math.round(stats.averageTimePerQuestion)} min/question avg
          </div>
        </div>
      </div>

      {/* Progress Bars */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="font-semibold text-gray-900 mb-4">Assignment Completion</h3>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span>Completed</span>
              <span>{Math.round(completionRate)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-green-600 h-3 rounded-full transition-all"
                style={{ width: `${completionRate}%` }}
              ></div>
            </div>
            <div className="text-xs text-gray-500">
              {stats.completedAssignments} of {stats.totalAssignments} assignments completed
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="font-semibold text-gray-900 mb-4">Question Progress</h3>
          <div className="space-y-3">
            <div className="flex justify-between text-sm">
              <span>Answered</span>
              <span>{Math.round(questionCompletionRate)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-blue-600 h-3 rounded-full transition-all"
                style={{ width: `${questionCompletionRate}%` }}
              ></div>
            </div>
            <div className="text-xs text-gray-500">
              {stats.answeredQuestions} of {stats.totalQuestions} questions answered
            </div>
          </div>
        </div>
      </div>

      {/* Study Insights */}
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="font-semibold text-gray-900 mb-4">Study Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-lg">
            <div className="text-2xl mb-2">📚</div>
            <div className="text-sm font-medium text-blue-900">Study Streak</div>
            <div className="text-xs text-blue-700">Keep it up!</div>
          </div>
          
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl mb-2">🎯</div>
            <div className="text-sm font-medium text-green-900">Efficiency</div>
            <div className="text-xs text-green-700">
              {stats.totalHintsUsed > 0 ? "Using hints wisely" : "Independent learner"}
            </div>
          </div>
          
          <div className="text-center p-4 bg-purple-50 rounded-lg">
            <div className="text-2xl mb-2">⚡</div>
            <div className="text-sm font-medium text-purple-900">Pace</div>
            <div className="text-xs text-purple-700">
              {stats.averageTimePerQuestion < 10 ? "Quick solver" : "Thorough thinker"}
            </div>
          </div>
        </div>
      </div>

      {stats.totalAssignments === 0 && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">📊</div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No data yet</h3>
          <p className="text-gray-500">Create some assignments to see your progress!</p>
        </div>
      )}
    </div>
  );
}
