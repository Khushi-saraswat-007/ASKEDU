import { v } from "convex/values";
import { query, mutation } from "./_generated/server";

// Mock user ID for demo purposes
const DEMO_USER_ID = "demo-user" as any;

export const list = query({
  args: {
    status: v.optional(v.union(v.literal("pending"), v.literal("in_progress"), v.literal("completed"))),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    let query = ctx.db.query("assignments").withIndex("by_user", (q) => q.eq("userId", userId));
    
    if (args.status) {
      query = ctx.db.query("assignments").withIndex("by_user_and_status", (q) => 
        q.eq("userId", userId).eq("status", args.status!)
      );
    }

    const assignments = await query.order("asc").collect();
    
    // Add question counts and progress for each assignment
    const assignmentsWithProgress = await Promise.all(
      assignments.map(async (assignment) => {
        const questions = await ctx.db
          .query("questions")
          .withIndex("by_assignment", (q) => q.eq("assignmentId", assignment._id))
          .collect();
        
        const answeredQuestions = questions.filter(q => q.isAnswered);
        const totalProgress = await ctx.db
          .query("progress")
          .withIndex("by_assignment", (q) => q.eq("assignmentId", assignment._id))
          .collect();
        
        const totalTimeSpent = totalProgress.reduce((sum, p) => sum + p.timeSpent, 0);
        
        return {
          ...assignment,
          questionCount: questions.length,
          answeredCount: answeredQuestions.length,
          timeSpent: totalTimeSpent,
          isOverdue: assignment.dueDate < Date.now() && assignment.status !== "completed",
        };
      })
    );

    return assignmentsWithProgress.sort((a, b) => a.dueDate - b.dueDate);
  },
});

export const create = mutation({
  args: {
    title: v.string(),
    subject: v.string(),
    description: v.optional(v.string()),
    dueDate: v.number(),
    difficulty: v.union(v.literal("easy"), v.literal("medium"), v.literal("hard")),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    // Determine priority based on due date and difficulty
    const daysUntilDue = (args.dueDate - Date.now()) / (1000 * 60 * 60 * 24);
    let priority: "low" | "medium" | "high" = "medium";
    
    if (daysUntilDue <= 1 || args.difficulty === "hard") {
      priority = "high";
    } else if (daysUntilDue <= 3 || args.difficulty === "medium") {
      priority = "medium";
    } else {
      priority = "low";
    }

    const assignmentId = await ctx.db.insert("assignments", {
      userId,
      title: args.title,
      subject: args.subject,
      description: args.description,
      dueDate: args.dueDate,
      difficulty: args.difficulty,
      status: "pending",
      priority,
    });

    // Create reminder 24 hours before due date
    const reminderTime = args.dueDate - (24 * 60 * 60 * 1000);
    if (reminderTime > Date.now()) {
      await ctx.db.insert("reminders", {
        userId,
        assignmentId,
        reminderTime,
        message: `Reminder: "${args.title}" is due tomorrow!`,
        sent: false,
      });
    }

    return assignmentId;
  },
});

export const updateStatus = mutation({
  args: {
    assignmentId: v.id("assignments"),
    status: v.union(v.literal("pending"), v.literal("in_progress"), v.literal("completed")),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    const assignment = await ctx.db.get(args.assignmentId);
    if (!assignment || assignment.userId !== userId) {
      throw new Error("Assignment not found or unauthorized");
    }

    await ctx.db.patch(args.assignmentId, {
      status: args.status,
    });
  },
});

export const getUpcoming = query({
  args: {},
  handler: async (ctx) => {
    const userId = DEMO_USER_ID;

    const now = Date.now();
    const nextWeek = now + (7 * 24 * 60 * 60 * 1000);

    const assignments = await ctx.db
      .query("assignments")
      .withIndex("by_user_and_due_date", (q) => 
        q.eq("userId", userId).gte("dueDate", now).lt("dueDate", nextWeek)
      )
      .filter((q) => q.neq(q.field("status"), "completed"))
      .collect();

    return assignments.sort((a, b) => a.dueDate - b.dueDate);
  },
});
