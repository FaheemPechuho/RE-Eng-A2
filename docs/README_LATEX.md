# LaTeX Report Files

This directory contains the LaTeX version of the Code Smell Detection project report.

## Files

- **REPORT.tex** - Main LaTeX source file (professional academic format)
- **REPORT.md** - Markdown version (original format)
- **COMPILE_LATEX.md** - Comprehensive compilation guide
- **compile_latex.sh** - Bash script for Linux/Mac compilation
- **compile_latex.ps1** - PowerShell script for Windows compilation

## Quick Start

### Option 1: Online (No Installation Required) ⭐ RECOMMENDED

1. Go to [Overleaf](https://www.overleaf.com/)
2. Create a free account
3. Click "New Project" → "Upload Project"
4. Upload `REPORT.tex`
5. Click "Recompile" to generate PDF
6. Download the PDF

### Option 2: Local Compilation

#### Windows
```powershell
cd docs
powershell -ExecutionPolicy Bypass -File .\compile_latex.ps1
```

#### Linux/Mac
```bash
cd docs
chmod +x compile_latex.sh
./compile_latex.sh
```

#### Manual Compilation
```bash
cd docs
pdflatex REPORT.tex
pdflatex REPORT.tex  # Run twice for cross-references
```

## What's Included in the LaTeX Report

The LaTeX version provides:

✅ **Professional Formatting**
- Academic paper layout with proper sections
- Automatic table of contents
- Professional typography
- Proper page numbering and headers

✅ **Enhanced Code Listings**
- Syntax-highlighted Python code
- Line numbers
- Professional code formatting
- Proper spacing and indentation

✅ **Better Tables**
- Publication-quality tables using booktabs
- Professional spacing and alignment
- Clear visual hierarchy

✅ **Mathematical Formulas**
- Proper equation formatting
- Technical debt ratio formulas
- Maintainability index calculation

✅ **Hyperlinks**
- Clickable table of contents
- Cross-references within document
- External URL links
- Bibliography references

✅ **References**
- Proper bibliography formatting
- Academic citation style
- Numbered references

## Document Structure

```
1. Executive Summary
2. Introduction
   - Background
   - Project Objectives
   - Scope
3. Deliberately Smelly Code
   - Overview
   - Introduced Code Smells (all 6)
   - Unit Tests
4. Detection Application Design
   - Architecture
   - Design Patterns
   - Configuration System
5. Detection Logic and Thresholds
   - Individual detector descriptions
   - Threshold selection methodology
6. Testing and Results
   - Test setup
   - Analysis results
   - CLI feature testing
7. Technical Debt and Maintainability
   - Impact metrics
   - Maintainability index
8. Conclusion
Appendices
Bibliography
```

## Page Count

Approximately **25-30 pages** when compiled to PDF.

## Customization

### Change Your Name
Edit line 72 in `REPORT.tex`:
```latex
\author{Your Name \\ Your Student ID}
```

### Adjust Margins
Edit line 7:
```latex
\usepackage[margin=1in]{geometry}  % Change to 0.8in, 1.2in, etc.
```

### Change Font Size
Edit line 3:
```latex
\documentclass[11pt,a4paper]{article}  % 10pt, 11pt, or 12pt
```

## Troubleshooting

### Package Missing Error

If you see errors like "listings.sty not found":

**MiKTeX (Windows):**
- Packages auto-install when prompted
- Or use MiKTeX Console → Packages

**TeX Live (Linux/Mac):**
```bash
sudo tlmgr install listings
sudo tlmgr install booktabs
sudo tlmgr install xcolor
```

### Compilation Hangs

1. Press Ctrl+C to cancel
2. Delete all auxiliary files:
   ```bash
   rm REPORT.aux REPORT.log REPORT.out REPORT.toc
   ```
3. Try compiling again

### Table of Contents Missing

Run pdflatex **twice**:
```bash
pdflatex REPORT.tex
pdflatex REPORT.tex  # Second run includes TOC
```

## Required LaTeX Packages

The report uses these packages (all standard):
- inputenc, geometry - Document setup
- graphicx - Image support
- listings - Code listings
- xcolor - Color support
- hyperref - Hyperlinks
- booktabs - Professional tables
- longtable - Multi-page tables
- fancyhdr - Headers/footers
- titlesec - Section formatting
- enumitem - List formatting
- amsmath, amssymb - Math symbols

## Output Specifications

**Generated PDF:**
- Format: PDF/A compliant
- Page Size: A4 (210mm × 297mm)
- Orientation: Portrait
- Margins: 1 inch (25.4mm) all sides
- Font: Computer Modern (default LaTeX font)
- Font Size: 11pt body text
- Line Spacing: Single
- Colors: Yes (code syntax highlighting)
- Hyperlinks: Yes (clickable)
- Bookmarks: Yes (PDF navigation)

## Converting to Other Formats

### HTML Version
```bash
pandoc REPORT.tex -s -o REPORT.html --mathjax
```

### Microsoft Word
```bash
pandoc REPORT.tex -o REPORT.docx
```

**Note:** Conversions may not preserve all LaTeX formatting perfectly.

## Comparison: LaTeX vs Markdown

| Feature | Markdown | LaTeX |
|---------|----------|-------|
| Formatting | Basic | Professional |
| Code Listings | Plain | Syntax-highlighted |
| Tables | Simple | Publication-quality |
| Math Equations | Limited | Full support |
| Page Layout | No control | Full control |
| Citations | Manual | Automatic |
| Hyperlinks | Basic | Advanced |
| Output Quality | Good | Excellent |
| Compilation | N/A | Required |
| Learning Curve | Easy | Moderate |

## When to Use Each Format

**Use Markdown (REPORT.md) when:**
- Reading on GitHub/GitLab
- Quick reference
- Editing in simple text editors
- Don't need printing

**Use LaTeX (REPORT.tex) when:**
- Submitting formal report
- Printing physical copies
- Need professional formatting
- Academic/conference submission
- Want publication quality

## Support

For LaTeX help:
- 📘 [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)
- 💬 [TeX Stack Exchange](https://tex.stackexchange.com/)
- 📖 [Overleaf Documentation](https://www.overleaf.com/learn)
- 🎓 [LaTeX Tutorial](https://www.latex-tutorial.com/)

## License

This LaTeX report is part of the Code Smell Detection assignment and is for educational purposes.

---

**Pro Tip:** If you're new to LaTeX, use Overleaf! It's the easiest way to compile without installing anything.

