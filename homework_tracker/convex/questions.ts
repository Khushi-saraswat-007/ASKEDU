import { v } from "convex/values";
import { query, mutation, action } from "./_generated/server";
import { api } from "./_generated/api";
import OpenAI from "openai";

// Mock user ID for demo purposes
const DEMO_USER_ID = "demo-user" as any;

const openai = new OpenAI({
  baseURL: process.env.CONVEX_OPENAI_BASE_URL,
  apiKey: process.env.CONVEX_OPENAI_API_KEY,
});

export const listByAssignment = query({
  args: {
    assignmentId: v.id("assignments"),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    const assignment = await ctx.db.get(args.assignmentId);
    if (!assignment || assignment.userId !== userId) {
      throw new Error("Assignment not found or unauthorized");
    }

    return await ctx.db
      .query("questions")
      .withIndex("by_assignment", (q) => q.eq("assignmentId", args.assignmentId))
      .collect();
  },
});

export const create = mutation({
  args: {
    assignmentId: v.id("assignments"),
    questionText: v.string(),
    difficulty: v.union(v.literal("easy"), v.literal("medium"), v.literal("hard")),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    const assignment = await ctx.db.get(args.assignmentId);
    if (!assignment || assignment.userId !== userId) {
      throw new Error("Assignment not found or unauthorized");
    }

    const questionId = await ctx.db.insert("questions", {
      userId,
      assignmentId: args.assignmentId,
      questionText: args.questionText,
      difficulty: args.difficulty,
      isAnswered: false,
    });

    // Update assignment status to in_progress if it was pending
    if (assignment.status === "pending") {
      await ctx.db.patch(args.assignmentId, {
        status: "in_progress",
      });
    }

    return questionId;
  },
});

export const analyzeQuestion = action({
  args: {
    questionId: v.id("questions"),
  },
  handler: async (ctx, args): Promise<any> => {
    const question: any = await ctx.runQuery(api.questions.getQuestion, {
      questionId: args.questionId,
    });

    if (!question) {
      throw new Error("Question not found");
    }

    try {
      const response: any = await openai.chat.completions.create({
        model: "gpt-4.1-nano",
        messages: [
          {
            role: "system",
            content: `You are a helpful homework assistant. Analyze the given question and provide:
1. Question type (e.g., "Math - Algebra", "Science - Physics", "English - Essay", etc.)
2. 3 helpful hints that guide the student without giving the direct answer
3. A brief explanation of the concept being tested

Format your response as JSON with keys: questionType, hints (array), explanation`
          },
          {
            role: "user",
            content: question.questionText
          }
        ],
      });

      const content: string | null = response.choices[0].message.content;
      if (!content) {
        throw new Error("No response from AI");
      }

      let analysis: any;
      try {
        analysis = JSON.parse(content);
      } catch {
        // If JSON parsing fails, create a structured response
        analysis = {
          questionType: "General",
          hints: ["Break down the problem into smaller parts", "Look for key terms and concepts", "Consider what you already know about this topic"],
          explanation: content
        };
      }

      await ctx.runMutation(api.questions.updateAnalysis, {
        questionId: args.questionId,
        questionType: analysis.questionType,
        hints: analysis.hints,
        explanation: analysis.explanation,
      });

      return analysis;
    } catch (error) {
      console.error("Error analyzing question:", error);
      throw new Error("Failed to analyze question");
    }
  },
});

export const getQuestion = query({
  args: {
    questionId: v.id("questions"),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    const question = await ctx.db.get(args.questionId);
    if (!question || question.userId !== userId) {
      throw new Error("Question not found or unauthorized");
    }

    return question;
  },
});

export const updateAnalysis = mutation({
  args: {
    questionId: v.id("questions"),
    questionType: v.string(),
    hints: v.array(v.string()),
    explanation: v.string(),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    const question = await ctx.db.get(args.questionId);
    if (!question || question.userId !== userId) {
      throw new Error("Question not found or unauthorized");
    }

    await ctx.db.patch(args.questionId, {
      questionType: args.questionType,
      hints: args.hints,
      explanation: args.explanation,
    });
  },
});

export const markAnswered = mutation({
  args: {
    questionId: v.id("questions"),
    answer: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const userId = DEMO_USER_ID;

    const question = await ctx.db.get(args.questionId);
    if (!question || question.userId !== userId) {
      throw new Error("Question not found or unauthorized");
    }

    await ctx.db.patch(args.questionId, {
      isAnswered: true,
      answer: args.answer,
    });

    // Check if all questions in the assignment are answered
    const allQuestions = await ctx.db
      .query("questions")
      .withIndex("by_assignment", (q) => q.eq("assignmentId", question.assignmentId))
      .collect();

    const allAnswered = allQuestions.every(q => q._id === args.questionId || q.isAnswered);
    
    if (allAnswered) {
      await ctx.db.patch(question.assignmentId, {
        status: "completed",
      });
    }
  },
});
