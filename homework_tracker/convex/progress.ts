import { v } from "convex/values";
import { query, mutation } from "./_generated/server";

// Mock user ID for demo purposes
const DEMO_USER_ID = "demo-user" as any;

export const trackTime = mutation({
  args: {
    assignmentId: v.id("assignments"),
    questionId: v.optional(v.id("questions")),
    timeSpent: v.number(),
    hintsUsed: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    await ctx.db.insert("progress", {
      userId,
      assignmentId: args.assignmentId,
      questionId: args.questionId,
      timeSpent: args.timeSpent,
      hintsUsed: args.hintsUsed || 0,
      completed: false,
    });
  },
});

export const getStats = query({
  args: {},
  handler: async (ctx) => {
    const userId = DEMO_USER_ID;

    const progress = await ctx.db
      .query("progress")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .collect();

    const assignments = await ctx.db
      .query("assignments")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .collect();

    const questions = await ctx.db
      .query("questions")
      .withIndex("by_user", (q) => q.eq("userId", userId))
      .collect();

    const totalTimeSpent = progress.reduce((sum, p) => sum + p.timeSpent, 0);
    const totalHintsUsed = progress.reduce((sum, p) => sum + p.hintsUsed, 0);
    const completedAssignments = assignments.filter(a => a.status === "completed").length;
    const answeredQuestions = questions.filter(q => q.isAnswered).length;

    return {
      totalTimeSpent,
      totalHintsUsed,
      completedAssignments,
      totalAssignments: assignments.length,
      answeredQuestions,
      totalQuestions: questions.length,
      averageTimePerQuestion: answeredQuestions > 0 ? totalTimeSpent / answeredQuestions : 0,
    };
  },
});
