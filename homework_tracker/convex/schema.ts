import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

const applicationTables = {
  assignments: defineTable({
    userId: v.string(), // Changed from v.id("users") to v.string() for demo
    title: v.string(),
    subject: v.string(),
    description: v.optional(v.string()),
    dueDate: v.number(),
    difficulty: v.union(v.literal("easy"), v.literal("medium"), v.literal("hard")),
    status: v.union(v.literal("pending"), v.literal("in_progress"), v.literal("completed")),
    priority: v.union(v.literal("low"), v.literal("medium"), v.literal("high")),
  })
    .index("by_user", ["userId"])
    .index("by_user_and_status", ["userId", "status"])
    .index("by_user_and_due_date", ["userId", "dueDate"]),

  questions: defineTable({
    userId: v.string(), // Changed from v.id("users") to v.string() for demo
    assignmentId: v.id("assignments"),
    questionText: v.string(),
    questionType: v.optional(v.string()),
    difficulty: v.union(v.literal("easy"), v.literal("medium"), v.literal("hard")),
    hints: v.optional(v.array(v.string())),
    explanation: v.optional(v.string()),
    answer: v.optional(v.string()),
    isAnswered: v.boolean(),
  })
    .index("by_assignment", ["assignmentId"])
    .index("by_user", ["userId"])
    .index("by_user_and_answered", ["userId", "isAnswered"]),

  progress: defineTable({
    userId: v.string(), // Changed from v.id("users") to v.string() for demo
    assignmentId: v.id("assignments"),
    questionId: v.optional(v.id("questions")),
    timeSpent: v.number(), // in minutes
    hintsUsed: v.number(),
    completed: v.boolean(),
  })
    .index("by_user", ["userId"])
    .index("by_assignment", ["assignmentId"])
    .index("by_question", ["questionId"]),

  reminders: defineTable({
    userId: v.string(), // Changed from v.id("users") to v.string() for demo
    assignmentId: v.id("assignments"),
    reminderTime: v.number(),
    message: v.string(),
    sent: v.boolean(),
  })
    .index("by_user", ["userId"])
    .index("by_reminder_time", ["reminderTime"])
    .index("by_assignment", ["assignmentId"]),
};

export default defineSchema({
  ...applicationTables,
});
