# LaTeX Report Compilation Guide

## Prerequisites

You need a LaTeX distribution installed on your system. Choose one based on your operating system:

### Windows
- **MiKTeX**: https://miktex.org/download
- **TeX Live**: https://www.tug.org/texlive/

### macOS
- **MacTeX**: https://www.tug.org/mactex/

### Linux
```bash
# Ubuntu/Debian
sudo apt-get install texlive-full

# Fedora
sudo dnf install texlive-scheme-full

# Arch Linux
sudo pacman -S texlive-most
```

## Compilation Methods

### Method 1: Using pdflatex (Command Line)

```bash
# Navigate to the docs directory
cd docs

# Compile (run twice for proper cross-references)
pdflatex REPORT.tex
pdflatex REPORT.tex

# Clean up auxiliary files (optional)
rm REPORT.aux REPORT.log REPORT.out REPORT.toc
```

### Method 2: Using latexmk (Automated)

```bash
cd docs
latexmk -pdf REPORT.tex
```

### Method 3: Using Online LaTeX Editors

1. **Overleaf** (Recommended):
   - Go to https://www.overleaf.com/
   - Create a free account
   - Click "New Project" → "Upload Project"
   - Upload the REPORT.tex file
   - Click "Recompile" to generate PDF

2. **Papeeria**:
   - Go to https://papeeria.com/
   - Upload REPORT.tex
   - Compile online

### Method 4: Using LaTeX IDEs

1. **TeXstudio** (Cross-platform):
   - Download from https://www.texstudio.org/
   - Open REPORT.tex
   - Press F5 or click "Build & View"

2. **TeXmaker** (Cross-platform):
   - Download from https://www.xm1math.net/texmaker/
   - Open REPORT.tex
   - Press F1 (Quick Build)

3. **Visual Studio Code**:
   - Install "LaTeX Workshop" extension
   - Open REPORT.tex
   - Save the file (auto-compiles)

## Expected Output

After successful compilation, you should get:
- **REPORT.pdf** - The main output document
- REPORT.aux - Auxiliary file (can be deleted)
- REPORT.log - Compilation log (can be deleted)
- REPORT.out - Hyperlink information (can be deleted)
- REPORT.toc - Table of contents data (can be deleted)

## Troubleshooting

### Missing Packages Error

If you get errors about missing packages (e.g., `listings.sty not found`):

**MiKTeX (Windows):**
- Packages will be installed automatically when prompted
- Or use MiKTeX Console → Packages → Search and install

**TeX Live (Linux/Mac):**
```bash
# Install specific package
sudo tlmgr install listings

# Or install all recommended packages
sudo tlmgr install collection-latexrecommended
```

### Common Issues

1. **Error: "! Undefined control sequence"**
   - Make sure all required packages are installed
   - Check for typos in LaTeX commands

2. **Error: "! LaTeX Error: File 'XXX.sty' not found"**
   - Install the missing package using your LaTeX distribution's package manager

3. **Table of Contents not showing**
   - Run pdflatex twice (first run generates TOC data, second run includes it)

4. **Compilation freezes**
   - Press Ctrl+C to cancel
   - Check the .log file for errors
   - Try deleting auxiliary files and recompile

## Quick Compile Script

For convenience, use the provided compile script:

**Windows (PowerShell):**
```powershell
cd docs
.\compile_latex.ps1
```

**Linux/Mac (Bash):**
```bash
cd docs
chmod +x compile_latex.sh
./compile_latex.sh
```

## Customization

### Change Author Name
Edit line 72 in REPORT.tex:
```latex
\author{Your Name \\ Your Student ID}
```

### Adjust Page Margins
Edit line 7 in REPORT.tex:
```latex
\usepackage[margin=1in]{geometry}  % Change "1in" to desired margin
```

### Change Font Size
Edit line 3 in REPORT.tex:
```latex
\documentclass[11pt,a4paper]{article}  % Change "11pt" to 10pt or 12pt
```

## Output Specifications

The generated PDF will have:
- **Page Size**: A4
- **Font Size**: 11pt
- **Margins**: 1 inch on all sides
- **Pages**: Approximately 25-30 pages
- **Sections**: 7 main sections + appendices
- **Code Listings**: Syntax-highlighted Python code
- **Tables**: Professional formatting with booktabs
- **Hyperlinks**: Clickable cross-references and URLs

## Alternative Formats

If you need other formats:

### HTML Version
```bash
pandoc REPORT.tex -o REPORT.html
```

### Word Document
```bash
pandoc REPORT.tex -o REPORT.docx
```

Note: These conversions may not preserve all formatting perfectly.

## Need Help?

1. Check the LaTeX log file: `REPORT.log`
2. Search for the specific error message online
3. Visit LaTeX Stack Exchange: https://tex.stackexchange.com/
4. Check LaTeX documentation: https://www.latex-project.org/help/

## Summary

**Easiest Method**: Use Overleaf (no installation required)
**Best for Customization**: Install TeXstudio or VS Code with LaTeX Workshop
**Fastest**: Use `latexmk -pdf REPORT.tex` if you have LaTeX installed

