import { useState, useEffect } from "react";
import { useQuery, useMutation, useAction } from "convex/react";
import { api } from "../../convex/_generated/api";
import { Id } from "../../convex/_generated/dataModel";
import { toast } from "sonner";

interface QuestionViewProps {
  assignmentId: Id<"assignments">;
  onBack: () => void;
}

export function QuestionView({ assignmentId, onBack }: QuestionViewProps) {
  const [newQuestionText, setNewQuestionText] = useState("");
  const [selectedDifficulty, setSelectedDifficulty] = useState<"easy" | "medium" | "hard">("medium");
  const [expandedQuestion, setExpandedQuestion] = useState<Id<"questions"> | null>(null);
  const [startTime, setStartTime] = useState<number>(Date.now());

  const assignment = useQuery(api.assignments.list, {})?.find(a => a._id === assignmentId);
  const questions = useQuery(api.questions.listByAssignment, { assignmentId });
  
  const createQuestion = useMutation(api.questions.create);
  const analyzeQuestion = useAction(api.questions.analyzeQuestion);
  const markAnswered = useMutation(api.questions.markAnswered);
  const trackTime = useMutation(api.progress.trackTime);

  useEffect(() => {
    setStartTime(Date.now());
  }, [assignmentId]);

  const handleCreateQuestion = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newQuestionText.trim()) {
      toast.error("Please enter a question");
      return;
    }

    try {
      const questionId = await createQuestion({
        assignmentId,
        questionText: newQuestionText.trim(),
        difficulty: selectedDifficulty,
      });

      toast.success("Question added! Analyzing...");
      setNewQuestionText("");
      
      // Analyze the question with AI
      try {
        await analyzeQuestion({ questionId });
        toast.success("Question analyzed successfully!");
      } catch (error) {
        toast.error("Question added but analysis failed");
      }
    } catch (error) {
      toast.error("Failed to create question");
      console.error(error);
    }
  };

  const handleMarkAnswered = async (questionId: Id<"questions">) => {
    try {
      await markAnswered({ questionId });
      
      // Track time spent
      const timeSpent = Math.round((Date.now() - startTime) / 60000); // in minutes
      await trackTime({
        assignmentId,
        questionId,
        timeSpent,
      });
      
      toast.success("Question marked as answered!");
      setStartTime(Date.now()); // Reset timer
    } catch (error) {
      toast.error("Failed to mark question as answered");
      console.error(error);
    }
  };

  if (!assignment) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <button
          onClick={onBack}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-700 mb-4"
        >
          ← Back to Assignments
        </button>
        
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-2">{assignment.title}</h1>
          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span>📖 {assignment.subject}</span>
            <span>📅 Due: {new Date(assignment.dueDate).toLocaleDateString()}</span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              assignment.difficulty === "easy" ? "bg-green-100 text-green-800" :
              assignment.difficulty === "medium" ? "bg-yellow-100 text-yellow-800" :
              "bg-red-100 text-red-800"
            }`}>
              {assignment.difficulty}
            </span>
          </div>
          {assignment.description && (
            <p className="text-gray-700 mt-3">{assignment.description}</p>
          )}
        </div>
      </div>

      {/* Add New Question */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Add a Question</h2>
        <form onSubmit={handleCreateQuestion} className="space-y-4">
          <div>
            <textarea
              value={newQuestionText}
              onChange={(e) => setNewQuestionText(e.target.value)}
              placeholder="Paste your homework question here..."
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex items-center gap-4">
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value as "easy" | "medium" | "hard")}
              className="px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="easy">🟢 Easy</option>
              <option value="medium">🟡 Medium</option>
              <option value="hard">🔴 Hard</option>
            </select>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Add Question
            </button>
          </div>
        </form>
      </div>

      {/* Questions List */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold">Questions ({questions?.length || 0})</h2>
        
        {questions?.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow-sm border">
            <div className="text-6xl mb-4">❓</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No questions yet</h3>
            <p className="text-gray-500">Add your first question to get started!</p>
          </div>
        ) : (
          questions?.map((question) => (
            <div
              key={question._id}
              className={`bg-white rounded-lg shadow-sm border p-6 ${
                question.isAnswered ? "bg-green-50 border-green-200" : ""
              }`}
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      question.difficulty === "easy" ? "bg-green-100 text-green-800" :
                      question.difficulty === "medium" ? "bg-yellow-100 text-yellow-800" :
                      "bg-red-100 text-red-800"
                    }`}>
                      {question.difficulty}
                    </span>
                    {question.questionType && (
                      <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                        {question.questionType}
                      </span>
                    )}
                    {question.isAnswered && (
                      <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                        ✓ Answered
                      </span>
                    )}
                  </div>
                  <p className="text-gray-900 mb-3">{question.questionText}</p>
                </div>
                
                <div className="flex gap-2 ml-4">
                  <button
                    onClick={() => setExpandedQuestion(
                      expandedQuestion === question._id ? null : question._id
                    )}
                    className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200 transition-colors"
                  >
                    {expandedQuestion === question._id ? "Hide Help" : "Get Help"}
                  </button>
                  {!question.isAnswered && (
                    <button
                      onClick={() => handleMarkAnswered(question._id)}
                      className="px-3 py-1 text-sm bg-green-100 text-green-700 rounded hover:bg-green-200 transition-colors"
                    >
                      Mark Done
                    </button>
                  )}
                </div>
              </div>

              {expandedQuestion === question._id && (
                <div className="border-t pt-4 space-y-4">
                  {question.explanation && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">💡 Concept Explanation</h4>
                      <p className="text-gray-700 bg-blue-50 p-3 rounded">{question.explanation}</p>
                    </div>
                  )}
                  
                  {question.hints && question.hints.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">🔍 Hints</h4>
                      <div className="space-y-2">
                        {question.hints.map((hint, index) => (
                          <div key={index} className="bg-yellow-50 p-3 rounded border-l-4 border-yellow-400">
                            <span className="font-medium text-yellow-800">Hint {index + 1}:</span>
                            <span className="text-yellow-700 ml-2">{hint}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {question.answer && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">✅ Your Answer</h4>
                      <p className="text-gray-700 bg-green-50 p-3 rounded">{question.answer}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
