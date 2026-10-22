---
name: document-converter
description: Convert between Markdown, DOCX, and PDF formats. Extract text from PDFs and Word documents, convert Markdown to DOCX or PDF, or convert PDF directly to DOCX. Use when user wants to convert a document format, extract content from a Word or PDF file, or asks to turn notes/markdown into a Word doc or PDF.
license: MIT
metadata:
  category: productivity
---

# Document Converter

Convert documents between Markdown, DOCX, and PDF formats. Automatically selects the best available tool for the job, handles the conversion, and delivers the output file.

## Conversion Directions

| From | To | Primary Tool | Fallback |
|---|---|---|---|
| DOCX | Markdown | markitdown | pandoc |
| PDF | Markdown | pymupdf4llm | markitdown |
| Markdown | DOCX | pandoc | — |
| Markdown | PDF | pandoc + typst | pandoc + xelatex |
| PDF | DOCX | pdf2docx | — |

## Process

```
1. READ SKILL  -> Check ./skills/docx/SKILL.md or ./skills/pdf/SKILL.md if relevant
2. DETECT      -> Identify input format and desired output format
3. TOOL CHECK  -> Detect which tools are available (see tool detection below)
4. CONVERT     -> Run conversion using best available tool
5. VALIDATE    -> Verify output file exists and has content
6. DELIVER     -> Save to ./outputs/ and present the output using clickable markdown link [filename](file:///absolute/path/to/file)
```

## Tool Detection

Always check tool availability before attempting a conversion:

```python
import subprocess, shutil, sys

def check_tool(name):
    return bool(shutil.which(name))

def check_python_package(pkg):
    try:
        __import__(pkg)
        return True
    except ImportError:
        return False

tools = {
    'markitdown': check_tool('markitdown'),
    'pandoc': check_tool('pandoc'),
    'pymupdf4llm': check_python_package('pymupdf4llm'),
    'pdf2docx': check_python_package('pdf2docx'),
}
print(tools)
```

## Implementation by Conversion Type

### DOCX → Markdown

```python
import subprocess, shutil, os

input_path = './inputs/document.docx'  # use actual uploaded file
output_path = './outputs/document.md'

# Try markitdown first (better table preservation)
result = subprocess.run(['markitdown', input_path], capture_output=True, text=True)
if result.returncode == 0:
    with open(output_path, 'w') as f:
        f.write(result.stdout)
else:
    # Fallback: pandoc
    subprocess.run(['pandoc', input_path, '-o', output_path], check=True)

print(f"Converted to: {output_path}")
```

### PDF → Markdown

```python
import subprocess, shutil

input_path = './inputs/document.pdf'  # use actual uploaded file
output_path = './outputs/document.md'

try:
    import pymupdf4llm
    md_text = pymupdf4llm.to_markdown(input_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(md_text)
except ImportError:
    # Fallback: markitdown
    result = subprocess.run(['markitdown', input_path], capture_output=True, text=True)
    with open(output_path, 'w') as f:
        f.write(result.stdout)

print(f"Converted to: {output_path}")
```

### Markdown → DOCX

```python
# Always read ./skills/docx/SKILL.md first for best practices
import subprocess, shutil

input_path = './inputs/document.md'  # use actual uploaded file
output_path = './outputs/document.docx'

subprocess.run(['pandoc', input_path, '-o', output_path], check=True)
print(f"Converted to: {output_path}")
```

### Markdown → PDF

```python
import subprocess, shutil

input_path = './inputs/document.md'  # use actual uploaded file
output_path = './outputs/document.pdf'

# Try Typst engine first (faster, modern)
result = subprocess.run(
    ['pandoc', input_path, '-o', output_path, '--pdf-engine=typst'],
    capture_output=True
)
if result.returncode != 0:
    # Fallback: xelatex
    subprocess.run(
        ['pandoc', input_path, '-o', output_path, '--pdf-engine=xelatex'],
        check=True
    )

print(f"Converted to: {output_path}")
```

### PDF → DOCX

```python
# Always read ./skills/pdf/SKILL.md first
from pdf2docx import Converter

input_path = './inputs/document.pdf'  # use actual uploaded file
output_path = './outputs/document.docx'

cv = Converter(input_path)
cv.convert(output_path, start=0, end=None)
cv.close()
print(f"Converted to: {output_path}")
```

## Installing Missing Tools

If a required tool is missing, install it before converting:

```bash
# markitdown
pip install markitdown --break-system-packages

# pymupdf4llm
pip install pymupdf4llm --break-system-packages

# pdf2docx
pip install pdf2docx --break-system-packages

# pandoc (system package)
apt-get install -y pandoc
```

## Quality Expectations

| Conversion | Fidelity | Notes |
|---|---|---|
| DOCX → Markdown | 75–80% | Tables preserve well with markitdown |
| PDF → Markdown | 65–75% | Scanned PDFs will be lower quality |
| Markdown → DOCX | 95%+ | Excellent with pandoc |
| Markdown → PDF | High | Typst faster; xelatex more compatible |
| PDF → DOCX | 80–85% | Layout preserved better than via Markdown |

## Rules

- Always check which tools are available before attempting conversion — never assume
- If a tool is missing, install it first using pip or apt, then convert
- Use the actual uploaded file from `./inputs/` — never hardcode filenames
- Always save output to `./outputs/` and use `markdown file link` to deliver
- For DOCX output, read `./skills/docx/SKILL.md` first
- For PDF output, read `./skills/pdf/SKILL.md` first
- If conversion fails with primary tool, always attempt the fallback before giving up
- Warn the user if the source is a scanned PDF (OCR quality may be low)

## How to Trigger

- "Convert this Word doc to Markdown"
- "Extract text from this PDF"
- "Turn this Markdown file into a Word document"
- "Convert this PDF to DOCX"
- "Make a PDF from these notes"
