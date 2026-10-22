---
name: decision-logger
description: Document any important decision as a formal Decision Record for a team wiki. Captures context, options considered, reasoning, trade-offs, and trigger conditions for revisiting. Use when a decision has been made and the context needs to be preserved before it's lost, or when a team wants to avoid re-litigating past decisions.
license: MIT
metadata:
  category: operations
---

# Decision Logger

Capture decisions with enough context that anyone who joins the team two years from now can understand not just WHAT was decided, but WHY — and what would cause it to be revisited.

## Process

```
1. EXTRACT   -> Identify the decision, the options considered, and the final choice
2. GAP CHECK -> Ask for any missing context before writing (don't invent it)
3. WRITE     -> Complete the Decision Record template below
4. SUMMARY   -> Add a 1-paragraph plain-English summary at the end
```

## Decision Record Template

```markdown
# Decision Record: [Short Title]

**Date**: [Date]
**Decision Made By**: [Names and roles]
**Status**: Decided / Under Review / Superseded by [link]

---

## Context
[2–4 sentences: What was the situation? What problem were we solving?
What made this a decision worth documenting?]

## Options Considered

### Option A: [Name]
- **Description**: [What would this look like in practice?]
- **Pros**: [What would have worked about this?]
- **Cons**: [What were the risks or downsides?]

### Option B: [Name]
- **Description**: [...]
- **Pros**: [...]
- **Cons**: [...]

### Option C: [Name] *(if applicable)*
- **Description**: [...]
- **Pros**: [...]
- **Cons**: [...]

## Decision

**We chose**: [Option name]

**Why**: [2–4 sentences. What made this the right choice given the context?
What were we optimizing for?]

**Trade-offs accepted**: [What are we knowingly giving up or taking on?]

**Confidence level**: [High / Medium / Low — and why, if not high]

## What This Decision Is NOT
[Explicitly state what this decision does NOT imply, to prevent scope creep.
e.g., "This does not mean we are committed to X long-term."]

## Trigger Conditions for Revisiting
[What would need to be true for us to reconsider this?
e.g., "If X grows beyond Y" or "If Z technology becomes available"
Every decision has an expiration condition — even if it's "only if the entire business model changes."]

## Relevant Context
- [Link to relevant doc / meeting notes / data]

---

## Decision Summary *(plain English, 60-second version for new hires)*
[1 paragraph: What was decided, why, and what would change it. Write as if explaining to someone joining the team who has no context.]
```

## Rules

- Include every option that was REJECTED and why — this is as important as what was chosen
- Trigger conditions are mandatory — every decision has an expiration condition
- Never make the decision sound more certain than it was — include confidence level if appropriate
- Be factually precise — no narrative embellishment or post-hoc rationalization
- The plain-English summary is always the last section — it's what people will actually read

## How to Trigger

```
"Document this as a formal Decision Record for our team wiki.
Here's what we decided and why: [describe]."
```

Or for a decision still in progress:
```
"We're deciding between [Option A] and [Option B]. Help me frame this as a decision record
so we can document it properly once we choose."
```

## Edge Cases

**Decision made under time pressure with incomplete information**: Document this explicitly in the Context section — "This decision was made with limited data because [constraint]. We committed to revisiting it once [new data] was available." Don't make it sound cleaner than it was.

**Controversial or unpopular decision**: Document the dissenting view honestly in the Options section. A good decision record shows that alternative views were heard, not just overridden. If there was a strong minority view, add a "Dissenting View" subsection under the Decision.

**Decision that was later reversed**: Do NOT delete the original record. Update its Status to "Superseded by [link to new record]" and add a brief note at the top: "This decision was reversed on [date]. See [link] for context." The history is valuable.

**Decision with multiple stakeholders who disagreed**: Add a RACI or "Who Was Consulted" section before the Options section, and note explicitly which stakeholders approved vs. were informed vs. objected.
