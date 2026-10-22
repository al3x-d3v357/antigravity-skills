# Quick Research Workflow

**Mode:** Single Claude researcher, 1 query | **Timeout:** 30 seconds

## When to Use

- User says "quick research" or "minor research"
- Simple, straightforward queries
- Time-sensitive requests
- Just need a fast answer

## Workflow

### Step 1: Launch Single Claude Agent

**ONE Task call - Claude researcher with a single focused query:**

```typescript
Task({
  subagent_type: "ClaudeResearcher",
  description: "[topic] quick lookup",
  prompt: "Do ONE web search for: [query]. Return the key findings immediately. Keep it brief and factual."
})
