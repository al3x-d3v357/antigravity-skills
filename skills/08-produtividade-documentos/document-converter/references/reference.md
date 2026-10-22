# Document Converter - Technical Reference

Complete technical documentation for the document-converter skill, including tool specifications, quality metrics, API reference, and performance benchmarks.

## Tool Specifications

### MarkItDown

**Version**: Latest (pip installable)
**Repository**: https://github.com/microsoft/markitdown
**License**: MIT
**Platform**: Cross-platform (Python)

**Capabilities**:
- DOCX → Markdown conversion
- PDF → Markdown conversion
- Excel → Markdown table extraction
- PowerPoint → Markdown outline extraction
- Image OCR support (with pytesseract)

**Quality Metrics** (from testing):
- DOCX tables: 100% pipe-style markdown preservation
- Heading preservation: 95%+
- Unicode/emoji support: Perfect
- Image extraction: Reliable
- Processing speed: Fast (0.5-2s per file)

**Command Interface**:
```bash
markitdown input.docx > output.md
markitdown input.pdf > output.md
