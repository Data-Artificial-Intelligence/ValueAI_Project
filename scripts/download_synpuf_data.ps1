# CMS DE-SynPUF Sample 1 Download Script
$ErrorActionPreference = "Stop"
$DataDir = Join-Path $PSScriptRoot "..\data\raw\synpuf"
$DataDir = [System.IO.Path]::GetFullPath($DataDir)

if (-not (Test-Path $DataDir)) {
    New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
}

# Note: 2010 Beneficiary Sample 1 is intentionally omitted due to a known, 
# longstanding 404 error on the official CMS portal. 
# 2008 and 2009 files provide complete baseline demographics for the cohort.

$Files = @(
    @{ Name = "DE1_0_2008_Beneficiary_Summary_File_Sample_1.csv"; Url = "https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/de1_0_2008_beneficiary_summary_file_sample_1.zip" },
    @{ Name = "DE1_0_2009_Beneficiary_Summary_File_Sample_1.csv"; Url = "https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/de1_0_2009_beneficiary_summary_file_sample_1.zip" },
    @{ Name = "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv"; Url = "https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/de1_0_2008_to_2010_inpatient_claims_sample_1.zip" },
    @{ Name = "DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv"; Url = "https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/de1_0_2008_to_2010_outpatient_claims_sample_1.zip" },
    @{ Name = "DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.csv"; Url = "https://downloads.cms.gov/files/DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.zip" },
    @{ Name = "DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.csv"; Url = "https://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_1A.zip" },
    @{ Name = "DE1_0_2008_to_2010_Carrier_Claims_Sample_1B.csv"; Url = "https://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_1B.zip" }
)

Write-Host "[INFO] Starting CMS DE-SynPUF Sample 1 download..." -ForegroundColor Cyan
Write-Host "[INFO] Destination: $DataDir" -ForegroundColor Gray

$DownloadedCount = 0
$SkippedCount = 0

foreach ($File in $Files) {
    $ExpectedFile = Join-Path $DataDir $File.Name
    $ZipPath = Join-Path $DataDir "$($File.Name).zip"

    Write-Host "`nProcessing: $($File.Name)" -ForegroundColor Yellow

    if (Test-Path $ExpectedFile) {
        Write-Host "[SKIP] File already exists" -ForegroundColor Gray
        $SkippedCount++
        continue
    }

    try {
        Write-Host "Downloading..." -ForegroundColor Gray
        Invoke-WebRequest -Uri $File.Url -OutFile $ZipPath -UseBasicParsing
        
        Write-Host "Extracting..." -ForegroundColor Gray
        Expand-Archive -Path $ZipPath -DestinationPath $DataDir -Force
        Remove-Item $ZipPath -Force

        # Handle potential nested folders in ZIP
        $FoundFile = Get-ChildItem -Path $DataDir -Filter "*.csv" -Recurse -File | Where-Object { $_.Name -eq $File.Name } | Select-Object -First 1
        if ($FoundFile) {
            Move-Item -Path $FoundFile.FullName -Destination $ExpectedFile -Force
        }

        Write-Host "[OK] Extracted: $($File.Name)" -ForegroundColor Green
        $DownloadedCount++
    }
    catch {
        Write-Host "[ERROR] Failed: $($_.Exception.Message)" -ForegroundColor Red
        if (Test-Path $ZipPath) { Remove-Item $ZipPath -Force }
    }
}

Write-Host "`n==========================================" -ForegroundColor Cyan
Write-Host "Download Summary: $DownloadedCount New, $SkippedCount Skipped" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan



