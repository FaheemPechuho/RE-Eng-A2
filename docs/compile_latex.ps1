# LaTeX Compilation Script for REPORT.tex (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "LaTeX Report Compilation Script" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if pdflatex is installed
$pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue

if (-not $pdflatex) {
    Write-Host "ERROR: pdflatex not found!" -ForegroundColor Red
    Write-Host "Please install a LaTeX distribution:" -ForegroundColor Yellow
    Write-Host "  - MiKTeX: https://miktex.org/download" -ForegroundColor Yellow
    Write-Host "  - TeX Live: https://www.tug.org/texlive/" -ForegroundColor Yellow
    Write-Host "  - Or use Overleaf online: https://www.overleaf.com/" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ pdflatex found" -ForegroundColor Green
Write-Host ""

# Check if REPORT.tex exists
if (-not (Test-Path "REPORT.tex")) {
    Write-Host "ERROR: REPORT.tex not found in current directory!" -ForegroundColor Red
    Write-Host "Please run this script from the docs/ directory." -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ REPORT.tex found" -ForegroundColor Green
Write-Host ""

# Compile LaTeX document (first pass)
Write-Host "Compiling LaTeX document (first pass)..." -ForegroundColor Cyan
$process1 = Start-Process -FilePath "pdflatex" -ArgumentList "-interaction=nonstopmode", "REPORT.tex" -NoNewWindow -Wait -PassThru

if ($process1.ExitCode -ne 0) {
    Write-Host "✗ First compilation failed. Check REPORT.log for errors." -ForegroundColor Red
    exit 1
}

Write-Host "✓ First pass complete" -ForegroundColor Green
Write-Host ""

# Compile LaTeX document (second pass for cross-references)
Write-Host "Compiling LaTeX document (second pass for cross-references)..." -ForegroundColor Cyan
$process2 = Start-Process -FilePath "pdflatex" -ArgumentList "-interaction=nonstopmode", "REPORT.tex" -NoNewWindow -Wait -PassThru

if ($process2.ExitCode -ne 0) {
    Write-Host "✗ Second compilation failed. Check REPORT.log for errors." -ForegroundColor Red
    exit 1
}

Write-Host "✓ Second pass complete" -ForegroundColor Green
Write-Host ""

# Check if PDF was generated
if (Test-Path "REPORT.pdf") {
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host "✓ SUCCESS! PDF generated: REPORT.pdf" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Green
    Write-Host ""
    
    # Clean up auxiliary files
    Write-Host "Cleaning up auxiliary files..." -ForegroundColor Cyan
    Remove-Item -Path "REPORT.aux", "REPORT.log", "REPORT.out", "REPORT.toc" -ErrorAction SilentlyContinue
    Write-Host "✓ Cleanup complete" -ForegroundColor Green
    Write-Host ""
    
    # Show file size
    $fileSize = (Get-Item "REPORT.pdf").Length / 1KB
    Write-Host "PDF file size: $([math]::Round($fileSize, 2)) KB"
    Write-Host ""
    
    # Try to open PDF (optional)
    $response = Read-Host "Open PDF now? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Start-Process "REPORT.pdf"
    }
}
else {
    Write-Host "✗ ERROR: PDF was not generated!" -ForegroundColor Red
    Write-Host "Check REPORT.log for error details." -ForegroundColor Yellow
    exit 1
}

