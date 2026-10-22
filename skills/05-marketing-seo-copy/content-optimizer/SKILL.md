---
name: content-optimizer
description: Optimize any piece of content for on-page SEO. Checks keyword density, meta tags, heading structure, and readability. Use when optimizing existing content for better rankings, validating new content against SEO requirements, or asking for meta title/description help.
license: MIT
metadata:
  category: seo
---

# Content Optimizer

Analyze and optimize any piece of content for on-page SEO. Run a full audit against the checklist below and give specific, actionable fixes — not just a score.

## Process

```
1. IDENTIFY   -> Primary keyword + target audience + page goal (rank / convert / inform)
2. AUDIT      -> Check all elements against the framework below
3. FLAG       -> List every issue found with severity (critical / recommended / optional)
4. FIX        -> Provide the corrected version for each flagged issue
5. CHECKLIST  -> Confirm every item passes before sign-off
```

## Keyword Density

**Target:** 1–2% for primary keyword

```
Density = (Keyword Count / Total Words) × 100
```

**Placement priorities (in order):**
1. Title / H1 — required
2. First 100 words — required
3. At least one H2 — recommended
4. Conclusion — recommended
5. Distributed naturally in body — required

**Warning thresholds:**
- >3% = Keyword stuffing risk — rewrite affected paragraphs
- <0.5% = Under-optimized — add keyword to intro and one H2
- Exact match every paragraph = Unnatural — use synonyms and LSI variants

## Meta Tags

### Title Tag
- Length: 50–60 characters
- Keyword: Near the beginning
- Format: `{Keyword} - {Benefit} | {Brand}`
- Must be unique per page

### Meta Description
- Length: 150–160 characters
- Include keyword naturally
- End with an action verb (CTA)
- Must be unique per page

### URL Slug
- 3–5 words maximum
- Include primary keyword
- Hyphens between words, lowercase only
- No stop words (the, and, of, etc.)

## Heading Structure

**Valid hierarchy:**
```
H1: Page Title (exactly 1 — never repeat)
├── H2: Main Section
│   ├── H3: Subsection
│   └── H3: Subsection
├── H2: Main Section
│   └── H3: Subsection
└── H2: Conclusion
```

**Critical errors to flag:**
- Multiple H1 tags — critical
- Skipping levels (H1 → H3 with no H2) — critical
- No keyword in H1 — critical
- Headings used purely for visual styling — flag and remove

## Readability

**Target: Flesch Reading Ease 60–70** (standard, 8th–9th grade)

| Score | Level | Notes |
|---|---|---|
| 70–79 | Fairly Easy | Fine for most blogs |
| 60–69 | Standard | ✅ Target range |
| 50–59 | Fairly Difficult | Acceptable for technical content |
| <50 | Difficult | Rewrite for general audiences |

**How to improve readability:**
- Average sentence length under 20 words
- Paragraphs: 2–3 sentences max
- Replace jargon with plain language
- Active voice over passive
- Add a subheading every 200–300 words
- Use bullet points for any list of 3+ items

## Full Optimization Checklist

When auditing content, verify every item. Flag each as ✅ pass / ⚠️ fix needed / ❌ critical issue.

**Keyword**
- [ ] Primary keyword in title / H1
- [ ] Primary keyword in first 100 words
- [ ] Keyword density 1–2%
- [ ] No keyword stuffing (exact match not in every paragraph)

**Meta**
- [ ] Meta title 50–60 characters
- [ ] Meta description 150–160 characters with CTA
- [ ] URL slug is short, keyword-inclusive, lowercase

**Structure**
- [ ] Exactly one H1
- [ ] Valid heading hierarchy (no skipped levels)
- [ ] Keyword appears in at least one H2
- [ ] Subheadings every 200–300 words

**Content**
- [ ] Flesch score 60–70
- [ ] No paragraphs over 3 sentences
- [ ] At least 3 internal links
- [ ] At least 1 external authoritative link

## Output Format

```
## SEO Audit: [Page Title / URL]
Primary keyword: [keyword]
Word count: [X]

### Critical Issues ❌
[Issue] → [Exact fix]

### Recommended Fixes ⚠️
[Issue] → [Exact fix]

### Passing ✅
[List of elements that are already optimized]

### Suggested Meta Tags
Title: [optimized title — X chars]
Description: [optimized description — X chars]
Slug: [optimized-slug]

### Checklist
[Full checklist with pass/fix/critical status for each item]
```

## How to Trigger

```
"Optimize this content for SEO. Primary keyword: [keyword]."
"Audit this page against SEO requirements."
"Write a meta title and description for this article targeting [keyword]."
"Check the heading structure of this content."
```
