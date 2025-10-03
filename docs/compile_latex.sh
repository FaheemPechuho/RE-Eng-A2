#!/bin/bash
# LaTeX Compilation Script for REPORT.tex

echo "=========================================="
echo "LaTeX Report Compilation Script"
echo "=========================================="
echo ""

# Check if pdflatex is installed
if ! command -v pdflatex &> /dev/null
then
    echo "ERROR: pdflatex not found!"
    echo "Please install a LaTeX distribution:"
    echo "  - Ubuntu/Debian: sudo apt-get install texlive-full"
    echo "  - macOS: Install MacTeX from https://www.tug.org/mactex/"
    echo "  - Or use Overleaf online: https://www.overleaf.com/"
    exit 1
fi

echo "✓ pdflatex found"
echo ""

# Check if REPORT.tex exists
if [ ! -f "REPORT.tex" ]; then
    echo "ERROR: REPORT.tex not found in current directory!"
    echo "Please run this script from the docs/ directory."
    exit 1
fi

echo "✓ REPORT.tex found"
echo ""

# Compile LaTeX document
echo "Compiling LaTeX document (first pass)..."
pdflatex -interaction=nonstopmode REPORT.tex > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "✗ First compilation failed. Check REPORT.log for errors."
    exit 1
fi

echo "✓ First pass complete"
echo ""

echo "Compiling LaTeX document (second pass for cross-references)..."
pdflatex -interaction=nonstopmode REPORT.tex > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "✗ Second compilation failed. Check REPORT.log for errors."
    exit 1
fi

echo "✓ Second pass complete"
echo ""

# Check if PDF was generated
if [ -f "REPORT.pdf" ]; then
    echo "=========================================="
    echo "✓ SUCCESS! PDF generated: REPORT.pdf"
    echo "=========================================="
    echo ""
    
    # Clean up auxiliary files
    echo "Cleaning up auxiliary files..."
    rm -f REPORT.aux REPORT.log REPORT.out REPORT.toc
    echo "✓ Cleanup complete"
    echo ""
    
    # Show file size
    SIZE=$(du -h REPORT.pdf | cut -f1)
    echo "PDF file size: $SIZE"
    echo ""
    
    # Try to open PDF (optional)
    read -p "Open PDF now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v xdg-open &> /dev/null; then
            xdg-open REPORT.pdf
        elif command -v open &> /dev/null; then
            open REPORT.pdf
        else
            echo "Please open REPORT.pdf manually."
        fi
    fi
else
    echo "✗ ERROR: PDF was not generated!"
    echo "Check REPORT.log for error details."
    exit 1
fi

