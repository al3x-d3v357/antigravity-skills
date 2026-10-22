# Fabric Workflow

Intelligent pattern selection for Fabric CLI. Automatically selects the right pattern from 242+ specialized prompts based on your intent - threat modeling, analysis, summarization, content creation, extraction, and more.

**USE WHEN** processing content, analyzing data, creating summaries, threat modeling, or transforming text.

## When to Activate This Skill

**Primary Use Cases:**
- "Create a threat model for..."
- "Summarize this article/video/paper..."
- "Extract wisdom/insights from..."
- "Analyze this [code/malware/claims/debate]..."
- "Improve my writing/code/prompt..."
- "Create a [visualization/summary/report]..."
- "Rate/review/judge this content..."

**The Goal:** Select the RIGHT pattern from 242+ available patterns based on what you're trying to accomplish.

## Pattern Selection Strategy

### 1. Identify Intent Category

**Threat Modeling & Security:**
- Threat model -> `create_threat_model` or `create_stride_threat_model`
- Threat scenarios -> `create_threat_scenarios`
- Security rules -> `create_sigma_rules`, `write_nuclei_template_rule`

**Summarization:**
- General summary -> `summarize`
- 5-sentence summary -> `create_5_sentence_summary`
- Meeting -> `summarize_meeting`
- Paper/research -> `summarize_paper`
- Video/YouTube -> `youtube_summary`

**Wisdom Extraction:**
- General wisdom -> `extract_wisdom`
- Article wisdom -> `extract_article_wisdom`
- Book ideas -> `extract_book_ideas`
- Insights -> `extract_insights`
- Main idea -> `extract_main_idea`

**Analysis:**
- Malware -> `analyze_malware`
- Code -> `analyze_code` or `review_code`
- Claims -> `analyze_claims`
- Debate -> `analyze_debate`
- Paper -> `analyze_paper`

**Content Creation:**
- PRD -> `create_prd`
- Design document -> `create_design_document`
- User story -> `create_user_story`
- Visualization -> `create_visualization`, `create_mermaid_visualization`

**Improvement:**
- Writing -> `improve_writing`
- Prompt -> `improve_prompt`
- Code -> `review_code`

**Rating/Evaluation:**
- AI response -> `rate_ai_response`
- Content quality -> `rate_content`
- General judgment -> `judge_output`

### 2. Execute Pattern

```bash
# Basic format
fabric [input] -p [selected_pattern]

# From URL
fabric -u "URL" -p [pattern]

# From YouTube
fabric -y "YOUTUBE_URL" -p [pattern]

# From file
cat file.txt | fabric -p [pattern]
