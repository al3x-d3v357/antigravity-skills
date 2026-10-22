# Claude Web Research Workflow

Intelligent multi-query WebSearch using Claude's built-in tool. Decomposes research questions into 4-8 targeted sub-queries and executes them in parallel.

## Features

- Intelligent query decomposition into multiple focused searches
- Parallel execution using Claude WebSearch for speed
- Iterative follow-up searches based on initial findings
- Comprehensive synthesis of all findings

## Advantages

- Uses Claude's built-in WebSearch (no API keys needed)
- Free and unlimited usage
- Integrated with Claude's knowledge and reasoning

## When to Use

- User says "claude research" or "use websearch"
- Want free research without API costs
- Need Claude's reasoning integrated with search

## Workflow

### Step 1: Decompose Query

Break the research question into 4-8 focused sub-queries:

1. **Original question** - The exact query
2. **Background context** - "what is [topic] background context"
3. **Recent news** - "[topic] latest news [year]"
4. **Recent developments** - "[topic] recent developments [year]"
5. **Technical details** - "[topic] technical details explained"
6. **Comparison** - "[topic] comparison alternatives options"
7. **Expert analysis** - "[topic] expert analysis opinion"
8. **Implications** - "[topic] implications impact consequences"

### Step 2: Execute Parallel WebSearches

Launch all queries simultaneously using Claude's WebSearch:

```typescript
// Execute all in parallel
WebSearch({ query: query1 })
WebSearch({ query: query2 })
WebSearch({ query: query3 })
// ... up to 8 queries
