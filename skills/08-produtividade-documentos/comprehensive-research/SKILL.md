---
name: comprehensive-research
description: Comprehensive research and content analysis system. Use when the user says 'do research', 'quick research', 'extensive research', 'find information', 'investigate', 'analyze this content', 'extract key insights', or requests any web or content research. Supports three depth modes (quick / standard / extensive) and specialized research types.
license: MIT
metadata:
  category: research
---

# Research Skill

Comprehensive research, analysis, and content extraction. Automatically selects the right research mode based on the request, then delivers structured, sourced findings.

## Research Mode Routing

Select the mode based on how the user phrases their request:

| Trigger phrase | Mode | Approach |
|---|---|---|
| "quick research", "minor research" | **Quick** | 1–2 targeted searches, fast summary |
| "research this", "find information" (default) | **Standard** | 3–5 searches, structured report |
| "extensive research", "deep research" | **Extensive** | 6–10 searches across multiple angles, comprehensive report |
| "extract insights", "analyze this content" | **Content Analysis** | Deep analysis of provided content, no web search needed |
| "research [person/company] background" | **→ Use OSINT mode** | See OSINT section below |

---

## Quick Research

**Use when**: User wants a fast answer, a brief overview, or says "quick" or "minor."

```
1. SEARCH    -> 1-2 targeted web searches on the core question
2. SYNTHESIZE -> Pull the key facts, skip the noise
3. DELIVER   -> 3-5 bullet summary + 1-2 source links
```

**Output format**:
```
## Quick Research: [Topic]

Key findings:
- [Finding 1 + source]
- [Finding 2 + source]
- [Finding 3 + source]

Sources: [link 1], [link 2]
```

---

## Standard Research (Default)

**Use when**: User says "research this" or "find information" without specifying depth.

```
1. FRAME     -> Identify the core question + 2-3 sub-questions worth answering
2. SEARCH    -> 3-5 searches covering different angles (recent news, background, data, expert views)
3. SYNTHESIZE -> Identify patterns, conflicts, and gaps across sources
4. DELIVER   -> Structured report with sections, findings, and cited sources
```

**Output format**:
```
## Research Report: [Topic]

### Overview
[2-3 sentence summary of the most important finding]

### Key Findings

**[Theme 1]**
[Finding with source citation]

**[Theme 2]**
[Finding with source citation]

**[Theme 3]**
[Finding with source citation]

### What's Unclear / Contested
[Any conflicting information or gaps found]

### Sources
[Numbered list of sources used]
```

---

## Extensive Research

**Use when**: User says "extensive", "deep", or "comprehensive" research.

```
1. MAP        -> Break the topic into 3 distinct research angles (e.g., historical / current / future)
2. SEARCH     -> 6-10 searches, covering each angle with 2-3 queries each
3. CROSS-REF  -> Look for contradictions, consensus, and outlier views across sources
4. SYNTHESIZE -> Build a structured report with sections per angle
5. GAPS       -> Explicitly note what couldn't be found or verified
6. DELIVER    -> Long-form report with executive summary + detailed sections + full source list
```

**Output format**:
```
## Comprehensive Research Report: [Topic]

### Executive Summary
[4-6 sentence overview of the most important findings]

### Angle 1: [e.g., Current State]
[Detailed findings with citations]

### Angle 2: [e.g., Key Players / Trends]
[Detailed findings with citations]

### Angle 3: [e.g., Future Outlook / Implications]
[Detailed findings with citations]

### Conflicting Views
[Where sources disagreed and what to make of it]

### Research Gaps
[What wasn't findable or needs primary research]

### Full Source List
[All sources used, numbered]
```

---

## Content Analysis

**Use when**: User provides content (article, transcript, document) and wants insights extracted — no web search needed.

```
1. READ       -> Fully read the provided content
2. EXTRACT    -> Pull out: main argument / key claims / supporting evidence / assumptions / gaps
3. EVALUATE   -> Assess quality of reasoning and evidence
4. DELIVER    -> Structured analysis report
```

**Output format**:
```
## Content Analysis: [Title/Source]

### Main Argument
[The central claim or thesis in one sentence]

### Key Points
- [Point 1]
- [Point 2]
- [Point 3]

### Evidence Quality
[Strong / Weak / Mixed — with specific examples]

### Assumptions Made
[What the author takes for granted that may not hold]

### What's Missing
[Counterarguments not addressed, gaps in evidence]

### Bottom Line
[Your assessment: is this credible, useful, worth acting on?]
```

---

## OSINT / Background Research

**Use when**: User asks about a specific person, company, or organization for vetting, due diligence, or background purposes.

This requires a different approach — do NOT use general web search as the primary method. Instead:

```
1. FLAG      -> Note this is a background/OSINT request
2. SOURCES   -> Search LinkedIn, Crunchbase, Companies House (or local equivalent), news archives
3. STRUCTURE -> Organize findings by category: professional history / public statements / affiliations / red flags
4. CAVEATS   -> Always note what couldn't be verified and the limits of public information
```

---

## URL Verification Rule

**Never deliver a URL without verifying it exists.** Before including any link in the output:
- Use web_fetch to confirm the page loads and contains the expected content
- If a URL returns an error, find the correct URL or remove it
- A broken source link undermines the entire research output

---

## Rules

- Always match research depth to the request — don't run 10 searches for a quick question
- Cite every specific claim — no unsourced assertions
- When sources conflict, say so explicitly — don't pick one silently
- If a topic requires primary research (surveys, interviews, proprietary data), flag it as a gap
- For person/company background checks, apply extra care around accuracy and privacy
- Never fabricate sources, URLs, statistics, or quotes
