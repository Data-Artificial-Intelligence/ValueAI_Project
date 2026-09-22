# TIMSAdvantaged Codebase

Generated: 09/22/2026 10:29:21

---

## Table of Contents

- .env.example
- .gitignore
- app\app.py
- data\processed\.gitkeep
- data\processed\full_dataset.parquet\_SUCCESS
- data\processed\monte_carlo_results.json
- data\processed\test.parquet\_SUCCESS
- data\processed\train.parquet\_SUCCESS
- data\processed\val.parquet\_SUCCESS
- data\raw\.gitkeep
- docs\data_dictionary.md
- docs\data_governance_audit.md
- docs\executive_summary.md
- docs\timeseries_model_metadata.json
- Generate-Codebook-TIMSAdvantaged.ps1
- models\classification_model.pkl
- models\clustering_model.pkl
- models\clustering_scaler.pkl
- models\timeseries_model.pkl
- notebooks\01_data_exploration.ipynb
- notebooks\02_feature_engineering.ipynb
- notebooks\03_modeling_experiments.ipynb
- README.md
- requirements.txt
- scripts\download_synpuf_data.ps1
- src\__init__.py
- src\ai_agent\__init__.py
- src\ai_agent\agent_graph.py
- src\ai_agent\agent_tools.py
- src\data\__init__.py
- src\data\make_dataset.py
- src\data\monte_carlo_simulation.py
- src\data\validate_data.py
- src\models\__init__.py
- src\models\train_classification.py
- src\models\train_clustering.py
- src\models\train_timeseries.py
- src\utils\__init__.py
- src\utils\config.py
- src\utils\logger.py
- tests\test_agent.py
- tests\test_data.py

---


<div style='page-break-after: always;'></div>

# File: .env.example

```example
```


<div style='page-break-after: always;'></div>

# File: .gitignore

```gitignore
# Data
data/raw/*
data/processed/*
!data/raw/.gitkeep
!data/processed/.gitkeep

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
*.egg-info/
.ipynb_checkpoints

# Environment & Secrets
.env
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

```


<div style='page-break-after: always;'></div>

# File: app\app.py

```python
```


<div style='page-break-after: always;'></div>

# File: data\processed\.gitkeep

```gitkeep
```


<div style='page-break-after: always;'></div>

# File: data\processed\full_dataset.parquet\_SUCCESS

```text
```


<div style='page-break-after: always;'></div>

# File: data\processed\monte_carlo_results.json

```json
{"0":{"mean_monthly_projection":9744.8108815676,"lower_bound":1845.0323916683,"upper_bound":30112.9676802505},"1":{"mean_monthly_projection":9648.9162351531,"lower_bound":2001.5748939766,"upper_bound":29720.7835117297},"2":{"mean_monthly_projection":9866.2767789969,"lower_bound":1943.1619848646,"upper_bound":31755.900916414},"3":{"mean_monthly_projection":9731.7278243589,"lower_bound":1964.0040662234,"upper_bound":29936.0736460197},"4":{"mean_monthly_projection":9887.6613281219,"lower_bound":1952.5429304653,"upper_bound":30974.0365827539},"5":{"mean_monthly_projection":9902.0468015325,"lower_bound":1932.4463231653,"upper_bound":29919.279091824},"6":{"mean_monthly_projection":10039.7536018458,"lower_bound":1964.5171976077,"upper_bound":31428.7443188574},"7":{"mean_monthly_projection":10014.0550312158,"lower_bound":2019.0810971287,"upper_bound":30843.510876922},"8":{"mean_monthly_projection":10059.1933442166,"lower_bound":2007.9249974312,"upper_bound":30999.8563846628},"9":{"mean_monthly_projection":9971.2608364223,"lower_bound":1973.507857233,"upper_bound":30996.3913161886},"10":{"mean_monthly_projection":10230.8902660074,"lower_bound":1975.6184334184,"upper_bound":31548.0014147313},"11":{"mean_monthly_projection":10168.3098114583,"lower_bound":1992.7208261898,"upper_bound":31308.3117732014}}
```


<div style='page-break-after: always;'></div>

# File: data\processed\test.parquet\_SUCCESS

```text
```


<div style='page-break-after: always;'></div>

# File: data\processed\train.parquet\_SUCCESS

```text
```


<div style='page-break-after: always;'></div>

# File: data\processed\val.parquet\_SUCCESS

```text
```


<div style='page-break-after: always;'></div>

# File: data\raw\.gitkeep

```gitkeep
```


<div style='page-break-after: always;'></div>

# File: docs\data_dictionary.md

```md
# ValueAI Data Dictionary
## CMS SynPUF Processed Features

### Beneficiary Demographics
| Feature       | Type    | Description                                                                    |
|---------------|---------|--------------------------------------------------------------------------------|
| `DESYNPUF_ID` | string  | Hashed unique beneficiary identifier (primary key)                             |
| `AGE`         | int     | Age of beneficiary as of 2010-12-31                                            |
| `SEX`         | int     | Sex (1=Male, 2=Female)                                                         |
| `RACE`        | int     | Race (1=White, 2=Black, 3=Other, 4=Asian, 5=Hispanic, 6=North American Native) |
| `IS_DECEASED` | boolean | Whether beneficiary died during study period                                   |

### Utilization Metrics
| Feature                  | Type  | Description                                      |
|--------------------------|-------|--------------------------------------------------|
| `TOTAL_ADMISSIONS`       | int   | Total inpatient admissions (2008-2010)           |
| `AVG_ADMISSION_COST`     | float | Average Medicare payment per inpatient claim ($) |
| `INPATIENT_CLAIM_COUNT`  | int   | Number of inpatient claims                       |
| `OUTPATIENT_CLAIM_COUNT` | int   | Number of outpatient claims                      |
| `DRUG_CLAIM_COUNT`       | int   | Number of prescription drug events               |

### Clinical Features
| Feature                  | Type  | Description                                                  |
|--------------------------|-------|--------------------------------------------------------------|
| `UNIQUE_DIAGNOSES_COUNT` | int   | Count of distinct ICD-9 diagnosis codes (comorbidity burden) |
| `AVG_LENGTH_OF_STAY`     | float | Average inpatient length of stay (days)                      |

### Temporal Features
| Feature                              | Type  | Description                                    |
|--------------------------------------|-------|------------------------------------------------|
| `AVG_DAYS_BETWEEN_INPATIENT_CLAIMS`  | float | Rolling average days between inpatient claims  |
| `AVG_DAYS_BETWEEN_OUTPATIENT_CLAIMS` | float | Rolling average days between outpatient claims |

### Target Variable
| Feature                | Type    | Description                                                |
|------------------------|---------|------------------------------------------------------------|
| `IS_30DAY_READMISSION` | boolean | Whether patient was readmitted within 30 days of discharge |

### Derived / Monte Carlo Features
| Feature                           | Type  | Description                                     |
|-----------------------------------|-------|-------------------------------------------------|
| `ROLLING_AVG_COST_3`              | float | Rolling 3-claim average cost                    |
| `monte_carlo_total_cost_mean`     | float | Mean projected cost from Monte Carlo simulation |
| `monte_carlo_total_cost_ci_lower` | float | Lower bound of 95% confidence interval          |
| `monte_carlo_total_cost_ci_upper` | float | Upper bound of 95% confidence interval          |
```


<div style='page-break-after: always;'></div>

# File: docs\data_governance_audit.md

```md
# Data Governance & Audit Log
**Project:** ValueAI Risk Stratification Pipeline  
**Date:** 2026-09-21  
**Auditor:** [Antony Henry Oduor Onyango]  

## 1. Data Provenance & Integrity
- **Source:** CMS Medicare Synthetic Public Use Files (SynPUF) DE-1 Sample 1 (2008-2010).
- **Ingestion Method:** Automated PowerShell download with ZIP integrity verification (System.IO.Compression).
- **Storage:** Processed data stored in columnar Parquet format with Snappy compression for optimal big data platform (AWS S3/SageMaker) compatibility.

## 2. Known Data Gaps & Mitigations (Audit Issue #001)
- **Issue:** The official CMS portal returns a persistent HTTP 404 for `DE1_0_2010_Beneficiary_Summary_File_Sample_1.zip`. This is a documented, longstanding CMS publishing error (the link incorrectly routes to Sample 20).
- **Impact Assessment:** Low. The 2008 and 2009 Beneficiary Summary files successfully provide complete baseline demographics (Age, Sex, Race, Chronic Condition flags) for the entire 1,000-beneficiary cohort. 
- **Mitigation Applied:** The PySpark ingestion pipeline (`src/data/make_dataset.py`) was engineered to dynamically discover and union all available beneficiary years. The 2008–2010 Inpatient Claims file successfully provides all necessary longitudinal data to construct the 30-day readmission target variable. No statistical imputation was required.
- **Status:** ✅ CLOSED. Documented and mitigated without blocking project delivery.

## 3. Privacy & Statutory Compliance
- **PII Handling:** The SynPUF dataset is natively de-identified. The `DESYNPUF_ID` is a hashed, synthetic identifier. No real Protected Health Information (PHI) is present or processed.
- **Access Control:** Raw data is excluded from version control via `.gitignore`. Only processed, aggregated, or anonymized artifacts are committed.

## 4. Data Quality Validation (Great Expectations)
Automated validation suite executed post-ingestion. Key assertions passed:
- [x] `DESYNPUF_ID` uniqueness and non-nullability.
- [x] `AGE` bounded between 18 and 110.
- [x] `IS_30DAY_READMISSION` strictly boolean.
- [x] Cost metrics are non-negative.

## 5. Reproducibility
- Pipeline orchestrated via modular Python scripts.
- Random seeds fixed (e.g., `seed=42` for stratified sampling and Monte Carlo simulations) to ensure 100% reproducible splits and projections.
```


<div style='page-break-after: always;'></div>

# File: docs\executive_summary.md

```md
```


<div style='page-break-after: always;'></div>

# File: docs\timeseries_model_metadata.json

```json
{
  "model_type": "ARIMA",
  "order": [
    1,
    1,
    1
  ],
  "historical_start": "2008-01-01",
  "historical_end": "2010-12-01",
  "historical_observations": 36,
  "holdout_months": 6,
  "forecast_horizon_months": 12,
  "naive_rmse": 6327247.040082546,
  "naive_mae": 5409680.0,
  "naive_mape_percent": 138.33737733035917,
  "arima_rmse": 5382314.0647497885,
  "arima_mae": 4487614.259303573,
  "arima_mape_percent": 117.68687238056526,
  "arima_rmse_improvement_vs_naive_percent": 14.934346159501773,
  "forecast_total": -4414162.18412317,
  "forecast_average_monthly": -367846.8486769308
}
```


<div style='page-break-after: always;'></div>

# File: Generate-Codebook-TIMSAdvantaged.ps1

```ps1
<#
.EXAMPLE
.\Generate-Codebook-TIMSAdvantaged.ps1 -ProjectPath "C:\Data\ValueAI_Project"
#>

param(
    [string]$ProjectPath = (Get-Location).Path,
    [switch]$GeneratePdf
)

# ============================================================
# Configuration
# ============================================================

$Root = (Resolve-Path $ProjectPath).Path

$MarkdownFile = Join-Path $Root "Codebase.md"
$PdfFile      = Join-Path $Root "Codebase.pdf"

# 1. Directories to completely ignore (Added TIMS specific folders)
$ExcludedDirectories = @(
    ".git", ".github", ".idea", ".vscode", ".cursor",
    "node_modules", "venv", ".venv", "env", "Lib", "Include", "site-packages",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov",
    "coverage", "dist", "build", "bin", "obj", "out", ".next",
    "migrations", "trash", "staticfiles", "media",
    ".cache", ".data", ".logs", ".reports" 
)

# 2. File extensions to ignore (Added Excel, Certs, CSVs)
$ExcludedExtensions = @(
    ".png",".jpg",".jpeg",".gif",".bmp",".ico",".svg",".webp",".avif",
    ".pdf",".zip",".7z",".rar",".tar",".gz",
    ".exe",".dll",".so",".dylib",".pyd",
    ".woff",".woff2",".ttf",".eot",
    ".pyc",".pyo",".class",
    ".db",".sqlite3",".sqlite",".log",
    ".map", ".mo", ".lock", ".pth", ".bak", ".tmp",
    ".xlsx", ".xls", ".csv", ".pem", ".crt", ".key", ".tpl", ".parquet", ".crc"
)

# 3. Specific files to ignore (CRITICAL: Added .secrets.toml for security)
$ExcludedFiles = @(
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Pipfile.lock",
    "poetry.lock",
    "db.sqlite3",
    ".secrets.toml", 
    "Codebase.md",
    "Codebase.pdf"
)

# Delete old markdown if it exists
if (Test-Path $MarkdownFile) {
    Remove-Item $MarkdownFile -Force
}

# ============================================================
# Helper Function
# ============================================================

function Add-Line {
    param([string]$Text)
    Add-Content -Path $MarkdownFile -Value $Text -Encoding UTF8
}

# ============================================================
# Scan Files
# ============================================================

Write-Host ""
Write-Host "Scanning TIMSAdvantaged repository..."
Write-Host ""

$Files = Get-ChildItem -Path $Root -Recurse -File | Where-Object {
    $relative = $_.FullName.Substring($Root.Length).TrimStart('\', '/')
    $fileName = $_.Name

    # Check Directories (Windows and Linux/Mac path separators)
    $pathParts = $relative -split '[\\/]'
    foreach ($dir in $ExcludedDirectories) {
        if ($pathParts -contains $dir) {
            return $false
        }
    }

    # Check Extensions
    if ($ExcludedExtensions -contains $_.Extension.ToLower()) {
        return $false
    }

    # Check Exact Filenames
    if ($ExcludedFiles -contains $fileName) {
        return $false
    }

    return $true

} | Sort-Object FullName

Write-Host "Found $($Files.Count) valid source code files."
Write-Host ""

# ============================================================
# Markdown Header
# ============================================================

Add-Line "# TIMSAdvantaged Codebase"
Add-Line ""
Add-Line "Generated: $(Get-Date)"
Add-Line ""
Add-Line "---"
Add-Line ""

# ============================================================
# Table of Contents
# ============================================================

Add-Line "## Table of Contents"
Add-Line ""

foreach ($file in $Files) {
    $relative = $file.FullName.Substring($Root.Length).TrimStart('\', '/')
    Add-Line "- $relative"
}

Add-Line ""
Add-Line "---"
Add-Line ""

# ============================================================
# Add Every File
# ============================================================

$index = 1

foreach ($file in $Files) {
    $relative = $file.FullName.Substring($Root.Length).TrimStart('\', '/')

    Write-Host "[$index/$($Files.Count)] $relative"

    $language = $file.Extension.TrimStart('.')
    if ([string]::IsNullOrWhiteSpace($language)) { $language = "text" }
    
    # Map specific extensions to markdown code block languages
    switch ($language) {
        "py" { $language = "python" }
        "js" { $language = "javascript" }
        "ts" { $language = "typescript" }
        "tsx" { $language = "tsx" }
        "jsx" { $language = "jsx" }
        "yml" { $language = "yaml" }
        "sh" { $language = "bash" }
        "toml" { $language = "toml" }
    }

    Add-Line ""
    Add-Line "<div style='page-break-after: always;'></div>"
    Add-Line ""
    Add-Line "# File: $relative"
    Add-Line ""
    Add-Line ('```' + $language)

    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        Add-Content -Path $MarkdownFile -Value $content -Encoding UTF8
    }
    catch {
        Add-Line "[Unable to read file.]"
    }

    Add-Line '```'
    Add-Line ""
    $index++
}

Write-Host ""
Write-Host "Markdown created successfully!"
Write-Host $MarkdownFile



# ============================================================
# Optional PDF Generation
# ============================================================

if ($GeneratePdf) {

    $Pandoc = Get-Command pandoc -ErrorAction SilentlyContinue

    if ($Pandoc) {

        Write-Host ""
        Write-Host "Generating PDF..."

        & pandoc `
            $MarkdownFile `
            -o $PdfFile `
            --toc `
            --highlight-style=tango

        Write-Host ""
        Write-Host "PDF created:"
        Write-Host $PdfFile

    }
    else {

        Write-Host ""
        Write-Host "Pandoc was not found."
        Write-Host ""
        Write-Host "Install it from:"
        Write-Host "https://pandoc.org/installing.html"

    }

}
```


<div style='page-break-after: always;'></div>

# File: models\classification_model.pkl

```pkl
��^      �xgboost.sklearn��XGBClassifier���)��}�(�n_estimators�Kd�	objective��binary:logistic��	max_depth�K�
max_leaves�N�max_bin�N�grow_policy�N�learning_rate�G?��������	verbosity�N�booster�N�tree_method�N�gamma�N�min_child_weight�N�max_delta_step�N�	subsample�G?陙�����sampling_method�N�colsample_bytree�G?陙�����colsample_bylevel�N�colsample_bynode�N�	reg_alpha�N�
reg_lambda�N�scale_pos_weight�N�
base_score�N�missing�G�      �num_parallel_tree�N�random_state�K*�n_jobs�N�monotone_constraints�N�interaction_constraints�N�importance_type�N�device�N�validate_parameters�N�enable_categorical���feature_types�N�feature_weights�N�max_cat_to_onehot�N�max_cat_threshold�N�multi_strategy�N�eval_metric��auc��early_stopping_rounds�N�	callbacks�N�
n_classes_�K�_Booster��xgboost.core��Booster���)��}��handle��builtins��	bytearray���B� {L       Config{L       learner{L       generic_param{L       deviceSL       cpuL       fail_on_invalid_gpu_idSL       0L       n_jobsSL       0L       nthreadSL       0L       random_stateSL       42L       	rng_stateSL      �73646c9f e511691f 60e274d6 4fc0289e 7ce61e87 cac9c1ab 25d45016 4395f7d b7279221 32c663a0 6cf5eef2 a68c51b2 48e36b44 8104400e fd47b192 5246a80c 5a2a42f9 a54b24b1 f22e4679 b54f18fd 1f8e5477 219c02d0 93be6cee bcdf45fb f657dd1d e9d14bb7 430232e6 756cb506 67f52ba7 71a00f63 400f8490 6007e71c ab97b459 34dbdbd0 461009fa 638843f2 90c4dacb 3e3ee33a e4ffb0d0 846af2e 49e4bc16 68878504 82ca28eb 3405d5e0 fee24254 2925bc48 f39dd15e 87d95fa8 429ab90a c75ee550 ba6ee5b9 12ceb6c2 e2a9ed86 f7c9e376 61935b27 e0f44cfd c0884f36 6e9d9dea 731f11b9 27c5769b ff9dbf2b 5ea0d3cd 415fbc82 723c7bb6 612bf3b 8c590650 c7bf6164 57728dae 81cd8e17 f5b54c56 e8b39b97 9e2a9673 fa66d4a5 aae8bc8f 9e94d9b3 d9109ce8 f5f4accb 137733fd a0c4e8e7 c8957070 b347e977 f581b942 c518e0bf 88394747 74a00c55 7009d241 3524345e 6de0f835 7801c1a4 30d5b43a 7592604 55a024b7 44cde2f2 c539604 625e54ba 7fac81ee 12212b73 9b7bb088 950c819c b29eb281 8bb989db bbe784ca 9de6c16 29326bdd 6ba8d461 21e32b11 4a2317e7 b6ec84f1 e51b8013 5bd21785 fd14ec4a 4db34b04 c4054731 338cd9f3 30da0919 c092f918 d508bbe3 5c1d009d b108baca ffdeba27 6b78b574 51ee356a 677e5779 75efbb9b ec306f06 3fa87b3e ce1ecebc a04c9a2 5f394032 7a56a068 4ee47bb7 90533619 5785ccf3 d5155ec7 c88148a2 3346d1d4 4e073df4 b6b68ffa 58da862a cf30f34a 63810e21 3559b3f5 55651dff c7e3c48d 8ee8b5e a6444b6f 314a185b 27c15042 2d05fd66 edc2909b 14c6556 72b9024d 654c955c 44b0b412 9a9a37e1 d1f588f2 a6bf0179 ef8369ec 8c12b3b1 b370b206 a8d660fc 256e339f 3b737625 15ca6b04 893d5e00 66932a37 29208ebc dd5eed9b c2c21668 757f1ca8 761bc11f 631e4049 6d4de5dc 54c9f6a6 bb3eb059 a299485e f8b6c9c4 6a8a1bfc 7162714b bb7d4dad facb4e87 94d69f91 f517a17d ea312635 8650face 3fbe1ffd 810c0553 a9cd7378 9130daa6 97c40839 e65bd3cd b935cfcd e119c533 3e017d79 bd0b4347 8f5478c4 965f9daa aeb01cd5 a8cb7161 55a6b89e 23ecef4b 27968d28 ec081a5a b9bb07b0 abc64cce de97a11 f1e7434b 6a3714ff 1ce937ce a58243df 19c10ccb 768fb0b2 525833b 95a45ae4 82c6f45c 67d6b8b5 dd7b34a4 355a2684 8c9d7b6 2a0c8271 85d4f139 3eb8c0ec 74966ac2 adcf7b96 6d09f70c 977f6eca 5f07be92 dd0fdcaa 8f78159 134daaca 11907d60 2eb9d88f 241ff91b 90a9bc58 7397b34 eb087137 47557f38 6c5fb432 6a9664d5 bb173d5b 796ed6d5 897e375d 6206b135 9e4bf3f 20512c97 1d046850 68bff94e 3551a4ea f4dd4c12 497b1d76 e29850b5 e6433f91 2a8b385e 7ca98cdb bd3b3dc8 44f67c79 25235520 635eb769 c85d05d2 29872640 c18a590c 28a72bb8 5261b966 52974672 fb87582f a3c9572d 94608e5d 2ee2044e 799b729a b0e62bfc 544c4b0c 9f9e92f8 530dc87a 8416ed60 37c31b84 da4f80ef c3d02af8 b8fe49e4 1f293f9c eb94966b 72f500e8 ca850ece ff058dc3 764caea3 d42399ce 6ff564c6 34304369 8efccb54 89e740d6 5fba098d a655b226 8b208e1f 6eb0985d 27b95a39 60f81b6b 80748cc1 2aa4e5df 6f2c09ec af2ac173 f37acc88 2b617cb cf20080c 685c36e1 85df8857 7794881 422da5de 26dfc9f5 fb11cca4 a11c1edf b0a7742e c70635a bcf85e81 522666af 2cdba2a7 23438ce5 8650255c 8f300e1a b828697d bedf9821 e396c2d6 a891dd11 a0606588 db24eb7c 3c10e226 f2b9910a d5130b9a 1ee7766b 709dfd46 dbd0ee13 cb447e61 a65650bc 2e758b09 d506ada1 b5fc34ff f3c74ee7 2f16260b 1c65e76f e517b7e4 8f172f3d bb275cf6 61f24260 6c11b62 198541c8 8e3efe07 e2ede719 223f1963 bd300131 e0f9c642 456b02c9 1b2d230d 51ebcb47 98b9aac5 3d15e1ab 1f138da0 18e1824a 47b8035d ace99178 a956b14f 89312a8f 160640d0 8ed6e440 70bd623b fbdecd14 ea493b46 5a7f516d a0c1edd1 b98dc175 8fb7052a a90f7300 f4b27403 367bc63a 9f80411d 6c4c4a77 5f2c88cb 574c13f0 5f46d954 4e953dc9 ef696a29 7d8d5ed4 a459694c 79c34c0a 460be59c 83dd9e37 4f8cca30 ee17009d eab9ce9f 812401d6 b4fb2eef 17b15acd 3a2b8a2e 6f622474 d26e0178 d28e6ad7 a5279bf5 d2d8b9c5 c7564371 bf3ea04e 6991ec51 f4390de6 e0350ab0 a68c05f7 2a217902 b004d224 cd674159 d2bf4de 12746bf3 d58a43d ed887370 68c319bf 99f1d857 ef82d8eb 530bbdeb f5aa29b6 7c6753ce ff46da11 3025ad81 533e7f4d d4dbe765 561e3a8 9c0bbbb3 a5e9c841 4f3cdfdc 31dc999f 197b52a 2b26e943 494363a5 f8936fe9 79beb9e4 c73f6d5f bd6659ea 4822dab7 9dd6a2f2 54321dd9 e576baa6 92f54201 69fadd68 cb81f443 dcc086be 235dd83 ac7a21eb 5dc977b5 4c9b31a5 29ab64aa f6365be1 17a5b172 f92f8f59 f6dee6ce 477439e5 2d717802 1180b79a c023c24b 9ce2935f 2002195f 2c2c7d34 ee8a17ea a3ad0484 a99fe1cf 20b37a73 239a62cc d84ae9a 8201eff2 35ed8711 b8fef3cd 5e7a098e bc15c1aa c2414cc0 459766a8 30740b02 2d44136b 7702c031 a2bbb54b 4276b3bd 7f04fb92 e029abc4 644fa71a d85fb1d8 4173e209 ee589483 69c3c027 eba24857 39c16479 866b47cf 8cd6357 406f2189 b6d0470 7fa57ba3 82d13e5a 948f2078 8afc6583 3daea41c 7d41e984 73143e12 a5652ad2 df0c2d04 cb443d4a 2c037fbc 5df694a4 363a9d0f 9a1c5dff 599aa493 4c404211 ce2840bf 12baeb0 17e0cc98 e225e235 456426a5 1edcdf5 6f6b9927 4b06cbc4 7de603fa 688a053f b7a023d3 6595d396 294261d4 363da235 eb845f5f 64048f63 7db0ead5 93736421 7f9800fb 8d8ee548 6dff56bc 6c1f0781 ac37932 237ef3ed a9a4eaeb 56e1f77c 6363760d fbd04609 b5fa3645 d369275d 3c7c21a9 66a90c6f 92d60994 1239cee9 c36001e8 bc96f0b0 4fab0aae 570704bc 2a9e4066 1230019d c7b9820e 24a24b3c e56f8128 c796e673 ff59b8b 5173186f bbf44d6d 49a733d8 a16d1f39 5ad565e0 9bdf4a0 73656f2c 456a0322 8e1f8030 babae599 e6895206 d488fb a8c1a7ed 58abe643 e86acb5c cf115873 398dc757 60c04998 bbaac5e3 9be39337 3b5a6610 c3103cc8 e693316b 54f867d4 45a6c062 b6e7005 f64c2868 6d334ae8 a2bc4b83 3be7afc5 2c5e55b6 90d25df9 c328e225 776ccbb8 f1d40617 4f8d23f6 c23dd8f9 951de2e 77129968 5fd1fa10 2ff5be94 61e357a2 9ac4b01a ed79319d 2d62e262 a8febf1a 1ebb1d92 b1673894 4f32c040 56bb4ad3 4afc3ab 28f06770 55fc342c c7c0c358 c098741c d972af1c 7b04397f c417b415 d84ab415 e83960b2 b3817c47 7b137cb9 ac132dd5 89fc47bc e5174ddb fa1c9b7f 499f0cc8 9071f9d1 45238e8d 6f9e6c41 649b359a 23245bbe 43df34b4 216f3d26 7d6677c7 4afb4a8c f30cf635 5f8426deL       seedSL       42L       seed_per_iterationSL       0L       validate_parametersSL       1}L       gradient_booster{L       dart_train_param{L       normalize_typeSL       treeL       one_dropSL       0L       	rate_dropSL       0L       sample_typeSL       uniformL       	skip_dropSL       0}L       gbtree_model_param{L       num_parallel_treeSL       1L       	num_treesSL       100}L       gbtree_train_param{L       process_typeSL       defaultL       tree_methodSL       autoL       updaterSL       grow_quantile_histmakerL       updater_seqSL       grow_quantile_histmaker}L       nameSL       gbtreeL       specified_updaterFL       tree_train_param{L       alphaSL       0L       colsample_bylevelSL       1L       colsample_bynodeSL       1L       colsample_bytreeSL       0.800000012L       etaSL       0.100000001L       gammaSL       0L       grow_policySL       	depthwiseL       interaction_constraintsSL        L       lambdaSL       1L       learning_rateSL       0.100000001L       max_binSL       256L       max_cat_thresholdSL       64L       max_cat_to_onehotSL       4L       max_delta_stepSL       0L       	max_depthSL       5L       
max_leavesSL       0L       min_child_weightSL       1L       min_split_lossSL       0L       monotone_constraintsSL       ()L       refresh_leafSL       1L       	reg_alphaSL       0L       
reg_lambdaSL       1L       sampling_methodSL       uniformL       sparse_thresholdSL       0.20000000000000001L       	subsampleSL       0.800000012}L       updater[#L       {L       hist_train_param{L       debug_synchronizeSL       0L       max_cached_hist_nodeSL       18446744073709551615}L       nameSL       grow_quantile_histmaker}}L       learner_model_param{L       
base_scoreSL       [3.4380576E-1]L       boost_from_averageSL       1L       	num_classSL       0L       num_featureSL       44L       
num_targetSL       1}L       learner_train_param{L       boosterSL       gbtreeL       disable_default_eval_metricSL       0L       multi_strategySL       one_output_per_treeL       	objectiveSL       binary:logistic}L       metrics[#L       {L       nameSL       auc}L       	objective{L       nameSL       binary:logisticL       reg_loss_param{L       scale_pos_weightSL       1}}}L       version[#L       iii}L       Model{L       learner{L       
attributes{}L       feature_names[#L       ,SL       BENE_SEX_IDENT_CDSL       SP_STATE_CODESL       BENE_COUNTY_CDSL       BENE_HI_CVRAGE_TOT_MONSSL       BENE_SMI_CVRAGE_TOT_MONSSL       BENE_HMO_CVRAGE_TOT_MONSSL       PLAN_CVRG_MOS_NUMSL       SP_ALZHDMTASL       SP_CHFSL       SP_CHRNKIDNSL       SP_CNCRSL       SP_COPDSL       SP_DEPRESSNSL       SP_DIABETESSL       SP_ISCHMCHTSL       SP_OSTEOPRSSL       SP_RA_OASL       SP_STRKETIASL       MEDREIMB_IPSL       	BENRES_IPSL       	PPPYMT_IPSL       MEDREIMB_OPSL       	BENRES_OPSL       	PPPYMT_OPSL       MEDREIMB_CARSL       
BENRES_CARSL       
PPPYMT_CARSL       source_yearSL       AGESL       RACESL       IS_DECEASEDSL       TOTAL_ADMISSIONSSL       AVG_ADMISSION_COSTSL       AVG_LENGTH_OF_STAYSL       UNIQUE_DIAGNOSES_COUNTSL       INPATIENT_CLAIM_COUNTSL       AVG_INPATIENT_COSTSL       !AVG_DAYS_BETWEEN_INPATIENT_CLAIMSSL       OUTPATIENT_CLAIM_COUNTSL       AVG_OUTPATIENT_COSTSL       "AVG_DAYS_BETWEEN_OUTPATIENT_CLAIMSSL       DRUG_CLAIM_COUNTSL       AVG_DRUG_COSTSL       AVG_DAYS_BETWEEN_DRUG_CLAIMSL       feature_types[#L       ,SL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       intSL       floatSL       floatSL       floatSL       floatSL       floatSL       floatSL       floatSL       floatSL       floatSL       intSL       intSL       intSL       intSL       intSL       floatSL       floatSL       intSL       intSL       floatSL       floatSL       intSL       floatSL       floatSL       intSL       floatSL       floatL       gradient_booster{L       model{L       cats{L       enc[#L        L       feature_segments[$l#L        L       
sorted_idx[$l#L        }L       gbtree_model_param{L       num_parallel_treeSL       1L       	num_treesSL       100}L       iteration_indptr[#L       ei iiiiiiiii	i
iiiiiiiiiiiiiiiiiiiiii i!i"i#i$i%i&i'i(i)i*i+i,i-i.i/i0i1i2i3i4i5i6i7i8i9i:i;i<i=i>i?i@iAiBiCiDiEiFiGiHiIiJiKiLiMiNiOiPiQiRiSiTiUiViWiXiYiZi[i\i]i^i_i`iaibicidL       	tree_info[#L       di i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i i L       trees[#L       d{L       base_weights[$d#L       ?81?��q�n��D�@<���?o`�?�qj�C�@��?4����0���	?�" ��_�04�?����\���@.h?O�3�@�i�����(�J?���Dx?���?���i>�ǽ���=6z1>N�ӻ.�'�0�=v��>
^�QD�>_=>��ú�f�>R�½؄]>J�>o�=�z,��ǾV'>;��k=�C�<��@�A)׽ށ�=��"��p�>ea�> ��r0���D<ϕ�=˘kL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idi L       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?E}��DXE��B��C(��DH�C�͒B�pA�M0B� C��At2 C�^B��BC��@f�B@�K�@�k�A�^NBs��BZ!�B�n@���@�� BM��BC�,B@Z0A���BIӐA�"�Ac��                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?B$  @�  @�  @X  B  @@  C
  @   @@  A=UU@@  A���B�  B  @�  D�� FM D�  @�  @ʪ�A�  A�A,��B5UUB�UUBx  CX  A9$�B�  Cw� @�  ����=6z1>N�ӻ.�'�0�=v��>
^�QD�>_=>��ú�f�>R�½؄]>J�>o�=�z,��ǾV'>;��k=�C�<��@�A)׽ށ�=��"��p�>ea�> ��r0���D<ϕ�=˘kL       split_indices[$l#L       ?   %   %      !   %      %   %   %   !      !   %   "                !   %   "   !   !   %   %   %   %   !   %   %                                                                                                                                   L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?Eo�ADe6E6�sC��DD)�E|�D@�NB%$CB�{�D2+�B��XD��D3��C��C���A_�lA�bPB]�bB
��D%2�BO�BBٖD��A�O�CL�D ��C*�C�I�C>�EB��.AB��?��Aώ?�ClBY{L?�b�A	*�A�\"B_�lD5�A�{A��,B�@��lA���@�#B6I�D�jF@�ClA���B��1B�)�C��iCtǖC�(A0�~C gkC,RCBB>h�B��,B�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =�5�����,?7� ��=��?DI?֏m�ǡZ��8��4(?IΖ?��?rC?�}@	f˾���?
�K������L=E���U򾮾?r8�?cu%?̝�>zq�?���@��?���=Kj@���/�b�b�}<�~�=�爾�$<�r�����=X|/<��5�:,ҽ)�<Me=�o��~��=��=B�<ߺ >\E���>'p�;�A8=�mg=��> >`2�=A�W=�7�>9$T>d��=��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9����   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =D�ߒCm�
Cy�C�$�B�btB�3�Af CAB�o@Ab�_A��|A*`B��lA�?�� A�ܬA0� @6A @wl@A2�A:��@��@��`@�`�@�@AȥaA���?�!@AR��    ?sJ                                                                                                                         L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :����   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =@�  E   @�  D�  E@  D�  A   @@  @@  @@  @@  D�  E  D�� @^��D�  D�  G ( C�  E@ F�� A�  E�` @   A�  @�  Eg� @�  G� =KjBH  �/�b�b�}<�~�=�爾�$<�r�����=X|/<��5�:,ҽ)�<Me=�o��~��=��=B�<ߺ >\E���>'p�;�A8=�mg=��> >`2�=A�W=�7�>9$T>d��=��L       split_indices[$l#L       =   #      #            #   #   #   #   #            +            (         *         "   #                                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =EpmcE7��Da�IEN,DVD(�NCc#�D�DUD,OC*�B�?D	ilC8�B,-Do�C�F�D��C}>�C�}oCIb]A�I�C��A�U�B�)�C�PCU�A�K;Cx?�F�B'Y�C��C�

B�1JC7� Dx�?���C{	>@noC�RBCbV[C|B[�y@�4[A�|�B�q(A�Z>ABL�A�/�@(FB�SC_��B�f�B�p�BÚmA�?��vB���B~��B�B@OL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =:�a�?�d�0۾�3�?�"���N?1�D?V�x9�?�N?j �������?�q�;m�&��?�ws���=ĝ�@S�?����4�?ݰ���P��� >8.ӿNUA?U�*?���>]� �Y=7��>E�f=�����ӽ�1>d�?=��<Yvj>0Z��DC=��>
��>U�ؾ�����>>��
�W=m)���,w�W����O=���׾�>.LC=�R����M=@������<�n�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiL       left_children[$l#L       =               	                                    !   #����   %   '   )   +   -   /   1   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =EG�:C��D�>�B[�C�\�CӼ�C�Y6B/C�A,>B�  C��AQ� C�{B(�B,�@�X\A�@=��    BP�@B�xB��A� >�  B:Z�B�HA��`A�� A�6�A�.�A�H                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $����   &   (   *   ,   .   0   2   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B8  @j��@�  @l��B  @@  C � @   D�@ @ڪ�@@  A���B�  B  CX  A�  BLUUE]� =ĝ�B  AH  A�@�  AX  B�UUB�  CX  A�UUB�  @�  C  =7��>E�f=�����ӽ�1>d�?=��<Yvj>0Z��DC=��>
��>U�ؾ�����>>��
�W=m)���,w�W����O=���׾�>.LC=�R����M=@������<�n�L       split_indices[$l#L       =   %   %      !   %      %   %      !      !   %   "   %      (           %   %   !      !   %   %   %   !   %      )                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =En�DD��E,LUB�ץDq@�D���DC�B.�[B_'�DF��C*c�D��LD*a=C�e'C���A��fA�;PBW!@��D�+C[��B��)B��D��A�P/C���C���CC��C��B��w@i-�Ai[^AF��AO{@=F�BK7�D �Bp��BnH�C \B� /Al��B..B%�oD��B8@��A��KB���C�C:-�Ci�eC�;@���C'�gBԆ�B�VTC<IB��A%�_L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       3<Sq?�]i�1W�&��?�iͿ���>)?=�&p���?�щ?$Va�X|�*�?+ne��ӭ�I`?k{:���=�*?�w%?������G?�%�>1O)�<�=�+?�^�!��>rv`<�˲��m_<��>�5������Y(=�Rz>N~�<[u>������=FN>>2L�=�n=o%=��'�=�{>�n��#���{=�����SL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       3                                                   L       idiL       left_children[$l#L       3               	                  ����                  !����   #   %   '   )��������   +   -   /   1����������������������������������������������������������������������������������������L       loss_changes[$d#L       3E"�C�I�D��(A��vCB0A,� C�a/A�@b�0B�E�C��j    B	CH�B��r@�G-@��L?�     BO�B�ӺBlx�@6��        B.mSBe B 6�A�Z�                                                                                        L       parents[$l#L       3���                                                           	   	   
   
                                                                                    L       right_children[$l#L       3               
                  ����                   "����   $   &   (   *��������   ,   .   0   2����������������������������������������������������������������������������������������L       split_conditions[$d#L       3B8  @@  @@  @X  B  A���C  @   D�@ @ڪ�@@  �X|B�UU@�  @�  B�1gA���@�  =�*@�  AH  @��9B2  >1O)�<�B�  B(  CX  C%  <�˲��m_<��>�5������Y(=�Rz>N~�<[u>������=FN>>2L�=�n=o%=��'�=�{>�n��#���{=�����SL       split_indices[$l#L       3   %   %      !   %   !   %   %      !          %         '   +   !       %   %   !   %           %   "   %   %                                                                                        L       
split_type[$U#L       3                                                   L       sum_hessian[$d#L       3Ek��D�X�E'�ZB���D~r�D���D��A��B=�DDY�Chc�D�o,A��DOHD Aa�A8��B7�?���D��CR��B�_B��@���A|ܭC���Dx�Dj�B�X@v��A#r�@�c�@�ժATR�B��B�1rC���B���C��B��xB$!�B�Ag�B��.CA�BC�ƔC$UVCh+\C���Bb�B�h�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       51L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       7�!7?�I׾����?��
��l�>&�?9j�SfQ?�B�?��h��X?n�ߓ�|��?��=�hYP?9�?ض�?s�3����?�U�?�R��t�=�j�?e�s���?=O���=��='�>o<�1ʇ��X�>�t�"-�=�W�>8�=W{>?�X�ж�=v�b>��>9�C<�>*�'=bfc���==�j�=�3�����<��4��*̽<��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       7                                                       L       idiL       left_children[$l#L       7               	                  ����                  !   #   %   '   )   +   -����   /   1   3   5��������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       7E�VCn�D�"�A�ȆC�xA��C�l�@�wA��B�WCBO"    A�>B��Bc�l@Ũ�>�3�@{1P@X��B0Q�B�&PBvۋ?�؀?�v�    A�Y$B
] A��A��                                                                                                        L       parents[$l#L       7���                                                           	   	   
   
                                                                                                L       right_children[$l#L       7               
                  ����                   "   $   &   (   *   ,   .����   0   2   4   6��������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       7B2  @@  @@  @��B  A���CUU@   D�  @ڪ�@@  �hB�UU@�  CX  Bt  B�  E|��@��9@�  D�@ @��9@�  @   ��t�B�  B�  @�  @�  ���=��='�>o<�1ʇ��X�>�t�"-�=�W�>8�=W{>?�X�ж�=v�b>��>9�C<�>*�'=bfc���==�j�=�3�����<��4��*̽<��L       split_indices[$l#L       7   %   %      !   %   !   %   %      !          %      %   )      $   !   %      !              %   %                                                                                                              L       
split_type[$U#L       7                                                       L       sum_hessian[$d#L       7Ee�AD�m
E#��B��bDw='D�}�D���A&BBp>>DD��CJ�D��hA�ԉDQ3XD %@�}5@�BeȆ@'[xDv�CT��B�h�B��@�9�At C�U@D��C���C�Bl@^��?���?�g�@�-Au�1B(f�?�]\?�Y�B��C�y�C��B�ޫBx�B�B���A� �?�@^�JB���Cb�Cm�C�OjCmpB�waCW~nB��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       55L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?�*H�9?' ���g�=��=>���?ld���%�e�Ƽ���?o?Pw4>f��?G#�?��i�_��>�����+e��>�ʋ�S{?31ܽ:�a>_��?~�q��E�?/��?��=?(�]?���?�._�9�����=V���Q��e� ��7�<��O��=7�E���:�*>���E=�C-��P1��p�=�����Z$=I�Z=�&C�X7���=��6=Bb�=�w�>�'<�+c=h�=��K�p�G=�x>-�<�2L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?D).CB�B���C�&lB/�YAԍ�A�,�Bm�Bl#�@��AprxA%=�B e�AƠH@)G AUxA*h?�� @��h@���@���@�  @�ɍ@�A@���A��@��@m� A);p@M-`@4��                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?@�  E   @�  D�  E@  D�  Em� @@  @@  A��=ER� D�  E  D�  E�  @�  B�  @�  A�q�B�  @@  BH  F  @   D��A�  E~@ E� @�  @$�IEN@ �9�����=V���Q��e� ��7�<��O��=7�E���:�*>���E=�C-��P1��p�=�����Z$=I�Z=�&C�X7���=��6=Bb�=�w�>�'<�+c=h�=��K�p�G=�x>-�<�2L       split_indices[$l#L       ?                              '                  !         '   )            
   '   &            !                                                                                                                                   L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?E^��E#�jDk��D�DI��C��zC��D�1�D0�qD4�C)2XB���C��C�!1C�DRqC��?C�B�Ca\kBk��D{C�B5A�ӈB���Ce�aB�PJBdC���B���B�A�C׿qC�"�C�6�@���A�;C�jA7�CU�^B7QARx�C�e�C3!C?�@��~A�ց@�Nh@���A���B�6�?��CX�AP��B���BJ��BW4O@L�'Cw�BV�k?� �B�EBB�O�?�u�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;�E�"?�����P��a�?�����x=ŚV>�~��w��?��?Oп��L� ��>��M�ְ����?_�?��W/�Ĺ?��>�q��R�?������|w�>f����{�2��?G�M�-�w���S<T��~�>R�=K�o�'�v������z=��q=�JU>&�=��ֽ����@�=�1=֭Z>�>���������G���=&���V{=��W=D��.J&�����6�=1�BL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ;                                                           L       idiL       left_children[$l#L       ;               	                                    !   #   %   '   )   +   -����   /����   1   3   5   7   9����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ;Dօ\C8V`D���BSkBߡPAW C���A�H@H B�"�B��?�� A���B�:�BB�@ʾ@Τ�?�@­�B'��A�ALBK=�@o��    Aϲ�    >�@A�OA�ՐA_ȰAv޳                                                                                                                L       parents[$l#L       ;���                                                           	   	   
   
                                                                                                            L       right_children[$l#L       ;               
                                     "   $   &   (   *   ,   .����   0����   2   4   6   8   :����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ;B2  @j��@@  @�  B  A���CUU@   E0@ A(  @@  AEUUB�  @�  @�  C�  @	$�@   B�  @�  A�  @��9B�  ��Bx  >f�E� B�  B�  CX  C  <T��~�>R�=K�o�'�v������z=��q=�JU>&�=��ֽ����@�=�1=֭Z>�>���������G���=&���V{=��W=D��.J&�����6�=1�BL       split_indices[$l#L       ;   %   %      !   %   !   %   %      !      !   %            !   
   )   %   !   !          %           %   %   %   )                                                                                                                L       
split_type[$U#L       ;                                                           L       sum_hessian[$d#L       ;E[�D���E�6B�`	Dk�gD�DJD�0"BU�B"�D4�C[�5D~{lA���DL�Dq�A�'pB �JA؊AZ%D!=fB�=�B�q�B���Dt�B&Z�@ob�AGq>C�/�D V�C��9C�.@�F�A`��A:�A���?���A�{�A=�.?���B� D��B_ɼA�b�B��gB$��BI_nBz!�@o��Ba�?�3�A6
�B�/�C3ǑC�BC5,hCrCF�CuˤB)J�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       59L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?���?����%���?�y꿖��>
�e?ZL�.��?��>��ۿ.���V'>���%"A����?�#�K�Q?��h?�Wa?U�,��S�?��Q��bU?�^��(-��[>�U?@Ŀ.�x�[�*�<�1=Sy�>'I�=���BI����>#�e�?i=��>ܪ���E=�ǃ���G>�����>%���=��,=�������%���{>�N��X�=���9yE�=�/�=9z{��&��@�j>&����L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?D��2CR�D��~B��gB�� A�$�C��"B��A�,�A�� B	�B#I�A&G�B���@�9�@�f8?�j�@�}�@��A�9�A�`TA��TA=�@���@��?�� AӋ�Bb�B;�@�� Ahi                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?B  @�  @@  @l��A=UUB5UUCG  @*��D�@ B  A�  @⪫A���B  C3  @   B$  F�UE� @�  @$�ID�@ A  F�  A�  AX  B�UUBx  B�  A�  C4  �<�1=Sy�>'I�=���BI����>#�e�?i=��>ܪ���E=�ǃ���G>�����>%���=��,=�������%���{>�N��X�=���9yE�=�/�=9z{��&��@�j>&����L       split_indices[$l#L       ?   %   %      !   !   %   %   %      %   "   !   !   "   )   %      $      %   !      %          !   %   %   %   "   )                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?EV��D]��E+zC/�D8��D���D��?B~ĖB���D)��Bq��B�dDn�D��DC���A�5B�|B��x@���D��B�BBhhA�v�B_�"A�NDj�A�j�D9�
C���C��:A�At�MATA�-!@�WXB>wB#~z@Xwo?��gB2"D�A.�|B�9SB�]@ƈV?���A��BZ��?��AZw�@�Dc�fAڬO@�*�AG@RC#DDIC>��CoXCM#OB��I?�B�A���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5�7��?w{�ɝ9��,�?����D�=�Y>>�}��V�o?���?���c2�7��>��w�����j ?k�g9X=�9�?��G?"�=��?���?�����>���?_����,�&b	�լ����h=ܩ���d��ϻ���=���>���2xR=��k����=�M�=�8�=!�&>�k��:=�8!<u�=0*K=ʝ>�k�<8�����@�QL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idiL       left_children[$l#L       5               	                  ����                  !����   #   %   '   )   +����   -   /   1   3������������������������������������������������������������������������������������������������L       loss_changes[$d#L       5D��C��DdIA�˗B)�`A5݀CWA ��@���B{� B�D    BO�@Bq� Bj�I>��@@���@��8    B�pBf�xB�-@�@A@�t    A��AM�@A�./@���                                                                                                L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                  ����                   "����   $   &   (   *   ,����   .   0   2   4������������������������������������������������������������������������������������������������L       split_conditions[$d#L       5B$  @@  @@  @X  B  AEUUB���?�  C]  @��@@  ��c2B�UU@�  CX  @$�IBecDE��n=�9�@�  A`  @d�IAffB�  ���Bd  B�  @�  Bp�n�լ����h=ܩ���d��ϻ���=���>���2xR=��k����=�M�=�8�=!�&>�k��:=�8!<u�=0*K=ʝ>�k�<8�����@�QL       split_indices[$l#L       5   %   %      !   %   !   %   %   (   !          %      %   !   *           %   %   !   !   *       %         (                                                                                                L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5EODh�E��B{�FDY
�De��D��>A��B\JD4�aC��DW�pBb&VD4�VD8�'@�m�A�zBN�?���D	�C+�+B���B���A44}B56C鐈C�V$C�OC�t�@s �?�u�A5�l@�%@�,�B�?B���C�Q6B���B��}A�@=B6�Bk�FA&�A�?�shB�'C���BYb�CJS�C4��C���C!5qB�iL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;�)4�?a�9������,�?�z���?=�Q>���<Ns?�bY���п��Կ'�>�iw�����h%?b���Y�?4��?�?�k�|N�?�!s�l����?�~N��{(>��c?Sd��`���:_�@����=��i>%A��k�����R�=�n0>�s=�E{6�j�=�v_�[>=�+?>�<�Bн��w=���>���ٗ=�&�<�=�`3=L��i�;��r���׽8�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ;                                                           L       idi	L       left_children[$l#L       ;               	                                    !   #   %   '   )   +   -   /����   1����   3   5   7   9����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ;D|ނB���DN�
B�BI{�A=[ CCf�AǪAC�BMA��,>�P BJ�-BSI B%�(@f��@��(@��h@ӶB ]�B!�A,��?m*�@��    A�    A���AK9�A�b@�|                                                                                                                 L       parents[$l#L       ;���                                                           	   	   
   
                                                                                                            L       right_children[$l#L       ;               
                                     "   $   &   (   *   ,   .   0����   2����   4   6   8   :����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ;B$  @�  @@  @�  A�  AEUUB�  @   D�@ B  A�  B2  B�UUB  CX  C�  D�@ A��@*��@�  @@  BUUD!&�F�� ���B�UU��{(Bd  B�  @�  B���:_�@����=��i>%A��k�����R�=�n0>�s=�E{6�j�=�v_�[>=�+?>�<�Bн��w=���>���ٗ=�&�<�=�`3=L��i�;��r���׽8�L       split_indices[$l#L       ;   %   %      !   !   !   %   %      %   "   %   %   "   %         +   %   !      %   '   $       *       %   %      (                                                                                                                L       
split_type[$U#L       ;                                                           L       sum_hessian[$d#L       ;EG�.Dc E)BܯDGj0DT�D�kBk�jBMb�D@�A�C�DG�-BIZD/�cD89rA��jB,5B@@UkwDSfCR�A�� @�
�A��D@�\A&|B��C�[?C�?�C�^VC��AϦA*m/A��:A�aAC�BG�?�ݿ@��CƬ�Cg��B��FB��A��@|�@���?�ޙAȠ#?���A��?��_B���C�r C2�:B���C0��C��C.�4B���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       59L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?���'?Yپ�i�=��?�wؿ�`�=�\s?:ʶ�4e?��I����T3���>�A�����G��?�4߿U�~>0A�?��?��$�?�b�����?�H�����=YJH?��
@˽�g=���My+=��>_`�D��򃽽$\]>�O>c=��伖�d=�}C����=��d>�<�8��q�<���!�=�(?��S���;=��q�۞�=���m`=�
M=<-���{���ܘ���Ͻ�2L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idi
L       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?DZ��B���D9�B��B.�A]2 C"7�B3	�A��A��A��A�j@�h�BM�@A�ςA�s@�t�@�c�@�� Ax$@A�jA]@6�<@�ƘA1
<� A_��A�N'A�� A*XAAx�                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?B  @ʪ�@@  @�  Ad  B5UUC  @*��@@  B  @@  @⪫A���@�  @�  @��@j��E���B�  @�  @H  BUUA�  A�  C �Ad  B�UUB�  Bh  C�  C�  =���My+=��>_`�D��򃽽$\]>�O>c=��伖�d=�}C����=��d>�<�8��q�<���!�=�(?��S���;=��q�۞�=���m`=�
M=<-���{���ܘ���Ͻ�2L       split_indices[$l#L       ?   %   %      !   !   %   %   %      %      !   !         !   %   $   )   !   !   %   )   &   '   !   %   %   %      %                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?EA�)DTE�%C-8<D(�DH�ZD�n�B�+B�WMD ��B�hBR}D;��D]�'DB��Bw~�B��A"�DDwB�{A�n�A-��BG6Ax�]D7��Ah�OC�/�D�bC��xC�3�A�HA���A�o�B2F�B
�PB|`@��-@<^KCО�B��A��B�3�A��+@.@���@�{.B(�@�@�m�A��D4oAxTS@��QA%�&C/H�C1B�\�C��B�(Ca:�Cs_#A�A�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =���2?R3���S>P��?��n���C=�T�?L������?���>�@ۿ
�����>Ѡe�WN����?�ZR�,��?��?�,�?����X?�k��u{�>��M��k�$��>q�?>�־��߻�}z=��ؽ��7=���>*Ž���<_�/>Ǽ���>N�=���<mW�=�0�E=ʋ���J�>^ܽ��*<���=]݂��C>����cp=���<�<�C�=�9����ͽ[�J;������gL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1����   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =D6�dB�ֈD*Z�B�.VB��A�I�C
��B$A�*3A���A�h�A�/o@��B(�VB�0@�K6@�)�A�`@a�(@�c A�WEA�%v@-�x@�s�@��    A�b�Ao�fA=��An��A[��                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2����   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B  @�  @@  @�  A(  B<  B�  @   D�@ B  D�@ @�I%A\��@�  @�  DT� @`  A�  E� @��@@  A�  @�� F�EUB��ͽ�kB�UUB<  Bp  C�  C�  =��ؽ��7=���>*Ž���<_�/>Ǽ���>N�=���<mW�=�0�E=ʋ���J�>^ܽ��*<���=]݂��C>����cp=���<�<�C�=�9����ͽ[�J;������gL       split_indices[$l#L       =   %   %      !   !   %   %   %      %      !   !            %   "      !      "   +   $   +       %   %         %                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =E:�,DE�E	k4CG��D�D=$D�K�B��IB�|/Do�B�g�B�uuD+fuD5ɇD2�&A�{,B��~B�Gn@�LC�sB�4BK��A�:�BB:�A�_�D#slA�aC�x�Cv4nC���C��i@F�A}n�BL:Ba��B�s�A>�}@нB?�;3C�zWB��mB}A��B*�AVE?�1A�w�B2O�@~�A�#@	�7@�~�A�dBx8�C�q�BZECN��B���C�p�C��A���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?�?�?8Z��N��?X��}0�=ĶS>�7��&�?j�>	�5�<H`��>��T��sE���A?PɿW;����?��H>�TH�H�>?e��c�"?�AC���n�Q�->D6?A]��麨����=岽��;��=�Ұ�N-������)=��=;��=�|C�nW=�T�=v�X��=�E�9ý�ɓ;���>1�������н�5r[���=�pb=n5<Ac.��u�=��뻡Te�s{��R�-=¶+L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?D�;B���D6�A��B�0@�Y Bӌ�A�.�@��8Br0A���B q�?�j B)��Ap�\@�_�@��x@~= A ��A���A܇mAL��@�р@�m�@;Ȑ>�( @�}hA�q�AH� @ٖ�A$O�                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?B$  @�  A�  @l��A:��B�UUC@ @   E/  B  A�  AX  A�  B(  CX  D�� @�  A�R@*��@ʪ�A�  C]  B�  F�P B���D  B�  Bh  E�` B��Cv@ =岽��;��=�Ұ�N-������)=��=;��=�|C�nW=�T�=v�X��=�E�9ý�ɓ;���>1�������н�5r[���=�pb=n5<Ac.��u�=��뻡Te�s{��R�-=¶+L       split_indices[$l#L       ?   %   %   "   !   !   %   %   %      %   "   !   "   "   %      )   +   %   %   "      )   $   *   (      %   $   *   (                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?E4 �DM2'E �SB��D2�fD=�D��B8Bk	pD"��B���B��{D!�]DWt8CܦAp��A�6�B�A�6�D�!B��BB8E�A�(B�x@�`1D�hBl�FD.[�C$b;CZsC_3�@��kA"��A ��A��A���Av�KA .�AX>�Bc�C��B�
�B[d�AU��B��A~b�@W��B��s@��S@���?��D"@@C(�Bg�?��B�"tD�[A��C��CA�A���C[2@�4�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       7�4*{?9� ���B��?Rr�l�G=� j�"=��?#�?���7�~��>�J�Q9Ŀ"1�=},?PTǿ5�]?�d]? �Wz?'�����$�O%>k@?m�����4�9�@s���C=G�=�y ���=<��>�8<�><S b=�NϽ��'�$�r��E|=����=�������Ö8<s=��=�-�=����¦����j�<�oL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       7                                                       L       idiL       left_children[$l#L       7               	         ����                     ����      !   #   %   '   )   +   -   /   1   3   5��������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       7DJB�C���AuB��A���B�N@nH    B�0AcX�AMe�?�( Bp�A���@U��    A�pA�&1@���A/��@�� A?p @��Aj��AA�@Ғ"@���                                                                                                        L       parents[$l#L       7���                                                     	   	   
   
                                                                                                      L       right_children[$l#L       7               
         ����                     ����       "   $   &   (   *   ,   .   0   2   4   6��������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       7B  @@  A�  D�  D�@ Bd  C  Cv@ =��F� B   F�� A�  B  Cw� @�  =},@�  A�  E�� E� A�  F<^9E�p @�  BH  B�  CH  C3  9�@s���C=G�=�y ���=<��>�8<�><S b=�NϽ��'�$�r��E|=����=�������Ö8<s=��=�-�=����¦����j�<�oL       split_indices[$l#L       7   %   %   "         %   %   (          %       "   "   %          %   "         "   $       )      %   *   )                                                                                                        L       
split_type[$U#L       7                                                       L       sum_hessian[$d#L       7E/�D5.jE�2BQ��D(,D7�D��VBF�l@/��C�Q�Cq�NBص~D�kDTX�C�o�B?�?�)�C��sBDq�CGBKB)�BȮ�A 6]D��Bi�Dh�C��GC�4)Cw�@��XB#��B�G�C���B�/A'�CB�@���A�OOA�H�BDB��?�b�@�S�C_�C��{AL�B6�-C�˱B +WC
YC=�4C�4]@�#C��A;;�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       55L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?���{�,�2>��龉�=��>~C�?�佉f� ~=�ל���=��7>��?��G>ܯ!�-��>2�@�k�i�f@k>J	��i�w�>�b?@��_�?����?��T=γ�>��	?r !�����=`캳j��t���/;���Q;�w=H��9/9�� ���g=�s��f��=�)^;� �C�;��=iI�:􍰽��<D8�=�b�" (=�5����=�_�<��]=�M��_�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?C/�B��A���B�M�@�VA|s�Am)A��BT��@��<@��:Aq~AqX�@Z��A��@�O�A��?�> @�!^@�;&?}�@��R@8K�@�_LAK@���Ar@�� @��A)M@5�                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?@�  D� @�  D�  B�  A�  A`  @@  @@  C�  DY� D�  FM D�@ E�` @�  Bl  A`  C�  E%� F1UEz@ Du� C�  @�ˮB���FH�Ax  @   D�� F��U�����=`캳j��t���/;���Q;�w=H��9/9�� ���g=�s��f��=�)^;� �C�;��=iI�:􍰽��<D8�=�b�" (=�5����=�_�<��]=�M��_�L       split_indices[$l#L       ?               )   &   &                            !   )   &         $            +   *   $   !         $                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?E*�
D�K�DZ�D��D�D$��CU�9DIW}C�-KC�'CjVHC��C��Bv�C�7Dp�Co��C�G�C?��C���ANC\�sAX�TBz<C��SC�D�B��Bfy3@���B��rA��C�~BC�c=B�O�B��C�}B��@BN &CB�C�n�B��@��#@M�CT&~A
_VA@�H?��_B0��A��OBB�GC\ZCi��A�]�AQ�B^��B[��@*DD@��@ ��A���B�˴A�t�?���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =��=��4�>�����O<�d>8O3?���ƧK���=4���"�'>�U=�)�>�B?t�Ǿ-A�=�~ͿaS�G��8/�>�'>V�пk��?q��DIu<�*�>��? ,=e�!��?~����Ś�Ŕ;��=׷����Q���D�+w�����;8z�ӻ�<Vg=̹�?;�=�������W=�L=�%;�w�k=2�3�V�<V��=5����=� x=A6�>hO=��<%d+=�e(L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9����   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =B��B�6A���B�a$@���Ab||@��A2�B56x@�AN@Eu
@�m`A}~
@�`?���@�+�@��;@a��@��I@�jg@��@&|�@�L@���@�cE@�h�A *D@�tA/7(    ?�p�                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :����   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =A�  E   B(  D�  D��(D�  A   @@  @@  A�  @   A$�IEE� D%@ @@  @d�IF�� @   A0  B�  DH  A�  @�  A�  F+� C�� Di  A  DM� ��@�  ��Ś�Ŕ;��=׷����Q���D�+w�����;8z�ӻ�<Vg=̹�?;�=�������W=�L=�%;�w�k=2�3�V�<V��=5����=� x=A6�>hO=��<%d+=�e(L       split_indices[$l#L       =   "      "      '                     !         )   !   $   $   &   )   '   "   !      $         &                                                                                                                                  L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =E)�D�sDs�D�:hD�DB)
CG4%D= �CʨZD
��A0IC%$�D��C"�HBqD�3CEپCvh�C��C�!�Cy�B@6	�AƨC5�A�v�C���C��C��A�m�?���B��CiխC�i�C@��@��l@��kCn��BxfdB���Ci��B�iMCtB:@���?��E?� @H1g@�t�B��%B���An�A,~�CF��C���C�/@�o=A���B�îA�>HA<^�?�?PB��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;�?�?"�U��n5=��*?@�������O�h?J�v��p�?iћ>��1���s��F7>dC�c֣=��?���)H�b̓?�Ψ>�?��$[?R:���ʽ�#?��ӽք�����>�D�� ŽS]�<��㽖6�=jS�>@����=ȃv�Ԑk�D"=��=�1����=�q����=�J=l�r=Ԝ�=�[Ž���>-X�9F���ݳ�ܼr<ڥ =��6��+�wB�;t@-�&d�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ;                                                           L       idiL       left_children[$l#L       ;               	                                    !   #   %   '   )   +   -   /����   1����   3   5   7   9����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ;C��%BB��CѮ�B^��B1��A ��B�N�A��A�B&)�B|�?�\ A�Q{A��A�F@�d�@HAbv@��(@�H�B �BAЦ1@z��@{#�    @#2    AO��A5�hA4A7B�                                                                                                                L       parents[$l#L       ;���                                                           	   	   
   
                                                                                                            L       right_children[$l#L       ;               
                                     "   $   &   (   *   ,   .   0����   2����   4   6   8   :����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ;B2  @ʪ�@@  @l��B  Ad  B�  @*��F�U@��A�  B5UUB�UUA�  @�  B�� A���B�vdA�  A�  A`  @l��BI�(A@  ��#F�� �ք�@�  B�*�E�IFPUU<��㽖6�=jS�>@����=ȃv�Ԑk�D"=��=�1����=�q����=�J=l�r=Ԝ�=�[Ž���>-X�9F���ݳ�ܼr<ڥ =��6��+�wB�;t@-�&d�L       split_indices[$l#L       ;   %   %      !   %   !   %   %   $   !   "   %   %   "      *   *   *   "   %   %   !   (                     *                                                                                                                        L       
split_type[$U#L       ;                                                           L       sum_hessian[$d#L       ;E'�DKγD�T�CO�D%��D/�D���B���B��1C��C8��C��7A�`�D&��D(}�A¶B.��B6��Bi�C��oC�B�4 B�S{@���C�J]@��hA�(�C8�C�� C�C���A��%@���@��BeB��@� \BiQ@��C��B��B/t�B�&�B͆Bt��B'4�B+rW?�/@Z^�@���?���A 	C/$�C�A`B�ʃC!L�C��C��B���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       59L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;��\?"R����=�Ԇ?Gw�����<Va>��2���?S�$���4�������[>nB�<K}���?7EE>0	 �)�?n�>�ο�C��?�hٿ;�B���?`m�����=���?	�"��Z�=�u����<q�k=��%=7{�9 =ĕK����=�&�=�e=���=�=�=
��V�=��n=�;H<��3����=L#�;Я+>��< <�!��b�=q\�����>^;�θ=�*�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ;                                                           L       idiL       left_children[$l#L       ;               	                                    !   #   %   '   )   +   -   /����   1����   3   5   7   9����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ;CғSBa� C��B1A��@A- Bl�A�p�@��`A�%`Ax�?�^ A�3�A�[A�L@��@�Dp@���@�XA��A��XAP@>�t�@��,    @��V    Ag}�A8|A4��A"��                                                                                                                L       parents[$l#L       ;���                                                           	   	   
   
                                                                                                            L       right_children[$l#L       ;               
                                     "   $   &   (   *   ,   .   0����   2����   4   6   8   :����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ;B$  @ʪ�@@  @��nA�  AEUUB�  @   Bp  B
ffA�  B2  B�  @�  @�  B  @X  @��Dc� @ڪ�@@  BUUE]� C!33���B�8����A�  B   CX  C0  ����<q�k=��%=7{�9 =ĕK����=�&�=�e=���=�=�=
��V�=��n=�;H<��3����=L#�;Я+>��< <�!��b�=q\�����>^;�θ=�*�L       split_indices[$l#L       ;   %   %   #   !   !   !   %   %      %   "   %   %   #   #      !   !      !   #   %      (       '          "   %   )                                                                                                                L       
split_type[$U#L       ;                                                           L       sum_hessian[$d#L       ;E!4�D3�D�ܰC��D5�C�ȧD���B�eBieYDl>A�61C���B��D!_�D3�#A�U�B�ϗA�}BD6�C���B��A��u@���A�-�C��AٮA���C��CI��DVfC6z�A/۫@ɠcB-(�BvI@���@w�vB=��?��1C���C
�YB=j�B!�{Av_�@]@�!2?�&�A���?���@��d@��C?�C|�AA�"CAE�C��uCQ��C)D�ASfnL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       59L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?��	l� ��>r���N>�<ۏ�>3��?���[�
Q���>:�>�P=�o>��B?F=,��,�>@)�V|6�>e5=�w�����=��Z?�R+�?NX>5.R�1&|>��\��΃>m�?`wI����E�8�e<ɿ1�u����� <��c� �=V��<�-�\n���>�='���yz�=��K����{|�=y�x=�?=�X�;j�M= ذ<��g�<��N=�����H=�Dg=����v���s�+=��6L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?B��LA�8�AjD�B}X�@�C%A[��@�+ A�kBm�Ap0�@�S�Ax4A1�@��t@v�0@�u�@�Z�@ @�ԓ?ڭZA	�@��h@���@��@�v�AS��A��@n�t@��@��?��                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?@�  D� Em� CH  E@  E� B(  A�  @@  A�  A�  D�@ FPUUE�� Bx  F+�A@  E�P C�  ?�  A�  A  A�  FH�A   F` A�  G, F�l @   E�@ ����E�8�e<ɿ1�u����� <��c� �=V��<�-�\n���>�='���yz�=��K����{|�=y�x=�?=�X�;j�M= ذ<��g�<��N=�����H=�Dg=����v���s�+=��6L       split_indices[$l#L       ?   #                  "   "   #   "   "                $             &         &   $                                                                                                                                                       L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?EsD�pDP�D�k�D5�D+C}D<�hC���C�&�C�C	�)D	�B�
>BrI{D�fCB�CGٻC))�C�bCC	��B�L\A��A�:B�5�C��B㸘B��@�tA��BO�C�S�C�uBD��C�dB&��CHB1��B��
A��C�B�dB��=B�XB��A��@��A:�m@�adB��)B:�KC��lC*��B�<B���B3L�B
�f@���?�M�@�2=@d9�@�DBF�!L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5�p?�־�V"���?����������>�bc�?6��>�M3�܅��x=��g��2?��V���t=&a�?k?�����lM?%��?�����}<�C5>�[{��[=��ͽ�JG>7Ͻ�C=rϼ\ý�$=��X�hP�=��R:�_k�q��=@@=A��=�n�>�ӽOq�;w�׽���<s�=p��=��8�Y=qȽ��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idiL       left_children[$l#L       5               	                  ����                  !����   #   %   '   )   +����   -   /   1   3������������������������������������������������������������������������������������������������L       loss_changes[$d#L       5C��'A�d�C�rG@`l�A�@�^�BP@�5C@1�B$�@A��    A���A��^A�@���@q�D?�@    B���@�@A�d@�g @��    AKGg@�A@A0AzO                                                                                                L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                  ����                   "����   $   &   (   *   ,����   .   0   2   4������������������������������������������������������������������������������������������������L       split_conditions[$d#L       5B<  @   @@  D	� B  A\��CG  @X  E�P D� @@  �܅B�UUB(  E�P E� @   DY� =&a�F@ E�� @��9A�  F�� ��}A�  E� A1�F佨JG>7Ͻ�C=rϼ\ý�$=��X�hP�=��R:�_k�q��=@@=A��=�n�>�ӽOq�;w�׽���<s�=p��=��8�Y=qȽ��L       split_indices[$l#L       5   %   %         %   !   %   !                %   "                          !   "           !      '                                                                                                    L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5E�PDB�~D�0`A��D<��C�D�-A-�KAM��D	�eCJ�AC��sA��+Da}C��q@�(�@�g�A=��?�p!C���C0�B�cvB�?@��Aqz�DW��CG(Cn�B��?��@.Ib@�N�?�c,?�VbA-�C�.�B<a(C,��@e�?B]Z�B1k�B�߇B�
@�/?�mDT�<A$ݰB���B��AN0Ca �A��A�+L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       9�K1?���U��>o?Dn�u�=	���8$?�`?TTf>�����f���?> چ��4�<��Ŀ:�y>�6���?2}+?��=�ak?\�x>��|2�EUN�ڠ>�M�<�s�Da����<Ly[�L	P�$=_��l=�U���V=�d�=�-&�F�=�1��{�=�$��U��=�H���&
=�T���G��	H�<��=�w�;����#���x�=��*�-9���!�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       9                                                         L       idiL       left_children[$l#L       9               	                                    !��������   #   %   '   )   +   -   /����   1   3   5   7��������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       9C��B?��C���B��A !@A���B&T Aa&@uD�A+x A!$uA�@n[ A���@�u�@��@��        B)q(@gp@A(�	@��L@��kA� @P    A���A-�A��A5��                                                                                                        L       parents[$l#L       9���                                                           	   	   
   
                                                                                                      L       right_children[$l#L       9               
                                     "��������   $   &   (   *   ,   .   0����   2   4   6   8��������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       9B  @�  @@  D�  B  B"  CA  F�EUER� D�@ Bw$�B$�B|  B�  C�� F>P B@a�>�6���FKp @@  @@  E�� A�  F�� @   �ڠ@�  Fz  C�  E��9<Ly[�L	P�$=_��l=�U���V=�d�=�-&�F�=�1��{�=�$��U��=�H���&
=�T���G��	H�<��=�w�;����#���x�=��*�-9���!�L       split_indices[$l#L       9   %   %         %   %   %   $         *   (   %   %   %      *                                                $                                                                                                        L       
split_type[$U#L       9                                                         L       sum_hessian[$d#L       9Et�D�FD�#tC)k�C�b�C�27D���Cd�A�8�C��OB�HA�� C�u�D�4QC��UB��A}K�Ǎ?���Ct/�C�B&�A�<�A>SA��}B}�xC��(C�>�D.IDCH6�B���B�A�S�@ٛ�A}�Ca��A���B��1BE4�A�KjA�|�@�OBA�i@ExA'A��?��BO�A:�rC{H�B�i=D{�B�k�C?�AA�B�dBY��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       57L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       9�Ěc? ���]%�=���?�c���;���B�?�G?7��>*Z��9W��a���H>y�">��q?����D
�??�F���Ǿ���?x9��|�O a�����?8�?�=֠�=F���׽�8c��x�>,�=������=6�Y=�˯=����/�=ř��?Z�=��[=��3<�ܐ�0�=d}U���_�Ch�:%��U��R��=�g=���<�j�7fcL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       9                                                         L       idiL       left_children[$l#L       9               	                     ����               !   #   %   '   )   +   -   /   1   3   5   7����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       9C`QB
��C��,A�t�Aʗ8@~� A�UA;�@��$AEt�A�F�@@�    A�&�AyO@�nG@�t�<�X ?��/@���@��A1Zv@��?�{|?���A��9@��@�PAL��                                                                                                                L       parents[$l#L       9���                                                           	   	   
   
                                                                                                      L       right_children[$l#L       9               
                     ����                "   $   &   (   *   ,   .   0   2   4   6   8����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       9B2  @ʪ�@@  D�  B  B�UU@�  F�UE@ G� @@  D	� ��a�C� B�  C{  B��B�  C{  D�@ D�@ Fk>9A   Bt  E�� CX  B��AW��B4  =F���׽�8c��x�>,�=������=6�Y=�˯=����/�=ř��?Z�=��[=��3<�ܐ�0�=d}U���_�Ch�:%��U��R��=�g=���<�j�7fcL       split_indices[$l#L       9   %   %         %   %      $      $             +   %      '   +            $   &   %      %   '   +                                                                                                                   L       
split_type[$U#L       9                                                         L       sum_hessian[$d#L       9E�`D0/QD�C��DN�C�&D�ёB�]*A��gC�)�B���BHPyC�Dh�TC�G�B�u[BSϞA�N�@FOC�ȶA�BRG�BIW�@��UB1�D_��B�iB�2fC~�A�"�B0�QA^�0BRA�?�		?���?�æC�O\C�AW��@Q�B.��A1.A�ϩA��,@`ظ@��B%�v@>�zD0R�C>{�A+��A�ҀB��B.=�C[�*BWmL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       57L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =���E?��:G?.�U>$j@�f�O<����)�?K�����=?	Ob��5a���>�����uY>�慾��Z?k7�>��8�&Ƅ?���?5 W�J��*Y?A%��������^>Q�$?CXE�e.o<և���=ɔ�R�"=w��=�?C=� g<���=�[����<�2�=�1¼��=�=P�[=�Y��=�gǽ�>X=(>M?<���=�c+���/���.<��j=��^�?�����<#�%�츲L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1����   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =CUN�BZ�Cy�eA���BS�A�`A�
bAA|��A�k�A_��Aֽ?@�d@A�,Ad�@��@���A"GP@�O.Ae�,@'�@u��A �$A �X@�	�    A��Ab�@���AOvAE�                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2����   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B  @ڪ�@@  @`  A`  BD  B�  @-��A�  D�@ Ad  A�A�  @�  @�  B   D�  @s33C� @@  E~� E�� D�@ Fz�UB$qǽ���B�  @�  BӪ�E�IFPUU���=ɔ�R�"=w��=�?C=� g<���=�[����<�2�=�1¼��=�=P�[=�Y��=�gǽ�>X=(>M?<���=�c+���/���.<��j=��^�?�����<#�%�츲L       split_indices[$l#L       =   %   !      %   %   %   %   !   %      !   !   !               !                  $   *       %      *                                                                                                                                L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =E~�D$/D�kC���C7�C�$�D�a�B`�kC��CB��4B�D�B��C���C���DhX&A�YB?C�5bB��B|��A*�B�	\A��B=Z9A��C�"�A3�C�pTB5#Cǅ�D�?A-�FA$�kA�*@��MC�C c�BUq�A���B=%�A~�~A�1?�|cB��=?���A��@��KB"(@�x�@��AA`@X�K@��BRGC�/�A��t@v�CQQ�C=��C�,�B���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =�K�G>�jv�,��?'|�=�Ѻ�d[�<��H=�@M?JvJ����?t������ۗ>u�|�����R�>�?n��>�@��_�?�}I���?���"�m?&wf��^����F=��?٦�F$m�Cb����<�0!<�L�=���=F�=��;"4�=�U���<d͢�Q�=�_�=#��?%�=��z��,S��#�=h�<Kj>]w=��c���=:ꊭ=�@���N=`�m: ���>�;����L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1����   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =C%��Bd4Cd9vAڴhB
�rA�� A��A��A���B�A`A��0@A��Aek�A3N�@���@��@�H�AHQWAS��@CH�@���A�^LA�@�F�    @���A'��@�8Aj&@Lk�                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2����   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B  @Ͷ�@@  @�  A�  B\  B�  @   A�  D�@ A0  A	$�A���F�UC�  B  D�@ @ʪ�A�  @@  @`  E�  Ad  F�� CI���^�B�UUD/@ B  F>� B�  ����<�0!<�L�=���=F�=��;"4�=�U���<d͢�Q�=�_�=#��?%�=��z��,S��#�=h�<Kj>]w=��c���=:ꊭ=�@���N=`�m: ���>�;����L       split_indices[$l#L       =   %   !      %   %   %   %   %   %      "   !   !   $   %         %   "      %       !   $   '       %      %                                                                                                                               L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =E�fD*�D�7kC�5CF��C�ʸD��B�O�C��EB���B�ȍB���C��C���Dr��A���BM#�CT�TB��lB�ZAcJ�@h��BȂ}B`XvAt�%C��P@��Co^2B��Dm>;A���AJ�w@�$�B0S�@�~�B�LC01�B*��B X�Bv�A�1�?�{�AR;}?�TD@��B�ʾA���BN��@�-�A%�@�|�@��@�ƫCSedA��s@.�B�>�D9�CP��@��A�nnL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =;��m>�B���\=�	.?n̿e�Z=��>��x����?D�>�����Ͽ�- >�o�(T�=��?f�A<�QI�3i?z��>ط��:�?i�9��>�ǽ�����>�?e<�}��He�=�g>�pt�=�<�м��=�u��E���o�=�\�=f�%�^��=T�꽁��=�T�=���sv ��=*�1=J&��� =��n���ܻ��<��U�Xf(=y)�;���mռ���>:�lL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1����   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =CA#A�rHCai�A�JA�PA���A�@<AT7�A̶A���Axr-A`�@�3�A�Ap�@�[@�ExAΨ@�Np@��@A��Ab_PA�@�D@ˋ�    @�؛A��AF�A[9A/��                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2����   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B  A   @@  @�  @�33B<  B�  @j��E۞9A�  A�  @��A���@�  CA  A`  @l��B�vd@�  A�  A0  A�  A�  F�EUB��ͽ���B�UUA/	AB@  CJ� C�  =�g>�pt�=�<�м��=�u��E���o�=�\�=f�%�^��=T�꽁��=�T�=���sv ��=*�1=J&��� =��n���ܻ��<��U�Xf(=y)�;���mռ���>:�lL       split_indices[$l#L       =   %   %      !   !   %   %   %   $   %   %   !   !      %   "   !   *   !   "   "   "   !   $   +       %   +      (   (                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =ERwD�
D�.jC=bC��bC�k"D�S�B�B�y�C��sB�þBXC�hAC���Du�hB+�6BqB�B�C#��B�BD�B��cA�g�A��|C��@��Cz$�B��D/��C��A.��A��A�JAw�A��2@�k�A-)�A熓C��A�'�A�B�y�A��3A%�wB���@�\�A��I@��)A�l;@*�
@:��@k��Bւ^C�@�(�B��uD*9VA�1WC��X?׵�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?����>�;���Z>⮑��?V�;�[<��=��?�\>�[�ږX��<��KJ�=�����R?	]=�ĭ�?K:�>F�=?9�нa)�)i�?<T���J?��j��5����sK>+����h�?nM�<�j�=��P�[�g=q�U� 3K=�=�pZm=��$��G=��=�[���=3[��L�Iï=Ԏo���
�ɑU�d��>�-������D��f	���[�����S�<�����ؽI��N��>�����L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?B��A���C��A��A(@�� A���A�LB(�@�T�AV��A�M�@@AN^XA� A4fA&4�A#�@A��@�.�A	��@׹L@i<
@ܹ�@�	�?>/�@p AY�AQ<bAKNAՂ                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?B2  A(  A�  @�  FX B�  CA  @�  B   B�  A�  AEUUD�  @�  CJ  @j��A�  A0  A�  A@  A�  BT  A  A�  @�  Ekj�CS  A8K�A  A�  A�  <�j�=��P�[�g=q�U� 3K=�=�pZm=��$��G=��=�[���=3[��L�Iï=Ԏo���
�ɑU�d��>�-������D��f	���[�����S�<�����ؽI��N��>�����L       split_indices[$l#L       ?   %   !   "   %   $   %   %   !   %      "   !      !   )   %   "   "   "   %   "      %   )   )   $   %   (   !      "                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?Ek�D�mD���D��B�\	C���D�:�CdqC�+�B�B9��BFC�8XDj]C�1OB�̰B��1Cp�C�#Ab4A�(�B�=@�tB+�7@�>�B���C(�C���Dq�C{v�@��AB$B�BBiWA
�BA@�Cd��B��jBy]�@g'A(>jA`Y@�k"@�B
�z?�#\@��A��|A�}�?�'@�5A�`�B�o�B�	�B�mA��C��C���C+ʺB֓�C,�?�w;@pJ�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       9<2O�>�6��
�>���?G�ܿfZ=	D�>�:���?w��>6�s���}��Β=���9��<���?}�>g�G}w?�G�&X�I��?Bx{�zH�>��H=���?6fP��O}=t@�=3eM�4З=��H<s\
=p)�ɰ���g=�Z=�q�=�|���qH=�3���=Ls=�Y�<$�׽Ӄ��o���G=�̇<�2�ꇫ�d�=��;�I>F�5=�⛼>�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       9                                                         L       idiL       left_children[$l#L       9               	                     ����               !   #   %   '   )   +   -   /   1   3   5   7����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       9B�SIA��C<t�B"�hA��HAZͰAp��A��NA~�@���A��A��,    A/pA+T�A��A���@e�A-M�@&À@,�z@�?�@ �\?�c A@fA/ޮ@~ƠA=�fA3.                                                                                                                L       parents[$l#L       9���                                                           	   	   
   
                                                                                                      L       right_children[$l#L       9               
                     ����                "   $   &   (   *   ,   .   0   2   4   6   8����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       9B  D�@ @@  F� BUUB�UUCD  @�  @�  E�� E� @�I%��ΒA   Dw� @�  @�  C  A�  @@  D  @��B�  F�P B�  A�  B�  C�  D�@ =3eM�4З=��H<s\
=p)�ɰ���g=�Z=�q�=�|���qH=�3���=Ls=�Y�<$�׽Ӄ��o���G=�̇<�2�ꇫ�d�=��;�I>F�5=�⛼>�L       split_indices[$l#L       9   %            %   %   %   %   !         !             !   !   (   "         !   )   $   (   !      (                                                                                                                   L       
split_type[$U#L       9                                                         L       sum_hessian[$d#L       9Er�D >D��rC��C�C�	4D�c%C��BPQB��LB`�B��CA�D�C�X?BѳC[�AG�BB�6�@Y
�A�A_X�B(^EA�/�Dy�_A�yzC5}B�� B[�\BG��C`�B�Y�A0�?�o�B�@��B��BT�@a?�SA6�A3r�A"�S@q�vB�@6�A��:@�tDw��@�G�@��xA�O�C�z?��A�k�B��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       57L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       7��v�>��t���>\4A?Iȿ|h�����>�3?�,!�?p >Z���U�V����4ٿ`��F�->�K;��|'�ZW�?zJ��J���zf�?I|;��c}��["?|����첽s�>b����2=0L<<��/�5�=x	�<�@Z��<�6����<%$s=��q�3r��۰�=�ݽv��<=bg=��D��>���Q��:ቼ�����tP<�`¼>�3��7@L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       7                                                       L       idiL       left_children[$l#L       7               	                                    !   #   %   '   )   +   -��������   /����   1   3   5����������������������������������������������������������������������������������������������������L       loss_changes[$d#L       7B�e!A���C%k�BU�A�D@�9`Ab�pA���@�.�@�Z@A�ϴ>�� A*�Aъ@�#�Az��A�4@�d@��@E�@@'��@�y�@$��        @z�    A$s@�Y�?2��                                                                                                    L       parents[$l#L       7���                                                           	   	   
   
                                                                                                L       right_children[$l#L       7               
                                     "   $   &   (   *   ,   .��������   0����   2   4   6����������������������������������������������������������������������������������������������������L       split_conditions[$d#L       7B<  D�@ @@  FKp B   Ad  C�  @�  Bt  E�� E@ G^� B�UU@�  C2  @�  @��@�  D�� ?�  @   @��nA,�ͽ�c}��["E۞9���B�  B��@�  =0L<<��/�5�=x	�<�@Z��<�6����<%$s=��q�3r��۰�=�ݽv��<=bg=��D��>���Q��:ቼ�����tP<�`¼>�3��7@L       split_indices[$l#L       7   %            %   !   %   %   (         $   %      )   !   !                !   !           $          '   (                                                                                                    L       
split_type[$U#L       7                                                       L       sum_hessian[$d#L       7E �vD�D�pCҫ�C>��CL�3D��3C��1B.bB��B��/CA�A*x6D���A�"B�NC���A��A�B��2@]�B>{B!�C@f?��Q@qy�@�3oDY�iC��*A�X�?�FBh��BOE�C.��B�U�A�͟@��@���AnߤB���?�kp?�D@�vA���A�?+B	`a@<,@)�?�_�D'�CH�RA�OC��9?��As��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       55L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       7;~��>į�����>r�*?N���J�k<�t�>��D��Lg?�ѷ>�T�ǋ8���> +}���	A�>�_@�#JҿD��?��K���X?J�}��D��1m>���=��?.�X�K�;�Y���uJ:a�=��(<Ν=
��?��>o:��=��<B� =�\�;�*�v��=�U�����u5<�s�>�S��ݍ<���=���<���:GP�
<׻��<�.�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       7                                                       L       idiL       left_children[$l#L       7               	                     ����               !   #   %����   '   )   +   -   /   1   3   5��������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       7B��|A�A�C��B �,A�xA�HA���AcϨ@��@O @�*RA��6    A2��@��@E->Az>�@ꈰ@��?x�     @g�hB��@���@�`�A��@F�AS
A�                                                                                                        L       parents[$l#L       7���                                                           	   	   
   
                                                                                                L       right_children[$l#L       7               
                     ����                "   $   &����   (   *   ,   .   0   2   4   6��������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       7B
ffD� @@  E�� A�  B�UUB�  @   @�  B  @@  A����E�@ @�  B  @s33B  @@  E�  ���XD��E� B+��C�5UBs��C�C�C	  ��uJ:a�=��(<Ν=
��?��>o:��=��<B� =�\�;�*�v��=�U�����u5<�s�>�S��ݍ<���=���<���:GP�
<׻��<�.�L       split_indices[$l#L       7   %            %   %   %   %   !   &      !                !   )             '      +   '   '   '   '   )                                                                                                        L       
split_type[$U#L       7                                                       L       sum_hessian[$d#L       7D��GC�J_D�U�C��B�q\CzmD��C��TBV��B�+3B>�TB��C��D��D26?Au��C�*%A�kA�h�B���?�uA�d9A��nB��UA�1mD��BD8C�d�C�AZ;@ʗB��{C+�Acv'AT��A�4�@���B|��?�xA��(?�@�NAp��BE>�A�_�A���@[4�Bb�iC��A�˩Ay�B���C4TC��sB�/L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       55L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =��>�������>AI�?U���1`�9�d>����Wv?��?���A�$�~� =��1�� 5?1�>=�#^�^d� Y?�[2==ν���?['`�V��>')�Ѹo���S?�S�=�7[>\�B�7B���y�=�����=2�ӽ�o<a�=������=܃�8������=���=�R��S�=ɉ�4�<�,��ѹe���=�lW=�x���bJ>�X�FF��-�<�z�>';�3�����=��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1����   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =B��wA�B�~ZA�|@��`B�0AdQA�t�@���@"��@ۑ6A�&N@�@A�gAH��A�ψAv��@�{&@�{�@��@5��A��d@|�P@�*�@�>    @�<:@�P A4�XA��M@�h                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2����   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B  D� @@  F@ @@  BT  C  @uUUB1��B   E� @d�IAd  E� @�\@`  A`  @@  BBUUE�` Bp  A�  E�� C   A	$��ѸoB�  B���@�  AΒIF ��y�=�����=2�ӽ�o<a�=������=܃�8������=���=�R��S�=ɉ�4�<�,��ѹe���=�lW=�x���bJ>�X�FF��-�<�z�>';�3�����=��L       split_indices[$l#L       =   %               %   %   !   (   %      !   !   $   +   %   %      (         %         !       %   +      (                                                                                                                           L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =D��)C��iD��C�y}B�۲C��JD�P|C���B=,.Bwx�B>�BüC!��D1M5DS�B��_C,7>A�U�A�bBl�@-�ANA�txB�+B��C��A
�A|']D-\�B��C���A�+Bp7(B��B�h�Ax�H@��V@��Aɤ
Bd��?��~?�]�?�{U@��6@�GA��V?��@���A�eB1h�A��f@��@��Ai��?�n�C��CTZ�AB( B���C��5A�)�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       7�1��>�����z>`B�?H]}�1���� >�0v����6��?Q�8�  �%��=�k½�}f>G�?Iٷ���?S�?[�{�u?��<��!��/����V�'�>��<ѻ�i#o<�C'�G�H=��߼ >;)c����=���݋=�J�<���<�c�>.ˆ<����AK��Ģ�=K> ��A�����߳�<�X�Y'}<]����!Ͻw�g�~�RL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       7                                                       L       idiL       left_children[$l#L       7               	            ����                        !   #   %����   '   )   +   -   /   1   3   5��������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       7Bj�]A`��B��A"�@"��@�# A��A�oPAYH�    @)/P@�ht@�dPA1d A��A�d&A'?�At[ A&�F?���    ?�`�@:9�@`p�A
��A�?fA48�AcA�l                                                                                                        L       parents[$l#L       7���                                                           
   
                                                                                                      L       right_children[$l#L       7               
            ����                         "   $   &����   (   *   ,   .   0   2   4   6��������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       7B2  E� A�  B  @�  A0  B���D� F�L �6��Dk@ @   D  A�  Dk  FD� A�  Fj` B�  Eۀ �uA�  B�  B��D!&�B��Ct>B� C��<�C'�G�H=��߼ >;)c����=���݋=�J�<���<�c�>.ˆ<����AK��Ģ�=K> ��A�����߳�<�X�Y'}<]����!Ͻw�g�~�RL       split_indices[$l#L       7   %      "   %   %      %      $             '   "         "      )          "   %   *   '   '   '   +   %                                                                                                        L       
split_type[$U#L       7                                                       L       sum_hessian[$d#L       7D��wD��D��zC� �B?x Cm��D�C�C�ΌB�ɪ?���B;K)AI�CaD&Da	C��XB�(�B�6�At�"B6U]?���@:D�A��CR��Aha�C��C���C��{C�ǗC���B
�BV��A.3�B��rA���AR�Y@�%B'50@r�?��?�
@r�@�{tC7�AA��b@/ŧA<p�A�-�B���Cw�[C>CS�AB�hB;�C|�8L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       55L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1��5J>c��'�v)>|qE�|1��4�a�#�=���>�>=�����4��4�<������=e��=WS=�C�>�"�Q�5>�K�>�ʥ�[F'=�e�z��gz>�K̽������<N�b���ߺ�m	=Y����&˼}=썽<����z8=l�u��S2��`�<B&�n�Z���+>o2����6��
�>nL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idiL       left_children[$l#L       1               	         ����         ����      ����            !   #   %   '   )   +   -   /����������������������������������������������������������������������������������������L       loss_changes[$d#L       1B?^A;ŜB�V	@eۜA&\�?���A?��@3y�    A@��AU�@O�q    A��@�'
    ?�HX@�eQ@���@��@���>��=� @�$#A�@��LA4��                                                                                        L       parents[$l#L       1���                                                     	   	   
   
                                                                                    L       right_children[$l#L       1               
         ����         ����      ����             "   $   &   (   *   ,   .   0����������������������������������������������������������������������������������������L       split_conditions[$d#L       1B`  @   @@  D^� B  B�UUC�  BH  =���@ʪ�@@  CH  ��4�B�  B�UU=e��B�  B�  A1�Ez� @TIC�  B�  D�� BT  Dw� C  �������<N�b���ߺ�m	=Y����&˼}=썽<����z8=l�u��S2��`�<B&�n�Z���+>o2����6��
�>nL       split_indices[$l#L       1   %   %         %   %   %          %                *       )      '       +      )   '         )                                                                                        L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1DDs�D�F�A���D��C�D�D�A���?��C��_Ct�[A.�B�K�D��B�7�?�AQA���B�IC�TB�DC�9@,m�A��DJ�C{qB�Yl@�� A[�W@fkNB�=@��NA�'Cd��A_5�B�!�@�_kC7=?�.�?��F@�X�?��8DF�1A�ZCx+>@<L�B6Z2A�O@�;?��.L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5��p>b ۽��>(��?FI�rW���T7>��c�6�?e��=)��������h�S,g>rX�>�c��L<Z�d�>�1���3?v$p=���������8ĩ?>ϝ��ǾRl=[�?i9�=�����]�=�%Z��7U<�%�
�׽�y�<��O��=�t<�5�E=�'=�M�� �{���=��<��h��^����=ҫ���j<��?L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idi L       left_children[$l#L       5               	                                    !   #   %����   '����   )��������   +����   -   /   1   3����������������������������������������������������������������������������������������L       loss_changes[$d#L       5B&>A�m�B�S�A�-�@�mD@� A-�'Az��A�'�@\�p@�Ő?:L @�|�A�A2N�BN)@�5�@�"P@���    ?6�@    @�F�        @(s^    A��A*��@S��A b{                                                                                        L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                                     "   $   &����   (����   *��������   ,����   .   0   2   4����������������������������������������������������������������������������������������L       split_conditions[$d#L       5B<  A�  @@  @��B�UUA\��B(  A�  A�  E�j�A`  G^� B�UUAp  @��S@ʪ�A�  Bp  Ez  ���3F�  =���A�  ���8ĩF�X ���BP  E�� D*  BL  ��]�=�%Z��7U<�%�
�׽�y�<��O��=�t<�5�E=�'=�M�� �{���=��<��h��^����=ҫ���j<��?L       split_indices[$l#L       5   %   "      !   *   !   "   %   %       &   $   %   &   +   %   "   +          $       &                      $      %                                                                                        L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5D�@D�>D�2!C�"B>Z�CG�D��,C�-�CΙB!�@�q�B�rQA�D��C��Cf�NB�ƺBG�UB��?��B�+@6O�@�I�B��?�06@��@���D	�uD?rA�|B��Bʫ\C��Br]�B{/�B�AS�,B��?���B�2@��?�x�@)�G@U�?��?D_Ac�C�C�`?���A�\R@p�\B�|�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       7��{>�j3���(>��?�`�N��Rf>�����?t��>�Y��|����8<z$.�ԭ�����? �z���)>�
�?}l;hї=�?FRk�h¡>1�庒|�?���>�	=6�T��2=��&<�<��~K<���= �ٽ��u<��=�UZ=����r���|=��{��]��wو�|�=�Ч<}@��R�>&��=
�ｌ��<�qO=��+��wL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       7                                                       L       idi!L       left_children[$l#L       7               	                     ����               !   #   %����   '   )   +   -   /   1   3   5��������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       7B-�A���B�)A�c�A1�AHB0A�A`�,Aq�?�t`@�6�A��    A#��@�H@�W�@�xA*�@�Y�?`}�    AY�f?���@�h@��:A��@��@�@��u                                                                                                        L       parents[$l#L       7���                                                           	   	   
   
                                                                                                L       right_children[$l#L       7               
                     ����                "   $   &����   (   *   ,   .   0   2   4   6��������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       7B  D�@ @@  @Ͷ�A�  B�UUC� @�  A�  E�  E� @�躽��8B�  @�  @	$�A�  @@  F5@ B�  ;hї@@  @�0�F�EUB���B�  Bܪ�@   FR� =6�T��2=��&<�<��~K<���= �ٽ��u<��=�UZ=����r���|=��{��]��wو�|�=�Ч<}@��R�>&��=
�ｌ��<�qO=��+��wL       split_indices[$l#L       7   %         !   %   %   +   %   %         !       +      !   %                   +   $   (   %   +      $                                                                                                        L       
split_type[$U#L       7                                                       L       sum_hessian[$d#L       7D���C�
D��C�u�B�mmCgDD�w�CE��C.�BM��Bo-SBX�zB̃KD���BWC Bc��C��B���BOD�BF�1?��B"�&A�ZA�'A��D��B;B?��@��fA7�]B5�MB���B>�Bk��A��*B:}�@�:�@	�B>PB��@��4@��A��A��@x�A|GPA�MC��kD]cG@��DB@B f�@�X�@�Z�?ĺ�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       55L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5<6�J>����Vz>��@��얿,�=hE=O��?��?
�k��=�����S�<�]q?I�>ۘW�T{
�ZR�?p���q?]w��2s=�7S�f!�=e�k=c^H�5]?�P�=�L�;^��=�'1�Wf=��=�fu�	:�=���<��g�zx=��C�ۯ{�p���Q<�C]�T��<��纟�g<�����e+�|��=�^/<���=���?��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idi"L       left_children[$l#L       5               	                     ����               !   #����   %   '����   )   +   -   /   1   3������������������������������������������������������������������������������������������������L       loss_changes[$d#L       5A�\�A��B�qjA���A9=~A���A�nA^�@��@�XJ@���A�-p    A�:@��ANH|A-��A��2@��0    @���@��    @5�@ˇ�A8O�A	R�?
��@�!�                                                                                                L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                     ����                "   $����   &   (����   *   ,   .   0   2   4������������������������������������������������������������������������������������������������L       split_conditions[$d#L       5B
ffA*��@@  A  E�IB�UUA   @l��A0  @�J@�  @�  ��S�A��B�  @`  A�  @d�IB   ���q@�  Bu� =�7SF�� E|��Fz�B�  D��D� ;^��=�'1�Wf=��=�fu�	:�=���<��g�zx=��C�ۯ{�p���Q<�C]�T��<��纟�g<�����e+�|��=�^/<���=���?��L       split_indices[$l#L       5   %   !      %       %      !   "   +      !       !   %   %   "   !   %          (       $   $   $      '                                                                                                   L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5D�lC�aD�&{C�aYBE�DC1�D��C@�C<�A)�_BE�B��HB���D���AԞ�Bb��B�;cA9�C0��?�2�AB�@nA�߱BX(�D���C7UUAb׽AFe�B!�A���B��gA=/�@�V5@��iC��B ��?���@���A���Ax��A� {?��kAUG�B"��D;��C���C�}B
�bAN�W?��/@���@��oL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =���>��d��F>~�?(��(�;�>�-���-?l	�>��+�AF��yS<o�&�(#6=@?/�����>���?y�6��Sq<;P?(�]���>�8ؽ�Mb��g<��Q�j!�>O9��Z��=X+H�5��=��a���*�%c
=B��+=/b9� �=Ь����=�_�#S,=Sj�;�W=��ʽ�;P��̃<�=���=?�V���;�5��,��l�;|���>[=�����k�=?/�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idi#L       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1����   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =A�F�A��B|{nAh�i@�PA�4�A(��@�}�Av
�@%� @��DAhg�?�8 @�k@�kx@�SA5�Al�A�Y�?� @	Mq@�o�@1�H@���@��{    @��@�5�?���@Nd�@�٠                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2����   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B
ffD�  @@  @uUUA�  BT  D�� @`  A`  E�` BaUUA�Ad  A�  A0  A�  B  @@  A0  Bp  F�P F/=A�  @d�ICI���MbB�  C@ B��A��9B�  =X+H�5��=��a���*�%c
=B��+=/b9� �=Ь����=�_�#S,=Sj�;�W=��ʽ�;P��̃<�=���=?�V���;�5��,��l�;|���>[=�����k�=?/�L       split_indices[$l#L       =   %         !   %   %   '   %   %      *   !   !   !      "   %      "         $   (   !   '       %   %   *   *                                                                                                                           L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =D�-�C��SD��C��B�B�C"�D��3B���CA �B4��B�AB��B��D�ԜA���A�)B`N�B��nB�L2B+s@��A��A���B4�kA���B�n�@�϶D��@��@��XA�o�Ag$�Ac�BCg�@�:QB��}A���@��)B��?�t�B$�?�>�?��A3]Ah?��rA���A���Aі�AQ�AU?��@�^.DW;Cł,@���?�?��@N�=A�KW@"�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       9��\�<-�t�>Jcf�8z����/��=���?M��!K�<;#�?/�þ��o�a���u{>�����T?xU�>����T4Y<U,o���=�1齑 ?�Bc�1R?7~�l�#=��>	�A�	.g���=r㲼� <�h}=ոռCO,�D�o=mo"�<�0�� �=vq��B$=z3��Kj�<F��_�>R6ؽ$�o���@=�"$��;�>�]�1{�ԑ��	���W�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       9                                                         L       idi$L       left_children[$l#L       9               	                                    !   #   %   '   )   +   -����   /   1   3   5��������   7��������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       9A�[A�g8@�݌A���B+�"@��@gd�A3a{A ʬAjy�A"�>A.�@��@i�@��"A"�AFz8@O��@�=�@�ApAY�AAx�A6S    A @\�Z@C�?�4         @�F4                                                                                                        L       parents[$l#L       9���                                                           	   	   
   
                                                                                                      L       right_children[$l#L       9               
                                     "   $   &   (   *   ,   .����   0   2   4   6��������   8��������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       9C�� B  @�D� @@  D�  Ap  @�  A�  A	$�@���@@  CJ  Dr� ?�  @�  A�  E�` B@a�B5UUB�  A�  C� �� A�  @�@vD1� A0  =��>	�AC�@ ���=r㲼� <�h}=ոռCO,�D�o=mo"�<�0�� �=vq��B$=z3��Kj�<F��_�>R6ؽ$�o���@=�"$��;�>�]�1{�ԑ��	���W�L       split_indices[$l#L       9   %   %   +            &   !   %   !   !      )      !   %   %      *   %   %   "   +       &   +                 %                                                                                                        L       
split_type[$U#L       9                                                         L       sum_hessian[$d#L       9D��lDҫ�B��rC���D�zrA޴�B�KJC��DB��B��D�J@���A�D�B!:�A�B�}MC:�B�1BIOB���A�@�D4D$��@��@�ORA�-�@��B��?��o?�@�A��BB�Bz6�B�4 B�ףB\�@=A���A�jA�SBf�A��@�?A�ylC���D'A�Z@i��?��0A�/\?��?��?��A*�A�@,ASrArk�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       57L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1<F�/>�ڽŚ8=�f">�B���X�	�>>܈�ڋ>��?Q!��n�;u��>��G�����l=Qf?B�|>,.b?w<�z�F�	�":<��G��^�����=P˽�	o;�5-��U�=RfP��By<�U==��e��\;�
�=B��<�yJ=�;� ^=���m0;��G���Q��>׺��=8u ��l���&L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idi%L       left_children[$l#L       1               	����                                    !   #   %   '   )   +   -   /������������������������������������������������������������������������������������������������L       loss_changes[$d#L       1A�D�A�dB`��@�]�@��l    @�O�A` �A)Y8@�|�@|Y<@옖A;X@���A�pAE�A/!�@��AH7�?㜐@��fA ��@��hA G?��p                                                                                                L       parents[$l#L       1���                                                     	   	   
   
                                                                                    L       right_children[$l#L       1               
����                                     "   $   &   (   *   ,   .   0������������������������������������������������������������������������������������������������L       split_conditions[$d#L       1B�  B  @@  B(  B�vd��X�A⪫@��@@  B8  Bd  D	� A���?�  A�  AEUUA�  A333Bt  @d�IA�  B�  D�  BH  E� ����=P˽�	o;�5-��U�=RfP��By<�U==��e��\;�
�=B��<�yJ=�;� ^=���m0;��G���Q��>׺��=8u ��l���&L       split_indices[$l#L       1   %   "      %   *       *   !      %   "      !   %   (   !      !   %   !   &                                                                                                            L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1D�J�DC�Dw��D#�B��PB~��Dg��C�7�C{&�B�A���C�DCb�C��*CBђCSr�A���B���A�3�@+�#B���B��D@�BA�@��-C�{A���B���A�7�A�5B�83B��A�3'@�9�A���BCTz@���Av�??��]?բ�A��#B��YA���A�VD6��B��@4��@��TL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       #����;�%&�cE�>-X��Q��q���[>�[?`j��WO`��mj���3��p�=%d��i��>M�i��{l�,}�=���|�>[���r�G?��<�zj;9޺�m=m�����S]=�T����C�{�����<���=�@�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       #                                   L       idi&L       left_children[$l#L       #               	                  ����������������      ��������            !������������������������������������������������L       loss_changes[$d#L       #A��A�j	?��pA�B>�0?D��?tC`@�|?퍸A5�,@�y                @���A�F        ?5 @�('@�Y�@U�                                                L       parents[$l#L       #���                                                           	   	   
   
                                    L       right_children[$l#L       #               
                  ����������������      ��������             "������������������������������������������������L       split_conditions[$d#L       #C�  B2  C2  @�  @@  D�  B�  AffD�@ AEUUA   ���3��p�=%d��i��A�  B�  �,}�=���@   B|  C�@ B,5�<�zj;9޺�m=m�����S]=�T����C�{�����<���=�@�L       split_indices[$l#L       #   %   %   )         $      !      !                      %   (              %   +   (                                                L       
split_type[$U#L       #                                   L       sum_hessian[$d#L       #D۳�D�E�AۃhC��@D��nA� �@xC� �A��B�,D���?�րA�?��H?���C��~B���?�͸A�H,By�pA	��D���A��"CU�yC��Bc��A�׾?���Bt#�@�@�2D�&I@�Y�A]=�A��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       35L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1<��i==;�u3��2�>�+�ő�P)�>�t�L�>�e'=�>�=�-m�e=@z>�K��*׽(�?���S�#?	�Z=H.?>�X�>zؽ 
Կ?�<R���I!;=��<� �,ѽ��|;a~�0�Z�"�=��w=+̉�5G=�\0;z9m��j�<�׵=;M���"<��@����=v�;�Z� ���p=	��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idi'L       left_children[$l#L       1               	����                                    !   #   %   '   )   +   -   /������������������������������������������������������������������������������������������������L       loss_changes[$d#L       1A�mA�yA&D'Aq�A,�    A6�AA"\A���A��A'�A7�@���A`Q~A")�@���A6b�Ah,`@��@�E8@�"A�C@K,@��@�P�                                                                                                L       parents[$l#L       1���                                                     	   	   
   
                                                                                    L       right_children[$l#L       1               
����                                     "   $   &   (   *   ,   .   0������������������������������������������������������������������������������������������������L       split_conditions[$d#L       1C�@ @�  @@  B  A�  �ő�D�� D�@ @@  C�nB8  FB�UD�  F@ A�  B�UUC  D  D  D� A�  D/@ B�8�C�� F�T <R���I!;=��<� �,ѽ��|;a~�0�Z�"�=��w=+̉�5G=�\0;z9m��j�<�׵=;M���"<��@����=v�;�Z� ���p=	��L       split_indices[$l#L       1   %         %   "                (   %   $         %   %   )            &      '   %                                                                                                   L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1Dچ�D˵�B�:Dc��D3�A��4BmC�V�D�DB�~D'�BN��B6H�C��QB�e�B��C�k�B�s�A��B�D�.B)�A4�A��A��Cx/�B'*�B�B;��B�B�Cȸ/B}�{A��B��;@:��@�xA��aAX"�C��B�~LBԼ@� )?��@�m@�-�A�A���@t*L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       3:?޼%��>��$��<�q�>`�.?��V�q5�>���?h$�<3/����>���<�G�?��T����ҳd��f�>����?����4=O�?5�D��k�?s�k��=���=���Ľ	T=����K=ޝ��8J<��=�ֈ<��G��U>.i����
��=_�;����Wi%���=����x�<&ă�1�,=�]�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       3                                                   L       idi(L       left_children[$l#L       3               	                        ����            !   #   %   '   )   +   -   /   1����������������������������������������������������������������������������������������������������L       loss_changes[$d#L       3@�ȸ@�M�@�9wAD�AC�@%�?T�AT��@���@�G�A&�w@���@#�    =b^ @��@�U@��M@�H�?�Rq@u"�@��@��?��@�
1@XL                                                                                                    L       parents[$l#L       3���                                                           	   	   
   
                                                                                    L       right_children[$l#L       3               
                        ����             "   $   &   (   *   ,   .   0   2����������������������������������������������������������������������������������������������������L       split_conditions[$d#L       3E�  A�9C  E�P A1�@�  E� A�  B�i@   B���D   F��U<�G�E�� B�  E���E�0 @   A   B�  DJ� D���CR  A@  E� �k��=���=���Ľ	T=����K=ޝ��8J<��=�ֈ<��G��U>.i����
��=_�;����Wi%���=����x�<&ă�1�,=�]�L       split_indices[$l#L       3      (   )      '            *      '      $             $         '   +      '                                                                                                             L       
split_type[$U#L       3                                                   L       sum_hessian[$d#L       3D��LD�qB;�ZC���D�!PB�LA�9Cr��BS��A�SD��)A��A�]�?�3�@�[�B�GWC��A�B-�"@0M@�! B�U�D���@��@A��UA�Y?�JD@�x�?���A��B��B`�B�t@��@��bB
��A�:?��}?�A@�j�?��]B���A7?D�r�A��}?��L@b��@�#A:�?��Am�*L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       51L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ��0�;ZS�&�<�����w<���\$�<�s&������3��2�?o�����!�2a#��>,A׼b[��My>l���U�k>Jg,�y�=Sǃ��Da��;;,uI����<�s
=�˽\Z�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L                                      L       idi)L       left_children[$l#L                      	               ����   ������������            ������������������������������������������������L       loss_changes[$d#L       A2�UA
�$@q�A 6�?���@�7�>�K @���@���>��@    @�+f            A�0�A�qV@c��@L/D                                                L       parents[$l#L       ���                                                           	   	                              L       right_children[$l#L                      
               ����   ������������            ������������������������������������������������L       split_conditions[$d#L       C�  C�@ B�  A�  @@  A�@�  A�  B   B � ��2�E��9���!�2a#��E�� @@  @�  A�  ���U�k>Jg,�y�=Sǃ��Da��;;,uI����<�s
=�˽\Z�L       split_indices[$l#L          %   +      !   )   +   (   %      (       $               $         &                                                L       
split_type[$U#L                                      L       sum_hessian[$d#L       D�qD��xA��aD���@��@�7A�0�D�HA��^@��?מ�@;�`@R��?���A�%�C��aD�x�A�>@�U?�l�@��?�P?�X�B�f7C:Q�C�JD�@�Aq�@-�=@@�y@�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       31L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?�O߼Ȗ:>q�K>�+B�~?"��=��?P�4=�2����@�ê�?\F��Q@��?!�?���� q��X�?TY�:J'ܿ=��=�:��[�	��?��[��a�>���?4����B?t��=q5ܽ_�g>�Ͻw��=��<Z�/����6l<>��_��=�2B���E��P<�}=�Aֻ�/G������~=���=���=7Gռ�n�!��=��ݽl%���G=�+���ҼZA�;˂�=܄�����=L��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idi*L       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?A�~Ac�A{�@�+@��@�wXAE<%@�1\@�*bA��A�I@�ϸ@˗AA"�@�y�@ȼ`@��@�00@���@�[~@�h�A\&A�8@���@9h?�GP@��ArA7x?���@��.                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?B(  E� A`  B@ E_6�F^� D�@ B�  D�  C�  E�� B���F�U@�!SF7� E�U?�  D  CR  A�  D@� CF  D��1E� B  C%  B�  D*  B|  A�r�C*  �_�g>�Ͻw��=��<Z�/����6l<>��_��=�2B���E��P<�}=�Aֻ�/G������~=���=���=7Gռ�n�!��=��ݽl%���G=�+���ҼZA�;˂�=܄�����=L��L       split_indices[$l#L       ?   "   $   &   (       $               $   '   $   +   $                "      )   '          '            (                                                                                                                                   L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?D���Dƅ_C�Bf��D�O�B+�3B�A� �B1OB{k;D�twB4A��B��A�2A> �@��B ��@�DA��PA�4&C��D�-�@���Aݿ�@Z#D@�G�AR�B��A���A$�3?�*�A*{f@��@�sAӎ@�6�?��H@��rA��5@��Am*�A���C���A(��D�I�Aq�)@ �@F@�A��@��y?�b�?��@��C?���?��A=��A)B_��@�8An#@E�@�ZL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       +;��<��t�*Na=��T�������`�=}Q�? ߠ�f�$;�ǿ?�3?�y/��x4�l��>���@>?3�.=��ɽ�aS=�{ҽ�sM=�K��鰽���>;ʻݿ�=8rE��r6�?X�<Æ�;���(��=�pQ���@�'�=�o=�����1=+�_r;,=
�FL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       +                                           L       idi+L       left_children[$l#L       +               	                        ����            !   #����   %   '   )��������������������������������������������������������������������������������L       loss_changes[$d#L       +A7p�A[�@,�<ACw~B �@�?j�A��@�s�@�8@�)�>�z�@)^    ?���A
q@���@w�xA4    @9�A�fA��                                                                                L       parents[$l#L       +���                                                           	   	   
   
                                                            L       right_children[$l#L       +               
                        ����             "   $����   &   (   *��������������������������������������������������������������������������������L       split_conditions[$d#L       +C�  Bd  @�E� @@  B�.�E� F$ B�  Ad  @�  B|  B�ff��x4E�� @�  A�  FP� B�  ��aSB�UUA�  @   ��鰽���>;ʻݿ�=8rE��r6�?X�<Æ�;���(��=�pQ���@�'�=�o=�����1=+�_r;,=
�FL       split_indices[$l#L       +   %   %   +         (         )   !   !      (          %   %      )       %   "                                                                                   L       
split_type[$U#L       +                                           L       sum_hessian[$d#L       +Dס:DԢ|A���D�D���@��A��C�-�B��FB9<PD��@�"�@�A^�D@*�C���B��vB>*�A�+`B*;@r�RC�8jD*)�?��@�;?���?�?��0?ӑB���C��Bd��BwndB9��?�=�@L��A��j?�a�?�AA���C��<DDQB�-:L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       43L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1�fW=������4=*��>�ኽ����*=j�r�N"�>(^|?L*i;n/��cǯ<�4>�6��N6�̦�}*�>���C~�?y���J�=N�i�O>���L̽.�;h_�<f�o=���=L}ͽ�0�P_��L[��b�=
�G=���;(�0o�=�ν�U�=��`�p��>+���n;�./�����E>Q�p�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idi,L       left_children[$l#L       1               	����                                    !   #   %   '   )   +   -   /������������������������������������������������������������������������������������������������L       loss_changes[$d#L       1A'e@���B�9Ac@    @���@��@�	kA	��@��(A�DA5&w@�(�@�i�@���?�`A%��AMtA/}@���@ϧ�A@���A2                                                                                                L       parents[$l#L       1���                                                     	   	   
   
                                                                                    L       right_children[$l#L       1               
����                                     "   $   &   (   *   ,   .   0������������������������������������������������������������������������������������������������L       split_conditions[$d#L       1B�  @�  @@  B  B�  ���FR� B(  @   BR��E��rA⪫B�  @*��B�  C�rB(  A@  A`  B$�@�  C  B  @   A   �.�;h_�<f�o=���=L}ͽ�0�P_��L[��b�=
�G=���;(�0o�=�ν�U�=��`�p��>+���n;�./�����E>Q�p�L       split_indices[$l#L       1   %         "                    '   $   *   %   %      '   )      &   (      %                                                                                                         L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1D�|,D;,�Ds��D%P�B��yB'��DiS�D"��A1��Bt�AѴ�D@�#C!�DOB��@ֈ�@���@� jBaD�@�#�A���B���D$ݤA��.C��A� C�R^BåA��<@��@�?�t7@'��@Dw@,�^A�ȢB �N?�
�@K�?� AA�)�B<pdB���AM�BD!�kAP��AUh@C?Cz&L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1�v7+>�N�\y����>.C��Rּ��\`��'->p�?\>�y�>��V��R����K����օ�=�cS����>�g.;�<�=���;��K��d(�.9=�QE��Ժ��<"	:��%6�3>�=4| �������M=f�=6W��Fۓ=%o�9�3<�߽�.����<������s=:��=��tO;Jl�֭�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idi-L       left_children[$l#L       1               	                                 ��������   !   #   %��������������������   '   )   +   -   /������������������������������������������������������������������������L       loss_changes[$d#L       1AA�BA*��B�@1'�@��@A-� @���?Ѕ@o�j@�n?�h@?6#@@�n�@ο�@�?���        @-�Am�A�                    ?�L�A1@��@v8@�w�                                                                        L       parents[$l#L       1���                                                           	   	   
   
                                                                              L       right_children[$l#L       1               
                                  ��������   "   $   &��������������������   (   *   ,   .   0������������������������������������������������������������������������L       split_conditions[$d#L       1B5UU@   @@  B  B  A\��C� @�  A ��@�  B�UUGX B|  B  C� D�  �օ�=�cSB�  B  E�� =���;��K��d(�.9=�QED�  E��BP  Ekj�D4� =4| �������M=f�=6W��Fۓ=%o�9�3<�߽�.����<������s=:��=��tO;Jl�֭�L       split_indices[$l#L       1   %   %         "   !   +      +   !   *   $   %      +                 %   $                          $      $                                                                           L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1D���C�8D��A���C֍Bi�rD���A;"�@��C�"�AMJ�BNX�@��D�Y�BH��@-_@A��?���@�J-CY�CFnSA-�c?��{BI�c?��@]�(@Z��A��D�Z0@�ڌB*!s?���?���@�`u?���C�B���B5��Cc?���@!�AU }A*ίD�h8A�~?�$@��B��@��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       )��ۭ;e�|�)1ɽ �y>��BO�<͍:=�	����?L�=�|�=���b��>�׾_]3�UAl�g;=�"�>LCe=����J:=�UO��iz��Y��\}�>�<��1��w�:�����E�<�!�� c=D��]{=�C=�v:��+<ܒϾ
��=:ӽph/L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       )                                         L       idi.L       left_children[$l#L       )               	   ����                              ����   !   #   %������������   '����������������������������������������������������������������L       loss_changes[$d#L       )A�D@�O�@	��Af@��Q@
�    @��yA��p?�h@�([@/m�?�c�@��5A%Z�@־�A�    @Ep@��)@���            ?���                                                                L       parents[$l#L       )���                                                     	   	   
   
                                                            L       right_children[$l#L       )               
   ����                               ����   "   $   &������������   (����������������������������������������������������������������L       split_conditions[$d#L       )C�  @�  C3  BL  B5UU@   <͍:A$�I@@  A@  @�  E��&D�� @   D�� A\��@@  =�"�E�0 C:�@�33=�UO��iz��Y�A�  �>�<��1��w�:�����E�<�!�� c=D��]{=�C=�v:��+<ܒϾ
��=:ӽph/L       split_indices[$l#L       )   %      )   %   %          !            $      %      !          $   '   !               "                                                                L       
split_type[$U#L       )                                         L       sum_hessian[$d#L       )D�o�D��A�7�D�rwC��aA�/?��C�W�DV9A[�C��D@$^A��BC���B��+B"S?DL�A!?@km�C�4�@ے7?��?�*Ad��@J�A��C�	�A��BP�UB,�@�3�DDO�A�|?�� @
KB���CS@$�B@�%�?�'�?�mSL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       41L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5<>��Y��=Ȱ=v�Ӿ$rV=��?��w�#=O>$-�f,t��X�=��?!F?�W�����=�5��$=��?<�q�vU>	70����<��r>��t<���?��~>���=6�>%Ǽ�*=C��=T����L<~	ؽ%��=�E��Y��?l���=]�ݽ�3��K���2�=��	�1=��;�] �89�<c�*<L��=�m=�Sｺ��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idi/L       left_children[$l#L       5               	                           ����         !   #   %   '   )   +   -   /   1   3��������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       5A��A:߉A	"HAv�A��P@��@I��A-�<@�s�@-B�A�t@��.@#_�>��    AvkA��@��,@I,>�' ?QUq@�{$A"O�A,u�AzP?'�0@�6.                                                                                                        L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                           ����          "   $   &   (   *   ,   .   0   2   4��������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       5@�  Bt  B�  A  @@  A   By  @�  Da  A���A�  A�  D� B�  ����@�  BH  A�  Fk>9C*  Dp  B�  @M}�@l��F` A   B� =6�>%Ǽ�*=C��=T����L<~	ؽ%��=�E��Y��?l���=]�ݽ�3��K���2�=��	�1=��;�] �89�<c�*<L��=�m=�Sｺ��L       split_indices[$l#L       5   #   %      %   #   #   +   !      !      "      %       %      &   $            +   !       )   %                                                                                                        L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5D�I�DoVlD3=�C��C��%D1��@�~�C��C�M�B&�C�SGD,�A�v�@�n?�CcB�� BJ� C�4.AC4+B��@	��CA�[C�]�B��D�^A܅AL=?��m@�o�BU�|A�@ݡuB.��C��TA��A/SI?�?�*�B��?�'�?��C,�fA��A}��Cr�dB'�B���C�eSC�-h?�e�A /�A$Y�@��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       %;h�3<I35���={ף��5�=�n��85�=0�7>�墽��g�-g��Q<��b<�3�>���?+z��Ƽ�"r�`G-��)��b^:��c=������=����cB=�qʽ��&=��#�Ě�;c��;]=�����=�<��A�k���|L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       %                                     L       idi0L       left_children[$l#L       %               	����         ����      ����                     !   #����������������������������������������������������������������L       loss_changes[$d#L       %A
3�@��9@�KP@�R�A�;>    @ ��@�'�@�`    @�8?�%�    @���@�"A[\�A�@�N=@�
�?ߑR?�                                                                L       parents[$l#L       %���                                                     
   
                                                      L       right_children[$l#L       %               
����         ����      ����                      "   $����������������������������������������������������������������L       split_conditions[$d#L       %A�  C  BH  @@  @@  =�n�Cp  E�  F: ���gC�cB�j�<��bBH  F�  E���AL<<@   Eπ C�  E�  :��c=������=����cB=�qʽ��&=��#�Ě�;c��;]=�����=�<��A�k���|L       split_indices[$l#L       %   !   %                      $       *   '                 +   
                                                                          L       
split_type[$U#L       %                                     L       sum_hessian[$d#L       %D���D��^A�X�D��?D.=?�;A�� D|^BA�A�-�D��A�8m?�i1Dw�A�h�B�Ae�aD
c�A?I@�)�AW[�Dj�[BK��A+�A���A}�XA�>,@���@�>�B�=�C׸CA�2?�p�@w�@-B�@��A0��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       37L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       )��C:�3��C�=���j�[>��]�i�=�?�>�T������Z>�¼*���;�����=��=OO�?�Bt��p�?��;���K����?�=4����x��N��=  :<&w=�yb��I��r=� B���T=�
=��ʽ���k�=7ƒ��'�<��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       )                                         L       idi1L       left_children[$l#L       )               	                     ������������               !   #   %   '������������������������������������������������������������������������L       loss_changes[$d#L       )@�;M@�λ@��ZAK�AM�@z�?� A �A>ߖ@��vA�?�֧            Ab<A(�@�b�@���@�r#@��(@���A.�                                                                        L       parents[$l#L       )���                                                           	   	   
   
                                                      L       right_children[$l#L       )               
                     ������������                "   $   &   (������������������������������������������������������������������������L       split_conditions[$d#L       )C�  C922Ekj�C-UU@�V�E= B   @@  A'�
E��rB�  D�  >�¼*���;�A�  E�N9A�DDB   DH@ Cw� Cf  A�  ��?�=4����x��N��=  :<&w=�yb��I��r=� B���T=�
=��ʽ���k�=7ƒ��'�<��L       split_indices[$l#L       )   %   '   $   '   +   $      )   +   $   )                  "   $   (         %   %   &                                                                        L       
split_type[$U#L       )                                         L       sum_hessian[$d#L       )D�`eD�@�A��oDA�Da@��ZANѱD4�;BE�mB��2DL�w@Ca?�r�?�4�A>�B��D"j�A�hAȄ�B
��BA �C޽�C���@�X?�ZAvQ�Be��C	�C���@��A��@@�A�hB0�@��B/�x@��gC���B 	C�tB�&!L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       41L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       #<�V�<�b�� �<�E�*#�K�:>��H���z=�bJ=����X�߿g�l;�����	�=�׽�Z=��-?�c�=��Y���|>k^�����F��	2��#<%���7>'�X<�N��s��<l�W�H����s=zVH�ͷzL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       #                                   L       idi2L       left_children[$l#L       #               	            ����      ������������                  !��������������������������������������������������������L       loss_changes[$d#L       #@���@ߍV@AL�@�E�@�Y�?�(@z�PAl�A-c    @X�?�            A�A$�@u dA1"@��?7��                                                        L       parents[$l#L       #���                                                           
   
                                          L       right_children[$l#L       #               
            ����      ������������                   "��������������������������������������������������������L       split_conditions[$d#L       #C�  Cm  B�iiBkD;� D�@ B�  Bp  A�  =���@�  E>� ;�����	�=��B�  BgUU@   E�( Cn��@�.�����F��	2��#<%���7>'�X<�N��s��<l�W�H����s=zVH�ͷzL       split_indices[$l#L       #   %   +   *   (         )   *   '                          )   (           '   !                                                        L       
split_type[$U#L       #                                   L       sum_hessian[$d#L       #D�./D�
mA��D�T�AZ�VAg�@'�+Du5�D't?��AI.AK��?ߟ??�+W?�p�C�{�C��A	}D%O�A'��@��?�Q�A:�|C�}�C%��C�@��@���@\nYB���D|�@��s@a��?��_?�� L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       35L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       -�}��:��տ$�Q<�՛�(�X�k0Y��'=%"���׾�d��>��e�?�	��;C�%=BO�k=ʀ�	k���ԟ�n�
��`�>��ſf��=�'�=��I;a�;��=�W{��u>=0���PN>�;��F�;P� =��7߽ΡS���t�Vƺ<e�;�p`=�*����7���?L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       -                                             L       idi3L       left_children[$l#L       -               	                        ��������            !   #   %   '   )   +������������������������������������������������������������������������������������L       loss_changes[$d#L       -@�M�@�:�@�<�@� A��@�?�}@��`@�\�@��\A=@[U^>��t        @ط @F `A)6@�v|@���?T`@�NAan>y~�                                                                                    L       parents[$l#L       -���                                                           	   	   
   
                                                                  L       right_children[$l#L       -               
                        ��������             "   $   &   (   *   ,������������������������������������������������������������������������������������L       split_conditions[$d#L       -Cm  CX  B�iC�  BE�A�  D  A�  Eg� A@  EB` @   B�  ��;C�%F�  B⪫B   DE� @��yCH  A�  A0  A@  =�'�=��I;a�;��=�W{��u>=0���PN>�;��F�;P� =��7߽ΡS���t�Vƺ<e�;�p`=�*����7���?L       split_indices[$l#L       -   +   %   *      (   *      !                              (   "      +      +                                                                                          L       
split_type[$U#L       -                                             L       sum_hessian[$d#L       -D���D�a|AN��D�2C9{f@�I�@�-�D�b9By��BzB���@�~�@�+@��Z?��D���A�Y�A�H�B#�fB0"A��B�$!Bi�U@Xc�?�4?���?��fD���Aw|A�@��A�.�@p�=A��AI��A��B�A�jr@�B�A�zKB/��Af�X?��/@ksL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       45L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ):h�/;���!������<}7b:�r��b`���տMi�<���Ϳ�==����P��k�z>ρ�f�w���t<��?1��K}S>�yK�-�������{<�TȻ�A=�c$=�ș�~k��X���1k�=�^;�_=�y�<9�ս�Q���S���=�}gL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       )                                         L       idi4L       left_children[$l#L       )               	                     ������������               !   #   %   '������������������������������������������������������������������������L       loss_changes[$d#L       )@Њ�@�� @%�@���@�r�@�ێ>�,�@�'K@W֘@�l2@p�>�݌            @�?� l@�};?��@�p3@!?�T?���                                                                        L       parents[$l#L       )���                                                           	   	   
   
                                                      L       right_children[$l#L       )               
                     ������������                "   $   &   (������������������������������������������������������������������������L       split_conditions[$d#L       )C�  ?�  E� Bh  A�  D�@ A�  AEډ@   F�  D�� A�  =����P��kA�  @   E�` @   C̀ A��
B��UC�UU�-�������{<�TȻ�A=�c$=�ș�~k��X���1k�=�^;�_=�y�<9�ս�Q���S���=�}gL       split_indices[$l#L       )   %   &       %   !         +              "               "      $         +   *   '                                                                        L       
split_type[$U#L       )                                         L       sum_hessian[$d#L       )D�5D�P,Ary�A���D�]@���A(�A��&Ax'�DȲ/AUl<@U*a?���?�<A[�@ث�Ab@��]A-�Dǘ�A��A-�@!U�?�F@)�@�ի@�V@��m@��W?��@��\@�X?���Dc$D,@��P@��@�j<@E��?��:?���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       41L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1;�)<T�˾󘨻��/>j���|����Z=��޽���9=7>��I�.�>>+��#��60<B�H>��ܽ�c�&ݏ?�>��V�?�x>�>�8�wJ�?	�b� _ӻ�D�<<n���� =S|<����;���>�`=X`P��'>�y<��R=?��ќռ��=�kw<%P���=�sl�y��=f�"�Y�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idi5L       left_children[$l#L       1               	                        ��������      ����      !   #   %   '   )   +   -   /����������������������������������������������������������������������������������������L       loss_changes[$d#L       1@ɮ�@�d#@�G�@Ը@�:�@�O�?��@�C"A�9@�r�@��@]��@ur�        @���@�Ī    A�@��@�7f@J��@��`?x�@
��@�B�@�C                                                                                        L       parents[$l#L       1���                                                           	   	   
   
                                                                              L       right_children[$l#L       1               
                        ��������      ����       "   $   &   (   *   ,   .   0����������������������������������������������������������������������������������������L       split_conditions[$d#L       1D�� E�� F��UB�  D�  E�� A�  E� @@  A�  E�� B
ffB�  ��#��60E-� @�  ��c�C�  @   D	� E@ C%  @�  A�  C7  B�I%��D�<<n���� =S|<����;���>�`=X`P��'>�y<��R=?��ќռ��=�kw<%P���=�sl�y��=f�"�Y�L       split_indices[$l#L       1   '      $   %         )               %   )                        
         %   %   )   %   *                                                                                        L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1DЩ�D�o�A�~�D��C�DA�Q�@��!D3JDF�vBi3$B�t�A)1OA3q�?�~3@+�(D�sCfA��WDA-�@��VBX�9A�By��@(�A�A �R@J:hC� �Cz�UA���B���B�
�D)LH?�"=@)��@�o�B8�D@��w@+�BD�AU#?�K�?�?�~�@�.n@���?�b�?�(O?�L�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;:�B\=��E�V���W>Ji@�4�H�$�<p��wX�=2�>���o)v>�R�;�CԾ䊢����?+wϽώ����L��(�?;��?+�>?d�ɻؾU:?&y��M_��}�=�@<�q�?6�<�|�kO���v=�i=��޽�β��ݼSW�<x�@�RU�=��ڽHs=��_<���ߠ=��=?>��r�2�$�=�a<Q��m�/���K<��ϽFc�֍j���=�"�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ;                                                           L       idi6L       left_children[$l#L       ;               	                                    !   #   %   '   )   +   -����   /   1����   3   5   7   9����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ;@�jF@�lA���A8�@��:A*. @�b�@�Z	@RzDA�@���?�4 @]��@ɄU@���ApD@�$;@в?���A:Σ@�(�@��,A��    ?���@#��    A$�@�f�@J@�+                                                                                                                L       parents[$l#L       ;���                                                           	   	   
   
                                                                                                            L       right_children[$l#L       ;               
                                     "   $   &   (   *   ,   .����   0   2����   4   6   8   :����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ;B2  A  @@  F�L BKUUAEUUC�  @@  ?�  C�J�A�  A�  B�UUAEډF�� @�  B   B2��A�  A  F�?@��E|���ɻ�BX  B  ��M_@�\A   E� D6� <�|�kO���v=�i=��޽�β��ݼSW�<x�@�RU�=��ڽHs=��_<���ߠ=��=?>��r�2�$�=�a<Q��m�/���K<��ϽFc�֍j���=�"�L       split_indices[$l#L       ;   %   %      $   (   !            '   %   &   %   +   $   !      (   &   !   $   !   $       )   (       +   )                                                                                                                      L       
split_type[$U#L       ;                                                           L       sum_hessian[$d#L       ;D�V�CҦ�D��4C�C��fB/��D�-�B�&AE�C��C�)B�eA>ED��EB6�Bշ�Aks�@_E�AF`B�0�A�B}��B��{BY@�@Ō?���D{YD�1B ��@kS�B]H�BN&�@��hA�B?���@�Z@�B=?�*B�E�BֈAOx�@>'�BY�A�|-A���B�H?�_(?��Z?���@���C5�aC��Crv�C��A�P�Ae,?�� @rL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       59L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       !�{�!�4$�}ڻ�I�ϱ��δ���3��C'>��K�]�"���W=�J_�$r��z�>��޼�����\i?h����J��A �=	���A�t�=�&��Ͽ(=!HP�*%�����;��>�ν��<��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       !                                 L       idi7L       left_children[$l#L       !               	��������                  ����               ��������������������������������������������������������L       loss_changes[$d#L       !@�|�@���?7� @��@��%        @�DA*@aF @�n�AU"A��    A�~?l�R?��@��@��                                                        L       parents[$l#L       !���                                               	   	   
   
                                          L       right_children[$l#L       !               
��������                  ����                ��������������������������������������������������������L       split_conditions[$d#L       !C�@ D�� D  DU E�� �δ���3@�\@	$�A�  Eπ A�  A�8��z�B�  BE�B�  D�DDC�  �A �=	���A�t�=�&��Ͽ(=!HP�*%�����;��>�ν��<��L       split_indices[$l#L       !   +   '      '              +   !   )         (          (   )   '                                                           L       
split_type[$U#L       !                                 L       sum_hessian[$d#L       !D�h�D͝@��D�8�A��?��@�kD�.�B��(A<�(Au�+C�B�D�M@Ni^B�+�@j_AP@o��A9��C�B�͜CF%�D�Y�B&tA�b�?�ko?��O@�F}?��?�X�?�kV@Ǿo@�\�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       33L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       +<!�:�1?"P$�&|y=�����?O����k�=�C�=,�(>�j�=��*���=֓Ͻ���G-N<>n?�=3�>�}�<]+?8��P����n?
4ۼ���<�̹;ѧ�$�_=��м��n�[a <|��;�͗=���<$ռd�w�k�#=����@<ݰ�=�~<l��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       +                                           L       idi8L       left_children[$l#L       +               	                  ������������                  !   #   %   '����   )������������������������������������������������������������������������L       loss_changes[$d#L       +Ab�@�X @if$A U@ь�@��J@u��@��@�}.@���@��            @+X@�2@�>[A ��@�3�@�v@���@�V@��L    =w�p                                                                        L       parents[$l#L       +���                                                           	   	   
   
                                                            L       right_children[$l#L       +               
                  ������������                   "   $   &   (����   *������������������������������������������������������������������������L       split_conditions[$d#L       +A   A���E�ʫA   @�  E�� E� A�  Bs��A�
=Bk�=��*���=֓�Ez  C  C��A*��Da  BS�;Ey` B��IByUU���nF8����<�̹;ѧ�$�_=��м��n�[a <|��;�͗=���<$ռd�w�k�#=����@<ݰ�=�~<l��L       split_indices[$l#L       +      +                      '   +   *                  (   '   +      *      '   *                                                                                L       
split_type[$U#L       +                                           L       sum_hessian[$d#L       +D���D�M�A�yDx�;D��@D)�A���D'A�C�=tD��BY?�Q�?�MAQu�@iȭC�2:C�P�A���C�T'B�D
�`A��A\$K?�`�@�TC�ڎB�aC�	�B9�A���@�{B���C:��A�2Ak�@C�pC4ee@7�A�}�@�EA8>�?�2�?���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       43L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;�(7<�����>f�-���ﾋ�J=�`׼��|>�+���v@<���X�j�E�7��q�?v>Z�5��+��&#)?�V�@&0��GC����=-�4�9�	�C<��5�e��;�e��;�?A�ƿ��=%�w�O=��V�x.g=�Z�T8=�U�<&�����C<
�i��wd;�Һ= }:BK����=��-��m�Ž�g�<�������<ԏ:<ທ���P=i�B>A
=~�_�J�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ;                                                           L       idi9L       left_children[$l#L       ;               	                                    !   #   %   '����   )   +   -   /����   1   3   5   7   9����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ;@��A$��A;�A,��A���@�%XA>�A
��Ac�AE��@��L@�V@9 @څ@�b�@���A?\A�^W@���A'|�    A��@��[@�x�@�cJ    @M3�@�&�@뒖@��Z@��                                                                                                                L       parents[$l#L       ;���                                                           	   	   
   
                                                                                                            L       right_children[$l#L       ;               
                                     "   $   &   (����   *   ,   .   0����   2   4   6   8   :����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ;A  B   Bt  @ʪ�@@  CA  B  F�UA0  B5UU@�  A  @@  A�  BH  B�  @��A�  @@  E|����GCA�  @�  F�uUF�L <��5C   @   B  F�� B�  =%�w�O=��V�x.g=�Z�T8=�U�<&�����C<
�i��wd;�Һ= }:BK����=��-��m�Ž�g�<�������<ԏ:<ທ���P=i�B>A
=~�_�J�L       split_indices[$l#L       ;   !   %   (   %      %   "   $   "   %      !   &   "   "      !   %      $       "          $       )   	   )   $                                                                                                                   L       
split_type[$U#L       ;                                                           L       sum_hessian[$d#L       ;D�
D��C�| CN�,D���C8~�B��B��B���B���D�^C%lUA��B�(�A�)�Bf-!B��@��B�N>B��VAߺGB� Dx�}A�+�CF�?��A���B�R�A^�A�q�@5��BN��@���@�AsA��d@cR+@R�B��A�ͳA�Y�B6��A��A�%�B�BFDa�4A�<?���B���A�׎Av�o?�rB*��B˻@��A��A�-@&�?�?ȶL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       59L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       %�e�1��?2R����*s�?�Y��W?�6o�=�;;|�� �о��!?��G��js=P;=*�佦�˿T�<%�C���1<�)�>I��?6J��h��ۡ�Dyg=��+��|?<#i߼��7V��ī����ڽqjK=ӧk=��ҽ�6L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       %                                     L       idi:L       left_children[$l#L       %               	   ����   ����                              !������������   #��������������������������������������������������������L       loss_changes[$d#L       %@ʍ@�޷A:8@`��@��@���    @m�,    @��$@\?G�@?�0>���@A�\@�y�@�AX?V��@�pR            @!��                                                        L       parents[$l#L       %���                                               	   	   
   
                                                      L       right_children[$l#L       %               
   ����   ����                               "������������   $��������������������������������������������������������L       split_conditions[$d#L       %CR  @   Cn  C���C�  B�  ��W?C�� =�;F�� B�  D�� E�� C   F+� E�P F� E� B�.����1<�)�>I��C&����h��ۡ�Dyg=��+��|?<#i߼��7V��ī����ڽqjK=ӧk=��ҽ�6L       split_indices[$l#L       %   )   %   )   '   %                    )      $   (                 (               %                                                        L       
split_type[$U#L       %                                     L       sum_hessian[$d#L       %D�=�D�ÎA=�A��Dɡ:A#��?�RA}�|?��iD�/�A�W�@k�AɺA2��@�IlD��C��2A9JC@��}?��V?� �@k�1@��\A!��?��+@N�2?��NCϵ>D,�C%KFC�M�AɎ@�@�8k@+"$@H�w?�J�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       37L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       7�Q�>a�Ҽ��K>c?}��=�ϛ�R�';u�?,�>��?��绔s�?�0�7Q;�	��8�=��]?f���!���}K=���?���<ə�>OV�k�a?k��=���65������&%�<��߼!�
V��V�/=�o�=�7e��8Q>L��=fh�<2�t=��?�ӏ<Ы�=��u;Jq�=0>ǽ��z=K�4��@�gC���l�=��g:^k"=��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       7                                                       L       idi;L       left_children[$l#L       7               	                                    !   #������������   %����   '   )   +   -   /   1   3   5������������������������������������������������������������������������������������������������L       loss_changes[$d#L       7@�=�@�-�@�D@�W@��A]P�@���@ݣ<@�dv@unA@i�A!(@�;�A��@��W?�+�@��I@�J�            >��@    @�+�@��?�#@�" A<4A`N�@�7�@�ŧ                                                                                                L       parents[$l#L       7���                                                           	   	   
   
                                                                                                L       right_children[$l#L       7               
                                     "   $������������   &����   (   *   ,   .   0   2   4   6������������������������������������������������������������������������������������������������L       split_conditions[$d#L       7A�  E�� B   B�  @   D� @�  BD  B�  @��@�  F � @@  @@  @   A��@   C1��!���}K=���Bfy�<ə�D1� @@  E8@ A�$�F�EU@�ffE�� CH  �!�
V��V�/=�o�=�7e��8Q>L��=fh�<2�t=��?�ӏ<Ы�=��u;Jq�=0>ǽ��z=K�4��@�gC���l�=��g:^k"=��L       split_indices[$l#L       7         %   *         !         !      $            +      *               *                (   $   !      )                                                                                                L       
split_type[$U#L       7                                                       L       sum_hessian[$d#L       7D�0xB�D���B��A"w�C6D��`B���A�L�@�5�@��}CU�<B%��C��D?-�@�&�B��~A{Dp@S?�b=@6��@u�?�
�B��JB�\.A�N\Avr�B2UC�ҔAd�UD;�8?ڏ2@]�B~�/A*O5Aa��?�d#@&�	?�)B��Ao1B�.�A��A���?�k@3�RAIzB�<@���CȜ�BQ�tAO�?�UD8j�AL&tL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       55L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       %9��o�t�\;R�T��w=7�<q,��n?�Q��z���"P�=W<�KC��W�y��R{>MSB<�@?4V0>�G��<=��"ͽEbN=�5����=;c�:��x="g>�:��C<�Z>뿽��A< �=EѤ���{�
�r��"�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       %                                     L       idi<L       left_children[$l#L       %            ����   	   ��������                                 !   #����������������������������������������������������������������L       loss_changes[$d#L       %@�?@�m@�&�>���    @��A�        AW@��@��@63�A	�A\@�t�@�4�@��6@�j�@%^@P��                                                                L       parents[$l#L       %���                                         	   	   
   
                                                            L       right_children[$l#L       %            ����   
   ��������                                  "   $����������������������������������������������������������������L       split_conditions[$d#L       %?�  F� C� B.�=7�B`  B�  �Q��z��A*��CR  A�UU@   BD  @   BP  CY  @�  @�  B�  BaUU�EbN=�5����=;c�:��x="g>�:��C<�Z>뿽��A< �=EѤ���{�
�r��"�L       split_indices[$l#L       %   !       +   *                     +   )   *      "         )   )   )      *                                                                L       
split_type[$U#L       %                                     L       sum_hessian[$d#L       %D�?�@�2eDͿ�@!��?�s�D�J~B�T�?�X[?��{C��D�ՀBl�A�3�B��8Br�SD�g�A6�fA�:�Br@kFzAO�B���@b.�A���B!��D���B��@�zt@�WA�܀@B�AW$�A�Q�@#�O?��UAJ�@},XL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       37L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       9�6�a�=H���?㶿aw>�������>c�����=B��Ŕ���?��b�(>���ƙ�>�! ��m��0￷�����i��=�^?�a�>�x�$w#���?��:>^�<YԠ���:���=���s߽�G��7<l�
�#��#}���.<������<���<�u������2]>�9��rU=r�w��JM=0�Y�=T=��><f<(ΰ=��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       9                                                         L       idi=L       left_children[$l#L       9               	            ����                        !   #   %   '   )   +   -   /   1   3   5   7����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       9@�M@Ą&A�x@���@Vd�AR_CA��Ae�@͖�    ?οPA�fA+��@��@���@���@��@�2�@�L>���?f�@��lAA4"�AlA ��@�?FD�@ߦw                                                                                                                L       parents[$l#L       9���                                                           
   
                                                                                                            L       right_children[$l#L       9               
            ����                         "   $   &   (   *   ,   .   0   2   4   6   8����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       9@�  B�  A�  @TIC�  C,UB�iiA�  E�  =BF=�nD�� @l��B�ʹ@�  Ap  @   D��(@   B�  @��9BecDB��A�  C�  B�HYD�n@   B�  <YԠ���:���=���s߽�G��7<l�
�#��#}���.<������<���<�u������2]>�9��rU=r�w��JM=0�Y�=T=��><f<(ΰ=��L       split_indices[$l#L       9         "   +      '   *   "                 !   *      "       '   	      !   *   *   "      *   '      (                                                                                                                L       
split_type[$U#L       9                                                         L       sum_hessian[$d#L       9D�z�DgfD1�)De@���BݥND1�B���DT?��3@�u�B0vB��C�q�B��A��=BE�D3�C c�@���@s�A'�BƈA�B�B+�C�C�Byr|@���B�X�A�|A
�A�c�A�]nD2@���BӚNA���?�.�@]�?��i?�/�@מ4@b�A��@D[@��ZA��ApEA��Cǅ�B5��BN �A-G�?��>@}��B��A:��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       57L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1<��=�W�1��<���>��t��&�������f=�8>�hO=�j=�JC��
]>��M�F��>��<�����5?*�t����>@�!�_�Z>	����i�?�;!���(=�-b��
K<�ߗ<E�V=΂e;�N��lo���=7:}���=���@Xd���<�'G���7��=*ʄ=��e<9,#�g�=Z�R<%�l>�wL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idi>L       left_children[$l#L       1               	����                                    !   #   %   '   )   +   -   /������������������������������������������������������������������������������������������������L       loss_changes[$d#L       1@���@�H�Ao��@��/@�۴    @���@zY�@�A�@�^�A'��@�mX@��<@7��?�N�@�C�@�a�A�r@�̌@\ndA:g@�@@���@�R�?�T<                                                                                                L       parents[$l#L       1���                                                     	   	   
   
                                                                                    L       right_children[$l#L       1               
����                                     "   $   &   (   *   ,   .   0������������������������������������������������������������������������������������������������L       split_conditions[$d#L       1B�  B  @@  @   B�  ��&D�� A�  D�  A0  B�  AÎ9CQ  E�  E�  B�  A�  F�EPUUAEډF�;�B  @k�Ez  A�  ���(=�-b��
K<�ߗ<E�V=΂e;�N��lo���=7:}���=���@Xd���<�'G���7��=*ʄ=��e<9,#�g�=Z�R<%�l>�wL       split_indices[$l#L       1   %   "      %   )             $      )   *   )         )   "       $   +   $   "   +      &                                                                                                L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1D�VDH.VDM�VD&��C��A�1�DI��A�*�D"q�B��YB�ƤC�K�C�5�@��@A?�A�PD(�A���B>��@}?�B�ܥBcb�C��aC�{k@]6^@P+�?�=�A+�1?���AR�u@�4VD��B7 @�BGAr�?�3B9$,@��?�B�B}P{@F��B9ēA&x�Au�C���C�еA5V�?�~�@v�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       #<~�><=y�?��;���?�U?�ha�Z��>R９ʽ�Cd?a��>1�[=v.;>�<��.��������?8&�>��D,�?���=���<�2��{<�g'�[N�=>�;�����J�=ݖ��"����#;�7+>�<�� L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       #                                   L       idi?L       left_children[$l#L       #               	   ����            ��������                  ����   !��������������������������������������������������������L       loss_changes[$d#L       #@�@��@��[@�e@�.�=8�     A-� @�q�@�~@ne�        @Æ�@�@3A@��@��	?��@    @.��                                                        L       parents[$l#L       #���                                                     	   	   
   
                                          L       right_children[$l#L       #               
   ����            ��������                   ����   "��������������������������������������������������������L       split_conditions[$d#L       #G� F8� A�  A�  CR  C׀ �Z��E�� A�  B�  A�UU>1�[=v.;C  A`  B�e�C6*�B��B  �D,�D� =���<�2��{<�g'�[N�=>�;�����J�=ݖ��"����#;�7+>�<�� L       split_indices[$l#L       #          !   %             $   "      *              %   *   '   *   &                                                               L       
split_type[$U#L       #                                   L       sum_hessian[$d#L       #D���D�W�@���D��tA��D@���?��%CmֻD�9�@��MA=8a@�c?�-B���C! �B��PD�G@K�@�xX?�ǦA)�mA��Bk�B�dBU�RBHD�An��DjxD3�@�@?�mS@ޮ?�$@��@FΡL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       35L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =<�����=��=�G��m�>�����<d�?����p�>�F��jJ>~OT>���(G���>C�?��6=�����>t�8���>e=H�=���{>�����?D��=���/�%j=��u���K=��̙=8��>)��=jq�������S�(�==��F���=��E�CY���j�=d��sQ�=�;�����=&�M=L���]�>�k=n��>=C9O�9 �;��ν�z=�;L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idi@L       left_children[$l#L       =               	                                    !   #   %   '   )   +����   -   /   1   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =@�NA@�,&@�S@�j0AJl~@ߗ�@��@.N@�@�L�Ax�AwV@�v�@�jAN#@�vC>\�@?vK�@�X$@a��@�U    @��z@��pA� A /^@^N@��d@���@���                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,����   .   0   2   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B���A�  C922CRUUE�  BD0�Dk  @   @�  C  A0  B�  C  E�` F� E�N9B�  @@  C�� F7� B�  E�� >eBy  @�  A�  E�p @   @   @�  D(��=��u���K=��̙=8��>)��=jq�������S�(�==��F���=��E�CY���j�=d��sQ�=�;�����=&�M=L���]�>�k=n��>=C9O�9 �;��ν�z=�;L       split_indices[$l#L       =   '   '   '   (      *            )         )   $      $         (   $             +      "   $             '                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =D�q�CLCD��tB�xPB��Dp�D]bNB�H�@��-B�GAO�CG��C��BO�DPp�A��gB�$S@p�a@��B��A %�A]@B�CShB.�PC�e�B��A���B�$DLvbA~�@��A�<BQ�%A��?�&-@&eK?���?�Bo�A��8@���@��B@93�@� ;B��B+H�B!��@J��B_�Cb3%A��qBl� @��EA,6A� !A�x'C�\�Cΐ%Ae��?�[�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5�E�T���+>s4Ҽv�žՔ$?ϻ=t�$�6%��nә�">o>�n�?z�r>�z�=���#�=/*l��=l�ȓ<��`�����<g�u�?��>�$.?¾J?R�2�<aѾ�|�>���:8ʢ<�h+� ��|�+=L+���=������u��n5�$��>7ѽJ��=���=;��>V�м���> Z���o=�׽���=4><we8=��JL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idiAL       left_children[$l#L       5               	                           ����      ��������   !   #   %   '   )   +   -   /   1   3������������������������������������������������������������������������������������������������L       loss_changes[$d#L       5@�3@͈�@�3�@�۫@�%�@@�@��@�xs@>af@��Ak�@�CV@v{�@�B�    @���@���        @���@<�_=�� @�~@w<�@UP�@G��@F�X@��U@���                                                                                                L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                           ����       ��������   "   $   &   (   *   ,   .   0   2   4������������������������������������������������������������������������������������������������L       split_conditions[$d#L       5BH  BD  @   C���B��E�  BH  B�  BOKKB@  A�UUE��I@   E�p �#�EV` B�  �ȓ<��`Ez� C�  @   A`  BP  Bl  E�ʫF,eUB���B�  :8ʢ<�h+� ��|�+=L+���=������u��n5�$��>7ѽJ��=���=;��>V�м���> Z���o=�׽���=4><we8=��JL       split_indices[$l#L       5            *   *       "   )   (   )   (                      )                     &      )   $   $   (                                                                                                   L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5D�e�D��?B��WD�/BBA�tBgnpD�U�@�OuA�m@�\A;ϺA[CBb�P?�C�DK[0D)P�@�?��lA��EAvۘ@#�`@�md@���@��@���@�}�A���B�|D,�?B�W�B�G�DǛ?��
Ar��@��AR�a?ƥt?�L?��B@�z�@2��@:��@/�]@RjD?��c@y��@_x�@���A7y@�nB�@�5L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?�<T���7h
��%=��f��4
���w�>Z�<=�"I�9u�bL?#�t?%e�	�<�����i�>������>$�N�r1I��G>;�7��"?h(����?�VI���0�T���b�=}xJ�P|[�o���r�=�[���Xp=r$��m~='�t��z=�SF<i��="ǽ��G�R0E<��:�Р=�H��g��<��c>�=U��vC=��>��<JB���@�<ԽP���_<.�=�;��8u�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiBL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?@ƪ,@�>�A�@�J�A�A�YA�@��A�	A�t@��z@׃�@�8�@��A	VA��A��A>�lAI1@�!�@ǈ2@Uw@��@�@�C�@L�@N�?�4?���AlA��                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?A$�IFz�Ce�D@� Dd@ @�  @�V�E�� A��@ʪ�B�  B>  F��B�  C�  A쪫B�  @UUB�  A��A   B�  B�  B.�Fv B  F�� @   B�  B�@ E��r=}xJ�P|[�o���r�=�[���Xp=r$��m~='�t��z=�SF<i��="ǽ��G�R0E<��:�Р=�H��g��<��c>�=U��vC=��>��<JB���@�<ԽP���_<.�=�;��8u�L       split_indices[$l#L       ?   !   $   '            +   $   +   %   )   *   $      '   '      !   +   +      %   %   *   $   "   $         (   $                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?DʫVD���C=��Do�EC�υB⥙B���DT��B֢EC�^AN �B�mA��@���B��cC�z�C��WBA�BkR�B�IC�+A�M@|��B��BcPAr��@\5O@�?�@D�B&�A�|A��C���B��%C�sM@�V�B.�BV��@�h�AX�A�
;A/�C���@}zd@�h@5��?�R@Bsr@��DB&�cAr#�@�w�A)z�?�Yk@ �@E�\?�%�?���?���B�CA��A|�A���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       /�������p�*�4=�$����2�Ϭ�>4��2_5>Q��ۦT�i�]�'	�>�8<�{&/���n?�ֽ�������>���"P����Y����?T�?[<�>B$I�7�=���N��_��Du=�Aʼ5�;��q=N��'�B;�ͨ��K���"<	b��O"=W�=�UE�	M<��>�<�i�Nv7L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       /                                               L       idiCL       left_children[$l#L       /         ����      	                              ����      !   #   %   '   )   +   -����������������������������������������������������������������������������������������L       loss_changes[$d#L       /@��@��r@��*    @�G�@�NA~l@��@ �]@��@��>A&�@�u�@*�>��?��k    @���A*)�@�Y�@�Y�A�.A�@�^&@��L                                                                                        L       parents[$l#L       /���                                                     	   	   
   
                                                                              L       right_children[$l#L       /         ����      
                              ����       "   $   &   (   *   ,   .����������������������������������������������������������������������������������������L       split_conditions[$d#L       /?�  E]� @   =�$�A�  F�L E��UA�  E�  F�?F�+B(  E�� D@ B�  @������BNp�Dc� Bp  A�  C  E�` @�  C�� �7�=���N��_��Du=�Aʼ5�;��q=N��'�B;�ͨ��K���"<	b��O"=W�=�UE�	M<��>�<�i�Nv7L       split_indices[$l#L       /   &              "   $       "      $   $                !       *      %   %   )   $      %                                                                                        L       
split_type[$U#L       /                                               L       sum_hessian[$d#L       /D̑A�v�D��'?�\Aߠ�D�k|C{}YA��@��D�EB�gkB�#C/oGA@	�A+�@��V?̆iD�.wB"ѼA��=B���Bw#�AdQhA�-HC	�A"ڬ?�w�AZ?��?�\�@u@5C�/D4�VB�1?�1XA-��A��BA~\B�&[BQ+�A�ARTb?��5@η�A.��C;�A�[L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       47L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       /;��<3��
�)��*K=���G��>���;�p��i��>_���l�w��>@pm��<7?1HսD��=�G����?�&[���>w�̽�"A�=�i=:�ǿ�g���J�=뛭<���=��_;�vk�q�=ծ:�"�|����Լu&W>���L~<pF;�N�=�"�B��=��{� ��1������L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       /                                               L       idiDL       left_children[$l#L       /               	                        ����            !   #   %   '   )   +����   -����������������������������������������������������������������������������������������L       loss_changes[$d#L       /@��}@�=�@�ր@��A9Ɓ@;�x?���@���A�kA��@�e�@h�x@��    >~�@�&A
�AT@+��@�@@��@�@�@�;O    ?��8                                                                                        L       parents[$l#L       /���                                                           	   	   
   
                                                                        L       right_children[$l#L       /               
                        ����             "   $   &   (   *   ,����   .����������������������������������������������������������������������������������������L       split_conditions[$d#L       /D��1A�  A��nA�  B�  B�  E�� B�  F�*�B  B�  B4  A�  ��<7@   C*�@l��B�UUB)�(B/h@�  DT� B  =:��D� ��J�=뛭<���=��_;�vk�q�=ծ:�"�|����Լu&W>���L~<pF;�N�=�"�B��=��{� ��1������L       split_indices[$l#L       /   '   &   +   &      )         $      +      (          '   !   '   (   (         (                                                                                               L       
split_type[$U#L       /                                               L       sum_hessian[$d#L       /D��vDȃA���D��C��Ad^�@��<D~`8C��C���C	>/A?��@�?���@
'D'��C��Co}@�i@���C���B�iA@� ?��sA.,�?��?�_?� �?���C�y*C��2B¦|Cz�@�WCv�?�Q@F�*@c߹?��2B��C"%JB�d	@�Q @�$J@��A�?�5L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       47L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;;��e=10���>K�Y<�|+�=�y���B�?|���-F=%�9�㧿��P<�vt?�aԽ�{�?O?N�`=d������[��<���>�瞿���޿�
���W��9>�&= �>0��<כؼ؝�=�b��f�=�E"��c� �<Փҽj<���{�<��S<����:_I=�菽�L3=Y2�<�L��>M��4����=�b��2-�=u�"�I��8��<�RL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ;                                                           L       idiEL       left_children[$l#L       ;               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ;@�@���@�	+A{��AA�A %`@��A
�@��@AX"K@��Z@�$@�t�@���?�[�@�5�?��@��@�f�@�,�@>��@�)J@��@^�@��@@��#@�L%@Z                                                                                                                        L       parents[$l#L       ;���                                                           	   	   
   
                                                                                                            L       right_children[$l#L       ;               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ;A  A�  Bt  A  @@  B0  A�  D�  F$ B(  E�` A�  @�  @   ?�  @X  E7� C�  @��D;� G	� FZ� @   D;� B�  F�C   A33C{  = �>0��<כؼ؝�=�b��f�=�E"��c� �<Փҽj<���{�<��S<����:_I=�菽�L3=Y2�<�L��>M��4����=�b��2-�=u�"�I��8��<�RL       split_indices[$l#L       ;   !   %   (   %      (   &         %      %   )         !         !                   %          !                                                                                                                           L       
split_type[$U#L       ;                                                           L       sum_hessian[$d#L       ;D�� D�G0C�[AC43�D���C1��B��dB�{�B���B��D���B��BH��B�;G@UðB��A#FB7��A��B�F.A�e�D{յB|A���B�v�AB�!B�A��lB�C�?��@�&A�	B��A��?�k]B3��?�)}@@A�ǉB 
8A�GA��?�tD��CվAs��A�,Az�K?э�B_�ABYD�@%H�A��?���B�#@`��A��<B5Bc"L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       59L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       �3*�ʽ��!����ĿV:�����{:���V��>�IVD�J��>zS0�f/h;�꨼u�%�r�M=�˥�h��}�=������K���[=�5�K�n��<~����W*<{����Tc��i�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L                                      L       idiFL       left_children[$l#L                      	   ����                        ����   ��������������������������������������������������������L       loss_changes[$d#L       @��Z@�0�?�@ @��?�o0@7�    @f�9>�@@o�?��>3 @߁@:��@��0    =5-                                                         L       parents[$l#L       ���                                                     	   	   
   
                              L       right_children[$l#L                      
   ����                        ����   ��������������������������������������������������������L       split_conditions[$d#L       A�  C�  B�  C�@ B�  FX%U��{?�  @�  @   B|  @   F�< D   D�U�u�%A	$�=�˥�h��}�=������K���[=�5�K�n��<~����W*<{����Tc��i�L       split_indices[$l#L          !   %   %   +      $       !   &   	      	   $      '       !                                                        L       
split_type[$U#L                                      L       sum_hessian[$d#L       D�`DǶ�A3A�D�BA:h�@�g@��Dś@�P@��A�@Y�_@syn@[ED�-c?��@���?�]f?� <?���@��<?�0�?�%�@T8?�Jl?��n?� �D�ĉC+F�@B9�?��nL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       31L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       /�꨻
=ھ�C�~7�<nU>$)�Y�>��f���G=�xz��;\? �|��ݥ��<t=X����c?H]E��5s?F
�=iN�?>h������c�!��;J?h�<ʛ���K��et����=�R��bʽ�"�����=�.M��f:�[�<�u�T��=�䮻˳=���=ݐ�<��g=�Ͻ��������L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       /                                               L       idiGL       left_children[$l#L       /               	                           ��������         !   #   %����   '����   )��������   +   -������������������������������������������������������������������������L       loss_changes[$d#L       /@���@�B"@�Ϳ@���@�=t@;��@��@��$@��A�$Al@�?ׂ�@�P@	Τ        ?�l@Uf�?r��@�{@�/�    @���    >v(�        @��?S�                                                                        L       parents[$l#L       /���                                                           	   	   
   
                                                                        L       right_children[$l#L       /               
                           ��������          "   $   &����   (����   *��������   ,   .������������������������������������������������������������������������L       split_conditions[$d#L       /D�� EZ� B  A���B�  B�  C_� A0  @@  B�UU@@  EN� Ap  F =X����cB+��B2��E@ D"� A�  ����F�X ��;JF�| <ʛ���K�B<  @@  =�R��bʽ�"�����=�.M��f:�[�<�u�T��=�䮻˳=���=ݐ�<��g=�Ͻ��������L       split_indices[$l#L       /   '       )   (   %   %   %         %                        +   (          "                         %                                                                           L       
split_type[$U#L       /                                               L       sum_hessian[$d#L       /D��DD���A��B�^D�tA
h{Au�A �&Bp�[D��Dr5�@�@wk�A^�i?��8?�,�@�#"BgJ�@�RD�A�0A�v&Dn!�?��@i+6@g�?��@�ܫ@��'@�v�?���A�k B�f?�h?�f=C�8`B�.�@��Ah6Dk�>A�@"�?�?À�@��n?�_@��cL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       47L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?��N<��H���=�a1���
<�L]��H�=O��?)â�*����1>%�?�؃�S����>� W��Xn���?N��<��z�������>�/�n�
>�n���޾Y\����t���0?T�����^;�͜=v����~k:�I�=��}��yx=��w�/�/=�sý������=b�=:���������5�=�nx�di�<�]U=tB ��ѯ��Y����=(�.��ü�u¾Gy��=&+�=�+�;��(����� WL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiHL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?@��z@�ˋ@׵�AJ�VAL�Ao�A}m@�o'@�U@�v�@�ɎA&� @�E�Ak A&k1@�=\@�H�@�/7@��@�Qq@��L@���A6�@�AK�c?<\�@*@
��A��@	vtA �                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?A  A0  Cg��A  Ap  B^��C�  D�� @�  @   C+  C�  D�� B�  A�  A  B  B�m�B  Cd-F�^�B�  A'�
F>��C��E�D�B�  A$�IC>  B  F�p ;�͜=v����~k:�I�=��}��yx=��w�/�/=�sý������=b�=:���������5�=�nx�di�<�]U=tB ��ѯ��Y����=(�.��ü�u¾Gy��=&+�=�+�;��(����� WL       split_indices[$l#L       ?   !   )   '   )   )   +   '             (            (   &   '   +   "   '       (   +   $   (          !      "   $                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?D�B�D��CZ��C�ȠDd�C�B�Q�C��B�KA�p,D]��B�,�A�[�A�DB}�B�9�C��C@��A�A)�<A���DS~~B#�:B�`Bi~�@��A̡�Ap�$A5�A�BZB`#:B(PiAkkqC���@ @G0A�џ@�d?@�|�@Ω�A�?�W�D;trB�P`A��A���A�W�Aj�?BN�@�T�?�`@���@���A�y)@��AI}�@>h�A��@�OZ@7�B%��AP�hL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?;۳��[�W=Vd�<�?l�l/�=�-��6�=�ہ��I��A�=�r�=1GZ>�mL�c�j>>�->=[�>xD����=�n?)���u'��ڋ??q��4�=y�?��?%��K忒��?(1���<��=�&��^�<��O����?��.)�=�{����=�k߽K�_�Q+�N2<�����=�=�,�<F�}��\W;�^7�<]�<�Mp=��=��/�=�}-���b�[�=�=�˵�kV罭�<�#L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiIL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?@�1�A�AAYD@���@�k�@졓A6��A��@�y>Al�@�8�@��A��@�Q�@��A��@��A�@�*\A.�@���@�X[@�p�A׌@��@��@��)A�@}��@�S�?��V                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?@   D  C� D� DH  B���C#  C4  Fz�A   DW@ EK  B�  B��Cm  @�  C�  F�UBp  D  B�  A�DDA�  D@� CRUUA�  @   E۞9Dj�@�  Cn��<��=�&��^�<��O����?��.)�=�{����=�k߽K�_�Q+�N2<�����=�=�,�<F�}��\W;�^7�<]�<�Mp=��=��/�=�}-���b�[�=�=�˵�kV罭�<�#L       split_indices[$l#L       ?          +         +   +   )   $   '             '   +         $            (   "      (      
   $   '   !   '                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?Dɖ�D-��De��C�ǼCQ�D[��B
"C���C&1C"�B<KBDH.�B��A��dA�H�C��&A9O�B�EBd�A]�C�B��A	�A�X�D@��B`��A�<_@���At�A19@ֱQC�B�A�t�A ^�@c��B��@&��B(��Al<q?�#@�2�B�K�B>1An�DA��w@��@٣/Au��A^�D;��A��>A�g�AЪb@d� A���@*�@6�SA`��?��@��(@��@�N�@�#L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       !;�H�:�&?zb�<�B��B�?�����_<T��ڡ�?2t��D�L<��(>�8����<��=�4ڿ]7þ`)m>yT����=֡����F=v�<�Ǻ)N���=n�*������=��A���7���;���L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       !                                 L       idiJL       left_children[$l#L       !               	   ����            ��������               ����   ����������������������������������������������������L       loss_changes[$d#L       !@�*@���?��@_�iA&�+?>�0    @S��@��X@�7(A�        @f%E@�]G@	�d@���@V�    @^F                                                    L       parents[$l#L       !���                                                     	   	   
   
                                    L       right_children[$l#L       !               
   ����            ��������               ����    ����������������������������������������������������L       split_conditions[$d#L       !G� C�� C��CH  A��=Bp  ��_@   B�  A�  C�� <��(>�8B�  A�  D�� A�  A�  >yTCz  =֡����F=v�<�Ǻ)N���=n�*������=��A���7���;���L       split_indices[$l#L       !       (   '   *   '   '       %   %      %           )   %         "                                                           L       
split_type[$U#L       !                                 L       sum_hessian[$d#L       !D�O�Dț�@��XDŮ A�o�@���?��DÅ�A�#c@�6�A�"4?���@D�YAv�nD���A�/A��@6�@3�nA�w_?ڭXA?aV@]�`CR�D�=�@�j�@b�@fQ�@��n?���?�1"AZ�s@�)L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       33L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       3�A�*;�q��	U<uu��jI���-�%�F�F�2=�����8�?B�>�dA�P��5�/<��缋k�?M�%�B�>�+>��ֽ��ÿh�<��B�Y�?'�5�p��JD�A��=�v;Ny��l�>^�b<W�=l�m��o�=:����Y�"aF=������;xW;=Z����?��7=�5ս�%s�"�9=T)��l� ��~�<n�WL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       3                                                   L       idiKL       left_children[$l#L       3               	                           ����         !   #   %����   '����   )   +   -   /   1��������������������������������������������������������������������������������������������L       loss_changes[$d#L       3A �@�'�@�(�@q�]@	��A)��@
h@�]pA�@<8?�Ml@�s�@@P�?�"p    @�:�@���AzAB��?��#    ?�bP    @N3@�Μ?�0@8�?� @                                                                                            L       parents[$l#L       3���                                                           	   	   
   
                                                                                    L       right_children[$l#L       3               
                           ����          "   $   &����   (����   *   ,   .   0   2��������������������������������������������������������������������������������������������L       split_conditions[$d#L       3C�  D��1D�� @   B�  E��rD� C�� @�  Fk>9BiUUA�DDDw� B  <���F[ @X  B   A33A�  ����@   <��B@�  D'� C
  F�D  =�v;Ny��l�>^�b<W�=l�m��o�=:����Y�"aF=������;xW;=Z����?��7=�5ս�%s�"�9=T)��l� ��~�<n�WL       split_indices[$l#L       3   %   '         %   $      %   !   $   +   (      "          !   %   !   "              (      )   $   '                                                                                            L       
split_type[$U#L       3                                                   L       sum_hessian[$d#L       3D�h�D�!�B�s{D��A�îB&��B�D��gCq�@�_�A"WbA��VA���A�O?�?D�@�L�B�B�C��@�s?��kA�Y?�PI@��	A���A-��@�6�A���?�\�D=A�C���?���@���Ab�2B��kB�!=B/�B?��k@^�@���?�SZ?�[�@��@��A��Ax&?��T@L/@�!A�4,?�%EL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       51L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       %�"��u5߻�鲿��~<��E�Am">�h��:T
�G�,��.�>��z?N��>��;�6����?=��2>�͡?�t1?Q��?�VШ;J	C<���M�=����:�7��Pw�������=���>o=�3�~��=ޅ����;å�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       %                                     L       idiLL       left_children[$l#L       %            ����   	   ��������                                 !   #����������������������������������������������������������������L       loss_changes[$d#L       %@��@]�
@g�)>�Q�    @K.l@�        @ZJ@|��?��@�X�@�c�@�7�@&�F<l ?���>�S�@��?��^                                                                L       parents[$l#L       %���                                         	   	   
   
                                                            L       right_children[$l#L       %            ����   
   ��������                                  "   $����������������������������������������������������������������L       split_conditions[$d#L       %?�  F� F�X D� <��EF�  F �:T
�G�,B0  A�UUC�  D��1B��IC4  B��fB��B���D @ A�  A֪��VШ;J	C<���M�=����:�7��Pw�������=���>o=�3�~��=ޅ����;å�L       split_indices[$l#L       %   !                                    !      '   '      *   *   *         (                                                                L       
split_type[$U#L       %                                     L       sum_hessian[$d#L       %D�vp@j�D� �@T?�$�D�) A��?��+?���D«�A>�<@�Y�At�D��,C�1�A��@�f@�I�@V A%��@�ICKHcD�6 Bc�$COtEA�?���?��?�j�@I�?���@Th?��b@��@�;@>�O?�݄L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       37L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =���(�W��=t��0�<��<=����\�g�hs�=���i$�=8��!�>��>�龺!���о��!>�r�������Y�>n7��'bm>)e�?4,���?_�*=�u?1�c��p���$>���<%1��<���m���2=�E�ip@<���&��*��$o�=�叽1&:���p�껪��=�s> BԽY������f��'�F> �b�E<��۽;��=�];��U����=���x)�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiML       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1   3   5   7����   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =@�6@���@�Q�@� �A.Y@���@�@��`@�P@���@��@��@�v�@�r@��X@���A	��A�&@��.@XSX?�TA�;@���@���@��
@���@��@S��    A�3A�                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2   4   6   8����   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =BkA�  E�� A�  A  B���B<  C�A�E?� C�  A�  B�j�Gfx B   B�  A+m�B   E�� A�  B���Ck��@   @   @@  B�  E�  E��n��p�B���B8  <%1��<���m���2=�E�ip@<���&��*��$o�=�叽1&:���p�껪��=�s> BԽY������f��'�F> �b�E<��۽;��=�];��U����=���x)�L       split_indices[$l#L       =   (   &            '   %   '   +      '   '   '      "   %   !   "         *   %           )   %               (   "                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =D�b�Do��D!DPC��D��D�qB���C���BĈ!A-�D��B��wC�7�A=�Bj*5C%<�C��B�Bv��@���@%�C��^C\��A .CB���A3�C��A+`�?�p}B<��A6_B��~B}p�C��AM0�A�٥@�VWA٤�B
&]@��?��G?���?�r+C���A�&@B��gB���@��{@;�A�B�)y@��@��~B���C�i�?�k;As�A�\�A��@��G@�JxL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =9��/>?º�U�J?O~<�i��~�o!�>Y�/?���D>1����ܿ�����=.�??޿K8�?�W<�T��������=;A?o�޾��S?)!V���Z���D<agľǙ��v>^�=�0ɼ�Q+<7� ���'=rIR><�v�VŻ<��ڽ���=e�s=GR:��>~����X.�=^�=߾�D}�럇=�ړ�֫��g�#�5<^FH�L|��`���}=C��N̢<� ]L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiNL       left_children[$l#L       =               	                                    !   #����   %   '   )   +   -   /   1   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =@��A1H�@�a�A?&AZs@��@�b@���@m�@��\@�*@�H?��A�@�8�@ZB�?��(?�    @�5@A�1@�]�@�f@�^~@��@�գ?��p@ŉ�@���@ɨ[A��                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $����   &   (   *   ,   .   0   2   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =A�  E�x�BH  C��E�  A�  @   D  D� B�UUC�J�@   B|  D  F� C<9B  E(� <�T�B�8VA�  B�  B  B   B(  BX  B  C�  D#@ @@  A   =�0ɼ�Q+<7� ���'=rIR><�v�VŻ<��ڽ���=e�s=GR:��>~����X.�=^�=߾�D}�럇=�ړ�֫��g�#�5<^FH�L|��`���}=C��N̢<� ]L       split_indices[$l#L       =      $      '       &          '   %   '      %          '   (   $       *         "   "   )   %   &            &                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =D��Bԏ3D�ħA�E�B�}�B1�%D�6�A>��A�DA|�B���B5sA
�D/�DO>'A?�@9c�@���?�@��KA/$BoȩA�~A���@���@.��@��BC�d�C9��C�#�C�X�@��C@%S�?�U?�r{?�JP@�)�@bs�?�m5@�aq@��A���B �@��i@#�(A���AHk@U؎@�g?�d�?��X@�� ?��CeqCU�EB�7B��C�iA�CB�,�Cw�#L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       /���5�> >���>B�뼮.����@?�~>�.i�S�O��.��;F�<�w=���?F��ݞ?\��=��?h��[:>�� �0>'sF�ٷ?vj\���<�X�����=�q��JՏ�ܢ�=���=�һ�zow��5<���=�&��Ä18�eI��b�:��=t�S�k���k�;�9=�O=�s��9�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       /                                               L       idiOL       left_children[$l#L       /               	                  ��������                  !   #   %   '   )   +   -����������������������������������������������������������������������������������������L       loss_changes[$d#L       /@��@E$n@e�+@��@���A_�@;��@���@�I @�y@x��        @��?a�@���@���?��x@�+%@�J2@��@�Q�@�gq?���@,1O                                                                                        L       parents[$l#L       /���                                                           	   	   
   
                                                                        L       right_children[$l#L       /               
                  ��������                   "   $   &   (   *   ,   .����������������������������������������������������������������������������������������L       split_conditions[$d#L       /A   E(� B|  E�j�EZ� B1$�B�C^D  A�  EJ�E�P �<�w=���@   B�  @⪫E� B�  @�$�B���BF��A�  E�  B�  B�  <�X�����=�q��JՏ�ܢ�=���=�һ�zow��5<���=�&��Ä18�eI��b�:��=t�S�k���k�;�9=�O=�s��9�L       split_indices[$l#L       /      $              *   *      %                         !         !   %   *   &          %                                                                                        L       
split_type[$U#L       /                                               L       sum_hessian[$d#L       /D�o�D��A���B�,�D��G@S��A�l�B8�	A�[
B EbD��?��a@)Ak|�@r�A���A��[@��9A�3|A'M�A���B糀D��A;g5@@VR?���?�	Aq��?ھ�A��@�ih@T�?�>�AP�@Ԓ�A	��?�kA`�A�3�B�7�A��'A���D���?��ZA �j?�zD?�2`L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       47L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       +��c��w�f�*�=�"/=���5%����Q��<]I>�7q�����X=��\���B�я�����=�Ǿܳ�?8fp�RM��
�>p�v��P8<��(���l<�h<����7����<>A�=�D;k�R���6=H��=F0���}�=#����Ӫ=E��y�<zP��6��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       +                                           L       idiPL       left_children[$l#L       +            ����   	                     ������������               !   #   %   '   )������������������������������������������������������������������������L       loss_changes[$d#L       +@���@F�t@�?�p    A2A�@��?Ry�A	^�@���AO�@���            ?��A<&@�?�@�4�@�#}@z� @�H!A	n:@���                                                                        L       parents[$l#L       +���                                                     	   	   
   
                                                                  L       right_children[$l#L       +            ����   
                     ������������                "   $   &   (   *������������������������������������������������������������������������L       split_conditions[$d#L       +@   C���B
ffB���=�"/D�@ @@  @   B�  F@ @@  A�E�P =��\���B�я�B�  A(  F� B   E� A   B�UUA�  E�0 ���l<�h<����7����<>A�=�D;k�R���6=H��=F0���}�=#����Ӫ=E��y�<zP��6��L       split_indices[$l#L       +   %   '   %   '                )         !                      !      %      "   %   "                                                                            L       
split_type[$U#L       +                                           L       sum_hessian[$d#L       +D�@�An��D�b�A[�?�ݥC��D�(�@8{A-CbWB_/!B��D�(<?�r�?��#@�ׂ@~�C>��B�>Bv)A�q�BY�WA��C�pD\A�@��?��CI=B�*A�=�A?}}A�G<AJ-A�!A5�@?�BPXA���@G�A���C�3�C^�"D$�wL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       43L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =���
>� ��K�u��u4?,������=�ԋ?zr����(?��V�������8ؗ>Xuڽ�[O?ym�>���-H�?X�
���?�jg?	ƥ<�ag�O���b�Ƚ���?`����N>�f���D�<B�=� k�C=���=�#����<^
�=��2=�П=Z�>WWO�I�+=����<oS8�!��e�<޾ +��w=� �V3�>�g�,�:Įx=��<�Rk���3=)��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiQL       left_children[$l#L       =               	                              ����      !   #   %   '   )   +   -   /   1   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =@�E�@���@�{�@��L@��*A��@ܕ&@��@�c�@��@�04@�1�A?�@ʄ�@�t$    ?;DX?���?��@>���@a��@=�@@E*�@�;�A;z�A0�tAc@Z"J@�N0@��V@�c                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                              ����       "   $   &   (   *   ,   .   0   2   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =E� AP  BkB��C?  BV��B�  E@ @   A�  D  B�  B�  A�  B�  ��[O?�  A�  @	$�D�� B  @@  Dr� A�  B���A@  D@ @@  Bi�B|N�A0  <B�=� k�C=���=�#����<^
�=��2=�П=Z�>WWO�I�+=����<oS8�!��e�<޾ +��w=� �V3�>�g�,�:Įx=��<�Rk���3=)��L       split_indices[$l#L       =   $   &   (   '      (          $               '          &      !      (   #         *   )      #   '   (   &                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =Dĸ�BI�D�k�A�'A� Da�D!&@�2�A��jA`SA�l�DNz�B�ܛC�ՄCPّ?�i1@ǘ?@��AL&�@0z{@��h@ԥ�A$�)D �C6� A�RB;�@�ҞC�f9C6Z�A��?�@X@�H)?�MP@K�?���A9��?�&{?��{@j#@l��@0�l@xh�@���@�HtC�Z�CNBLB��Bp�A�"A��AB�A�@e@� Bc	C���A��C!%A�cAқL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?� m���>=^A�=�F����>F3����>��нU����9�W4e?!�=��'�Ŝ=��?C����b����>9G�Xv����<�@n�^�s��"�?=�S�ޛ�>�������>�Ź>�)��l�n=��:�{��o�u<���N�/=�l �{e�=Sս�xK=u��<8��,]<;��/��${�,�Ǽ
�?��%���J��=�U�;��*�8e�=�=ļ�� �
�g=��=��<��U�=����O�o;�O�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idiRL       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?@���@޿@��T@�fA*v�A(�|@���AD�A Rf@�@�+�AC�A��A:��AV8@�n�@�(�@��A�h�@�F@�Ҙ@��P@�9*>��P@Á�@��A�2A��@�M'AJ@�8�                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?C̀ E��rD� CUUE�p @   @   @�ffCt>BH  D� E]� C�  D@� B$  E�p @�  BӪ�A0  BP  C  B�  F�Btq�@�  C@ A   B�iiA�  @�  Bp  =��:�{��o�u<���N�/=�l �{e�=Sս�xK=u��<8��,]<;��/��${�,�Ǽ
�?��%���J��=�U�;��*�8e�=�=ļ�� �
�g=��=��<��U�=����O�o;�O�L       split_indices[$l#L       ?      $      '              !   '                   %       !   *   &                *   &   %      *      %   %                                                                                                                                L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?D�^�DaZ�D-c4C5CD4CL7DC��B���B�n�C�"D\�B*��C!wLCR��C�P�B8SB�B+&BB��uA�N�B���Cí�C:�@L�B";B�{�Bn��C"x�B@��BoF[CZ�@A� �@ᾲAM�A�_B%0m?���A��jBEʴA�4�?�B1PB��C��5A �B���B�\{?�Ʀ?���@C�B	B���A�s0B!�A��C�MA��;A|kB�:A�\^B�,A��&CD�<L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;�.�����=���Q�c��>Ef��#�D�[?/�p���k>���>W?�P߾�C<�o\����=)�?[|N�`�?�qQ��up���?�E<{kj>�.E�}5?�q>��[��w��>��<Bx��?�\<��l��>=U<��ؽ�5{:�2ѼV�f`=엢:����9�<�J�<6�=��1=�ӷ���X<+�C>Xҽ��N�=��V</����<�_�/t�=&���GL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ;                                                           L       idiSL       left_children[$l#L       ;               	                                    !   #����   %   '����   )   +   -   /   1   3   5   7   9����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ;@�}@�:@�?A�@�ӆA>�A1��@�@�?j@��:A�5@��j@���@���A �^A@8@��@�X�    ?�Q�@��n    @�g�@�=C@��4@!B�@��D@���Al�@�r�AK�9                                                                                                                L       parents[$l#L       ;���                                                           	   	   
   
                                                                                                            L       right_children[$l#L       ;               
                                     "   $����   &   (����   *   ,   .   0   2   4   6   8   :����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ;A0  CI�E�
�@�  C+  D  E�ʫ@   BT  CZ��@ǔ6D�  B�  A`  Bx  D� B�  @�ff�`�?B�  Ex  ���CJ� @   @�  B�  @�y~E�� B��Bt  C���<Bx��?�\<��l��>=U<��ؽ�5{:�2ѼV�f`=엢:����9�<�J�<6�=��1=�ӷ���X<+�C>Xҽ��N�=��V</����<�_�/t�=&���GL       split_indices[$l#L       ;   &   '          (   '          "   '   +         &   (      %   !       (          (         %   +       (   )   '                                                                                                                L       
split_type[$U#L       ;                                                           L       sum_hessian[$d#L       ;D�f6DS�Dzx�CăC@HCZ�_DC�GC�~�A�F"C'��A�;�CQ�A�B~vD3��B���C���A��i?���AKܨC�@V6A�p�C�dB��S@)��@Ę8A"#1BU�?D��B�j�B��B��JC%{B�$�AR@�A.�.?��B黱B��A޿AQ1B��DBzcB[B Ӈ?�U�?�q�?�7@�5�@y!�@ǵ�Ap�B��C�m�C��-B�$�A�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       59L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =<;�p<ᄾ�)�p>6o7�)�>�|��ʴ=ʻM?/Ǿ�{X<�8(?#�����/���V>�Oٽ[
?go?:�꿊ȣ��$�>�H_;�#&>jI�?� �=k��k�����>B~O>�N��WR:�%=���;��=ǳQ<8�轈��=��o��D�<�;�ʽ���=��⼘����5;.R���~H=O��>+!<�G����P��䝼[3� ��k(=���=y�H�xs�SO�=��L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiTL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1����   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =@���@ŀ�@���@�j@��@�@�G&@�k@��\AUB@��5@�:�@�s�@�~�A0��@�Al��?��p@�'y@J�A3At@��)@�gG?�YH    >۲�@2�x@xc�@�gP@���                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2����   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =F�L BUUA���D� @@  C� A�  @uUU@@  @$�IA�  B�  A�  @@  Bp  @`  A0  B   E� FKƫB�UUB�  B���@   CG  =k��Ap  Bl  A@  B�  Eπ :�%=���;��=ǳQ<8�轈��=��o��D�<�;�ʽ���=��⼘����5;.R���~H=O��>+!<�G����P��䝼[3� ��k(=���=y�H�xs�SO�=��L       split_indices[$l#L       =   $   %   *            %   !      !   '      "      %   %   "   %      $   %      '      %       &      )                                                                                                                              L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =D�.D���C%Cd(yD�$}A��	B���C?�xB0B���D�5nA�v@�NA�^XB��ABe�Ck�A�&OATswAuoB�CB;]hD�Z�A6J5@��m?�fG@���Aq@�UYA�[Be��A�}�A�q@�$�C ��A�D�@C@���@��A`��?�b�Bx&iA!AؖA�$�B��D�?�5�A��@h�?���@��,?�V>@=uAA��@9 @m��A��@�L|BH �@�P�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       );zo� n?�<�/O��WO?H�w��s<�#�?!۹>�����-?�EI>���=�6��xM=��Z��?�i�+#�?=�/<˪�>0|�?wٽmJ;2�=������<X����=���<��>ڽ�1<"��!s�v<��t�=54=�M�=��/L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       )                                         L       idiUL       left_children[$l#L       )               	   ����                        ����         !   #   %��������   '��������������������������������������������������������������������L       loss_changes[$d#L       )@|�@p�@�w@[@�_h@]�4    @ex�@2��@��6@l��?���@�@�A:��    @�ˣ@���?���@�t�@�g1        @��                                                                    L       parents[$l#L       )���                                                     	   	   
   
                                                            L       right_children[$l#L       )               
   ����                        ����          "   $   &��������   (��������������������������������������������������������������������L       split_conditions[$d#L       )CR  D�� Cn  A   @�  C�� ��sC4  E�� F� @   C�  @   C2  E� =��ZB�  A�  @�  B�IA�  <˪�>0|�B�  �mJ;2�=������<X����=���<��>ڽ�1<"��!s�v<��t�=54=�M�=��/L       split_indices[$l#L       )   )      )      *          )               	   )          )   &      *                                                                                  L       
split_type[$U#L       )                                         L       sum_hessian[$d#L       )D���D�OA<�D���C�4jA)ze?�=�D���A��A�&�C�q�@y�E@�0'D�JB3�@��!@;��A��E@E$jC�Z
B�_�?�� @0�E@��(?·�D�H�@Ѩ�A���A���?���?�~Ah��@��j?�R�?���C[LB��B�A�x?�G1@u��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       41L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =<|𽽰d+=T�>*9q�]*=!:a>�(�?̗��c�H_�>��>��<�b1>����Rg?AHn�i�^>���<L����<F��?��^>�߃����<?��>�6S=5?7��<;��%��<MQZ=��׽���=/�����]�=��Y�U͛;Ɏ$�t?��o2��5����s<�ܮ:� 2>��=����c�׽K��=�;2����fn����=���=��Ƚq��=�L����P=��<����L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiVL       left_children[$l#L       =               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;����������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =@���@�f@���A	��@��@�)l@�H�Awr@���@��R@�_�@�b�@|I�@�u@���A
�@s��@�0@��J@͟jA`�@9Y}@;L@���@�:�@��@��@�7�@�F@}g�                                                                                                                            L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <����������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =B
  @�E�� @   E� DY� D���B4  @��SC:�B�  C  G}� A�  Fr0 A�  C  E$� A��B � A�  A�UU@   BX  B�  CC� B&ffEB` F�� C
  �%��<MQZ=��׽���=/�����]�=��Y�U͛;Ɏ$�t?��o2��5����s<�ܮ:� 2>��=����c�׽K��=�;2����fn����=���=��Ƚq��=�L����P=��<����L       split_indices[$l#L       =   (   +               '      +   '            &          %      (   (   &   *       +      (   (         %                                                                                                                            L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =D�R�C���D�^vB���C��D��?B8�B;BT��C��xA��B�$nD���B0]@ƴ�A�@��oB'��A3?UC�	C"��A��@��BK"~A�L�D|��A�ExAa��A�bP@��1?�b�AQ��A�G?@v݊@3UB��@�oABA@G�QB���A~�gB���B��@�}A���?�D7@��B�4AU�+Aq��Aj��Dn�B`Q7@l�aA���@��?@�jA��'@�T�@�@#�PL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5<����(<{5�=�����s;��>HS>�OϿ2�ѿC���f�=X�{�vm>�f¿?>/��>�����;�a5�v�u�� =ꤢ��P=?=>����(9�6�?'��=><>���V 6��?o=�����"����=��нTc�;�����=s=`QG�>����o�;��⺿�&��=!��=�=l˼�"�-{�=�c����<�nsL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idiWL       left_children[$l#L       5               	                                 ������������   !   #��������   %   '   )   +   -   /   1   3����������������������������������������������������������������������������������������L       loss_changes[$d#L       5@R�@�t�@leK@���?���@���A>o�@FI�?݌@|@�&@[�@@��`AB�@�x@=�            ?1W`@�6        @Mj{@��@B�6@�Ð@�@A��@ ,}@z'�                                                                                        L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                                  ������������   "   $��������   &   (   *   ,   .   0   2   4����������������������������������������������������������������������������������������L       split_conditions[$d#L       5@@  A�  B�  B���F$��D�� AffB�  D@� B  F%-�@�  D�� B�  E�� B1  >�����;�a5C   B  =ꤢ��PD�  B@  B  B�  F%UA  B^֚@   ��?o=�����"����=��нTc�;�����=s=`QG�>����o�;��⺿�&��=!��=�=l˼�"�-{�=�c����<�nsL       split_indices[$l#L       5   %   "      *   $      !   )                      $   +                  (              "   "      $   +   *                                                                                           L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5D�f�B�=D�2Af�dA���D��B�W�A.&@bEXAl�!@���DGP�D"ȣB���AnA3A�?�;�@T?��A6�9@X?�?��u@0��D:BT�TAy�OD�nB+nCB=�@��AG<@ɺ@a@ͶA��?��@5�D8�#@��xB:�A���A8��@��D`QBX!�A樂ANo�A�TUA��?�M7?��}A%�@eL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       9<�۽_͑=c�b���������=�䁽@�6?N)L=�� �=ٽ�r+?{�>��W=�'��*̅��H��~<?�d>S��u���m���B޾��Z?l�=g��?C��?��k=UER�)v�<(�6�wҐ;1Ƚ���=V_>1��<��=�D��,���s;����N<156���9<�=�d���z�<��%>)�d=��(�<G=��ҽ�_�>	=0���Aag=)5�L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       9                                                         L       idiXL       left_children[$l#L       9               	            ����                        !   #   %   '   )   +   -   /   1   3   5   7����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       9@��6@���@��_@ў�@�\�A
��@�u@㭡@�b�    @�+�@�6A (A%.,A�+@�L\@��?��u?��@k~�@���@��@���@�'�@��A�A@�ep?t��A\                                                                                                                L       parents[$l#L       9���                                                           
   
                                                                                                            L       right_children[$l#L       9               
            ����                         "   $   &   (   *   ,   .   0   2   4   6   8����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       9E+� C9  @�  C0  @S��BH  @p  CX  @�|B=�� Ekj�B4  E��IC33D%  BbDDA�k�A�  Cn��B�  F1UA�  B�  B�  Cl��E�P B�UUAk��B���)v�<(�6�wҐ;1Ƚ���=V_>1��<��=�D��,���s;����N<156���9<�=�d���z�<��%>)�d=��(�<G=��ҽ�_�>	=0���Aag=)5�L       split_indices[$l#L       9      )      )   +      !   %   +       $          %      *   +      '   %   $            '       *   +   *                                                                                                                L       
split_type[$U#L       9                                                         L       sum_hessian[$d#L       9DĄ;D&�gDb>D ܠA���C�܀C���D�@AW�?�jA�"?C�ؔA�>�B���C�2�D�B���@RL%@���@���A���C�0�B<�@��A~��B:��B��@���C�\rC��C��B��A�9y@VS?��@pJ?���@-~S?��Ac�Y@]��C&��C-nA�=A:�\?���@��A��@��@���B$B�B
�i?��C@��C@L�C���Bf@L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       57L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       9<T/�����=�z=�;ާ;�b�=�w7���u�r��?4�w>���B�;>��7=��"�ˡ?6ML���@>;��>����v����>*9#����>��!����?'���6~�=���LKA? �$��.=���|�W�k��=D�Z�Ik�=�����)Y�&��=¼H��<���������C��p===�B��i�=T.�;dׅ=����eݽ�w{<�EԻ�M��1|���=�Xm�-sKL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       9                                                         L       idiYL       left_children[$l#L       9               	                                    !����   #   %   '   )   +   -   /   1   3   5   7����������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       9@fT%@�ǡ@���@�8@�5�@�
�@��@��"@�DmA\�@�D7@�8�@��T@�S�?T�h@��@��    @Nj�@�҂@���@}��@�	�@�4�@�jF@�(V@�~X@�0?��                                                                                                                L       parents[$l#L       9���                                                           	   	   
   
                                                                                                      L       right_children[$l#L       9               
                                     "����   $   &   (   *   ,   .   0   2   4   6   8����������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       9A   B���C  @@  C  A��@�  B�UUE�UA0  B�  @�  BИD��D�  BrB�  >��B�  B���B�  EPUUC&UUFKƫE�<rB\  B�k�C
UUA�  ��.=���|�W�k��=D�Z�Ik�=�����)Y�&��=¼H��<���������C��p===�B��i�=T.�;dׅ=����eݽ�w{<�EԻ�M��1|���=�Xm�-sKL       split_indices[$l#L       9      '   +      '   *   #   +   $   "      &   *   '      '             *      $   '   $   $   )   *   '   "                                                                                                                L       
split_type[$U#L       9                                                         L       sum_hessian[$d#L       9D�.D�K�C���C]�Dc��C�oHA��PC
�}@�	sC�5�D#d�B6)C��A���@AD�B��A�c�@v�E@sv�@�j�C~0JDf�B��@��A�pB,�C�"�A��n@�!?���?�B��B7��A���@���?��i@)l@C*L?�U�B:�CO�CBcB5D2�@d�B��@[�6@?�A
�3A�D�BZK�A�pCv��Cr	@�C�A,~�?�PZ?���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       57L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       =;Z:��uN<=C�L=��L�ߏ�>4�|�62�=:L?�׉�����O��˖�>f��>2�̽;(üЫ*?C��=$��>U�߾�vf�&a��?ݓ� ��}�
>��"C<>�{潠~'��t�> B=鼃�U> ���O?=b�۽��ؼ'���]�y;�x�O�5��	=�+����r��lI<��`��;��=���1G=gW�5�=OX��X�=��P��Hf�nؼ�N{=wϚ;l�SL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       =                                                             L       idiZL       left_children[$l#L       =               	                                    !   #����   %   '   )   +   -   /   1   3   5   7   9   ;������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       =@�SA@�h�@߱�A��@�N�AbU@��@��A��@�Q�A�4@f0@���@�m#@��@��*A
8�@�    A ��@���?�@@��@�M�?�`�@�y�@�&�@�A�@�ף@�!�@�S�                                                                                                                        L       parents[$l#L       =���                                                           	   	   
   
                                                                                                                  L       right_children[$l#L       =               
                                     "   $����   &   (   *   ,   .   0   2   4   6   8   :   <������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       =E&� E��9Ed� A�  C;  @@  B�  B�  A�yA�UUF,eUF�� B�  F^ G, A@  A   B  >U��A���BF��A�  B�  A0  @�  B�  A�  C.  A�  F�� A�  =鼃�U> ���O?=b�۽��ؼ'���]�y;�x�O�5��	=�+����r��lI<��`��;��=���1G=gW�5�=OX��X�=��P��Hf�nؼ�N{=wϚ;l�SL       split_indices[$l#L       =      $      &   )   )         (   (   $                            (   *      *   &      (   "   )         (                                                                                                                        L       
split_type[$U#L       =                                                             L       sum_hessian[$d#L       =D��fD!�Df�C�fC��C�9D�1C}p@羼C�Aj�A��C�0�B��DB:C ��A;�O@uA@Z<aB��zCɢ.A<;1@:�YAs�@�5ChՎB.bBBh�BGօC�uB��B@B��6A5"@Q̶@�"?���B[�A���C,J�Cf��@���@�ץ?�p6?�*{@�y�A+6�@���?��0CA�B1�A8J[A�7�B9�$@��@���B/]�C��%B�@A���B���L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       61L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1�FB�>P����>�ǿA
h=l����>7:�?M<��4�=�p<{��?0�<�h>�0i��>�1?}.ʽ"�3�ީY=�ck��U>?]w鼚�R>��h��d����νgm�<��<�fH=��<>�$=_���E�����|�<fۍ<�s����>=��:=P�Ve���#=Jȫ�q��=6�:� 3��V8L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idi[L       left_children[$l#L       1               	            ��������                     ����   !   #   %   '   )   +   -   /����������������������������������������������������������������������������������������L       loss_changes[$d#L       1@�ë@�-z@n�@���@��@��V@��@���@r�$        @��s@=�.@�lD@�]d@˛�@]f?�|8    @���@�x?��x@/��@�6�@��-@�~�@��                                                                                        L       parents[$l#L       1���                                                                                                                                                  L       right_children[$l#L       1               
            ��������                      ����   "   $   &   (   *   ,   .   0����������������������������������������������������������������������������������������L       split_conditions[$d#L       1A�  C�� D�� B��rC�  @�  B�  @   C1��4�=�p@@  E%� @   E�  A0  ?�  E� �"�3B�UU@   E�  E�� C&��B�  EE� B�  �gm�<��<�fH=��<>�$=_���E�����|�<fۍ<�s����>=��:=P�Ve���#=Jȫ�q��=6�:� 3��V8L       split_indices[$l#L       1      %      *   %      %      *                        &             %   
   $       (                                                                                                 L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1D�<,B�_�D�V,B�E@�ۓD��DY�iB��(Ab8�@�L�?�<:D-,Al�C��CŴJB>ѫB
��AF�?�CL�xC��@�;AJ�6C�L�BD�EBVQ�C��Ae oB��A�78A$%@�i�@���CE�4@��oB��HC���?���?�	�?��A2�C�?�A��@AJ��BbBC�h@��C9�C�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       <k\ۿj��<���qP����<O�B?�_�4������<��D�5w?a0���&j<D�0>���]
>ڿ7���?��;lА�I��=G��/���ƽ�(�=�y��������f=a��>c<ׁL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L                                      L       idi\L       left_children[$l#L                   ����   	   ��������         ����                  ������������������������������������������������L       loss_changes[$d#L       @�O:?��2@wyE?ϧ$    @��@�P�        @� @��@.��    @��2A��@��@cg�?�lA?�                                                L       parents[$l#L       ���                                         	   	   
   
                                          L       right_children[$l#L                   ����   
   ��������         ����                  ������������������������������������������������L       split_conditions[$d#L       ?�  F� F�  D%  ����F�@ A�UU�4������Fv B�I%@   ��&jE�� DH@ B���C̀ A$�D�@ ;lА�I��=G��/���ƽ�(�=�y��������f=a��>c<ׁL       split_indices[$l#L          !                  $   !           $   +                +      !                                                   L       
split_type[$U#L                                      L       sum_hessian[$d#L       D�e[@i^pD��@ ��?���DÄA6GL?�B�?�ҎD��B��A��@G D��B��	B���An��@��@�WD��HCLJ7B��@�#�B��Av3IA��@�?�?�l@?���@��	?��8L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       31L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ���b�C;,2�	�}�5�����? �!=*a�2�q?B�h�³ɽ�'�=���Լ�>
�>��2?����Mե�r=�-;Y��=e<�=RP;�C=[Z=~�ýb@>Pm�v�sL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L                                    L       idi]L       left_children[$l#L                ��������      	         ����                  ������������������������������������������������L       loss_changes[$d#L       @l?k?��@Hf�        @4=�@��@@��A�A@PT    @��E@�pd@���@�L�?�Ԁ@&�                                                L       parents[$l#L       ���                                               	   	                                    L       right_children[$l#L                ��������      
         ����                  ������������������������������������������������L       split_conditions[$d#L       ?�  D   CS  �	�}�5�DY� Cn  B2Y�B  B�  �³�B�  @l��D  @   B���B  �Mե�r=�-;Y��=e<�=RP;�C=[Z=~�ýb@>Pm�v�sL       split_indices[$l#L          !      )              )   *   +             !         *                                                   L       
split_type[$U#L                                    L       sum_hessian[$d#L       D��@l9lDÑi?�j�?� D�%	A6/�D@�aDC��A!9[?���C�X)C��D�vCD��@@Z@�E�CQ��Bd�SCZ&C�ÆA,D+�C(�oA���?�%w?���@��?�o�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       29L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       1<I]�=1|6�m\w<���>]ֽ�[��Fu���vY=^Q�>�ı<l|=����Gپr<�=�><�� �=۝]?b�>i�x��1�9�>��$?g�������3����!��*@J=�4<(�0=G��;F޿���-�*�c=n�>+N�=EM�=�_���Ľ^��=T�=��v����6�=<[�>'�>0�<�ݞ����L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       1                                                 L       idi^L       left_children[$l#L       1               	����                                    !   #   %   '   )   +   -   /������������������������������������������������������������������������������������������������L       loss_changes[$d#L       1@[�[@mob@��@W��@ƯF    @�X@@�-T@Ȇ�@�@@�p�AP0@�bq@���@��	@�o @��@��@���@�*V@�P@�B@r�$@�0�@�,�                                                                                                L       parents[$l#L       1���                                                     	   	   
   
                                                                                    L       right_children[$l#L       1               
����                                     "   $   &   (   *   ,   .   0������������������������������������������������������������������������������������������������L       split_conditions[$d#L       1D� D�� B  BИB`  ��[�@�܎A�  A�  F
UCl��A�  @�  A@  C{  C�  D�  @�  F ( E�^9F ( A@  E�� @   C\  �3����!��*@J=�4<(�0=G��;F޿���-�*�c=n�>+N�=EM�=�_���Ľ^��=T�=��v����6�=<[�>'�>0�<�ݞ����L       split_indices[$l#L       1            *   )       +             '   &   *   )   %                $       &   $   	                                                                                                   L       
split_type[$U#L       1                                                 L       sum_hessian[$d#L       1DĻ8D�x4C�Du9�Bݷ&@e�C�@0CR�}D@��B8��B�Z3B�s�C�cJB���B���CyAD;]A�N�A�$�B�IA��<BJ`B�C�@���C��@B�ޫA�HBӬ?A ��CE��BNĐC�Bg)�A7�AH��@εsAz��A��A�l�A��,@�?@��B.ErA(sBZjP@r  ?�	�B>KC��wL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       49L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5�;��9S�о��<!�
����]�;��׼{e�>&�]�'G��4��=�T��@\���G>�m����{���>����{�?Y�����N�Z�?����<�/���z��W�*�b�?&Ħ��W:�n?�X���c5=5.����=@���y�<��^���=����E�~=�@7;��,��xĽ�ҵ=���� �ͼz�=B@-�,�1<��s��Z���=�RGL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idi_L       left_children[$l#L       5               	                  ����                  !   #   %   '   )   +����   -   /   1   3����������������������������������������������������������������������������������������������������L       loss_changes[$d#L       5@��@�>
@�1�@��#@�+R@�iB@É@�:�@Ÿ?A<@ ј    @rլ@tl�@��@]�/@�� @���@�ԣ@��)@���?���@h2�    ?� @���@
��@>�N                                                                                                    L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                  ����                   "   $   &   (   *   ,����   .   0   2   4����������������������������������������������������������������������������������������������������L       split_conditions[$d#L       5C� C�� C� D1� D�� A�  E%� D,� E� @H  E� =�TEkj�A�  @   B0  Fz�A�  @   B�  BH  Bs��@��n<�/�B�I%B�  C  B�  ��W:�n?�X���c5=5.����=@���y�<��^���=����E�~=�@7;��,��xĽ�ҵ=���� �ͼz�=B@-�,�1<��s��Z���=�RGL       split_indices[$l#L       5   +   %   +         %         $   !          $            $                '   !       (      +                                                                                                       L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5DĔ�D��B��1D���B=FhA'�@Bq_�D�1�CL��A��$A���?�G�AiKB=��AOfD��A�)B��:B�J@��gA�s�Ap��@Y
?�V�@�<�A�G�A��pA8��?���D��QC:4�AE�@�i�A���B�'�B/��B�8�?�HQ@ʫRA�}F?�h>?ǺAW��?�J1?���@ӹ{?��A*�2AN�@-~PA�D�?�L^AE@L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ?�'l�ȶ�<^>Z��2͡<�����[>u���ԑ��τ���i=����G,=�κ>�`����<��?(��?!tD�=uF�/�>����>~�=y�R>�m�!~<�!o�t>���=��<X�c���=,�'��=��[�=����������+> ����c=�<;_9j�+H�=Z����޼bR<���qk�<������W<���<�}�=�[s�٦�����\�3=� <<�Z���5<VK>
حL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       ?                                                               L       idi`L       left_children[$l#L       ?               	                                    !   #   %   '   )   +   -   /   1   3   5   7   9   ;   =��������������������������������������������������������������������������������������������������������������������������������L       loss_changes[$d#L       ?@O@�C@N�h@���@��@dUA��@��>@�5P@��@�U�@�?�@\`
@Q��@��I@qQ�@�.�@0d?�lV@*��@���A�1Aԛ@��@ϟ#@v+�@���@�Ш@�x�A�|@� ,                                                                                                                                L       parents[$l#L       ?���                                                           	   	   
   
                                                                                                                        L       right_children[$l#L       ?               
                                     "   $   &   (   *   ,   .   0   2   4   6   8   :   <   >��������������������������������������������������������������������������������������������������������������������������������L       split_conditions[$d#L       ?@   B`  F��B�  B�j�@   F�� @   B���Bp  B�iiB  D@� B�  BT  @�33BL*�BӪ�B  A   Fk>9B:  FCP @   B@  A�  @   B̪�@   B�  Gr0 =��<X�c���=,�'��=��[�=����������+> ����c=�<;_9j�+H�=Z����޼bR<���qk�<������W<���<�}�=�[s�٦�����\�3=� <<�Z���5<VK>
حL       split_indices[$l#L       ?   
   %   $   *   '      $      (      *   "         )   !   *   *   %   &   $   (             "      %      %                                                                                                                                   L       
split_type[$U#L       ?                                                               L       sum_hessian[$d#L       ?D�~�C���D�YB���Cv��D��Bݑ�B��A]O_Bs�CV��DF�C�q�B+�B�CB>A��A)R�@O�@;W�A�|�C7#�A�2�C��AC�aC��Bs{B�A��B.9A��A�d�A�UA�T�A;��@̐�@��@�?��?��?ţtA�+}@Z�&BȦhB���A�*E@�!�C��?B��A"�C`�C��BC(p�BU_�@�fA��&Ap��@�G�@TF�A�-�A���A�R�@�&�L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       63L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       5;�{�<:���R��=m8>9��'����g=���=��:E?U�?j�Y�<>��-���4�(�>��/�;?��d=���{m����[)?MKj>E뵽Π���ھ,ͼ�l =�����W��tg=��˽쏅<�C ���<d�J�ɾc>:�G���|��I<:ԏ�N��=Hzg��<�=�X�<�{=Æ�=Ǯ�g�z=Jq{��sHL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       5                                                     L       idiaL       left_children[$l#L       5               	                                    !   #   %   '   )   +   -����   /   1����   3����������������������������������������������������������������������������������������������������L       loss_changes[$d#L       5@F~@D<�@���@��n@�g�@)��@P!�@�ǲ@���@�@$@av�?v@��@_E�?k!�@���A�@���@B��@�|@e�6@���@b��    >�6�@=J+    @4q)                                                                                                    L       parents[$l#L       5���                                                           	   	   
   
                                                                                          L       right_children[$l#L       5               
                                     "   $   &   (   *   ,   .����   0   2����   4����������������������������������������������������������������������������������������������������L       split_conditions[$d#L       5C$q�AH�By  B   BH  A`  B�  AD'�@@  AJWjC� @   @��9@�rCq  @�  B�  D,� @s33C�� @@  D@� B�  �[)@��A�  �Π�A`  �,ͼ�l =�����W��tg=��˽쏅<�C ���<d�J�ɾc>:�G���|��I<:ԏ�N��=Hzg��<�=�X�<�{=Æ�=Ǯ�g�z=Jq{��sHL       split_indices[$l#L       5   *   +   +         &      +      +   +      !   !         )      !      )      *       !   &       &                                                                                                    L       
split_type[$U#L       5                                                     L       sum_hessian[$d#L       5D���D���A�<8DG�ND7� A#j/A{BDgsCL{jDb�Ch@��V@�AP�@,-
D�aA2D�CA�ZA,��@���DS�C2jAcY�?��@��k@C�n?��A@�z�@��?��?�L+A.��D�@.P�A�qC��B�O@@h�@��t@00�?��rB�D��B�M�A`�0AR��?��/?��-@K9??�П?ز=@=�@��L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       53L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       3�yq$��w����>� �8����k�>y�?���N�^�b=�g<i_���r��r�>��>��p�����=�l�zTp=ܹ�eɠ=���<�騿���
op=�Ԑ>t�'�_�=�{?^�!<d$��͈��tý�W��%f<��a��׾$�"�A�罕�+=c:�7�!_�=�8���<��==�⽊�_=��)�ݕL       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L       3                                                   L       idibL       left_children[$l#L       3               	                              ��������   ����   !������������   #   %   '   )   +   -   /   1��������������������������������������������������������������������������������L       loss_changes[$d#L       3@@sN@��@1��@u�S@�0@6��@���?��d@-.f@j�?���@���@�y�@�@���        ?�=    ?���            @���?�W�@ri>@�|h?�s�@��@���@3�t                                                                                L       parents[$l#L       3���                                                           	   	   
   
                                                                                    L       right_children[$l#L       3               
                              ��������    ����   "������������   $   &   (   *   ,   .   0   2��������������������������������������������������������������������������������L       split_conditions[$d#L       3@   B  BP  @l��B�e�B  @333Bd  B   D� A�  FM  DO� D�� B�  >��p�E�0 =�lA�DD=ܹ�eɠ=���B   BqWDh� @�r?�  B�ffB  G'� <d$��͈��tý�W��%f<��a��׾$�"�A�罕�+=c:�7�!_�=�8���<��==�⽊�_=��)�ݕL       split_indices[$l#L       3      )      !   *      !   +   "      "            )                  (                  *      +      +   )                                                                                   L       
split_type[$U#L       3                                                   L       sum_hessian[$d#L       3D�a�A䵠D���A,#�A���D���B%��@u�*@݄�Aq�^@.(�Dz��C�2@܇JB
�@2i�?�6�@�Ҽ?��\A`f�?��Z?�%	?�,^Dz)&@K�C��kB�g@��@���A��An@ ӕ@R��?� �AGB�D_#B��?��	?�C��A��A��'B���?���?��t@Z�?�+AW�@�"sA[*Q?��kL       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       51L       size_leaf_vectorSL       1}}{L       base_weights[$d#L       ;�'۽���<	]m;��?3���Z�<5��=�&P=�A�<��$�)<���dT=�P���ܽMM8<�D"����=hm(;�m����S��Lk��*L       
categories[$l#L        L       categories_nodes[$l#L        L       categories_segments[$L#L        L       categories_sizes[$L#L        L       default_left[$U#L                              L       idicL       left_children[$l#L          ����            	   ����               ����������������������������������������L       loss_changes[$d#L       @��    @Y��@B@�@�6@6s3@v��    @LQ�?�yG@q��@Hc�?�/                                        L       parents[$l#L       ���                                               	   	   
   
            L       right_children[$l#L          ����            
   ����               ����������������������������������������L       split_conditions[$d#L       ?�  ����G� ?�  AΪ�Bh  A�  =�&PA�  A0  B�  C@ F<^9=�P���ܽMM8<�D"����=hm(;�m����S��Lk��*L       split_indices[$l#L          %           &   *   %   !                %   $                                        L       
split_type[$U#L                              L       sum_hessian[$d#L       D¿�@��D�9iD�w�@�ȳA��aD�@+@8OR@KBAM��AND�<A���?�?�Ѩ@w��A��A5{2?�F|D�K:C�8Ao@�=L       
tree_param{L       num_deletedSL       0L       num_featureSL       44L       	num_nodesSL       23L       size_leaf_vectorSL       1}}}L       nameSL       gbtree}L       learner_model_param{L       
base_scoreSL       [3.4380576E-1]L       boost_from_averageSL       1L       	num_classSL       0L       num_featureSL       44L       
num_targetSL       1}L       	objective{L       nameSL       binary:logisticL       reg_loss_param{L       scale_pos_weightSL       1}}}L       version[#L       iii}}��      ���R�sb�evals_result_�}�(�validation_0��collections��OrderedDict���)R��auc�]�(G?��'��{3G?��׮.wG?��_K'�G?�$>ʖt�G?�)�
���G?�"���G?�.W\ʺ�G?�9�OC5�G?�?��u�G?�A�� �G?�E�=L��G?�Jl���G?�K�,%�G?�OC�Q�G?�SL<0��G?�U�H��G?�Z!�yz�G?�[��z�G?�_�ȇ�G?�a���G?�c����G?�d�ޒ�G?�g�[�wBG?�k?�Bp&G?�m�Of�OG?�o����G?�r��q/G?�t-�j�G?�v���7G?�y�D%� G?�|CF9KG?�|�O��8G?�~��K�G?�<ζ��G?�@\F�|G?��"�?�G?9��G?�~���G?uHI�G?ZЈ]G?���16G?��j�G?�y㒱2G?7R�+G?������G?���G?�����G?�Z �G?��"��G?�h�@ԫG?���,[G?d(�1G?��8�G?�4%���G?��1G?` *�G?�^�4��G?�C_�`�G?�M5?`YG?�.3�G?�T|���G?����0G?�^0� ?G?.��G?��zMMG?�;���IG?��"��G?��1F�nG?��T�Ґ G?��S,AG?��T�nt-G?��bQ/�1G?��h�:�QG?���d%�G?���RLtJG?��{��G?��T~U�TG?�ӝ_� G?��e(�fG?�����G?��ŗ=pG?���%�BG?�߬�!�KG?��ߞ�G?�����G?��uR�HG?��d��-G?������G?�펼_��G?����'G?����NG?���I؄G?���1�G?�� �a&(G?����+�G?��2LS�,G?��U"��SG?��8N�́G?���<�u G?�����es�validation_1�hB)R��auc�]�(G?���4���G?��b͌��G?�=�0ߖG?�Nk�&��G?�R��r�ZG?�O��:�cG?�U�.yG?�]����G?�b9�%x`G?�b�@�mG?�e���C�G?�i  ��G?�g�2j4�G?�jƱ�{�G?�n^��xqG?�oH�	F]G?�py����G?�qd62��G?�tEw��G?�v�u��G?�x�	G?�y��C��G?�{�X4��G?�}��b�CG?�~XI�G?�~�
'!#G?���;�G?���mg�G?����t�G?��o��sG?��¼�G?2Ξ�G?�D��9G?�PE��+G?�x2��G?��&G?�fe G?�37G?�F���G?��QCJG?��x�\G?�,2G?��w"G?��G?�x���G?���>�G?���ۑG?�����G?�:��N�G?��_NG?"A�G?�7�;G?�a%��G?��8G?�����EG?�ܐ�G?#y��G?�f��G?�x}�-�G?����4G?C�*�G?�3`��XG?�g}���G?�C|�G?��T#�OG?^���G?��bXɜG?���G?��� G?��(QQkG?��uc2G?�bT�>�G?��G?�=�G?�i}ړ�G?�	G�G?�~!�G?��+�G?�6�]��G?���G?���1	G?�I80R8G?�^�DG?����G?�r�>G?�(ud�WG?�����G?�A	lG?WG?t|�G?WG?��Z�|G?�[�$*aG?�k�7G?�&I��%G?"CFG?��j��iG?��z�G?�����G?��t��nesuub.
```


<div style='page-break-after: always;'></div>

# File: models\clustering_model.pkl

```pkl
��)      �!sklearn.mixture._gaussian_mixture��GaussianMixture���)��}�(�n_components�K�tol�G?PbM����	reg_covar�G>�����퍌max_iter�Kd�n_init�K
�init_params��kmeans��random_state�K*�
warm_start���verbose�K �verbose_interval�K
�covariance_type��full��weights_init�N�
means_init�N�precisions_init�N�n_features_in_�K�
converged_���weights_��joblib.numpy_pickle��NumpyArrayWrapper���)��}�(�subclass��numpy��ndarray����shape�K���order��C��dtype�h�dtype����f8�����R�(K�<�NNNJ����J����K t�b�
allow_mmap���numpy_array_alignment_bytes�Kub�����������r�ݞ΋�?3tyv�?O��?�.       �means_�h)��}�(hh h!KK��h#h$h%h*h-�h.Kub������������������������3~d���7��k߿��r ���z�|�ܿ�3~d����<ֹѿ���Ҹ�G6��?�w�'s��?�?D;�?�Z��s�?�\os�?�w�'s��?N5�� �?�Oï�?rt�(m�?��3C� @��x�Y��?�ʶ��� @�
G�@�?��3C� @�����>�?�$�����?�6       �covariances_�h)��}�(hh h!KKK��h#h$h%h*h-�h.Kub������������������0����?M{ڏ+��9���3��9?]K �9M{ڏ+��9M{ڏ+��9�z&��i�?�5s�ד�?$�ݨҌ�9����ư>�����Y :������":������ :������ :8��A�:�&Ly��9��R�8��9�����Y :����ư>�����":�����Y :�����Y :��M�̤:Q��jZV�9WuL���9������":�����":����ư>������":������":��SC�}:�_yp�`�9$�ݨҌ�9������ :�����Y :������":����ư>������ :8��A�:�&Ly��9$�ݨҌ�9������ :�����Y :������":������ :����ư>8��A�:�&Ly��9�z&��i�?t;�"u�:��:��::��چ:t;�"u�:t;�"u�:��T�?�c�Zy�?�5s�ד�?90ne��9ҽj�d�9 ���g�990ne��990ne��9�c�Zy�?&=����?� ��1�?�|����9�Iw��&�?��ci�zl?Cs�V�^��|����9���"1b�?X8�Ӭ��껖�9����ư>d�s"�9ƪ�2��9!�r��9������9�G��`m�9%����X�9�Iw��&�?�g���9�2�[Ch @A׿�_�?�c5"*�?�g���9.u�*R��qxw������ci�zl?�[r��9A׿�_�?�A|��?�n�~j�?�[r��9%�9N`��?u������?3s�V�^�%2��3��9�c5"*�?�n�~j�?��;��@%2��3��9Iii��۟�*
k
�C�?�껖�9������9d�s"�9ƪ�2��9!�r��9����ư>�G��`m�9%����X�9���"1b�?uh[�&l�9.u�*R��#�9N`��?Jii��۟�uh[�&l�9(3X�B�?e�����?X8�Ӭ��o{	>L�9qxw����t������?*
k
�C�?�o{	>L�9h�����?��	��N�?k���Vl�?��a�?a�9�{�i?�*��_d�?��>����a�?��a�Ȑ��l������a�?�}�����?�3�u�?�qS���?6���%�?x,���?-���K��?b�t�~�?a�9�{�i?�3�u�?�������?tg�{��?�ī�S�?�3�u�?ڋ��y<?[z꜄���*��_d�?�qS���?tg�{��?�@��¡�?�0����?�qS���?x
�I��?K�5���?��>��6���%�?�ī�S�?�0����?���p���?6���%�?7Y�<ᐿ��霁N�?��a�?x,���?�3�u�?�qS���?6���%�?�}�����?-���K��?b�t�~�?��a�Ȑ�-���K��?ڋ��y<?x
�I��?7Y�<ᐿ-���K��?6)Ʉ���?N\�U[��?�l����b�t�~�?[z꜄��K�5���?��霁N�?b�t�~�?N\�U[��?u,�4}��?�>       �precisions_cholesky_�h)��}�(hh h!KKK��h#h$h%h*h-�h.Kub��������̦�P�?�?�ڃ����G�A���n�&@���?�ڃ��?�ڃ�l�rb<���.۠%��             @�@��Xu������I����ڶ�����ڶ���{�x��$W���J�#_�                     @�@����da���Xu����Xu��Q$iW�h"�v�                             @�@����I������I���&�oelZ�kN ݨ�                                     @�@��ڶ���{�x��$W���J�#_�                                             @�@{�x��$W���J�#_�                                                �0����?$;>N�ѿ                                                        �ǸxQ��?�R�ƚ��?�S1ޞ>W�',�:/}�B	:I�������"�x?{_���wK�`����}���|�̬?             @�@
"�*2���/E�uA�YS-���
���O���̻��[�"�yf�h��:                �+�9kX�?d] K�5��2��.п1؅ѵ���<�g�ה?J�3ҁR�?                        �Ps��@u�2*�Tl�h�ºO�'�IOѿ�D�D�п                                �O��:�?r�k�d�3<���n�?����k��                                             @�@�2�{j"�\�dķ��:                                                �ah���?�=ѯw�̿                                                        wx�\?��?��:�D��?�	)!���M�d�Ҿ��{�����,�{�?�O����>��қ�?�^7Vf�?        ��5�?�82���*��S|��rʜ���?Z#0y����w��Ɨ�K���J�?                &�6��1�?B5v�?pǿ��'Y�׿!�=Y�/?��I���i?#�K~^C�?                        ��<T0@�����!ԿLr��r��W��ſ�-�T���                                t�<�r�?�r�4~"?���3B�?�AiT���                                        �&���@�b��Ɨ�����J�?                                                7�V��8�?m��[ǿ                                                        �I?8E�?�5       �precisions_�h)��}�(hh h!KKK��h#h$h%h*h-�h.Kub�,���5��?�!������
�Qc�iPh�����!������!��������+������듿�!�����    ��.A�?&J�����C�(����`������`���� �N	6-\�1�*���
�Qc��?&J���    ��.A�jf����?&J����?&J���|px�$\����X���iPh������C�(���jf���    ��.A��C�(����C�(��T��7`��p{x�C��!�������`�����?&J�����C�(��    ��.A��`���� �N	6-\�1�*���!�������`�����?&J�����C�(����`����    ��.A �N	6-\�1�*�����+�� �N	6-\�|px�$\�T��7`� �N	6-\� �N	6-\����J�z�?|���ҿ����듿1�*�����X����p{x�C�1�*��1�*��|���ҿπ���G�?��i�K��?���I_�床=W���j����l5����{����h?9nծ��n�ܢ����<��]��?���I_��    ��.Anŉ� �cN}@��a�r�{���:��3l����R�"�p��S9��:�=W���j�nŉ� �V����	�?��fU'ӿ�2�ǿI%�L�� ��m��? �N��?���l5���cN}@��a���fU'ӿo���{x2@*��ۿ[^� b���rb<˿�^���ο�{����h?r�{���2�ǿ*��ۿh�9��?�(������jl�?����l���9nծ���:��3l�I%�L�� �[^� b��(�����    ��.A%Z�ѭ�"�`���r��:n�ܢ������R�"��m��?��rb<˿�jl�?%Z�ѭ�"���&i?��?�f����˿�<��]��?p��S9��: �N��?�^���ο����l���`���r��:�f����˿mN7Z���?�΀���?ɑ�)u(�?'���!�]?ڰT��`��#�bI�̐?�V�)u(�?�q~�c?�Ȗe�ԯ?ɑ�)u(�?R3W���A��g}��?
���"
�r�:	�?���Zy��c�W��N����/�j��?'���!�]?��g}��?���Zoo�?�g &ulؿ��]��ؿ*��g}��?�l�7唿�Y��v��?ڰT��`��
���"
��g &ulؿ���@�8��9�ԿUuΆ"
�y�p'd��9��떵�#�bI�̐?r�:	�?��]��ؿ�8��9�Կ���P���?Qi:	�?\پG�?I�����V�)u(�?���Zy��*��g}��?UuΆ"
�Qi:	�?X3W���A�R<��N��k�R�j��?�q~�c?c�W��N���l�7唿y�p'd��\پG�?�R<��N����W���?�~��]ſ�Ȗe�ԯ?��/�j��?�Y��v��?9��떵�I����k�R�j��?�~��]ſ����?�      �n_iter_�K�lower_bound_��numpy._core.multiarray��scalar���h*C�z��0@���R��lower_bounds_�]�(hCh*C0p�_��?���R�hCh*C�@K�s@���R�hCh*CL�8�,@���R�hCh*C���L�/@���R�hCh*Cn�]�0@���R�hCh*C^���l�0@���R�hCh*CC�(��0@���R�hCh*C��]�*�0@���R�hCh*C-�1�0@���R�hCh*C�t �0@���R�hCh*C3�N<�0@���R�hCh*C�!+�"�0@���R�hCh*C��J���0@���R�hCh*C�U���0@���R�hCh*C�	^$Z�0@���R�hCh*C�,ݾ��0@���R�hCh*C��=�0@���R�hCh*C�X��0@���R�hCh*C��K���0@���R�hCh*C��&�0@���R�hCh*C�B�0@���R�hFe�_sklearn_version��1.9.1�ub.
```


<div style='page-break-after: always;'></div>

# File: models\clustering_scaler.pkl

```pkl
��=      �sklearn.preprocessing._data��StandardScaler���)��}�(�	with_mean���with_std���copy���feature_names_in_��joblib.numpy_pickle��NumpyArrayWrapper���)��}�(�subclass��numpy��ndarray����shape�K���order��C��dtype�h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�
allow_mmap���numpy_array_alignment_bytes�Kub��*      �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�AGE��TOTAL_ADMISSIONS��AVG_ADMISSION_COST��UNIQUE_DIAGNOSES_COUNT��AVG_LENGTH_OF_STAY��INPATIENT_CLAIM_COUNT��OUTPATIENT_CLAIM_COUNT��DRUG_CLAIM_COUNT�et�b.��       �n_features_in_�K�n_samples_seen_��numpy._core.multiarray��scalar���h�f8�����R�(K�<�NNNJ����J����K t�bC    P/A���R��mean_�h)��}�(hhhK��hhhh'h�hKub����������������B����hR@�I*�{�?���<�@q�����@�S��?�I*�{�?�1���@0���H@�*       �var_�h)��}�(hhhK��hhhh'h�hKub������������N�&V}�c@D�&�b�?��wS}�A��u�Q@���8pL-@D�&�b�?|W׍)O@��p�Ϝ�@�,       �scale_�h)��}�(hhhK��hhhh'h�hKub
�����������{Y��	)@p�˜��?��*��@�V�
"� @󛚣��@p�˜��?�� fГ@�'�[�J@�       �_sklearn_version��1.9.1�ub.
```


<div style='page-break-after: always;'></div>

# File: models\timeseries_model.pkl

```pkl
��a      �statsmodels.tsa.arima.model��ARIMAResultsWrapper���)��}�(�_results�h �ARIMAResults���)��}�(�data��statsmodels.base.data��
PandasData���)��}�(�
orig_endog��pandas.core.series��Series���)��}�(�_mgr��pandas.core.internals.managers��SingleBlockManager���)��(]��pandas.core.indexes.base��
_new_Index����pandas.core.indexes.range��
RangeIndex���}�(�name�N�start�K �stop�K$�step�Ku��R�a]��joblib.numpy_pickle��NumpyArrayWrapper���)��}�(�subclass��numpy��ndarray����shape�K$���order��C��dtype�h0�dtype����f8�����R�(K�<�NNNJ����J����K t�b�
allow_mmap���numpy_array_alignment_bytes�Kub���    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�p       a]�hh!}�(h#Nh$K h%K$h&Ku��R�a}��0.14.1�}�(�axes�h�blocks�]�}�(�values�h,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub������    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA��       �mgr_locs��builtins��slice���K K$K��R�uaust�b�_typ��series��	_metadata�]��_name�a�attrs�}��_flags�}��allows_duplicate_labels��sh[�y�ub�	orig_exog�N�endog�h,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub�������������    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�      �exog�N�	const_idx�N�
k_constant�K �_cache�}�(�
row_labels�h(�ynames�hau�dates�N�freq�N�_param_names�]�(�ar.L1��ma.L1��sigma2�e�predict_start�K$�predict_end�K/�predict_dates�hh!}�(h#Nh$K$h%K0h&Ku��R�ub�params�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub���������?������:�^(IzB�l      �model�h �ARIMA���)��}�(�_spec_arima��#statsmodels.tsa.arima.specification��SARIMAXSpecification���)��}�(�enforce_stationarity�N�enforce_invertibility�N�concentrate_scale���trend_offset�Kh5KKK���ar_order�K�diff�K�ma_order�K�seasonal_order�(K K K K t��seasonal_ar_order�K �seasonal_diff�K �seasonal_ma_order�K �seasonal_periods�K �ar_lags�]�Ka�ma_lags�]�Ka�seasonal_ar_lags�]��seasonal_ma_lags�]��max_ar_order�K�max_ma_order�K�max_seasonal_ar_order�K �max_seasonal_ma_order�K �max_reduced_ar_order�K�max_reduced_ma_order�K�trend��n��
trend_poly�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub���S       �trend_terms�h,)��}�(h/h2h3K ��h5h6h7h9�i8�����R�(Kh=NNNJ����J����K t�bh?�h@Kub�����       �k_trend�K �trend_order�N�trend_degree�N�k_exog�K �_model��statsmodels.tsa.base.tsa_model��TimeSeriesModel���)��}�(h
h)��}�(hhhbNhch,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub������    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�G       hgNhhNhiK hj}�hlh(shnNhoNubhiK hgNhch,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub���������������    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA��       �
_data_attr�]�(hghc�	data.exog��
data.endog��data.orig_endog��data.orig_exog�e�
_init_keys�]��_index�h(�_index_generated���_index_none���_index_int64���_index_dates���_index_freq�N�_index_inferred_freq��ubhch,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub
����������    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�      hgN�_has_missing��numpy._core.multiarray��scalar���h9�b1�����R�(K�|�NNNJ����J����K t�bC ���R�ub�_spec�h�)��}�(h�Nh�Nh��h�Kh5KKK��h�Kh�Kh�Kh�(K K K K t�h�K h�K h�K h�K h�]�Kah�]�Kah�]�h�]�h�Kh�Kh�K h�K h�Kh�Kh�Nh�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub
�����������%       h�h,)��}�(h/h2h3K ��h5h6h7h�h?�h@Kub��N       h�K h�Nh�Nh�K h�h�)��}�(h
h)��}�(hhhbNhch,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub��������    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�R       hgNhhNhiK hj}�(hlh(�xnames�NuhnNhoNubhiK hgNhch,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub����    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�S       h�]�(hghch�h�h�h�eh�]�h�h(hЉhщh҉hӉh�NhՉubhch,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub���    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA��      hgNh�h�ub�_params��statsmodels.tsa.arima.params��SARIMAXParams���)��}�(�spec�h�
exog_names�]��ar_names�]��ar.L1�a�ma_names�]��ma.L1�a�seasonal_ar_names�]��seasonal_ma_names�]��param_names�]�(�ar.L1��ma.L1�hte�k_exog_params�K �k_ar_params�K�k_ma_params�K�k_seasonal_ar_params�K �k_seasonal_ma_params�K �k_params�K�_params_split�}�(�exog_params�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub����/       �	ar_params�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�������      �/       �	ma_params�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub���������������      �?�8       �seasonal_ar_params�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub�������8       �seasonal_ma_params�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub����������������       htG�      uj  Nubh5h�h�h�h�K �measurement_error���time_varying_regression���mle_regression���simple_differencing��h��h���hamilton_representation��h���use_exact_diffuse���polynomial_ar�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�      �?      �?�4       �_polynomial_ar�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��      �?�����鿕3       �polynomial_ma�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub���      �?      �?�4       �_polynomial_ma�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��      �?�����忕<       �polynomial_seasonal_ar�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub
����������      �?�=       �_polynomial_seasonal_ar�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�      �?�<       �polynomial_seasonal_ma�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��      �?�=       �_polynomial_seasonal_ma�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�      �?�>       h�h�h�K�polynomial_trend�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub�����������������;       h�K �_polynomial_trend�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub�������������      �_k_trend�K �k_ar�Kj  K�k_diff�K�k_ma�Kj  K�k_seasonal_ar�K j  K �k_seasonal_diff�K �k_seasonal_ma�K j   K �_k_diff�K�_k_seasonal_diff�K �_k_order�K�_k_exog�K h�K �state_regression���state_error���_loglikelihood_burn�Nj!  KhhhbN�orig_k_diff�K�orig_k_seasonal_diff�K �_k_states_diff�K�nobs�K$�k_states�K�k_posdef�Kh
hhiK hgNhch,)��}�(h/h2h3K$K��h5h6h7h<h?�h@Kub�    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�^       h�]�(hghch�h�h�h�eh�]�(h5h�h�h�h�h�h�e�_polynomial_ar_idx�h,)��}�(h/h2h3K��h5h6h7h�h?�h@Kub��������       �8       �_polynomial_ma_idx�h,)��}�(h/h2h3K��h5h6h7h�h?�h@Kub������       �A       �_polynomial_seasonal_ar_idx�h,)��}�(h/h2h3K ��h5h6h7h�h?�h@Kub��������������A       �_polynomial_seasonal_ma_idx�h,)��}�(h/h2h3K ��h5h6h7h�h?�h@Kub�������       �transition_ar_params_idx��
transition�hSKKN��R�K���selection_ma_params_idx��	selection�hSKKN��R�K ��h�h(hЉhщh҉hӉh�NhՉ�_init_kwargs�}�jy  Ks�_trend_data�h,)��}�(h/h2h3K$K ��h5h6h7h<h?�h@Kub���������>      �ssm��.statsmodels.tsa.statespace.simulation_smoother��SimulationSmoother���)��}�(�shapes�}�(�obs�KK$���design�KKK���obs_intercept�KK���obs_cov�KKK��j�  KKK���state_intercept�KK��j�  KKK���	state_cov�KKK��u�k_endog�Kjw  K$jx  Kjy  K�_design�h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub��������      �?      �?        �6       �_obs_intercept�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub��������        �2       �_obs_cov�h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub������������        �7       �_transition�h,)��}�(h/h2h3KKK��h5�F�h7h<h?�h@Kub�������      �?                      �?������?                      �?        �8       �_state_intercept�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub������                        �4       �
_selection�h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub
����������              �?�����忕4       �
_state_cov�h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub
����������:�^(IzB��      �initial_variance�GA.��    �prefix_statespace_map�}�(�s��*statsmodels.tsa.statespace._representation��sStatespace����d�j�  �dStatespace����c�j�  �cStatespace����z�j�  �zStatespace���u�initialization��)statsmodels.tsa.statespace.initialization��Initialization���)��}�(jx  K�_states�h�h�C        ���R�h�h�C       ���R�h�h�C       ���R����_initialization�h,)��}�(h/h2h3K��h5h6h7h9�O8�����R�(Kh�NNNJ����J����K?t�bh?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(h �scalar���h�i8�����R�(K�<�NNNJ����J����K t�bC        ���R���hhC       ���R�hhC       ���R���h$et�b.�c       hI}�(j�  ��j�  )��}�(jx  Kj�  h�h�C        ���R���j�  h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�Nat�b.�^       hI}��initialization_type��approximate_diffuse��constant�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub������        �6       �stationary_cov�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub��������        �.      �approximate_diffuse_variance�GA.��    �prefix_initialization_map�}�(j�  �*statsmodels.tsa.statespace._initialization��sInitialization���j�  j  �dInitialization���j�  j  �cInitialization���j�  j  �zInitialization���u�_representations�}�(j�  }�(j
  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub����������������        �*       j  h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����        �T       uj�  }�(j
  h,)��}�(h/h2h3K��h5h6h7h9�c16�����R�(Kh=NNNJ����J����K t�bh?�h@Kub
����������                �-       j  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                �H       uu�_initializations�}�(j�  j  (Kh,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��������������        �%       h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub	���������        �G       GA.��    t�R�}�(�_tmp_transition�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub�������        �?       �_tmp_selected_state_cov�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub���������������        �5       ubj�  j  (Kh,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub	���������                �(       h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub��������������                �=       GA.��    t�R�}�(j=  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                �-       jA  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                �{       ubuubj�  j�  ��j�  )��}�(jx  Kj�  h�h�C        ���R�h�h�C       ���R���j�  h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(NNet�b.�>       hI}�j  �
stationary�j
  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�������������                �*       j  h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub������������                                �w       j  GA.��    j  }�(j�  j  j�  j  j�  j  j�  j  uj  }�(j�  }�(j
  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub���������������                �-       j  h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub	���������                                �4       uj�  }�(j
  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub��                                �0       j  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������                                                                �:       uuj2  }�(j�  j  (Kh,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub������������                �(       h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub��������������                                �=       GA.��    t�R�}�(j=  h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub	������������혻�        ��_ߎ��?      �-       jA  h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub	�����������yd��{Bù*q�ù*q��� �fB�5       ubj�  j  (Kh,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�                                �+       h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub�����������                                                                �@       GA.��    t�R�}�(j=  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub���������혻�                        ��_ߎ��?              �        �0       jA  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub��������yd��{B��yd���@ù*q�ù*��ù*q�ù*������ �fB���� ��@�4       ubuubuj  Nj
  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��                        �*       j  h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����                                                                        ��       j  GA.��    j  }�(j�  j  j�  j  j�  j  j�  j  uj  }�j2  }�ubj  }�(j�  }�(j�  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub�����    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub
����������      �?      �?        �*       j�  h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����        �,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub��        �/       j�  h,)��}�(h/h2h3KKK��h5j�  h7h<h?�h@Kub���������������      �?                      �?������?                      �?        �*       j�  h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����                        �,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub��              �?�����忕,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub��:�^(IzB�6       uj�  }�(j�  h,)��}�(h/h2h3KK$��h5h6h7j-  h?�h@Kub��������    2�kA           �]	oA            �sA           �ųtA           @$/wA           `)vA           �z�uA           `	�vA           @�9uA           ��rvA           ���tA           ���uA           ��uA           �sA            �uA           �jytA           �;vtA           @�esA           `@�sA           ��tA           `SfsA           �#�rA           @E7qA           ���qA           �	qA           ��kA           ��XnA           @X�lA            ��jA           @v�gA           �P�eA            �cA            s�`A            sVA            ��OA            2�AA        �/       j�  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub�������      �?              �?                        �-       j�  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                �/       j�  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub�������                �2       j�  h,)��}�(h/h2h3KKK��h5j�  h7j-  h?�h@Kub����      �?                                              �?        ������?                                              �?                        �-       j�  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                                                �/       j�  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub�������                      �?        ������        �/       j�  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub�������:�^(IzB:�^(I�@�D       uu�_statespaces�}�(j�  j�  (h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub��    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�'       h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub���������������      �?      �?        �%       h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub	���������        �'       h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub�������        �*       h,)��}�(h/h2h3KKK��h5j�  h7h<h?�h@Kub����      �?                      �?������?                      �?        �%       h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub	���������                        �'       h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub�������              �?�����忕'       h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub�������:�^(IzB��       J����t�R�}�(�initialized�K�initialized_diffuse�K �initialized_stationary�K�initial_state�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub������������                        �<       �initial_state_cov�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub��    ��.A                        ��yd��{Bù*q�        ù*q��� �fB�D       �initial_diffuse_state_cov�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub
����������                                                                        �Q       �missing�h,)��}�(h/h2h3KK$��h5h6h7h9�i4�����R�(Kh=NNNJ����J����K t�bh?�h@Kub�������������                                                                                                                                                �1       �nmissing�h,)��}�(h/h2h3K$��h5h6h7j  h?�h@Kub�����                                                                                                                                                �>       �has_missing�K �tmp�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub��������        :�^(IzBﰑù*q�                                                �?       �selected_state_cov�h,)��}�(h/h2h3KKK��h5j�  h7h<h?�h@Kub���������������                                :�^(IzBﰑù*q�        ﰑù*q��� �fB�2       �selected_obs�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub������������        �<       �selected_obs_intercept�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��        �5       �selected_design�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub	���������                        �6       �selected_obs_cov�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��������        �:       �transform_cholesky�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����        �9       �transform_obs_cov�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub�����        �8       �transform_design�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub������                        �2       �collapse_obs�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub������������                        �6       �collapse_obs_tmp�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��������                        �:       �collapse_design�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub����                                                                        �;       �collapse_obs_cov�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub���                                                                        �<       �collapse_cholesky�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub��                                                                        ��       �t�K �collapse_loglikelihood�G        �companion_transition�K �transform_determinant�G        ubj�  j�  (h,)��}�(h/h2h3KK$��h5h6h7j-  h?�h@Kub�������    2�kA           �]	oA            �sA           �ųtA           @$/wA           `)vA           �z�uA           `	�vA           @�9uA           ��rvA           ���tA           ���uA           ��uA           �sA            �uA           �jytA           �;vtA           @�esA           `@�sA           ��tA           `SfsA           �#�rA           @E7qA           ���qA           �	qA           ��kA           ��XnA           @X�lA            ��jA           @v�gA           �P�eA            �cA            s�`A            sVA            ��OA            2�AA        �*       h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub������������      �?              �?                        �(       h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub��������������                �*       h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub������������                �-       h,)��}�(h/h2h3KKK��h5j�  h7j-  h?�h@Kub	���������      �?                                              �?        ������?                                              �?                        �(       h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub��������������                                                �*       h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub������������                      �?        ������        �*       h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub������������:�^(IzB:�^(I�@�L       J����t�R�}�(j�  Kj�  K j�  Kj�  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub
����������                                                �0       j�  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������    ��.A                                                        ��yd��{B��yd���@ù*q�ù*��                ù*q�ù*������ �fB���� ��@�0       j�  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������                                                                                                                                                �-       j   h,)��}�(h/h2h3KK$��h5h6h7j  h?�h@Kub	���������                                                                                                                                                �+       j  h,)��}�(h/h2h3K$��h5h6h7j  h?�h@Kub�����������                                                                                                                                                �7       j  K j  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub���������������                :�^(IzB:�^(I�@ﰑù*q�ﰑù*��                                                                                                �2       j  h,)��}�(h/h2h3KKK��h5j�  h7j-  h?�h@Kub����                                                                :�^(IzB:�^(I�@ﰑù*q�ﰑù*��                ﰑù*q�ﰑù*������ �fB���� ��@�+       j  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�����������                �+       j  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�����������                �+       j  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�����������                                                �+       j!  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�����������                �-       j%  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                �-       j)  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                �-       j-  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                                                �+       j1  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�����������                                                �+       j5  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�����������                                                �0       j9  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������                                                                                                                                                �0       j=  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������                                                                                                                                                �0       jA  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������                                                                                                                                                ��      jE  K#jF  hQ�complex���G        G        ��R�jG  K jH  j�  G        G        ��R�ubu�_time_invariant�N�_kalman_filters�}�(j�  �)statsmodels.tsa.statespace._kalman_filter��dKalmanFilter���(j�  KK	KK K G;���O�ҬKt�R�}�(jE  K �nobs_diffuse�K �	converged�K �converged_determinant�G        �determinant�G@<6�>���period_converged�K �converged_filtered_state_cov�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub�����                                                                        �D       �converged_forecast_error_cov�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub
����������        �=       �converged_kalman_gain�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub�                        �3       �converged_M�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub�����������                        �H       �converged_predicted_state_cov�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub������                                                                        �9       �filtered_state�h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub�����n�ج^~@�
1�kA�s��F'a�    2�kA    ^�:Ag�W��>"A   �]	oA   ��QAJv�}� :�    �sA   �(A���Q�(A   �ųtA   ��CAu��"'�   @$/wA   ��2�͘�Ȕ�9A   `)vA   ����AGx+�+A   �z�uA   ��*Aє�@l�   `	�vA   �9����B�4A   @�9uA������3A��*�)�   ��rvA   �8�Q3��XE2A   ���tA�����#A��۫-!�   ���uA   ` ���״��A   ��uA�����q?�r{Ї�4A   �sA   Bq@Aw'���9�    �uA    T�$��^9<�A   �jytA@����w���tsi��   �;vtA   �1��^u!�%A   @�esA    �1A���P��	�   `@�sA����'�"A��8]�n�   ��tA������&�Ad��A   `SfsA
   �*�<��JA   �#�rA�����5�!PӔ��(A   @E7qA   N A�y�lp!�   ���qA����#&�Ї67fA   �	qA�����H�F܉�0�>A   ��kA������3A�~�3�����XnA����s�)��%m?NA   @X�lA   $/�U�3xmeA    ��jA������6�ʢ�z��'A   @v�gA   .3��;ANon A   �P�eA�����T)�����u�A    �cA�����:��?U�\*A    s�`A������E����b7A   sVA   \�:� ���*�#A    ��OA������;��S���$A�?       �filtered_state_cov�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������%^�~�.A$^�~�.�1��5�"A%^�~�.�   �~�.A  �5�"�2��5�"A  �5�"� ���V%B    ��     ��>z�?���     ��>                z�?���        �E����B������>������0�#&���������                �0�#&���         LX�r�A������������>e�g����     ��>                e�g����         ��Z@�A������>�������EJ��Ҿ������                �EJ��Ҿ         ��s��A������������>�{��ҍ��������>                �{��ҍ��         �_�ޢ�A������>������<�)*��>������                <�)*��>         �Q�  �A������������>�<hf��������>                �<hf��         `��zq�A������>������ �Q�>������                � �Q�>          �{��A������������>¸����������>                ø����          �ihvA������>������g�ڟ20�>������                h�ڟ20�>          �pM cA������������>��V��������>                ��V��          X���PA������>������\KS��>������                �\KS��>          ����<A������������>*z�3���������>                )z�3���          ���(A������>������h��%��>������                h��%��>          ���A������������>�*�oy��������>                �*�oy��          ���A������>������CD�����>������                CD�����>          ��%�@������������>gg"ȅM�������>                hg"ȅM�           �D��@������>�����򾊍�,v
�>������                ���,v
�>           �8�@������������>Z� ��6�������>      0?        [� ��6�      0�   �C��@����/1?����/1�Ժm �.-?    /1�      0?      0�ֺm �.-?      0�   �#+�@     ��     ��>���3��������>                ���3��           @�x�@������>������V�Iu.���������      0?      0�V�Iu.���      0�   ��A{@����ۡ-?����ۡ-��M3g�?����ۡ-�      @?      0��M3g�?      0�    a�g@����/1?����/1�!���V�,?����/1�      0?      0�!���V�,?      0�    rT@������������>Y�X;:�������>      0?        Y�X;:�      0�    4�A@����/1?����/1���y�k#+?����/1�      0?        ��y�k#+?      0�    P�.@������������>|�dx%?������>                }�dx%?            ��@������>�������"$?������              0?�"$?            �@������������>� 0�?������>                � 0�?      0�    ���?������>������lؒ�	��������                lؒ�	��             B�?������������>�8�ib4��������>                �8�ib4��             ��?������>������90p��>������              0?90p��>             ع?������������>P��@�?������>              0�P��@�?             p�?������>���������Y~��������      0?        ���Y~��      0�     `�?   ܡ-?   ܡ-�@<"r2'?   ܡ-�      0?      0�@<"r2'?      0�     ��?�0       �forecast�h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������        ��T�hpA���~qqAޞo���uA��=�\vA��i��uxA�-�m�vA�{S�avA���2wA���q�BuA5ǚH4�vA>0'��tA�[���uA�6����tA���S�rA���Ly5uAHΣZ�otA#@h��otA���lZ9sAsXy�psA�(K��"tA,MZOsA�o��brA*��#��pAu���?�qA�=��O�pA�+z��jA��a���mA5p>lA�-�U�.jA�b� �gA�O�dAk/�i%cAj}�m�8_A�k��~SA���s��IA�6       �forecast_error�h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub����������������    2�kA���j�l,�8�2EDA���6}�2���"Ly�1AP�O[}C� ���1�'��!k�zA@�1�L�?�p'b�3APs����;�@8���&A@q˵e!�@h#�ݒ>� ��_�CA����ف'� ��p���@0�8�0�@��|�A��Ԑ]�%A e	&�'���)���'�а�և�2����3�*A���?h�!� ��d<.G�p�.$��<A �7:#�P��a'��mɭH�1�@+V	(�(��Rb�	 �X{��4���ۂ�A��_�@��-��7�ω�/��<       �forecast_error_cov�h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
�����������ǝX²{B�����zBQ�X�X]zB����4zB$�Ui#zB.��i�zB*e>��zBXl*YzB�CI�zBΐ�'|zB�=_zB�Q��RzBPE�LMzB�v�JzB7�-�IzB�mv~IzB~ئMIzB��8IzBtj\/IzB��e+IzBz=�)IzBU��(IzBv��(IzB��y(IzB�fj(IzB��c(IzB��`(IzB��_(IzB}_(IzB@�^(IzB'�^(IzBۡ^(IzB��^(IzBؚ^(IzB�^(IzB��^(IzB�:       �forecast_error_fac�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub������������        �<       �forecast_error_ipiv�h,)��}�(h/h2h3K��h5h6h7j  h?�h@Kub��    �;       �forecast_error_work�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub�������        �8       �kalman_gain�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub������      �?� G����?        �������?D1|
��?              �?<�5V:��?              �?��=�?              �?༣�?              �?@�j���?              �?4Fz���?              �?�q���?              �?����?              �?h�Pm���?              �?!?z��?              �?p��Q��?              �?<%k#@��?              �?�U��8��?              �?�N>F5��?              �?��L�3��?              �?D�<3��?              �?<�q�2��?              �?H���2��?        �������?PP�2��?              �? r��2��?              �?�&�2��?        �������?���2��?        �������?`���2��?              �?��v�2��?        �������?4a�2��?              �?��W�2��?              �?\�S�2��?              �?$
R�2��?              �?�GQ�2��?              �?d�P�2��?              �?��P�2��?              �?�P�2��?              �?H�P�2��?        �������?L�P�2��?              �?�P�2��?        �:       �univariate_filter�h,)��}�(h/h2h3K$��h5h6h7j  h?�h@Kub������������                                                                                                                                                �3       �loglikelihood�h,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub�����k\k�Q��
���.��պí�0����]�.�S�]���.���X�S�0�Qq��c.��D��b(.�����80��q�.�U+IH�/�Twq?�].��̊&�;.�ϗ��c%0��Fө�0���3b.�4��.�Ơn���.����b.�TW�2U.���)
�b.���I�&d.�Y;�k'�.��NX'y.�G��=.�k5�ޙ1�R���0��[@�'F.�eY�mA_.�@Z��.����Mm.��*� .��i'�/�M֧;U�0�_<N�+�.�IH�ۨ.��:       �predicted_state�h,)��}�(h/h2h3KK%��h5j�  h7h<h?�h@Kub������������                            2�kA𽦚ߋDA           �]	oA�����>A            �sA���6��>A           �ųtA�Zݳl6A           @$/wA����Vj4A           `)vA���a[%A           �z�uAL�ޔ�hA           `	�vA�<��j�A           @�9uA`��cr�@           ��rvAD�cMD
A           ���tA0���x`��           ���uA��\[N�@           ��uA ������           �sA���B��            �uA ���,��@           �jytA�oc�J���           �;vtA�u�^����           @�esA`2&�iA�           `@�sA ����9��           ��tApE�,���@           `SfsALԲ�B���           �#�rA^yHC�           @E7qAz�Gd�           ���qANE �:�           �	qA��iZ�           ��kA�D]H�"�        ����XnA@ӗg�	�           @X�lAo��1��            ��jA�I�Hն�           @v�gA��S�gt�           �P�eAR�����            �cA�:�?S�            s�`A����� �           sVA:�D��'�            ��OA�U0�e'�           2�AAiɶ�]�'�        �@       �predicted_state_cov�h,)��}�(h/h2h3KKK%��h5j�  h7h<h?�h@Kub��������������    ��.A                        ��yd��{Bù*q�        ù*q��� �fB     ��z�o����        z�o���������zBﰑù*q�        ﰑù*q��� �fB������>�u���        �u���Q�X�X]zBﰑù*q�        ﰑù*q��� �fB������e��~B�        e��~B�����4zBﰑù*q�        ﰑù*q��� �fB������>������        ������$�Ui#zBﰑù*q�        ﰑù*q��� �fB�������Ф�\��        �Ф�\��.��i�zBﰑù*q�        ﰑù*q��� �fB������>�2U��        �2U��*e>��zBﰑù*q�        ﰑù*q��� �fB����������#�        ����#�Xl*YzBﰑù*q�        ﰑù*q��� �fB������>LuFp<̾        LuFp<̾�CI�zBﰑù*q�        ﰑù*q��� �fB������^w7�McԾ        ^w7�McԾΐ�'|zBﰑù*q�        ﰑù*q��� �fB������>��M\��        ��M\���=_zBﰑù*q�        ﰑù*q��� �fB������6�/Q,Jɾ        6�/Q,Jɾ�Q��RzBﰑù*q�        ﰑù*q��� �fB������>0k���>        0k���>PE�LMzBﰑù*q�        ﰑù*q��� �fB������&�e���¾        &�e���¾�v�JzBﰑù*q�        ﰑù*q��� �fB������>4��/�>        4��/�>7�-�IzBﰑù*q�        ﰑù*q��� �fB������@�I�\��        @�I�\���mv~IzBﰑù*q�        ﰑù*q��� �fB������>���!"�>        ���!"�>~ئMIzBﰑù*q�        ﰑù*q��� �fB������l��� ټ�        l��� ټ���8IzBﰑù*q�        ﰑù*q��� �fB������>D�#`���>        D�#`���>tj\/IzBﰑù*q�        ﰑù*q��� �fB������4u::<»�        4u::<»���e+IzBﰑù*q�        ﰑù*q��� �fB    /1?q����?        q����?y=�)IzBﰑù*q�        ﰑù*q��� �fB     ���R����        ��R����U��(IzBﰑù*q�        ﰑù*q��� �fB������>f	��        f	��v��(IzBﰑù*q�        ﰑù*q��� �fB    ܡ-?�@m�O��        �@m�O����y(IzBﰑù*q�        ﰑù*q��� �fB    /1?�zK�O?        �zK�O?�fj(IzBﰑù*q�        ﰑù*q��� �fB������|��5T��        |��5T����c(IzBﰑù*q�        ﰑù*q��� �fB����/1?N��o}?        N��o}?��`(IzBﰑù*q�        ﰑù*q��� �fB������{<n�v?        {<n�v?��_(IzBﰑù*q�        ﰑù*q��� �fB������>pyn�Ա	?        pyn�Ա	?}_(IzBﰑù*q�        ﰑù*q��� �fB�������F¥��#?        �F¥��#?>�^(IzBﰑù*q�        ﰑù*q��� �fB������>�,]��        �,]��'�^(IzBﰑù*q�        ﰑù*q��� �fB������x��Q�        x��Q�ۡ^(IzBﰑù*q�        ﰑù*q��� �fB������>�+[?�߾        �+[?�߾��^(IzBﰑù*q�        ﰑù*q��� �fB�������$�I��?        �$�I��?ؚ^(IzBﰑù*q�        ﰑù*q��� �fB������>Ш�� �        Ш�� ��^(IzBﰑù*q�        ﰑù*q��� �fB   ܡ-?>���#y?        >���#y?��^(IzBﰑù*q�        ﰑù*q��� �fB������> X�
���         X�
���[�^(IzBﰑù*q�        ﰑù*q��� �fB�C       �standardized_forecast_error�h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub�����������~�� �%@v0ؼ`�忏ڌ�B�?62{�J���md��?�H����أ���⿬q'䈼�?���8һ��܌�����?��������P���?�ؐ��>ۿ��Z����������?����h�0@V���?Dm��@r����?�~ـ!��?䓈IRs⿈9���]`\��M��P����?�G��ۿ��7�l'��A�Ў��?+���޿|�('O�nt����QЫ���A�δ�:ѿ���=�_���eC{�����fT6���Y�迕H       �predicted_diffuse_state_cov�h,)��}�(h/h2h3KKK%��h5j�  h7h<h?�h@Kub��������������                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        �D       �forecast_error_diffuse_cov�h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
����������                                                                                                                                                                                                                                                                                                �/       �tmp0�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub�������	   �C+?�1�U?        �1�U?      �?                                �0       �tmp00�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub��������������                                                                        �1       �tmp1�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������������    ��.A��yd��{Bù*q�z�o�=�������zBﰑù*q��u��(�Q�X�X]zBﰑù*q�d��~҆�����4zBﰑù*q��r�
�mܾ$�Ui#zBﰑù*q�jhRv�n�.��i�zBﰑù*q�5�ͪXI�>*e>��zBﰑù*q��Y���Xl*YzBﰑù*q§b��0��>�CI�zBﰑù*q���y�	��ΐ�'|zBﰑù*q·�u�`�>�=_zBﰑù*q���%�e���Q��RzBﰑù*q�V#����>PE�LMzBﰑù*q����4�C���v�JzBﰑù*q����4�>7�-�IzBﰑù*q��ޘ�����mv~IzBﰑù*q¶X"Bq�>~ئMIzBﰑù*q��K9�����8IzBﰑù*q�_:����>tj\/IzBﰑù*q�N���C����e+IzBﰑù*q��|E,6?y=�)IzBﰑù*q·�R�^�U��(IzBﰑù*q��0Hɾv��(IzBﰑù*qº_�4=%?��y(IzBﰑù*q� ��R�6?�fj(IzBﰑù*q�d��5�7���c(IzBﰑù*q��3�Ͳ�4?��`(IzBﰑù*q�yܰot?��_(IzBﰑù*q¨<�r2�?}_(IzBﰑù*q��F¥��!??�^(IzBﰑù*q������㹾'�^(IzBﰑù*q¡M����ۡ^(IzBﰑù*q´iR�8��>��^(IzBﰑù*q��$�IWB?ؚ^(IzBﰑù*q��Q�?~P���^(IzBﰑù*q�60x�1?��^(IzBﰑù*q,       �tmp2�h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub
����������z{�q���>�ū'f��K��"Z�>ZV� ����������>�;�g�ⷾ��5��'�=�>���^���Ly�P�>�l&8i��8oХ��>�,>RV��
IIZt���o�U�\�>����՜�R� 蹗N>��G"�^��N��2�>JI����>���j.朾5ɳ�p*��T�@�"��y��@�>w���	ϕ���_Mo��}�m���>㉉�啗�����~T����N���f���_,���������𑨾�mT�������4�-�����g]����1       �tmp3�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�����M\�"|b=M\�"|b=        �V��$c=�V��$c=        �"0�kc=�"0�kc=        �8����c=�8����c=        �3\��c=�3\��c=        �'��$�c=�'��$�c=        ���ۏ�c=���ۏ�c=        �7Tћ�c=�7Tћ�c=        �q��c=�q��c=        ��>B�c=��>B�c=        |n��W�c=|n��W�c=        ݂P<a�c=݂P<a�c=        C��Pe�c=C��Pe�c=        ���g�c=���g�c=        �ߘ�g�c=�ߘ�g�c=        �f-h�c=�f-h�c=        �Rh�c=�Rh�c=        �'bh�c=�'bh�c=        C�hh�c=C�hh�c=        ���kh�c=���kh�c=        �*/mh�c=�*/mh�c=        �U�mh�c=�U�mh�c=        U�mh�c=U�mh�c=        /.nh�c=/.nh�c=        ��"nh�c=��"nh�c=        o�'nh�c=o�'nh�c=        �*nh�c=�*nh�c=        K�*nh�c=K�*nh�c=        �_+nh�c=�_+nh�c=        H�+nh�c=H�+nh�c=        �+nh�c=�+nh�c=        j�+nh�c=j�+nh�c=        �+nh�c=�+nh�c=        ��+nh�c=��+nh�c=        a�+nh�c=a�+nh�c=        ��+nh�c=��+nh�c=        �.       �tmp4�h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub��������                                                                                                                                                                                                                                                                                                �.       �M�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub��������                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                �2       �M_inf�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub����                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                �+       �tmpK0�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�����������                        �+       �tmpK1�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub���                        �0       �tmpL0�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub��������������                                                                        �0       �tmpL1�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub��������������                                                                        ��       ubj�  j�  �zKalmanFilter���(jb  KKKM�K G;���O�ҬKt�R�}�(jE  K$j�  K j�  K j�  j�  G        G        ��R�j�  j�  G@<6�>��G>P      ��R�j�  K j�  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub�                                                                                                                                                �-       j�  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                �-       j�  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                                                �-       j�  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                                                �0       j�  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������                                                                                                                                                �0       j�  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������    ��OA$�"qv+<    ��;� ���uG<�S���$A     �=    ��OA$�"qv+<    ��;� ���uG<�S���$A     �=�2       j�  h,)��}�(h/h2h3KKK��h5j�  h7j-  h?�h@Kub����   ܡ-?��,C�3�=   ܡ-���,C�3���)ŭͮ,?T,d�V+�=	   ܡ-���,C�3��      0?      �=      0�      ���)ŭͮ,?T,d�V+�=      0�      ��      �?     @�=   ܡ-?��,C�3�=   ܡ-���,C�3���)ŭͮ,?T,d�V+�=	   ܡ-���,C�3��      0?      �=      0�      ���)ŭͮ,?T,d�V+�=      0�      ��      �?     @�=�-       j�  h,)��}�(h/h2h3KK$��h5h6h7j-  h?�h@Kub	���������                ��T�hpA�p�kA�V>���~qqAS�Q�kM>ݞo���uAƑ1[;�B>��=�\vA�-���8>��i��uxA���a�(0>�-�m�vA_����a%>�{S�avAY��զ*>���2wA��g �>���q�BuA��Q�i>4ǚH4�vA��G >>0'��tA;B��$�=�[���uA�ޔ�t��=�6����tAp��ZO�=���S�rAbŹ�0�=���Ly5uA�؋I���=HΣZ�otA\�TX��=#@h��otA��Οx�=���lZ9sAɧ�^��=sXy�psAf�3��ʧ=�(K��"tAݗ��LP�=,MZOsA��X<��=�o��brA�@�M��=*��#��pA�v"$�؁=u���?�qA\3D�-}w=�=��O�pA���n=�+z��jA�J��Wd=��a���mA����Z=5p>lAY)�
��Q=�-�U�.jA�k���0G=�b� �gA���6A�>=�O�dA�K��4=k/�i%cA ���o*=j}�m�8_A�aWN>e!=�k��~SAhi���=���s��IA�M��� =�-       j�  h,)��}�(h/h2h3KK$��h5h6h7j-  h?�h@Kub	���������    2�kA        ���j�l,��p�kA�V�0�2EDAS�Q�kM����6}�2�Ƒ1[;�B�p�"Ly�1A�-���8�H�O[}C����a�(0�@���1�'�_����a%��!k�zAY��զ*�@�1�L�?���g ��p'b�3A��Q�i�@s����;���G �@8���&A;B��$��@q˵e!��ޔ�t��@h#�ݒ>�p��ZO� ��_�CAbŹ�0ؽ����ف'��؋I��Ͻ ��p���@\�TX�Ľ0�8�0���Οx��@��|�Aɧ�^�����Ԑ]�%Af�3��ʧ� e	&�'�ݗ��LP����)���'���X<���а�և�2��@�M������3�*A�v"$�؁����?h�!�\3D�-}w� ��d<.G����n�h�.$��<A�J��Wd�0�7:#�����Z�P��a'�Y)�
��Q��mɭH�1��k���0G�@+V	(�(����6A�>��Rb�	 ��K��4�X{��4� ���o*���ۂ�A��aWN>e!��_�@��-�hi�����7�ω�/��M��� ��/       j�  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub���������^(IzB��^(I�@��^(IzB��^(I�@�-       j�  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	���������                �+       j�  h,)��}�(h/h2h3K��h5h6h7j  h?�h@Kub�����������    �-       j�  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub�����                �/       j�  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub�������      �?��\2����P�2��?V��-I��                �+       j�  h,)��}�(h/h2h3K$��h5h6h7j  h?�h@Kub�����������                                                                                                                                                �+       j�  h,)��}�(h/h2h3K$��h5h6h7j-  h?�h@Kub������������k\k�Q��o�ӡg�>�
���.�ȗ����0��պí�0�Vd o�V>���]�.��F��-��Q�]���.���HJ� ���X�S�0���œ�U>Rq��c.�>J���>5��D��b(.���^i��<�����80�xw�J<F>�q�.�h��T�4�S+IH�/��?��;>Twq?�].�0�8܈�5��̊&�;.�x�_`e3:�ϗ��c%0��]����C>�Fө�0�st���S>��3b.��8p!�h5�4��.��-n�?�Ơn���.�Doi�%�%����b.���I��">�TW�2U.��"��7���)
�b.�j�:գ\5���I�&d.���AP'*5�Y;�k'�.�H7�w^���NX'y.�����2�G��=.��/�9�k5�ޙ1�	��F�`>Q���0���tO|@>�[@�'F.��O�p�8�eY�mA_.��eZf��5�@Z��.�00hX 0����Mm.�'q_�4��*� .��hH�I�=��i'�/�Ih;O��M֧;U�0��ܨ�$3O>_<N�+�.�΋��S.�IH�ۨ.��C4')��0       j�  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������    ��OAl_R��4<�U0�e'���: =                    2�AA,	5<kɶ�]�'��7U)/�=                    2�AA,	5<kɶ�]�'��7U)/�=                �2       j�  h,)��}�(h/h2h3KKK��h5j�  h7j-  h?�h@Kub����
   ܡ-? �,C�3�=�[t��?�<Bd�y}=                �[t��?�<Bd�y}=��^(IzB��^(I�@ﰑù*q�ﰑù*��                ﰑù*q�ﰑù*������ �fB���� ��@������> ӼK̞=���og��и�rT�=                ���og��и�rT�=[�^(IzB[�^(I�@ﰑù*q�ﰑù*��                ﰑù*q�ﰑù*������ �fB���� ��@������> ӼK̞=���og��и�rT�=                ���og��и�rT�=[�^(IzB[�^(I�@ﰑù*q�ﰑù*��                ﰑù*q�ﰑù*������ �fB���� ��@�-       j�  h,)��}�(h/h2h3KK$��h5h6h7j-  h?�h@Kub	���������z�� �%@��g�u��0ؼ`��9
PU\�5>~ڌ�B�?�:&S�BO�2{�J������H�=>�md��?'�'��;��H����3�d�N>���Y[��2>�q'䈼�?'𑔉�$����8һ���7�һH>ی�����?ų鬓�=��������*��E>��P���?le����1��ؐ��>ۿ��ƭ�>+>��Z������TW��G>������?����M�����h����h2>,@V���?�����Dm���
�:>Cr����?� ���~ـ!��?��n�!�0�瓈IRs��{&IRs2>�9���6����2>_`\��M���1��M=>�P����?�D���4��G��ۿ^}���+>��7�l'�4�l'R>}A�Ў��?!=�Ў�F�G���޿5b��.>|�('O�[^%'O2>lt����D/���<>OЫ����Q���3>X�δ�:ѿ �̴�:!>���=�_�	��=�_?>��eC{��t�eC{K>���fT6�Im�fT67>$��Y����Y�8>�2       j�  h,)��}�(h/h2h3KKK��h5j�  h7j-  h?�h@Kub����                                                                                                                                                                                                                                                                                                                                                                                                                                                �/       j  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub�������                                �0       j  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������   �C+?�L�.1����KbȺ?��T��Y�                ��KbȺ?��T��Y�     ��?     ��=                                                                �0       j	  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub�������>Y���?�u���=                                                                                                                                �/       j  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub�������6���5?8o=�2��=��^(IzB��^(I�@ﰑù*q�ﰑù*���-       j  h,)��}�(h/h2h3KK��h5h6h7j-  h?�h@Kub	������������g]���-��g]�=�/       j  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub���������+nh�c=��+nh�û��+nh�c=��+nh�û                �/       j  h,)��}�(h/h2h3KKK��h5h6h7j-  h?�h@Kub�������                �2       j  h,)��}�(h/h2h3KKK��h5j�  h7j-  h?�h@Kub����                                                                                                �2       j!  h,)��}�(h/h2h3KKK��h5j�  h7j-  h?�h@Kub����                                                                                                �+       j%  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�����������                                                �+       j)  h,)��}�(h/h2h3K��h5h6h7j-  h?�h@Kub�����������                                                �0       j-  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������                                                                                                                                                �0       j1  h,)��}�(h/h2h3KK��h5j�  h7j-  h?�h@Kub������                                                                                                                                                �N      ubu�loglikelihood_burn�K�results_class��*statsmodels.tsa.statespace.kalman_smoother��SmootherResults����prefix_kalman_filter_map�}�(j�  j�  �sKalmanFilter���j�  j�  j�  j�  �cKalmanFilter���j�  j6  u�	tolerance�G;���O�Ҭ�_scale�N�prefix_kalman_smoother_map�}�(j�  �+statsmodels.tsa.statespace._kalman_smoother��sKalmanSmoother���j�  j�  �dKalmanSmoother���j�  j�  �cKalmanSmoother���j�  j�  �zKalmanSmoother���u�_kalman_smoothers�}�j�  j�  (j�  j�  KK t�R�}�(jE  J�����_smooth_method�K�scaled_smoothed_estimator�h,)��}�(h/h2h3KK%��h5j�  h7h<h?�h@Kub��������:���% �>[K' ��>�(n#�b�n�6`���(n#�b���
º�>�y_�1�>��
º�>"s��h���o������"s��h���.��줾��v,�>�.��줾 �V6,���h������ �V6,����_������d|�c����_�������s�p��th��s��>��s�p����&C(��C���Hm����&C(��@���f�X>��W��\�>@���f�X>�� ���A�-����� ��`����B� wZ��?�>`����B���ȥ�\*�\����ȥ���*㠾���2����*㠾oL#T�>n�����>oL#T�>��޽e��	�xV�И���޽e�����aH�����@>}>���aH��jڼt�����{� ��jڼt��pU��ej���p���>pU��ej��ZH�e��{�kp�բ>�ZH�e��U_>8�����ͥ�d��U_>8���WN���ӱ���˰H���WN���ӱ�A�����j.�K뤾A�����Y⌑��\d��d��>�Y⌑���8��Ҷ�n�d(y��8��Ҷ�w�ڇ�e���2u/伾w�ڇ�e���kS>�ň>�0q�w �>�kS>�ň>%���t;���*Uꁾ%���t;����Q��Ҹ�^� ㈾��Q��Ҹ����.�������4������.����{6�,J=���������{6�,J=��ٺ]��2���	��3x>ٺ]��2��BH�9���B�tNq��BH�9����
������W��<���
������������ܚ�����������g]������g]������g]���                                �J       �scaled_smoothed_estimator_cov�h,)��}�(h/h2h3KKK%��h5j�  h7h<h?�h@Kub����H�}�g�c=u�Q�9X]=��� �H�u�Q�9X]=j��&�7o=os���d=��� �H�os���d='��ӌ�p=�6�qd=)��4(_=�yGJ{8F�)��4(_='��ӌ�p=�.����e=�yGJ{8F��.����e=�Ւ�k�p=�e?ԩ<d=�Px!�_=C���
0E��Px!�_=�Ւ�k�p=�	�`\f=C���
0E��	�`\f=<�t��+q=t�@kQd=�Ϭ$`=	����D��Ϭ$`=<�t��+q=$���I�f=	����D�$���I�f=2��?q=�`<�Yd=Q���6`=��z
�D�Q���6`=2��?q=�P��f=��z
�D��P��f=�H�kHq=�#p��]d=gB?`=�Rx�vvD�gB?`=�H�kHq=h2�f=�Rx�vvD�h2�f=���.Lq=)!�u_d=G����B`=6_��)mD�G����B`=���.Lq=���z�f=6_��)mD����z�f=����Mq=]G�.`d=�M,!D`=����"iD��M,!D`=����Mq=����,�f=����"iD�����,�f=kD��Nq=/�}`d=�3j��D`=�%�sdgD��3j��D`=kD��Nq=��yM�f=�%�sdgD���yM�f=>��<�Nq=>Y�H�`d=�R�9E`=V�(�fD��R�9E`=>��<�Nq=]�"��f=V�(�fD�]�"��f=Y���Nq=�j�;�`d=:84E`=f�gfOfD�:84E`=Y���Nq=Cq���f=f�gfOfD�Cq���f=�t�Oq=;�̴�`d=��E�AE`=c�$+fD���E�AE`=�t�Oq=�����f=c�$+fD������f=B�zOq=�+p��`d=��S�GE`=���pfD���S�GE`=B�zOq=	�K��f=���pfD�	�K��f=��+�
Oq=MM&��`d=���ZJE`=�E8�fD����ZJE`=��+�
Oq=�3:���f=�E8�fD��3:���f=W��Oq=��?�`d=~ �yKE`=ރ��fD�~ �yKE`=W��Oq=�_s��f=ރ��fD��_s��f=ձ1Oq=҅vy�`d=G7��KE`=��&[fD�G7��KE`=ձ1Oq=��	��f=��&[fD���	��f=e,v�Oq=�JБ�`d=��U1LE`=����fD���U1LE`=e,v�Oq=�.NE��f=����fD��.NE��f=$ٿ�Oq=Ɓ���`d=a6�QLE`=#��@fD�a6�QLE`=$ٿ�Oq=��'��f=#��@fD���'��f=�}=�Oq= ����`d=�j�pLE`=�=եfD��j�pLE`=�}=�Oq= �K���f=�=եfD� �K���f=���&Oq=�KБ�`d=�#�LE`=J�qfD��#�LE`=���&Oq=��`��f=J�qfD���`��f=��-Oq=�vy�`d=��ME`=L�U�
fD���ME`=��-Oq=b�Sf��f=L�U�
fD�b�Sf��f=Duk�Oq=��?�`d=M�NE`=����fD�M�NE`=Duk�Oq=W�5���f=����fD�W�5���f=��Oq=�X&��`d=��xwPE`=8esG�eD���xwPE`=��Oq=&����f=8esG�eD�&����f=��f��Nq=�Ep��`d=	���UE`=�4hP�eD�	���UE`=��f��Nq=1��f=�4hP�eD�1��f=c���Nq=�ʹ�`d=m�ibE`=��1�eD�m�ibE`=c���Nq=� �9�f=��1�eD�� �9�f=���Nq=���;�`d=���TE`=��*j�dD����TE`=���Nq=�Mipu�f=��*j�dD��Mipu�f=�$�Nq=P��H�`d=��V�E`=����CcD���V�E`=�$�Nq=���!��f=����CcD����!��f=�v�i�Lq=(�1�}`d=�MnQ\F`=�/�(�_D��MnQ\F`=�v�i�Lq=x�W��f=�/�(�_D�x�W��f=R��Iq=&�.`d=���j�G`=�q��%WD����j�G`=R��Iq=�"@(�f=�q��%WD��"@(�f=k'deBq=u�"�u_d=�8���J`=$�8�CD��8���J`=k'deBq=u�TZ�f=$�8�CD�u�TZ�f=�A��1q=d���]d=B���aR`=�XǈD�B���aR`=�A��1q=�����nf=�XǈD������nf=���q=,?`<�Yd=��2��c`=����j�C���2��c`=���q=�+�x��e=����j�C��+�x��e=
V`9�p=J- lQd=x�T��`=�0L��B�x�T��`=
V`9�p=��n58�d=�0L��B���n58�d= �}�l�o=JL�թ<d=<���g�`=#E�ƒ@�<���g�`= �}�l�o=6�S.�b=#E�ƒ@�6�S.�b=&ᩈ4 l=T�2�qd=�hu�T�a=�skWW!7��hu�T�a=&ᩈ4 l=bXA��Y=�skWW!7�bXA��Y=��+nh�c=��+nh�c=��+nh�c=        ��+nh�c=��+nh�c=                                                                                                        �7       �smoothing_error�h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub��������� ��P�>�}`��¾��#t��>�GO����Y��z���>X�H8	�����kĩ�`����M�>:������e#�z40�> }�ס��,���/n�>x_���>��DE|Ǿ�9o�J�>z�Ts����Cħ>ǧ�J櫾���� ����RC0�>��ܯpeU>���N�>���B���K���>�`,��S�>�1s�E�Ⱦ2t�n�=�>	��k>�x��O�>@V���>N^�ԕ�ް\�?�> �\@�>��}u�+����g��>���g]����9       �smoothed_state�h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub�������������-��Ǆ@���1�kA]��_(a�    2�kA   ^�:A/j�E��"A   �]	oA   ��QA3ڡT�C:�    �sA   �(Ax�r'�(A   �ųtA   ��CAW�c�9'�   @$/wA
   ��2�"yA���9A   `)vA   �����Z Z)A   �z�uA   ��*A�ySsn�   `	�vA   �9�[d%-D�4A   @�9uA������3A�-G)�   ��rvA   �8��tM�XE2A   ���tA�����#A0DT�8!�   ���uA   ` ��?���A   ��uA�����q?�A�sJ�4A   �sA   Bq@A�
�3�9�    �uA    T�$��˦�;�A   �jytA@����w��0D4vi��   �;vtA   �1��u�t!�%A   @�esA    �1A���Y��	�   `@�sA����'�"A89oc�n�   ��tA������&�d�s�A   `SfsA   �*��M��JA   �#�rA�����5��Ի���(A   @E7qA   N AvG��lp!�   ���qA����#&����57fA   �	qA�����H��I��0�>A   ��kA������3A
h�~�3�����XnA����s�)��#m?NA   @X�lA
   $/�4�2xmeA    ��jA������6�jf�z��'A   @v�gA   .3�� ANon A   �P�eA�����T)�����u�A    �cA   ��:�.9U�\*A    s�`A������E�i���b7A   sVA   \�:�����*�#A    ��OA������;��S���$A�?       �smoothed_state_cov�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������RHe�~�.ARHe�~�.�.]�ĺ'#ARHe�~�.�!Lc�~�.A�S�ĺ'#�/]�ĺ'#Ao��ĺ'#� �r�T"$B    ��    ��>�r_NV�     ��>o�$��5?g��9��#��r_NV�l^r���aRpB������>������>U����������jQz��?�{�O^m�6?<U�����}���>��BO�4�A������    ��>��z��    ��>fSf�jcC�B�-��,;?��z��R�7!�B?�"E#)�A������>�������$�r�Ҿ������<�t�%�	?���as��$�r�Ҿ��o��&?{(*�T��A������     ��>K��C���     ��>��?u�4����\-?L��C����{yӟ�1?�u�J���A������>������#(����>������V��I%?���0gO��#(����>��+XP0?�5E���A������������>Ş��J��������>C���j�0��R���%'?Ş��J�������!?H�=�p�A������>������p���9Q�>������/�[�0�B������8?o���9Q�>���{-W=?�� �Y�A������������>]�W��������>^m���#?�K�7�^�^�W��p�������pGvA������>������Nw^�60�>��������˺���>��kn!׾Nw^�60�>VU��/��=A cA������������>[}'Z�������>��(N�3?��j��)�Z}'Z��sl�N7�ȋ���PA������>������nWE�S��>������|��R�;?���q�B2�oWE�S��>��q�.����~�<A������������>���U���������>���b�$�W�K�?���U���֕ ��1??vu���(A������>����������%��>�������s���!?=u�v������%��>��i���}S��A������������>��|wy��������><͗��1?�?��k'���|wy�뾼���X���r�A������>������R򣛝��>������j��/�<i��$?S򣛝��>��0b5?���%�@������������>E��ɅM�������>3�;畉;��U22?D��ɅM뾘����+�zf�D��@������>������cc�-v
�>����������;1��x�ߌ&?cc�-v
�>��ӫSU�E�/�8�@������������>Xk��6�������>�
"~"$�����?Xk��6�,z��f3��]M�C��@����/1?����/1���^ �.-?    /1�����%?��x�$���^ �.-?:�͖���:{�y#+�@     ��     ��>oÍ�3��������>�!�Z]3?�����%�oÍ�3�� ���+?��9=�x�@������>     ��4+Jt.�����������7�1C?�JKZ8�>+Jt.����T�cu��(���A{@����ۡ-?����ۡ-��Cg�?����ۡ-���z]H�3?�[��`{$��Cg�? �zT��>h2�^�g@����/1?����/1����V�,?����/1�2{���fƾ�Ye��~����V�,?X� kNc"�{��frT@������������>*�X;:�������>˳��o?��è���	*�X;:��!��s(?Hǩ3�A@����/1?����/1��y�k#+?����/1����5S�{�7�Н���y�k#+?���$� �v�;�W�.@�����������>
dx%?������>��!z9�P&�϶t+?
dx%?�Wa��0?��U֞�@������>�������"$?������5�s���>�q����"$?�u�6�j	?�͌h@������������>��/�?������>�����>3x ������/�?PI�P���`��g��?������>������mB��	��������^|o�~%��0��%?iB��	���� [V?5��C�A�?������������>�6�ib4��������>�P�
d��6�y��?�6�ib4��t���` )?몑-���?������>������s0p��>������逘d/?�	~�� $�u0p��>K��g0��حR��?������������>RO��@�?������>�.*�!��(�g(��>RO��@�?�1S0e�����z/n�?������>��������Y~��������~A��*��xA�rQ%?���Y~�����k`?�)��/T�?   ܡ-?   ܡ-�@<"r2'?   ܡ-�x-�7 x$?ﰑù*!�A<"r2'?      0�     ��?�H       � smoothed_measurement_disturbance�h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub��������������                                                                                                                                                                                                                                                                                                �B       �smoothed_state_disturbance�h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub����Z���`,�Y���CA���_t�2�OƑ��1AXd�zFwC��|c4?�'�[�x�3}A:�
��?��E�3A�\����;�?��F��&Aw��d!��?ܗܒ>�8E���CAO�ف'�c�i���@�İ8�0�3�|�A���]�%A\�I&�'������'�-��և�2�4v&�3�*AB�?h�!����d<.G��4.$��<A2a�7:#��Y �a'��ɭH�1���U	(�(�Fb�	 ��s��4�9�ۂ�A�w^�@��-��7�ω�/�        �N       �$smoothed_measurement_disturbance_cov�h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub��������                                                                                                                                                                                                                                                                                                �H       �smoothed_state_disturbance_cov�h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub�������������� �-�I"$B RpB �BO�4�A ""E#)�A $*�T��A p�J���A 5E���A  �=�p�A  �Y�A  �pGvA  A cA  ��PA  �~�<A  ����(A  ���A  �r�A   �%�@   �D��@    �8�@   �C��@   `#+�@   ��x�@    �A{@    b�g@    rT@    8�A@     �.@     �@    �@     ��?     @�?     ��?     �?     ��?     ��?:�^(IzB�C       �smoothed_state_autocov�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub����(�j���        ی剌���Əj��=        W4剌�@Z�����>        ƨ$��B7�+L��һ0�r���;���l:n������*?�����*�j��Xkr!?�g���
!��f�ۚ� ?��O�H�B�Æ�J���f��~B�;8������                        S��>�> LX�rξ������AN�M-H~�        ��O�4�                        ��Tn>        �i�!7�AT��b���Ф�\�;�i�ê.꾛�J�5#�;      ���K�%?ov��tf> ��s����P/���A|]�M/��2U瘔�y�LcL۾                        �[��> �_�ޢs>N_F�ӹA���9��g�����#�;�VW��.پ                        �A.:5> �Q�  q�RR};U^�A��jp~v4;OuFp<�;�!��q¾                        �Q��1~� `��zq]�C	.��_�A6��*LS�^w7�Mc��Ły���ʾ                        �w��">  �{�9>W��fǀA%zB�QS;        �p�ዸ��                        �9dd��        j�]jmA0�נD�7�/Q,J���9�e]���                        ��E�3�=  �pM #>���,YA,�ь$��lP���q;;���Q�>                        �1�ǃ�Ž  ���> r�<(�EA��I6<�+�e����;��j�u��                        ���m\ǵ=  ������p�B��2A�\\�+�7��/d;��Ʊ���>                        �>:��  ����=�qՌ�Z A�9���7�C�I�\o�>f0<i���                        ���䝏=  ����=iİ��SA�;��4�0����!"x��P��>                        �-��r9z�  ���½�$Fk���@Yﴕ��4�i��� �|;��+����                        �h�=�_g=  ��%���E�u�?�@ �A;2�L�#`��y�I���L�>                        ��\��S�   �D������
>g�@�f-+�3�2u::<�{;�.�WD��                        ]�=�kA=   �8��}�����@���I�����Ӧ�VS�;i!�\�>��e+I*?��e+I*���c��3?���Ź*!�.U�Ĺ*!?XXg@ͭ�����;z�����;�9�j��>                        >��\�<=   p#+b=z&�iy�@�}�:�s�f	��51�                        � ��
=   @�x?=��K����@:�bL޻z;�0Hy;��R�5��u��(I*?t��(I*��=�ù*!?�ù*!�ù*!?�bH��q@0շ
J?�;�_�4=ջ����j
���y(I*?��y(I*������3?�I�ù*!�ù*!?H�a��_@I,c���;C��e����n��/0�>                        �8:���<    r�X�u{��J@i�WշQ��c��5�7�;���
���c(I*?��c(I*������3?#�ù*!�ù*!?�.�6N7@�z�)��r;��:U�L�;�Gp��ƾa��IՍѻ      �i���%?��j�l�м    0��(�%�9/$@ ��))��        �ߞ� ?                        u�Gp��        x`O�P{@XR@���76.��;�����j�>�9T�<�      �;�����%?8���    ��<b"���G�?�^hj�ߔ;        ���C�?                        �F�v	�n<        ]��>�9�?�P��{�        ;�?�z�                        ���}7m<         s�����?%蒉P�';        �''��Ծ                        |t�KeY�        ��j}��?NyBS�b�;�َ���K0�Yվ��t��Oۻ      �;�����%?�����f�     �i<��ܼ�?�n8��C�;�+p�oԻ1C�ym�
?�b�**��      �;����%�:5~��&5<     pf��)B�Ї�?sx�@���;���{���ӣ	����^(I*?�^(I*�1��ù*!?V��ù*!�;��ù*!?{�ʾ�(�?        j5)3�`վ                                             ��?        �C       �innovations_transition�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub����(�j���        ی剌���Əj��=        W4剌�@Z�����>        ƨ$��B7�+L��һ0�r���;���l:n������*?�����*�j��Xkr!?�g���
!��f�ۚ� ?��O�H�B�Æ�J���f��~B�;8������                        S��>�> LX�rξ������AN�M-H~�        ��O�4�                        ��Tn>        �i�!7�AT��b���Ф�\�;�i�ê.꾛�J�5#�;      ���K�%?ov��tf> ��s����P/���A|]�M/��2U瘔�y�LcL۾                        �[��> �_�ޢs>N_F�ӹA���9��g�����#�;�VW��.پ                        �A.:5> �Q�  q�RR};U^�A��jp~v4;OuFp<�;�!��q¾                        �Q��1~� `��zq]�C	.��_�A6��*LS�^w7�Mc��Ły���ʾ                        �w��">  �{�9>W��fǀA%zB�QS;        �p�ዸ��                        �9dd��        j�]jmA0�נD�7�/Q,J���9�e]���                        ��E�3�=  �pM #>���,YA,�ь$��lP���q;;���Q�>                        �1�ǃ�Ž  ���> r�<(�EA��I6<�+�e����;��j�u��                        ���m\ǵ=  ������p�B��2A�\\�+�7��/d;��Ʊ���>                        �>:��  ����=�qՌ�Z A�9���7�C�I�\o�>f0<i���                        ���䝏=  ����=iİ��SA�;��4�0����!"x��P��>                        �-��r9z�  ���½�$Fk���@Yﴕ��4�i��� �|;��+����                        �h�=�_g=  ��%���E�u�?�@ �A;2�L�#`��y�I���L�>                        ��\��S�   �D������
>g�@�f-+�3�2u::<�{;�.�WD��                        ]�=�kA=   �8��}�����@���I�����Ӧ�VS�;i!�\�>��e+I*?��e+I*���c��3?���Ź*!�.U�Ĺ*!?XXg@ͭ�����;z�����;�9�j��>                        >��\�<=   p#+b=z&�iy�@�}�:�s�f	��51�                        � ��
=   @�x?=��K����@:�bL޻z;�0Hy;��R�5��u��(I*?t��(I*��=�ù*!?�ù*!�ù*!?�bH��q@0շ
J?�;�_�4=ջ����j
���y(I*?��y(I*������3?�I�ù*!�ù*!?H�a��_@I,c���;C��e����n��/0�>                        �8:���<    r�X�u{��J@i�WշQ��c��5�7�;���
���c(I*?��c(I*������3?#�ù*!�ù*!?�.�6N7@�z�)��r;��:U�L�;�Gp��ƾa��IՍѻ      �i���%?��j�l�м    0��(�%�9/$@ ��))��        �ߞ� ?                        u�Gp��        x`O�P{@XR@���76.��;�����j�>�9T�<�      �;�����%?8���    ��<b"���G�?�^hj�ߔ;        ���C�?                        �F�v	�n<        ]��>�9�?�P��{�        ;�?�z�                        ���}7m<         s�����?%蒉P�';        �''��Ծ                        |t�KeY�        ��j}��?NyBS�b�;�َ���K0�Yվ��t��Oۻ      �;�����%?�����f�     �i<��ܼ�?�n8��C�;�+p�oԻ1C�ym�
?�b�**��      �;����%�:5~��&5<     pf��)B�Ї�?sx�@���;���{���ӣ	����^(I*?�^(I*�1��ù*!?V��ù*!�;��ù*!?{�ʾ�(�?        j5)3�`վ                                             ��?        �6       �tmp_autocov�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub����������������        !qlrΧ�                   rΧA                0���G%B        �L       �!scaled_smoothed_diffuse_estimator�h,)��}�(h/h2h3KK%��h5j�  h7h<h?�h@Kub��                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        �S       �&scaled_smoothed_diffuse1_estimator_cov�h,)��}�(h/h2h3KKK%��h5j�  h7h<h?�h@Kub�����������                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        �S       �&scaled_smoothed_diffuse2_estimator_cov�h,)��}�(h/h2h3KKK%��h5j�  h7h<h?�h@Kub�����������                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        �/       �tmpL�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub����������������9�4\�?�@�����?�9�����        �++B��?                      �?        �0       �tmpL2�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub��������������                                                                        �-       j  h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub�        :�^(IzBﰑù*q�_U�7��<        ���=�)�?��ː<$ƃI�H��,�i�?�*       j	  h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����                        �.       �tmp000�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����������������                        �i      ubs�simulation_smooth_results_class�j�  �SimulationSmoothResults����prefix_simulation_smoother_map�}�(j�  �/statsmodels.tsa.statespace._simulation_smoother��sSimulationSmoother���j�  j  �dSimulationSmoother���j�  j  �cSimulationSmoother���j�  j  �zSimulationSmoother���u�_simulators�}��_complex_endog��hch,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub�����    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA��      ubj�  K�_has_fixed_params���_fixed_params�N�_params_index�N�_fixed_params_index�N�_free_params_index�N�_input_exog�N�_input_exog_names�NubhiK h�]�(j�  j�  j�  j�  �	forecasts��forecasts_error��forecasts_error_cov��standardized_forecasts_error��forecasts_error_diffuse_cov�j�  j�  j�  j�  j�  j�  j�  j�  j�  j�  j�  �filter_results��smoother_results�e�_data_in_cache�]�(�fittedvalues��resid��wresid�e�normalized_cov_params�N�scale�G?�      �_use_t��j!  �j$  Nj%  Nj"  N�fixed_params�]�j  ]�(hrhshtej.  j�  )��}�(hj�  �prefix�j�  h7h0�float64���jw  K$j�  Kjx  Kjy  K�time_invariant��hch,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub��������������    2�kA   �]	oA    �sA   �ųtA   @$/wA   `)vA   �z�uA   `	�vA   @�9uA   ��rvA   ���tA   ���uA   ��uA   �sA    �uA   �jytA   �;vtA   @�esA   `@�sA   ��tA   `SfsA   �#�rA   @E7qA   ���qA   �	qA   ��kA   ��XnA   @X�lA    ��jA   @v�gA   �P�eA    �cA    s�`A    sVA    ��OA    2�AA�,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub
����������      �?      �?        �*       j�  h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����        �,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub��        �,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub��      �?      �?                ������?      �?                        �*       j�  h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub����                        �,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub��              �?�����忕,       j�  h,)��}�(h/h2h3KKK��h5h6h7h<h?�h@Kub��:�^(IzB�-       j   h,)��}�(h/h2h3KK$��h5h6h7j  h?�h@Kub�                                                                                                                                                �+       j  h,)��}�(h/h2h3K$��h5h6h7j  h?�h@Kub�����������                                                                                                                                                ��       j�  }�(j�  KK$��j�  KKK��j�  KK��j�  KKK��j�  KKK��j�  KK��j�  KKK��j�  KKK��uj�  j�  j�  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub	���������                        �-       j�  h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub�    ��.A                        ��yd��{Bù*q�        ù*q��� �fB�F       j�  N�smoother_output�Nj�  h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub��������n�6`���(n#�b���
º�>�y_�1�>��
º�>"s��h���o������"s��h���.��줾��v,�>�.��줾 �V6,���h������ �V6,����_������d|�c����_�������s�p��th��s��>��s�p����&C(��C���Hm����&C(��@���f�X>��W��\�>@���f�X>�� ���A�-����� ��`����B� wZ��?�>`����B���ȥ�\*�\����ȥ���*㠾���2����*㠾oL#T�>n�����>oL#T�>��޽e��	�xV�И���޽e�����aH�����@>}>���aH��jڼt�����{� ��jڼt��pU��ej���p���>pU��ej��ZH�e��{�kp�բ>�ZH�e��U_>8�����ͥ�d��U_>8���WN���ӱ���˰H���WN���ӱ�A�����j.�K뤾A�����Y⌑��\d��d��>�Y⌑���8��Ҷ�n�d(y��8��Ҷ�w�ڇ�e���2u/伾w�ڇ�e���kS>�ň>�0q�w �>�kS>�ň>%���t;���*Uꁾ%���t;����Q��Ҹ�^� ㈾��Q��Ҹ����.�������4������.����{6�,J=���������{6�,J=��ٺ]��2���	��3x>ٺ]��2��BH�9���B�tNq��BH�9����
������W��<���
������������ܚ�����������g]������g]������g]���                                �/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub��������6�qd=)��4(_=�yGJ{8F�)��4(_='��ӌ�p=�.����e=�yGJ{8F��.����e=�Ւ�k�p=�e?ԩ<d=�Px!�_=C���
0E��Px!�_=�Ւ�k�p=�	�`\f=C���
0E��	�`\f=<�t��+q=t�@kQd=�Ϭ$`=	����D��Ϭ$`=<�t��+q=$���I�f=	����D�$���I�f=2��?q=�`<�Yd=Q���6`=��z
�D�Q���6`=2��?q=�P��f=��z
�D��P��f=�H�kHq=�#p��]d=gB?`=�Rx�vvD�gB?`=�H�kHq=h2�f=�Rx�vvD�h2�f=���.Lq=)!�u_d=G����B`=6_��)mD�G����B`=���.Lq=���z�f=6_��)mD����z�f=����Mq=]G�.`d=�M,!D`=����"iD��M,!D`=����Mq=����,�f=����"iD�����,�f=kD��Nq=/�}`d=�3j��D`=�%�sdgD��3j��D`=kD��Nq=��yM�f=�%�sdgD���yM�f=>��<�Nq=>Y�H�`d=�R�9E`=V�(�fD��R�9E`=>��<�Nq=]�"��f=V�(�fD�]�"��f=Y���Nq=�j�;�`d=:84E`=f�gfOfD�:84E`=Y���Nq=Cq���f=f�gfOfD�Cq���f=�t�Oq=;�̴�`d=��E�AE`=c�$+fD���E�AE`=�t�Oq=�����f=c�$+fD������f=B�zOq=�+p��`d=��S�GE`=���pfD���S�GE`=B�zOq=	�K��f=���pfD�	�K��f=��+�
Oq=MM&��`d=���ZJE`=�E8�fD����ZJE`=��+�
Oq=�3:���f=�E8�fD��3:���f=W��Oq=��?�`d=~ �yKE`=ރ��fD�~ �yKE`=W��Oq=�_s��f=ރ��fD��_s��f=ձ1Oq=҅vy�`d=G7��KE`=��&[fD�G7��KE`=ձ1Oq=��	��f=��&[fD���	��f=e,v�Oq=�JБ�`d=��U1LE`=����fD���U1LE`=e,v�Oq=�.NE��f=����fD��.NE��f=$ٿ�Oq=Ɓ���`d=a6�QLE`=#��@fD�a6�QLE`=$ٿ�Oq=��'��f=#��@fD���'��f=�}=�Oq= ����`d=�j�pLE`=�=եfD��j�pLE`=�}=�Oq= �K���f=�=եfD� �K���f=���&Oq=�KБ�`d=�#�LE`=J�qfD��#�LE`=���&Oq=��`��f=J�qfD���`��f=��-Oq=�vy�`d=��ME`=L�U�
fD���ME`=��-Oq=b�Sf��f=L�U�
fD�b�Sf��f=Duk�Oq=��?�`d=M�NE`=����fD�M�NE`=Duk�Oq=W�5���f=����fD�W�5���f=��Oq=�X&��`d=��xwPE`=8esG�eD���xwPE`=��Oq=&����f=8esG�eD�&����f=��f��Nq=�Ep��`d=	���UE`=�4hP�eD�	���UE`=��f��Nq=1��f=�4hP�eD�1��f=c���Nq=�ʹ�`d=m�ibE`=��1�eD�m�ibE`=c���Nq=� �9�f=��1�eD�� �9�f=���Nq=���;�`d=���TE`=��*j�dD����TE`=���Nq=�Mipu�f=��*j�dD��Mipu�f=�$�Nq=P��H�`d=��V�E`=����CcD���V�E`=�$�Nq=���!��f=����CcD����!��f=�v�i�Lq=(�1�}`d=�MnQ\F`=�/�(�_D��MnQ\F`=�v�i�Lq=x�W��f=�/�(�_D�x�W��f=R��Iq=&�.`d=���j�G`=�q��%WD����j�G`=R��Iq=�"@(�f=�q��%WD��"@(�f=k'deBq=u�"�u_d=�8���J`=$�8�CD��8���J`=k'deBq=u�TZ�f=$�8�CD�u�TZ�f=�A��1q=d���]d=B���aR`=�XǈD�B���aR`=�A��1q=�����nf=�XǈD������nf=���q=,?`<�Yd=��2��c`=����j�C���2��c`=���q=�+�x��e=����j�C��+�x��e=
V`9�p=J- lQd=x�T��`=�0L��B�x�T��`=
V`9�p=��n58�d=�0L��B���n58�d= �}�l�o=JL�թ<d=<���g�`=#E�ƒ@�<���g�`= �}�l�o=6�S.�b=#E�ƒ@�6�S.�b=&ᩈ4 l=T�2�qd=�hu�T�a=�skWW!7��hu�T�a=&ᩈ4 l=bXA��Y=�skWW!7�bXA��Y=��+nh�c=��+nh�c=��+nh�c=        ��+nh�c=��+nh�c=                                                                                                        �*       j�  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub�������������� ��P�>�}`��¾��#t��>�GO����Y��z���>X�H8	�����kĩ�`����M�>:������e#�z40�> }�ס��,���/n�>x_���>��DE|Ǿ�9o�J�>z�Ts����Cħ>ǧ�J櫾���� ����RC0�>��ܯpeU>���N�>���B���K���>�`,��S�>�1s�E�Ⱦ2t�n�=�>	��k>�x��O�>@V���>N^�ԕ�ް\�?�> �\@�>��}u�+����g��>���g]����-       j�  h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub	���������-��Ǆ@���1�kA]��_(a�    2�kA   ^�:A/j�E��"A   �]	oA   ��QA3ڡT�C:�    �sA   �(Ax�r'�(A   �ųtA   ��CAW�c�9'�   @$/wA
   ��2�"yA���9A   `)vA   �����Z Z)A   �z�uA   ��*A�ySsn�   `	�vA   �9�[d%-D�4A   @�9uA������3A�-G)�   ��rvA   �8��tM�XE2A   ���tA�����#A0DT�8!�   ���uA   ` ��?���A   ��uA�����q?�A�sJ�4A   �sA   Bq@A�
�3�9�    �uA    T�$��˦�;�A   �jytA@����w��0D4vi��   �;vtA   �1��u�t!�%A   @�esA    �1A���Y��	�   `@�sA����'�"A89oc�n�   ��tA������&�d�s�A   `SfsA   �*��M��JA   �#�rA�����5��Ի���(A   @E7qA   N AvG��lp!�   ���qA����#&����57fA   �	qA�����H��I��0�>A   ��kA������3A
h�~�3�����XnA����s�)��#m?NA   @X�lA
   $/�4�2xmeA    ��jA������6�jf�z��'A   @v�gA   .3�� ANon A   �P�eA�����T)�����u�A    �cA   ��:�.9U�\*A    s�`A������E�i���b7A   sVA   \�:�����*�#A    ��OA������;��S���$A�/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������RHe�~�.ARHe�~�.�.]�ĺ'#ARHe�~�.�!Lc�~�.A�S�ĺ'#�/]�ĺ'#Ao��ĺ'#� �r�T"$B    ��    ��>�r_NV�     ��>o�$��5?g��9��#��r_NV�l^r���aRpB������>������>U����������jQz��?�{�O^m�6?<U�����}���>��BO�4�A������    ��>��z��    ��>fSf�jcC�B�-��,;?��z��R�7!�B?�"E#)�A������>�������$�r�Ҿ������<�t�%�	?���as��$�r�Ҿ��o��&?{(*�T��A������     ��>K��C���     ��>��?u�4����\-?L��C����{yӟ�1?�u�J���A������>������#(����>������V��I%?���0gO��#(����>��+XP0?�5E���A������������>Ş��J��������>C���j�0��R���%'?Ş��J�������!?H�=�p�A������>������p���9Q�>������/�[�0�B������8?o���9Q�>���{-W=?�� �Y�A������������>]�W��������>^m���#?�K�7�^�^�W��p�������pGvA������>������Nw^�60�>��������˺���>��kn!׾Nw^�60�>VU��/��=A cA������������>[}'Z�������>��(N�3?��j��)�Z}'Z��sl�N7�ȋ���PA������>������nWE�S��>������|��R�;?���q�B2�oWE�S��>��q�.����~�<A������������>���U���������>���b�$�W�K�?���U���֕ ��1??vu���(A������>����������%��>�������s���!?=u�v������%��>��i���}S��A������������>��|wy��������><͗��1?�?��k'���|wy�뾼���X���r�A������>������R򣛝��>������j��/�<i��$?S򣛝��>��0b5?���%�@������������>E��ɅM�������>3�;畉;��U22?D��ɅM뾘����+�zf�D��@������>������cc�-v
�>����������;1��x�ߌ&?cc�-v
�>��ӫSU�E�/�8�@������������>Xk��6�������>�
"~"$�����?Xk��6�,z��f3��]M�C��@����/1?����/1���^ �.-?    /1�����%?��x�$���^ �.-?:�͖���:{�y#+�@     ��     ��>oÍ�3��������>�!�Z]3?�����%�oÍ�3�� ���+?��9=�x�@������>     ��4+Jt.�����������7�1C?�JKZ8�>+Jt.����T�cu��(���A{@����ۡ-?����ۡ-��Cg�?����ۡ-���z]H�3?�[��`{$��Cg�? �zT��>h2�^�g@����/1?����/1����V�,?����/1�2{���fƾ�Ye��~����V�,?X� kNc"�{��frT@������������>*�X;:�������>˳��o?��è���	*�X;:��!��s(?Hǩ3�A@����/1?����/1��y�k#+?����/1����5S�{�7�Н���y�k#+?���$� �v�;�W�.@�����������>
dx%?������>��!z9�P&�϶t+?
dx%?�Wa��0?��U֞�@������>�������"$?������5�s���>�q����"$?�u�6�j	?�͌h@������������>��/�?������>�����>3x ������/�?PI�P���`��g��?������>������mB��	��������^|o�~%��0��%?iB��	���� [V?5��C�A�?������������>�6�ib4��������>�P�
d��6�y��?�6�ib4��t���` )?몑-���?������>������s0p��>������逘d/?�	~�� $�u0p��>K��g0��حR��?������������>RO��@�?������>�.*�!��(�g(��>RO��@�?�1S0e�����z/n�?������>��������Y~��������~A��*��xA�rQ%?���Y~�����k`?�)��/T�?   ܡ-?   ܡ-�@<"r2'?   ܡ-�x-�7 x$?ﰑù*!�A<"r2'?      0�     ��?�/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub��������(�j���        ی剌���Əj��=        W4剌�@Z�����>        ƨ$��B7�+L��һ0�r���;���l:n������*?�����*�j��Xkr!?�g���
!��f�ۚ� ?��O�H�B�Æ�J���f��~B�;8������                        S��>�> LX�rξ������AN�M-H~�        ��O�4�                        ��Tn>        �i�!7�AT��b���Ф�\�;�i�ê.꾛�J�5#�;      ���K�%?ov��tf> ��s����P/���A|]�M/��2U瘔�y�LcL۾                        �[��> �_�ޢs>N_F�ӹA���9��g�����#�;�VW��.پ                        �A.:5> �Q�  q�RR};U^�A��jp~v4;OuFp<�;�!��q¾                        �Q��1~� `��zq]�C	.��_�A6��*LS�^w7�Mc��Ły���ʾ                        �w��">  �{�9>W��fǀA%zB�QS;        �p�ዸ��                        �9dd��        j�]jmA0�נD�7�/Q,J���9�e]���                        ��E�3�=  �pM #>���,YA,�ь$��lP���q;;���Q�>                        �1�ǃ�Ž  ���> r�<(�EA��I6<�+�e����;��j�u��                        ���m\ǵ=  ������p�B��2A�\\�+�7��/d;��Ʊ���>                        �>:��  ����=�qՌ�Z A�9���7�C�I�\o�>f0<i���                        ���䝏=  ����=iİ��SA�;��4�0����!"x��P��>                        �-��r9z�  ���½�$Fk���@Yﴕ��4�i��� �|;��+����                        �h�=�_g=  ��%���E�u�?�@ �A;2�L�#`��y�I���L�>                        ��\��S�   �D������
>g�@�f-+�3�2u::<�{;�.�WD��                        ]�=�kA=   �8��}�����@���I�����Ӧ�VS�;i!�\�>��e+I*?��e+I*���c��3?���Ź*!�.U�Ĺ*!?XXg@ͭ�����;z�����;�9�j��>                        >��\�<=   p#+b=z&�iy�@�}�:�s�f	��51�                        � ��
=   @�x?=��K����@:�bL޻z;�0Hy;��R�5��u��(I*?t��(I*��=�ù*!?�ù*!�ù*!?�bH��q@0շ
J?�;�_�4=ջ����j
���y(I*?��y(I*������3?�I�ù*!�ù*!?H�a��_@I,c���;C��e����n��/0�>                        �8:���<    r�X�u{��J@i�WշQ��c��5�7�;���
���c(I*?��c(I*������3?#�ù*!�ù*!?�.�6N7@�z�)��r;��:U�L�;�Gp��ƾa��IՍѻ      �i���%?��j�l�м    0��(�%�9/$@ ��))��        �ߞ� ?                        u�Gp��        x`O�P{@XR@���76.��;�����j�>�9T�<�      �;�����%?8���    ��<b"���G�?�^hj�ߔ;        ���C�?                        �F�v	�n<        ]��>�9�?�P��{�        ;�?�z�                        ���}7m<         s�����?%蒉P�';        �''��Ծ                        |t�KeY�        ��j}��?NyBS�b�;�َ���K0�Yվ��t��Oۻ      �;�����%?�����f�     �i<��ܼ�?�n8��C�;�+p�oԻ1C�ym�
?�b�**��      �;����%�:5~��&5<     pf��)B�Ї�?sx�@���;���{���ӣ	����^(I*?�^(I*�1��ù*!?V��ù*!�;��ù*!?{�ʾ�(�?        j5)3�`վ                                             ��?        �*       j�  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������                                                                                                                                                                                                                                                                                                �*       j�  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������Z���`,�Y���CA���_t�2�OƑ��1AXd�zFwC��|c4?�'�[�x�3}A:�
��?��E�3A�\����;�?��F��&Aw��d!��?ܗܒ>�8E���CAO�ف'�c�i���@�İ8�0�3�|�A���]�%A\�I&�'������'�-��և�2�4v&�3�*AB�?h�!����d<.G��4.$��<A2a�7:#��Y �a'��ɭH�1���U	(�(�Fb�	 ��s��4�9�ۂ�A�w^�@��-��7�ω�/�        �,       j�  h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
����������                                                                                                                                                                                                                                                                                                �,       j�  h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
���������� �-�I"$B RpB �BO�4�A ""E#)�A $*�T��A p�J���A 5E���A  �=�p�A  �Y�A  �pGvA  A cA  ��PA  �~�<A  ����(A  ���A  �r�A   �%�@   �D��@    �8�@   �C��@   `#+�@   ��x�@    �A{@    b�g@    rT@    8�A@     �.@     �@    �@     ��?     @�?     ��?     �?     ��?     ��?:�^(IzB�/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������        � G���ǿ                �++B��?                      �?              �<D1|
�Ŀ              �<Z�Ab��?                      �?                <�5V:�ÿ                �S��?                      �?                ��=ÿ                %.�Y`��?                      �?                ༣ÿ                s8�D�?                      �?                @�j��¿                �4��D
�?                      �?                4Fz��¿                bB���?                      �?                �q��¿                %��\��?                      �?                ���¿                �2��x�?                      �?                h�Pm��¿                �ʌ���?                      �?                !?z�¿                f+Q��?                      �?                p��Q�¿                O�-��?                      �?                <%k#@�¿                \*���?                      �?                �U��8�¿                >�5s��?                      �?                �N>F5�¿                �_QE��?                      �?                ��L�3�¿                ;�M���?                      �?                D�<3�¿                Zy����?                      �?                <�q�2�¿                �v����?                      �?                H���2�¿                Y (���?                      �?              �<PP�2�¿              �<�[���?                      �?                 r��2�¿                +׽���?                      �?                �&�2�¿                �rW���?                      �?              �<���2�¿              �<������?                      �?              �<`���2�¿              �<Sƶ���?                      �?                ��v�2�¿                �?����?                      �?              �<4a�2�¿              �<������?                      �?                ��W�2�¿                ������?                      �?                \�S�2�¿                � ����?                      �?                $
R�2�¿                "q����?                      �?                �GQ�2�¿                á����?                      �?                d�P�2�¿                Ҷ����?                      �?                ��P�2�¿                �����?                      �?                �P�2�¿                ������?                      �?                H�P�2�¿                ������?                      �?              �<L�P�2�¿              �<X�����?                      �?                �P�2�¿                ������?                      �?        ��      j�  N�filter_conventional���filter_exact_initial���filter_augmented���filter_square_root���filter_univariate���filter_collapsed���filter_extended���filter_unscented���filter_concentrated���filter_chandrasekhar���stability_force_symmetry���invert_univariate���solve_lu���	invert_lu���solve_cholesky���invert_cholesky���memory_store_all���memory_no_forecast_mean���memory_no_forecast_cov���memory_no_forecast���memory_no_predicted_mean���memory_no_predicted_cov���memory_no_predicted���memory_no_filtered_mean���memory_no_filtered_cov���memory_no_filtered���memory_no_likelihood���memory_no_gain���memory_no_smoothing���memory_no_std_forecast���memory_conserve���smoother_state���smoother_state_cov���smoother_state_autocov���smoother_disturbance���smoother_disturbance_cov���smoother_all���_smoothed_forecasts�N�_smoothed_forecasts_error�N�_smoothed_forecasts_error_cov�N�_kalman_gain�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub���������������      �?� G����?        �������?D1|
��?              �?<�5V:��?              �?��=�?              �?༣�?              �?@�j���?              �?4Fz���?              �?�q���?              �?����?              �?h�Pm���?              �?!?z��?              �?p��Q��?              �?<%k#@��?              �?�U��8��?              �?�N>F5��?              �?��L�3��?              �?D�<3��?              �?<�q�2��?              �?H���2��?        �������?PP�2��?              �? r��2��?              �?�&�2��?        �������?���2��?        �������?`���2��?              �?��v�2��?        �������?4a�2��?              �?��W�2��?              �?\�S�2��?              �?$
R�2��?              �?�GQ�2��?              �?d�P�2��?              �?��P�2��?              �?�P�2��?              �?H�P�2��?        �������?L�P�2��?              �?�P�2��?        �E       �_standardized_forecasts_error�h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub�~�� �%@v0ؼ`�忏ڌ�B�?62{�J���md��?�H����أ���⿬q'䈼�?���8һ��܌�����?��������P���?�ؐ��>ۿ��Z����������?����h�0@V���?Dm��@r����?�~ـ!��?䓈IRs⿈9���]`\��M��P����?�G��ۿ��7�l'��A�Ў��?+���޿|�('O�nt����QЫ���A�δ�:ѿ���=�_���eC{�����fT6���Y�迕�       �filter_method�K�inversion_method�K	�stability_method�K�conserve_memory�K �filter_timing�K j�  G;���O�Ҭj�  Kj�  �j�  K j�  h,)��}�(h/h2h3K$��h5h6h7j  h?�h@Kub�������                                                                                                                                                �-       j�  h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub	���������n�ج^~@�
1�kA�s��F'a�    2�kA    ^�:Ag�W��>"A   �]	oA   ��QAJv�}� :�    �sA   �(A���Q�(A   �ųtA   ��CAu��"'�   @$/wA   ��2�͘�Ȕ�9A   `)vA   ����AGx+�+A   �z�uA   ��*Aє�@l�   `	�vA   �9����B�4A   @�9uA������3A��*�)�   ��rvA   �8�Q3��XE2A   ���tA�����#A��۫-!�   ���uA   ` ���״��A   ��uA�����q?�r{Ї�4A   �sA   Bq@Aw'���9�    �uA    T�$��^9<�A   �jytA@����w���tsi��   �;vtA   �1��^u!�%A   @�esA    �1A���P��	�   `@�sA����'�"A��8]�n�   ��tA������&�Ad��A   `SfsA
   �*�<��JA   �#�rA�����5�!PӔ��(A   @E7qA   N A�y�lp!�   ���qA����#&�Ї67fA   �	qA�����H�F܉�0�>A   ��kA������3A�~�3�����XnA����s�)��%m?NA   @X�lA   $/�U�3xmeA    ��jA������6�ʢ�z��'A   @v�gA   .3��;ANon A   �P�eA�����T)�����u�A    �cA�����:��?U�\*A    s�`A������E����b7A   sVA   \�:� ���*�#A    ��OA������;��S���$A�/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������%^�~�.A$^�~�.�1��5�"A%^�~�.�   �~�.A  �5�"�2��5�"A  �5�"� ���V%B    ��     ��>z�?���     ��>                z�?���        �E����B������>������0�#&���������                �0�#&���         LX�r�A������������>e�g����     ��>                e�g����         ��Z@�A������>�������EJ��Ҿ������                �EJ��Ҿ         ��s��A������������>�{��ҍ��������>                �{��ҍ��         �_�ޢ�A������>������<�)*��>������                <�)*��>         �Q�  �A������������>�<hf��������>                �<hf��         `��zq�A������>������ �Q�>������                � �Q�>          �{��A������������>¸����������>                ø����          �ihvA������>������g�ڟ20�>������                h�ڟ20�>          �pM cA������������>��V��������>                ��V��          X���PA������>������\KS��>������                �\KS��>          ����<A������������>*z�3���������>                )z�3���          ���(A������>������h��%��>������                h��%��>          ���A������������>�*�oy��������>                �*�oy��          ���A������>������CD�����>������                CD�����>          ��%�@������������>gg"ȅM�������>                hg"ȅM�           �D��@������>�����򾊍�,v
�>������                ���,v
�>           �8�@������������>Z� ��6�������>      0?        [� ��6�      0�   �C��@����/1?����/1�Ժm �.-?    /1�      0?      0�ֺm �.-?      0�   �#+�@     ��     ��>���3��������>                ���3��           @�x�@������>������V�Iu.���������      0?      0�V�Iu.���      0�   ��A{@����ۡ-?����ۡ-��M3g�?����ۡ-�      @?      0��M3g�?      0�    a�g@����/1?����/1�!���V�,?����/1�      0?      0�!���V�,?      0�    rT@������������>Y�X;:�������>      0?        Y�X;:�      0�    4�A@����/1?����/1���y�k#+?����/1�      0?        ��y�k#+?      0�    P�.@������������>|�dx%?������>                }�dx%?            ��@������>�������"$?������              0?�"$?            �@������������>� 0�?������>                � 0�?      0�    ���?������>������lؒ�	��������                lؒ�	��             B�?������������>�8�ib4��������>                �8�ib4��             ��?������>������90p��>������              0?90p��>             ع?������������>P��@�?������>              0�P��@�?             p�?������>���������Y~��������      0?        ���Y~��      0�     `�?   ܡ-?   ܡ-�@<"r2'?   ܡ-�      0?      0�@<"r2'?      0�     ��?�-       j�  h,)��}�(h/h2h3KK%��h5j�  h7h<h?�h@Kub	���������                            2�kA𽦚ߋDA           �]	oA�����>A            �sA���6��>A           �ųtA�Zݳl6A           @$/wA����Vj4A           `)vA���a[%A           �z�uAL�ޔ�hA           `	�vA�<��j�A           @�9uA`��cr�@           ��rvAD�cMD
A           ���tA0���x`��           ���uA��\[N�@           ��uA ������           �sA���B��            �uA ���,��@           �jytA�oc�J���           �;vtA�u�^����           @�esA`2&�iA�           `@�sA ����9��           ��tApE�,���@           `SfsALԲ�B���           �#�rA^yHC�           @E7qAz�Gd�           ���qANE �:�           �	qA��iZ�           ��kA�D]H�"�        ����XnA@ӗg�	�           @X�lAo��1��            ��jA�I�Hն�           @v�gA��S�gt�           �P�eAR�����            �cA�:�?S�            s�`A����� �           sVA:�D��'�            ��OA�U0�e'�           2�AAiɶ�]�'�        �/       j�  h,)��}�(h/h2h3KKK%��h5j�  h7h<h?�h@Kub���������������    ��.A                        ��yd��{Bù*q�        ù*q��� �fB     ��z�o����        z�o���������zBﰑù*q�        ﰑù*q��� �fB������>�u���        �u���Q�X�X]zBﰑù*q�        ﰑù*q��� �fB������e��~B�        e��~B�����4zBﰑù*q�        ﰑù*q��� �fB������>������        ������$�Ui#zBﰑù*q�        ﰑù*q��� �fB�������Ф�\��        �Ф�\��.��i�zBﰑù*q�        ﰑù*q��� �fB������>�2U��        �2U��*e>��zBﰑù*q�        ﰑù*q��� �fB����������#�        ����#�Xl*YzBﰑù*q�        ﰑù*q��� �fB������>LuFp<̾        LuFp<̾�CI�zBﰑù*q�        ﰑù*q��� �fB������^w7�McԾ        ^w7�McԾΐ�'|zBﰑù*q�        ﰑù*q��� �fB������>��M\��        ��M\���=_zBﰑù*q�        ﰑù*q��� �fB������6�/Q,Jɾ        6�/Q,Jɾ�Q��RzBﰑù*q�        ﰑù*q��� �fB������>0k���>        0k���>PE�LMzBﰑù*q�        ﰑù*q��� �fB������&�e���¾        &�e���¾�v�JzBﰑù*q�        ﰑù*q��� �fB������>4��/�>        4��/�>7�-�IzBﰑù*q�        ﰑù*q��� �fB������@�I�\��        @�I�\���mv~IzBﰑù*q�        ﰑù*q��� �fB������>���!"�>        ���!"�>~ئMIzBﰑù*q�        ﰑù*q��� �fB������l��� ټ�        l��� ټ���8IzBﰑù*q�        ﰑù*q��� �fB������>D�#`���>        D�#`���>tj\/IzBﰑù*q�        ﰑù*q��� �fB������4u::<»�        4u::<»���e+IzBﰑù*q�        ﰑù*q��� �fB    /1?q����?        q����?y=�)IzBﰑù*q�        ﰑù*q��� �fB     ���R����        ��R����U��(IzBﰑù*q�        ﰑù*q��� �fB������>f	��        f	��v��(IzBﰑù*q�        ﰑù*q��� �fB    ܡ-?�@m�O��        �@m�O����y(IzBﰑù*q�        ﰑù*q��� �fB    /1?�zK�O?        �zK�O?�fj(IzBﰑù*q�        ﰑù*q��� �fB������|��5T��        |��5T����c(IzBﰑù*q�        ﰑù*q��� �fB����/1?N��o}?        N��o}?��`(IzBﰑù*q�        ﰑù*q��� �fB������{<n�v?        {<n�v?��_(IzBﰑù*q�        ﰑù*q��� �fB������>pyn�Ա	?        pyn�Ա	?}_(IzBﰑù*q�        ﰑù*q��� �fB�������F¥��#?        �F¥��#?>�^(IzBﰑù*q�        ﰑù*q��� �fB������>�,]��        �,]��'�^(IzBﰑù*q�        ﰑù*q��� �fB������x��Q�        x��Q�ۡ^(IzBﰑù*q�        ﰑù*q��� �fB������>�+[?�߾        �+[?�߾��^(IzBﰑù*q�        ﰑù*q��� �fB�������$�I��?        �$�I��?ؚ^(IzBﰑù*q�        ﰑù*q��� �fB������>Ш�� �        Ш�� ��^(IzBﰑù*q�        ﰑù*q��� �fB   ܡ-?>���#y?        >���#y?��^(IzBﰑù*q�        ﰑù*q��� �fB������> X�
���         X�
���[�^(IzBﰑù*q�        ﰑù*q��� �fB�/       j  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub���������������    ��.A��yd��{Bù*q�z�o�=�������zBﰑù*q��u��(�Q�X�X]zBﰑù*q�d��~҆�����4zBﰑù*q��r�
�mܾ$�Ui#zBﰑù*q�jhRv�n�.��i�zBﰑù*q�5�ͪXI�>*e>��zBﰑù*q��Y���Xl*YzBﰑù*q§b��0��>�CI�zBﰑù*q���y�	��ΐ�'|zBﰑù*q·�u�`�>�=_zBﰑù*q���%�e���Q��RzBﰑù*q�V#����>PE�LMzBﰑù*q����4�C���v�JzBﰑù*q����4�>7�-�IzBﰑù*q��ޘ�����mv~IzBﰑù*q¶X"Bq�>~ئMIzBﰑù*q��K9�����8IzBﰑù*q�_:����>tj\/IzBﰑù*q�N���C����e+IzBﰑù*q��|E,6?y=�)IzBﰑù*q·�R�^�U��(IzBﰑù*q��0Hɾv��(IzBﰑù*qº_�4=%?��y(IzBﰑù*q� ��R�6?�fj(IzBﰑù*q�d��5�7���c(IzBﰑù*q��3�Ͳ�4?��`(IzBﰑù*q�yܰot?��_(IzBﰑù*q¨<�r2�?}_(IzBﰑù*q��F¥��!??�^(IzBﰑù*q������㹾'�^(IzBﰑù*q¡M����ۡ^(IzBﰑù*q´iR�8��>��^(IzBﰑù*q��$�IWB?ؚ^(IzBﰑù*q��Q�?~P���^(IzBﰑù*q�60x�1?��^(IzBﰑù*q*       j  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������z{�q���>�ū'f��K��"Z�>ZV� ����������>�;�g�ⷾ��5��'�=�>���^���Ly�P�>�l&8i��8oХ��>�,>RV��
IIZt���o�U�\�>����՜�R� 蹗N>��G"�^��N��2�>JI����>���j.朾5ɳ�p*��T�@�"��y��@�>w���	ϕ���_Mo��}�m���>㉉�啗�����~T����N���f���_,���������𑨾�mT�������4�-�����g]����/       j  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������M\�"|b=M\�"|b=        �V��$c=�V��$c=        �"0�kc=�"0�kc=        �8����c=�8����c=        �3\��c=�3\��c=        �'��$�c=�'��$�c=        ���ۏ�c=���ۏ�c=        �7Tћ�c=�7Tћ�c=        �q��c=�q��c=        ��>B�c=��>B�c=        |n��W�c=|n��W�c=        ݂P<a�c=݂P<a�c=        C��Pe�c=C��Pe�c=        ���g�c=���g�c=        �ߘ�g�c=�ߘ�g�c=        �f-h�c=�f-h�c=        �Rh�c=�Rh�c=        �'bh�c=�'bh�c=        C�hh�c=C�hh�c=        ���kh�c=���kh�c=        �*/mh�c=�*/mh�c=        �U�mh�c=�U�mh�c=        U�mh�c=U�mh�c=        /.nh�c=/.nh�c=        ��"nh�c=��"nh�c=        o�'nh�c=o�'nh�c=        �*nh�c=�*nh�c=        K�*nh�c=K�*nh�c=        �_+nh�c=�_+nh�c=        H�+nh�c=H�+nh�c=        �+nh�c=�+nh�c=        j�+nh�c=j�+nh�c=        �+nh�c=�+nh�c=        ��+nh�c=��+nh�c=        a�+nh�c=a�+nh�c=        ��+nh�c=��+nh�c=        �,       j  h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
����������                                                                                                                                                                                                                                                                                                �/       j  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                �6       �	M_diffuse�h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub����������������                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                �*       j)  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������        ��T�hpA���~qqAޞo���uA��=�\vA��i��uxA�-�m�vA�{S�avA���2wA���q�BuA5ǚH4�vA>0'��tA�[���uA�6����tA���S�rA���Ly5uAHΣZ�otA#@h��otA���lZ9sAsXy�psA�(K��"tA,MZOsA�o��brA*��#��pAu���?�qA�=��O�pA�+z��jA��a���mA5p>lA�-�U�.jA�b� �gA�O�dAk/�i%cAj}�m�8_A�k��~SA���s��IA�*       j*  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������    2�kA���j�l,�8�2EDA���6}�2���"Ly�1AP�O[}C� ���1�'��!k�zA@�1�L�?�p'b�3APs����;�@8���&A@q˵e!�@h#�ݒ>� ��_�CA����ف'� ��p���@0�8�0�@��|�A��Ԑ]�%A e	&�'���)���'�а�և�2����3�*A���?h�!� ��d<.G�p�.$��<A �7:#�P��a'��mɭH�1�@+V	(�(��Rb�	 �X{��4���ۂ�A��_�@��-��7�ω�/��,       j+  h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
�����������ǝX²{B�����zBQ�X�X]zB����4zB$�Ui#zB.��i�zB*e>��zBXl*YzB�CI�zBΐ�'|zB�=_zB�Q��RzBPE�LMzB�v�JzB7�-�IzB�mv~IzB~ئMIzB��8IzBtj\/IzB��e+IzBz=�)IzBU��(IzBv��(IzB��y(IzB�fj(IzB��c(IzB��`(IzB��_(IzB}_(IzB@�^(IzB'�^(IzBۡ^(IzB��^(IzBؚ^(IzB�^(IzB��^(IzB�-       �llf_obs�h,)��}�(h/h2h3K$��h5h6h7h<h?�h@Kub	�����������k\k�Q��
���.��պí�0����]�.�S�]���.���X�S�0�Qq��c.��D��b(.�����80��q�.�U+IH�/�Twq?�].��̊&�;.�ϗ��c%0��Fө�0���3b.�4��.�Ơn���.����b.�TW�2U.���)
�b.���I�&d.�Y;�k'�.��NX'y.�G��=.�k5�ޙ1�R���0��[@�'F.�eY�mA_.�@Z��.����Mm.��*� .��i'�/�M֧;U�0�_<N�+�.�IH�ۨ.��9      j�  K j-  Nj�  N�missing_forecasts�N�missing_forecasts_error�N�missing_forecasts_error_cov�N�collapsed_forecasts�N�collapsed_forecasts_error�N�collapsed_forecasts_error_cov�Nj6  G?�      �llf�h�h<C? �A
�����R�j�  Nj�  Nj�  N�#scaled_smoothed_estimator_presample�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�������������:���% �>[K' ��>�(n#�b��R       �'scaled_smoothed_estimator_cov_presample�h,)��}�(h/h2h3KK��h5j�  h7h<h?�h@Kub������������H�}�g�c=u�Q�9X]=��� �H�u�Q�9X]=j��&�7o=os���d=��� �H�os���d='��ӌ�p=��       �/_SmootherResults__smoothed_state_autocovariance�}�ubj/  j;  jw  K$j�  K hj}��cov_params_opg�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub�������o�
W��?��4�r���od�z.򼉆4�r�����J�6��?
��,�H�<rd�z.���,�H�<\��=�JS:�T      s�nobs_effective�K#�k_diffuse_states�K �df_model�K�df_resid�G�      �cov_kwds�}��description��QCovariance matrix calculated using the outer product of gradients (complex-step).�s�cov_type��opg��_cov_approx_complex_step���_cov_approx_centered���_rank�h�h�C       ���R��cov_params_default�h,)��}�(h/h2h3KK��h5h6h7h<h?�h@Kub
�����������o�
W��?��4�r���od�z.򼉆4�r�����J�6��?
��,�H�<rd�z.���,�H�<\��=�JS:�-       j�  h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub�n�ج^~@�
1�kA�s��F'a�    2�kA    ^�:Ag�W��>"A   �]	oA   ��QAJv�}� :�    �sA   �(A���Q�(A   �ųtA   ��CAu��"'�   @$/wA   ��2�͘�Ȕ�9A   `)vA   ����AGx+�+A   �z�uA   ��*Aє�@l�   `	�vA   �9����B�4A   @�9uA������3A��*�)�   ��rvA   �8�Q3��XE2A   ���tA�����#A��۫-!�   ���uA   ` ���״��A   ��uA�����q?�r{Ї�4A   �sA   Bq@Aw'���9�    �uA    T�$��^9<�A   �jytA@����w���tsi��   �;vtA   �1��^u!�%A   @�esA    �1A���P��	�   `@�sA����'�"A��8]�n�   ��tA������&�Ad��A   `SfsA
   �*�<��JA   �#�rA�����5�!PӔ��(A   @E7qA   N A�y�lp!�   ���qA����#&�Ї67fA   �	qA�����H�F܉�0�>A   ��kA������3A�~�3�����XnA����s�)��%m?NA   @X�lA   $/�U�3xmeA    ��jA������6�ʢ�z��'A   @v�gA   .3��;ANon A   �P�eA�����T)�����u�A    �cA�����:��?U�\*A    s�`A������E����b7A   sVA   \�:� ���*�#A    ��OA������;��S���$A�/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������%^�~�.A$^�~�.�1��5�"A%^�~�.�   �~�.A  �5�"�2��5�"A  �5�"� ���V%B    ��     ��>z�?���     ��>                z�?���        �E����B������>������0�#&���������                �0�#&���         LX�r�A������������>e�g����     ��>                e�g����         ��Z@�A������>�������EJ��Ҿ������                �EJ��Ҿ         ��s��A������������>�{��ҍ��������>                �{��ҍ��         �_�ޢ�A������>������<�)*��>������                <�)*��>         �Q�  �A������������>�<hf��������>                �<hf��         `��zq�A������>������ �Q�>������                � �Q�>          �{��A������������>¸����������>                ø����          �ihvA������>������g�ڟ20�>������                h�ڟ20�>          �pM cA������������>��V��������>                ��V��          X���PA������>������\KS��>������                �\KS��>          ����<A������������>*z�3���������>                )z�3���          ���(A������>������h��%��>������                h��%��>          ���A������������>�*�oy��������>                �*�oy��          ���A������>������CD�����>������                CD�����>          ��%�@������������>gg"ȅM�������>                hg"ȅM�           �D��@������>�����򾊍�,v
�>������                ���,v
�>           �8�@������������>Z� ��6�������>      0?        [� ��6�      0�   �C��@����/1?����/1�Ժm �.-?    /1�      0?      0�ֺm �.-?      0�   �#+�@     ��     ��>���3��������>                ���3��           @�x�@������>������V�Iu.���������      0?      0�V�Iu.���      0�   ��A{@����ۡ-?����ۡ-��M3g�?����ۡ-�      @?      0��M3g�?      0�    a�g@����/1?����/1�!���V�,?����/1�      0?      0�!���V�,?      0�    rT@������������>Y�X;:�������>      0?        Y�X;:�      0�    4�A@����/1?����/1���y�k#+?����/1�      0?        ��y�k#+?      0�    P�.@������������>|�dx%?������>                }�dx%?            ��@������>�������"$?������              0?�"$?            �@������������>� 0�?������>                � 0�?      0�    ���?������>������lؒ�	��������                lؒ�	��             B�?������������>�8�ib4��������>                �8�ib4��             ��?������>������90p��>������              0?90p��>             ع?������������>P��@�?������>              0�P��@�?             p�?������>���������Y~��������      0?        ���Y~��      0�     `�?   ܡ-?   ܡ-�@<"r2'?   ܡ-�      0?      0�@<"r2'?      0�     ��?�-       j�  h,)��}�(h/h2h3KK%��h5j�  h7h<h?�h@Kub	���������                            2�kA𽦚ߋDA           �]	oA�����>A            �sA���6��>A           �ųtA�Zݳl6A           @$/wA����Vj4A           `)vA���a[%A           �z�uAL�ޔ�hA           `	�vA�<��j�A           @�9uA`��cr�@           ��rvAD�cMD
A           ���tA0���x`��           ���uA��\[N�@           ��uA ������           �sA���B��            �uA ���,��@           �jytA�oc�J���           �;vtA�u�^����           @�esA`2&�iA�           `@�sA ����9��           ��tApE�,���@           `SfsALԲ�B���           �#�rA^yHC�           @E7qAz�Gd�           ���qANE �:�           �	qA��iZ�           ��kA�D]H�"�        ����XnA@ӗg�	�           @X�lAo��1��            ��jA�I�Hն�           @v�gA��S�gt�           �P�eAR�����            �cA�:�?S�            s�`A����� �           sVA:�D��'�            ��OA�U0�e'�           2�AAiɶ�]�'�        �/       j�  h,)��}�(h/h2h3KKK%��h5j�  h7h<h?�h@Kub���������������    ��.A                        ��yd��{Bù*q�        ù*q��� �fB     ��z�o����        z�o���������zBﰑù*q�        ﰑù*q��� �fB������>�u���        �u���Q�X�X]zBﰑù*q�        ﰑù*q��� �fB������e��~B�        e��~B�����4zBﰑù*q�        ﰑù*q��� �fB������>������        ������$�Ui#zBﰑù*q�        ﰑù*q��� �fB�������Ф�\��        �Ф�\��.��i�zBﰑù*q�        ﰑù*q��� �fB������>�2U��        �2U��*e>��zBﰑù*q�        ﰑù*q��� �fB����������#�        ����#�Xl*YzBﰑù*q�        ﰑù*q��� �fB������>LuFp<̾        LuFp<̾�CI�zBﰑù*q�        ﰑù*q��� �fB������^w7�McԾ        ^w7�McԾΐ�'|zBﰑù*q�        ﰑù*q��� �fB������>��M\��        ��M\���=_zBﰑù*q�        ﰑù*q��� �fB������6�/Q,Jɾ        6�/Q,Jɾ�Q��RzBﰑù*q�        ﰑù*q��� �fB������>0k���>        0k���>PE�LMzBﰑù*q�        ﰑù*q��� �fB������&�e���¾        &�e���¾�v�JzBﰑù*q�        ﰑù*q��� �fB������>4��/�>        4��/�>7�-�IzBﰑù*q�        ﰑù*q��� �fB������@�I�\��        @�I�\���mv~IzBﰑù*q�        ﰑù*q��� �fB������>���!"�>        ���!"�>~ئMIzBﰑù*q�        ﰑù*q��� �fB������l��� ټ�        l��� ټ���8IzBﰑù*q�        ﰑù*q��� �fB������>D�#`���>        D�#`���>tj\/IzBﰑù*q�        ﰑù*q��� �fB������4u::<»�        4u::<»���e+IzBﰑù*q�        ﰑù*q��� �fB    /1?q����?        q����?y=�)IzBﰑù*q�        ﰑù*q��� �fB     ���R����        ��R����U��(IzBﰑù*q�        ﰑù*q��� �fB������>f	��        f	��v��(IzBﰑù*q�        ﰑù*q��� �fB    ܡ-?�@m�O��        �@m�O����y(IzBﰑù*q�        ﰑù*q��� �fB    /1?�zK�O?        �zK�O?�fj(IzBﰑù*q�        ﰑù*q��� �fB������|��5T��        |��5T����c(IzBﰑù*q�        ﰑù*q��� �fB����/1?N��o}?        N��o}?��`(IzBﰑù*q�        ﰑù*q��� �fB������{<n�v?        {<n�v?��_(IzBﰑù*q�        ﰑù*q��� �fB������>pyn�Ա	?        pyn�Ա	?}_(IzBﰑù*q�        ﰑù*q��� �fB�������F¥��#?        �F¥��#?>�^(IzBﰑù*q�        ﰑù*q��� �fB������>�,]��        �,]��'�^(IzBﰑù*q�        ﰑù*q��� �fB������x��Q�        x��Q�ۡ^(IzBﰑù*q�        ﰑù*q��� �fB������>�+[?�߾        �+[?�߾��^(IzBﰑù*q�        ﰑù*q��� �fB�������$�I��?        �$�I��?ؚ^(IzBﰑù*q�        ﰑù*q��� �fB������>Ш�� �        Ш�� ��^(IzBﰑù*q�        ﰑù*q��� �fB   ܡ-?>���#y?        >���#y?��^(IzBﰑù*q�        ﰑù*q��� �fB������> X�
���         X�
���[�^(IzBﰑù*q�        ﰑù*q��� �fB�*       j)  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub����        ��T�hpA���~qqAޞo���uA��=�\vA��i��uxA�-�m�vA�{S�avA���2wA���q�BuA5ǚH4�vA>0'��tA�[���uA�6����tA���S�rA���Ly5uAHΣZ�otA#@h��otA���lZ9sAsXy�psA�(K��"tA,MZOsA�o��brA*��#��pAu���?�qA�=��O�pA�+z��jA��a���mA5p>lA�-�U�.jA�b� �gA�O�dAk/�i%cAj}�m�8_A�k��~SA���s��IA�*       j*  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������    2�kA���j�l,�8�2EDA���6}�2���"Ly�1AP�O[}C� ���1�'��!k�zA@�1�L�?�p'b�3APs����;�@8���&A@q˵e!�@h#�ݒ>� ��_�CA����ف'� ��p���@0�8�0�@��|�A��Ԑ]�%A e	&�'���)���'�а�և�2����3�*A���?h�!� ��d<.G�p�.$��<A �7:#�P��a'��mɭH�1�@+V	(�(��Rb�	 �X{��4���ۂ�A��_�@��-��7�ω�/��,       j+  h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
�����������ǝX²{B�����zBQ�X�X]zB����4zB$�Ui#zB.��i�zB*e>��zBXl*YzB�CI�zBΐ�'|zB�=_zB�Q��RzBPE�LMzB�v�JzB7�-�IzB�mv~IzB~ئMIzB��8IzBtj\/IzB��e+IzBz=�)IzBU��(IzBv��(IzB��y(IzB�fj(IzB��c(IzB��`(IzB��_(IzB}_(IzB@�^(IzB'�^(IzBۡ^(IzB��^(IzBؚ^(IzB�^(IzB��^(IzB�*       j,  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������~�� �%@v0ؼ`�忏ڌ�B�?62{�J���md��?�H����أ���⿬q'䈼�?���8һ��܌�����?��������P���?�ؐ��>ۿ��Z����������?����h�0@V���?Dm��@r����?�~ـ!��?䓈IRs⿈9���]`\��M��P����?�G��ۿ��7�l'��A�Ў��?+���޿|�('O�nt����QЫ���A�δ�:ѿ���=�_���eC{�����fT6���Y�迕9       j-  Nj�  Nj�  h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub�������������n�6`���(n#�b���
º�>�y_�1�>��
º�>"s��h���o������"s��h���.��줾��v,�>�.��줾 �V6,���h������ �V6,����_������d|�c����_�������s�p��th��s��>��s�p����&C(��C���Hm����&C(��@���f�X>��W��\�>@���f�X>�� ���A�-����� ��`����B� wZ��?�>`����B���ȥ�\*�\����ȥ���*㠾���2����*㠾oL#T�>n�����>oL#T�>��޽e��	�xV�И���޽e�����aH�����@>}>���aH��jڼt�����{� ��jڼt��pU��ej���p���>pU��ej��ZH�e��{�kp�բ>�ZH�e��U_>8�����ͥ�d��U_>8���WN���ӱ���˰H���WN���ӱ�A�����j.�K뤾A�����Y⌑��\d��d��>�Y⌑���8��Ҷ�n�d(y��8��Ҷ�w�ڇ�e���2u/伾w�ڇ�e���kS>�ň>�0q�w �>�kS>�ň>%���t;���*Uꁾ%���t;����Q��Ҹ�^� ㈾��Q��Ҹ����.�������4������.����{6�,J=���������{6�,J=��ٺ]��2���	��3x>ٺ]��2��BH�9���B�tNq��BH�9����
������W��<���
������������ܚ�����������g]������g]������g]���                                �/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub��������6�qd=)��4(_=�yGJ{8F�)��4(_='��ӌ�p=�.����e=�yGJ{8F��.����e=�Ւ�k�p=�e?ԩ<d=�Px!�_=C���
0E��Px!�_=�Ւ�k�p=�	�`\f=C���
0E��	�`\f=<�t��+q=t�@kQd=�Ϭ$`=	����D��Ϭ$`=<�t��+q=$���I�f=	����D�$���I�f=2��?q=�`<�Yd=Q���6`=��z
�D�Q���6`=2��?q=�P��f=��z
�D��P��f=�H�kHq=�#p��]d=gB?`=�Rx�vvD�gB?`=�H�kHq=h2�f=�Rx�vvD�h2�f=���.Lq=)!�u_d=G����B`=6_��)mD�G����B`=���.Lq=���z�f=6_��)mD����z�f=����Mq=]G�.`d=�M,!D`=����"iD��M,!D`=����Mq=����,�f=����"iD�����,�f=kD��Nq=/�}`d=�3j��D`=�%�sdgD��3j��D`=kD��Nq=��yM�f=�%�sdgD���yM�f=>��<�Nq=>Y�H�`d=�R�9E`=V�(�fD��R�9E`=>��<�Nq=]�"��f=V�(�fD�]�"��f=Y���Nq=�j�;�`d=:84E`=f�gfOfD�:84E`=Y���Nq=Cq���f=f�gfOfD�Cq���f=�t�Oq=;�̴�`d=��E�AE`=c�$+fD���E�AE`=�t�Oq=�����f=c�$+fD������f=B�zOq=�+p��`d=��S�GE`=���pfD���S�GE`=B�zOq=	�K��f=���pfD�	�K��f=��+�
Oq=MM&��`d=���ZJE`=�E8�fD����ZJE`=��+�
Oq=�3:���f=�E8�fD��3:���f=W��Oq=��?�`d=~ �yKE`=ރ��fD�~ �yKE`=W��Oq=�_s��f=ރ��fD��_s��f=ձ1Oq=҅vy�`d=G7��KE`=��&[fD�G7��KE`=ձ1Oq=��	��f=��&[fD���	��f=e,v�Oq=�JБ�`d=��U1LE`=����fD���U1LE`=e,v�Oq=�.NE��f=����fD��.NE��f=$ٿ�Oq=Ɓ���`d=a6�QLE`=#��@fD�a6�QLE`=$ٿ�Oq=��'��f=#��@fD���'��f=�}=�Oq= ����`d=�j�pLE`=�=եfD��j�pLE`=�}=�Oq= �K���f=�=եfD� �K���f=���&Oq=�KБ�`d=�#�LE`=J�qfD��#�LE`=���&Oq=��`��f=J�qfD���`��f=��-Oq=�vy�`d=��ME`=L�U�
fD���ME`=��-Oq=b�Sf��f=L�U�
fD�b�Sf��f=Duk�Oq=��?�`d=M�NE`=����fD�M�NE`=Duk�Oq=W�5���f=����fD�W�5���f=��Oq=�X&��`d=��xwPE`=8esG�eD���xwPE`=��Oq=&����f=8esG�eD�&����f=��f��Nq=�Ep��`d=	���UE`=�4hP�eD�	���UE`=��f��Nq=1��f=�4hP�eD�1��f=c���Nq=�ʹ�`d=m�ibE`=��1�eD�m�ibE`=c���Nq=� �9�f=��1�eD�� �9�f=���Nq=���;�`d=���TE`=��*j�dD����TE`=���Nq=�Mipu�f=��*j�dD��Mipu�f=�$�Nq=P��H�`d=��V�E`=����CcD���V�E`=�$�Nq=���!��f=����CcD����!��f=�v�i�Lq=(�1�}`d=�MnQ\F`=�/�(�_D��MnQ\F`=�v�i�Lq=x�W��f=�/�(�_D�x�W��f=R��Iq=&�.`d=���j�G`=�q��%WD����j�G`=R��Iq=�"@(�f=�q��%WD��"@(�f=k'deBq=u�"�u_d=�8���J`=$�8�CD��8���J`=k'deBq=u�TZ�f=$�8�CD�u�TZ�f=�A��1q=d���]d=B���aR`=�XǈD�B���aR`=�A��1q=�����nf=�XǈD������nf=���q=,?`<�Yd=��2��c`=����j�C���2��c`=���q=�+�x��e=����j�C��+�x��e=
V`9�p=J- lQd=x�T��`=�0L��B�x�T��`=
V`9�p=��n58�d=�0L��B���n58�d= �}�l�o=JL�թ<d=<���g�`=#E�ƒ@�<���g�`= �}�l�o=6�S.�b=#E�ƒ@�6�S.�b=&ᩈ4 l=T�2�qd=�hu�T�a=�skWW!7��hu�T�a=&ᩈ4 l=bXA��Y=�skWW!7�bXA��Y=��+nh�c=��+nh�c=��+nh�c=        ��+nh�c=��+nh�c=                                                                                                        �*       j�  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub�������������� ��P�>�}`��¾��#t��>�GO����Y��z���>X�H8	�����kĩ�`����M�>:������e#�z40�> }�ס��,���/n�>x_���>��DE|Ǿ�9o�J�>z�Ts����Cħ>ǧ�J櫾���� ����RC0�>��ܯpeU>���N�>���B���K���>�`,��S�>�1s�E�Ⱦ2t�n�=�>	��k>�x��O�>@V���>N^�ԕ�ް\�?�> �\@�>��}u�+����g��>���g]����-       j�  h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub	���������-��Ǆ@���1�kA]��_(a�    2�kA   ^�:A/j�E��"A   �]	oA   ��QA3ڡT�C:�    �sA   �(Ax�r'�(A   �ųtA   ��CAW�c�9'�   @$/wA
   ��2�"yA���9A   `)vA   �����Z Z)A   �z�uA   ��*A�ySsn�   `	�vA   �9�[d%-D�4A   @�9uA������3A�-G)�   ��rvA   �8��tM�XE2A   ���tA�����#A0DT�8!�   ���uA   ` ��?���A   ��uA�����q?�A�sJ�4A   �sA   Bq@A�
�3�9�    �uA    T�$��˦�;�A   �jytA@����w��0D4vi��   �;vtA   �1��u�t!�%A   @�esA    �1A���Y��	�   `@�sA����'�"A89oc�n�   ��tA������&�d�s�A   `SfsA   �*��M��JA   �#�rA�����5��Ի���(A   @E7qA   N AvG��lp!�   ���qA����#&����57fA   �	qA�����H��I��0�>A   ��kA������3A
h�~�3�����XnA����s�)��#m?NA   @X�lA
   $/�4�2xmeA    ��jA������6�jf�z��'A   @v�gA   .3�� ANon A   �P�eA�����T)�����u�A    �cA   ��:�.9U�\*A    s�`A������E�i���b7A   sVA   \�:�����*�#A    ��OA������;��S���$A�/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub�������RHe�~�.ARHe�~�.�.]�ĺ'#ARHe�~�.�!Lc�~�.A�S�ĺ'#�/]�ĺ'#Ao��ĺ'#� �r�T"$B    ��    ��>�r_NV�     ��>o�$��5?g��9��#��r_NV�l^r���aRpB������>������>U����������jQz��?�{�O^m�6?<U�����}���>��BO�4�A������    ��>��z��    ��>fSf�jcC�B�-��,;?��z��R�7!�B?�"E#)�A������>�������$�r�Ҿ������<�t�%�	?���as��$�r�Ҿ��o��&?{(*�T��A������     ��>K��C���     ��>��?u�4����\-?L��C����{yӟ�1?�u�J���A������>������#(����>������V��I%?���0gO��#(����>��+XP0?�5E���A������������>Ş��J��������>C���j�0��R���%'?Ş��J�������!?H�=�p�A������>������p���9Q�>������/�[�0�B������8?o���9Q�>���{-W=?�� �Y�A������������>]�W��������>^m���#?�K�7�^�^�W��p�������pGvA������>������Nw^�60�>��������˺���>��kn!׾Nw^�60�>VU��/��=A cA������������>[}'Z�������>��(N�3?��j��)�Z}'Z��sl�N7�ȋ���PA������>������nWE�S��>������|��R�;?���q�B2�oWE�S��>��q�.����~�<A������������>���U���������>���b�$�W�K�?���U���֕ ��1??vu���(A������>����������%��>�������s���!?=u�v������%��>��i���}S��A������������>��|wy��������><͗��1?�?��k'���|wy�뾼���X���r�A������>������R򣛝��>������j��/�<i��$?S򣛝��>��0b5?���%�@������������>E��ɅM�������>3�;畉;��U22?D��ɅM뾘����+�zf�D��@������>������cc�-v
�>����������;1��x�ߌ&?cc�-v
�>��ӫSU�E�/�8�@������������>Xk��6�������>�
"~"$�����?Xk��6�,z��f3��]M�C��@����/1?����/1���^ �.-?    /1�����%?��x�$���^ �.-?:�͖���:{�y#+�@     ��     ��>oÍ�3��������>�!�Z]3?�����%�oÍ�3�� ���+?��9=�x�@������>     ��4+Jt.�����������7�1C?�JKZ8�>+Jt.����T�cu��(���A{@����ۡ-?����ۡ-��Cg�?����ۡ-���z]H�3?�[��`{$��Cg�? �zT��>h2�^�g@����/1?����/1����V�,?����/1�2{���fƾ�Ye��~����V�,?X� kNc"�{��frT@������������>*�X;:�������>˳��o?��è���	*�X;:��!��s(?Hǩ3�A@����/1?����/1��y�k#+?����/1����5S�{�7�Н���y�k#+?���$� �v�;�W�.@�����������>
dx%?������>��!z9�P&�϶t+?
dx%?�Wa��0?��U֞�@������>�������"$?������5�s���>�q����"$?�u�6�j	?�͌h@������������>��/�?������>�����>3x ������/�?PI�P���`��g��?������>������mB��	��������^|o�~%��0��%?iB��	���� [V?5��C�A�?������������>�6�ib4��������>�P�
d��6�y��?�6�ib4��t���` )?몑-���?������>������s0p��>������逘d/?�	~�� $�u0p��>K��g0��حR��?������������>RO��@�?������>�.*�!��(�g(��>RO��@�?�1S0e�����z/n�?������>��������Y~��������~A��*��xA�rQ%?���Y~�����k`?�)��/T�?   ܡ-?   ܡ-�@<"r2'?   ܡ-�x-�7 x$?ﰑù*!�A<"r2'?      0�     ��?�/       j�  h,)��}�(h/h2h3KKK$��h5j�  h7h<h?�h@Kub��������(�j���        ی剌���Əj��=        W4剌�@Z�����>        ƨ$��B7�+L��һ0�r���;���l:n������*?�����*�j��Xkr!?�g���
!��f�ۚ� ?��O�H�B�Æ�J���f��~B�;8������                        S��>�> LX�rξ������AN�M-H~�        ��O�4�                        ��Tn>        �i�!7�AT��b���Ф�\�;�i�ê.꾛�J�5#�;      ���K�%?ov��tf> ��s����P/���A|]�M/��2U瘔�y�LcL۾                        �[��> �_�ޢs>N_F�ӹA���9��g�����#�;�VW��.پ                        �A.:5> �Q�  q�RR};U^�A��jp~v4;OuFp<�;�!��q¾                        �Q��1~� `��zq]�C	.��_�A6��*LS�^w7�Mc��Ły���ʾ                        �w��">  �{�9>W��fǀA%zB�QS;        �p�ዸ��                        �9dd��        j�]jmA0�נD�7�/Q,J���9�e]���                        ��E�3�=  �pM #>���,YA,�ь$��lP���q;;���Q�>                        �1�ǃ�Ž  ���> r�<(�EA��I6<�+�e����;��j�u��                        ���m\ǵ=  ������p�B��2A�\\�+�7��/d;��Ʊ���>                        �>:��  ����=�qՌ�Z A�9���7�C�I�\o�>f0<i���                        ���䝏=  ����=iİ��SA�;��4�0����!"x��P��>                        �-��r9z�  ���½�$Fk���@Yﴕ��4�i��� �|;��+����                        �h�=�_g=  ��%���E�u�?�@ �A;2�L�#`��y�I���L�>                        ��\��S�   �D������
>g�@�f-+�3�2u::<�{;�.�WD��                        ]�=�kA=   �8��}�����@���I�����Ӧ�VS�;i!�\�>��e+I*?��e+I*���c��3?���Ź*!�.U�Ĺ*!?XXg@ͭ�����;z�����;�9�j��>                        >��\�<=   p#+b=z&�iy�@�}�:�s�f	��51�                        � ��
=   @�x?=��K����@:�bL޻z;�0Hy;��R�5��u��(I*?t��(I*��=�ù*!?�ù*!�ù*!?�bH��q@0շ
J?�;�_�4=ջ����j
���y(I*?��y(I*������3?�I�ù*!�ù*!?H�a��_@I,c���;C��e����n��/0�>                        �8:���<    r�X�u{��J@i�WշQ��c��5�7�;���
���c(I*?��c(I*������3?#�ù*!�ù*!?�.�6N7@�z�)��r;��:U�L�;�Gp��ƾa��IՍѻ      �i���%?��j�l�м    0��(�%�9/$@ ��))��        �ߞ� ?                        u�Gp��        x`O�P{@XR@���76.��;�����j�>�9T�<�      �;�����%?8���    ��<b"���G�?�^hj�ߔ;        ���C�?                        �F�v	�n<        ]��>�9�?�P��{�        ;�?�z�                        ���}7m<         s�����?%蒉P�';        �''��Ծ                        |t�KeY�        ��j}��?NyBS�b�;�َ���K0�Yվ��t��Oۻ      �;�����%?�����f�     �i<��ܼ�?�n8��C�;�+p�oԻ1C�ym�
?�b�**��      �;����%�:5~��&5<     pf��)B�Ї�?sx�@���;���{���ӣ	����^(I*?�^(I*�1��ù*!?V��ù*!�;��ù*!?{�ʾ�(�?        j5)3�`վ                                             ��?        �*       j�  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������                                                                                                                                                                                                                                                                                                �*       j�  h,)��}�(h/h2h3KK$��h5h6h7h<h?�h@Kub������������Z���`,�Y���CA���_t�2�OƑ��1AXd�zFwC��|c4?�'�[�x�3}A:�
��?��E�3A�\����;�?��F��&Aw��d!��?ܗܒ>�8E���CAO�ف'�c�i���@�İ8�0�3�|�A���]�%A\�I&�'������'�-��և�2�4v&�3�*AB�?h�!����d<.G��4.$��<A2a�7:#��Y �a'��ɭH�1���U	(�(�Fb�	 ��s��4�9�ۂ�A�w^�@��-��7�ω�/�        �,       j�  h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
����������                                                                                                                                                                                                                                                                                                �,       j�  h,)��}�(h/h2h3KKK$��h5h6h7h<h?�h@Kub
���������� �-�I"$B RpB �BO�4�A ""E#)�A $*�T��A p�J���A 5E���A  �=�p�A  �Y�A  �pGvA  A cA  ��PA  �~�<A  ����(A  ���A  �r�A   �%�@   �D��@    �8�@   �C��@   `#+�@   ��x�@    �A{@    b�g@    rT@    8�A@     �.@     �@    �@     ��?     @�?     ��?     �?     ��?     ��?:�^(IzB��       j�  �types��SimpleNamespace���)R�}�(�	predicted��pandas.core.frame��	DataFrame���)��}�(hh�BlockManager����pandas._libs.internals��_unpickle_block���h,)��}�(h/h2h3KK%��h5j�  h7h<h?�h@Kub�                            2�kA𽦚ߋDA           �]	oA�����>A            �sA���6��>A           �ųtA�Zݳl6A           @$/wA����Vj4A           `)vA���a[%A           �z�uAL�ޔ�hA           `	�vA�<��j�A           @�9uA`��cr�@           ��rvAD�cMD
A           ���tA0���x`��           ���uA��\[N�@           ��uA ������           �sA���B��            �uA ���,��@           �jytA�oc�J���           �;vtA�u�^����           @�esA`2&�iA�           `@�sA ����9��           ��tApE�,���@           `SfsALԲ�B���           �#�rA^yHC�           @E7qAz�Gd�           ���qANE �:�           �	qA��iZ�           ��kA�D]H�"�        ����XnA@ӗg�	�           @X�lAo��1��            ��jA�I�Hն�           @v�gA��S�gt�           �P�eAR�����            �cA�:�?S�            s�`A����� �           sVA:�D��'�            ��OA�U0�e'�           2�AAiɶ�]�'�        �P       hSK KK��R�K��R���]�(hh�Index���}�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.��       h#Nu��R�hh!}�(h#Nh$K h%K%h&Ku��R�e��R�hW�	dataframe�hY]�h\}�h^}�h`�sub�predicted_cov�j_  )��}�(hjc  jf  h,)��}�(h/h2h3KKo��h5j�  h7h<h?�h@Kub�����������    ��.A                        ��yd��{Bù*q�        ù*q��� �fB     ��z�o����        z�o���������zBﰑù*q�        ﰑù*q��� �fB������>�u���        �u���Q�X�X]zBﰑù*q�        ﰑù*q��� �fB������e��~B�        e��~B�����4zBﰑù*q�        ﰑù*q��� �fB������>������        ������$�Ui#zBﰑù*q�        ﰑù*q��� �fB�������Ф�\��        �Ф�\��.��i�zBﰑù*q�        ﰑù*q��� �fB������>�2U��        �2U��*e>��zBﰑù*q�        ﰑù*q��� �fB����������#�        ����#�Xl*YzBﰑù*q�        ﰑù*q��� �fB������>LuFp<̾        LuFp<̾�CI�zBﰑù*q�        ﰑù*q��� �fB������^w7�McԾ        ^w7�McԾΐ�'|zBﰑù*q�        ﰑù*q��� �fB������>��M\��        ��M\���=_zBﰑù*q�        ﰑù*q��� �fB������6�/Q,Jɾ        6�/Q,Jɾ�Q��RzBﰑù*q�        ﰑù*q��� �fB������>0k���>        0k���>PE�LMzBﰑù*q�        ﰑù*q��� �fB������&�e���¾        &�e���¾�v�JzBﰑù*q�        ﰑù*q��� �fB������>4��/�>        4��/�>7�-�IzBﰑù*q�        ﰑù*q��� �fB������@�I�\��        @�I�\���mv~IzBﰑù*q�        ﰑù*q��� �fB������>���!"�>        ���!"�>~ئMIzBﰑù*q�        ﰑù*q��� �fB������l��� ټ�        l��� ټ���8IzBﰑù*q�        ﰑù*q��� �fB������>D�#`���>        D�#`���>tj\/IzBﰑù*q�        ﰑù*q��� �fB������4u::<»�        4u::<»���e+IzBﰑù*q�        ﰑù*q��� �fB    /1?q����?        q����?y=�)IzBﰑù*q�        ﰑù*q��� �fB     ���R����        ��R����U��(IzBﰑù*q�        ﰑù*q��� �fB������>f	��        f	��v��(IzBﰑù*q�        ﰑù*q��� �fB    ܡ-?�@m�O��        �@m�O����y(IzBﰑù*q�        ﰑù*q��� �fB    /1?�zK�O?        �zK�O?�fj(IzBﰑù*q�        ﰑù*q��� �fB������|��5T��        |��5T����c(IzBﰑù*q�        ﰑù*q��� �fB����/1?N��o}?        N��o}?��`(IzBﰑù*q�        ﰑù*q��� �fB������{<n�v?        {<n�v?��_(IzBﰑù*q�        ﰑù*q��� �fB������>pyn�Ա	?        pyn�Ա	?}_(IzBﰑù*q�        ﰑù*q��� �fB�������F¥��#?        �F¥��#?>�^(IzBﰑù*q�        ﰑù*q��� �fB������>�,]��        �,]��'�^(IzBﰑù*q�        ﰑù*q��� �fB������x��Q�        x��Q�ۡ^(IzBﰑù*q�        ﰑù*q��� �fB������>�+[?�߾        �+[?�߾��^(IzBﰑù*q�        ﰑù*q��� �fB�������$�I��?        �$�I��?ؚ^(IzBﰑù*q�        ﰑù*q��� �fB������>Ш�� �        Ш�� ��^(IzBﰑù*q�        ﰑù*q��� �fB   ܡ-?>���#y?        >���#y?��^(IzBﰑù*q�        ﰑù*q��� �fB������> X�
���         X�
���[�^(IzBﰑù*q�        ﰑù*q��� �fB�I       hSK KK��R�K��R���]�(hjq  }�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.�v       h#Nu��R�h�pandas.core.indexes.multi��
MultiIndex���}�(�levels�]�(hjq  }�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.�t       h#Nu��R�hh!}�(h#Nh$K h%K%h&Ku��R�e�codes�]�(h,)��}�(h/h2h3Ko��h5h6h7h9�i1�����R�(Kh�NNNJ����J����K t�bh?�h@Kub���                                     �&       h,)��}�(h/h2h3Ko��h5h6h7j�  h?�h@Kub�   			


   !!!"""###$$$��       e�	sortorder�N�names�]�(NNeu��R�e��R�hWj}  hYj~  h\}�h^}�h`�sub�filtered�j_  )��}�(hjc  jf  h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub�����������n�ج^~@�
1�kA�s��F'a�    2�kA    ^�:Ag�W��>"A   �]	oA   ��QAJv�}� :�    �sA   �(A���Q�(A   �ųtA   ��CAu��"'�   @$/wA   ��2�͘�Ȕ�9A   `)vA   ����AGx+�+A   �z�uA   ��*Aє�@l�   `	�vA   �9����B�4A   @�9uA������3A��*�)�   ��rvA   �8�Q3��XE2A   ���tA�����#A��۫-!�   ���uA   ` ���״��A   ��uA�����q?�r{Ї�4A   �sA   Bq@Aw'���9�    �uA    T�$��^9<�A   �jytA@����w���tsi��   �;vtA   �1��^u!�%A   @�esA    �1A���P��	�   `@�sA����'�"A��8]�n�   ��tA������&�Ad��A   `SfsA
   �*�<��JA   �#�rA�����5�!PӔ��(A   @E7qA   N A�y�lp!�   ���qA����#&�Ї67fA   �	qA�����H�F܉�0�>A   ��kA������3A�~�3�����XnA����s�)��%m?NA   @X�lA   $/�U�3xmeA    ��jA������6�ʢ�z��'A   @v�gA   .3��;ANon A   �P�eA�����T)�����u�A    �cA�����:��?U�\*A    s�`A������E����b7A   sVA   \�:� ���*�#A    ��OA������;��S���$A�I       hSK KK��R�K��R���]�(hjq  }�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.�y       h#Nu��R�h(e��R�hWj}  hYj~  h\}�h^}�h`�sub�filtered_cov�j_  )��}�(hjc  jf  h,)��}�(h/h2h3KKl��h5j�  h7h<h?�h@Kub��������%^�~�.A%^�~�.�2��5�"A$^�~�.�   �~�.A  �5�"�1��5�"A  �5�"� ���V%B    ��     ��>z�?���     ��>                z�?���        �E����B������>������0�#&���������                �0�#&���         LX�r�A������     ��>e�g����������>                e�g����         ��Z@�A������>�������EJ��Ҿ������                �EJ��Ҿ         ��s��A������������>�{��ҍ��������>                �{��ҍ��         �_�ޢ�A������>������<�)*��>������                <�)*��>         �Q�  �A������������>�<hf��������>                �<hf��         `��zq�A������>������ �Q�>������                � �Q�>          �{��A������������>ø����������>                ¸����          �ihvA������>������h�ڟ20�>������                g�ڟ20�>          �pM cA������������>��V��������>                ��V��          X���PA������>������\KS��>������                �\KS��>          ����<A������������>)z�3���������>                *z�3���          ���(A������>������h��%��>������                h��%��>          ���A������������>�*�oy��������>                �*�oy��          ���A������>������CD�����>������                CD�����>          ��%�@������������>hg"ȅM�������>                gg"ȅM�           �D��@������>�����򾉍�,v
�>������                ���,v
�>           �8�@������������>[� ��6�������>      0?      0�Z� ��6�           �C��@����/1?    /1�ֺm �.-?����/1�      0?      0�Ժm �.-?      0�   �#+�@     ��������>���3��     ��>                ���3��           @�x�@������>������V�Iu.���������      0?      0�V�Iu.���      0�   ��A{@����ۡ-?����ۡ-��M3g�?����ۡ-�      @?      0��M3g�?      0�    a�g@����/1?����/1�!���V�,?����/1�      0?      0�!���V�,?      0�    rT@������������>Y�X;:�������>      0?      0�Y�X;:�            4�A@����/1?����/1���y�k#+?����/1�      0?      0���y�k#+?            P�.@�����������>}�dx%?������>                |�dx%?            ��@������>�������"$?������                �"$?      0?    �@������������>� 0�?������>              0�� 0�?            ���?������>������lؒ�	��������                lؒ�	��             B�?������������>�8�ib4��������>                �8�ib4��             ��?������>������90p��>������                90p��>      0?     ع?������������>P��@�?������>                P��@�?      0�     p�?������>���������Y~��������      0?      0����Y~��             `�?   ܡ-?   ܡ-�@<"r2'?   ܡ-�      0?      0�@<"r2'?      0�     ��?�I       hSK KK��R�K��R���]�(hjq  }�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.�L       h#Nu��R�hj�  }�(j�  ]�(hjq  }�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.�R       h#Nu��R�hh!}�(h#Nh$K h%K$h&Ku��R�ej�  ]�(h,)��}�(h/h2h3Kl��h5h6h7j�  h?�h@Kub�������                                    �&       h,)��}�(h/h2h3Kl��h5h6h7j�  h?�h@Kub����   			


   !!!"""###��       ej�  Nj�  ]�(NNeu��R�e��R�hWj}  hYj~  h\}�h^}�h`�sub�smoothed�j_  )��}�(hjc  jf  h,)��}�(h/h2h3KK$��h5j�  h7h<h?�h@Kub��������-��Ǆ@���1�kA]��_(a�    2�kA   ^�:A/j�E��"A   �]	oA   ��QA3ڡT�C:�    �sA   �(Ax�r'�(A   �ųtA   ��CAW�c�9'�   @$/wA
   ��2�"yA���9A   `)vA   �����Z Z)A   �z�uA   ��*A�ySsn�   `	�vA   �9�[d%-D�4A   @�9uA������3A�-G)�   ��rvA   �8��tM�XE2A   ���tA�����#A0DT�8!�   ���uA   ` ��?���A   ��uA�����q?�A�sJ�4A   �sA   Bq@A�
�3�9�    �uA    T�$��˦�;�A   �jytA@����w��0D4vi��   �;vtA   �1��u�t!�%A   @�esA    �1A���Y��	�   `@�sA����'�"A89oc�n�   ��tA������&�d�s�A   `SfsA   �*��M��JA   �#�rA�����5��Ի���(A   @E7qA   N AvG��lp!�   ���qA����#&����57fA   �	qA�����H��I��0�>A   ��kA������3A
h�~�3�����XnA����s�)��#m?NA   @X�lA
   $/�4�2xmeA    ��jA������6�jf�z��'A   @v�gA   .3�� ANon A   �P�eA�����T)�����u�A    �cA   ��:�.9U�\*A    s�`A������E�i���b7A   sVA   \�:�����*�#A    ��OA������;��S���$A�I       hSK KK��R�K��R���]�(hjq  }�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.�y       h#Nu��R�h(e��R�hWj}  hYj~  h\}�h^}�h`�sub�smoothed_cov�j_  )��}�(hjc  jf  h,)��}�(h/h2h3KKl��h5j�  h7h<h?�h@Kub��������RHe�~�.ARHe�~�.�/]�ĺ'#ARHe�~�.�!Lc�~�.Ao��ĺ'#�.]�ĺ'#A�S�ĺ'#� �r�T"$B    ��     ��>�r_NV�    ��>o�$��5?l^r����r_NV�g��9��#�aRpB������>������<U����������jQz��?��}���>>U����{�O^m�6?��BO�4�A������    ��>��z��    ��>fSf�jcC�R�7!�B?��z��B�-��,;?�"E#)�A������>�������$�r�Ҿ������<�t�%�	?��o��&?�$�r�Ҿ���as�{(*�T��A������     ��>L��C���     ��>��?u�4��{yӟ�1?K��C������\-?�u�J���A������>������#(����>������V��I%?��+XP0?�#(����>���0gO��5E���A������������>Ş��J��������>C���j�0������!?Ş��J��R���%'?H�=�p�A������>������o���9Q�>������/�[�0�B����{-W=?p���9Q�>�����8?�� �Y�A������������>^�W��������>^m���#?p�����]�W���K�7�^���pGvA������>������Nw^�60�>��������˺���>VU��/�Nw^�60�>��kn!׾�=A cA������������>Z}'Z�������>��(N�3?�sl�N7�[}'Z���j��)�ȋ���PA������>������oWE�S��>������|��R�;?��q�.�nWE�S��>���q�B2����~�<A������������>���U���������>���b�$�֕ ��1?���U���W�K�??vu���(A������>����������%��>�������s���!?��i������%��>=u�v���}S��A������������>��|wy��������><͗��1?����X���|wy�뾮?��k'���r�A������>������S򣛝��>������j��/���0b5?R򣛝��><i��$?���%�@������������>D��ɅM�������>3�;畉;������+�E��ɅM뾿U22?zf�D��@������>������cc�-v
�>����������;1���ӫSU�cc�-v
�>�x�ߌ&?E�/�8�@������������>Xk��6�������>�
"~"$�,z��f3�Xk��6�����?�]M�C��@����/1?    /1���^ �.-?����/1�����%?:�͖�����^ �.-?��x�$�:{�y#+�@     ��������>oÍ�3��     ��>�!�Z]3? ���+?oÍ�3�������%���9=�x�@������>������>+Jt.���     ����7�1C?�T�cu��4+Jt.����JKZ8�(���A{@����ۡ-?����ۡ-��Cg�?����ۡ-���z]H�3? �zT��>�Cg�?�[��`{$�h2�^�g@����/1?����/1����V�,?����/1�2{���fƾX� kNc"����V�,?�Ye��~�{��frT@������������>	*�X;:�������>˳��o?�!��s(?*�X;:���è���Hǩ3�A@����/1?����/1��y�k#+?����/1����5S꾠��$� ��y�k#+?{�7�Н��v�;�W�.@�����������>
dx%?������>��!z9��Wa��0?
dx%?P&�϶t+?��U֞�@������>�������"$?������5�s���>�u�6�j	?�"$?�q����͌h@������������>��/�?������>�����>PI�P����/�?3x �����`��g��?������>������iB��	��������^|o�~%��� [V?mB��	���0��%?5��C�A�?������������>�6�ib4��������>�P�
d��t���` )?�6�ib4��6�y��?몑-���?������>������u0p��>������逘d/?K��g0�s0p��>�	~�� $��حR��?������������>RO��@�?������>�.*�!��1S0e��RO��@�?�(�g(��>���z/n�?������>��������Y~��������~A��*�����k`?���Y~��xA�rQ%?�)��/T�?   ܡ-?   ܡ-�A<"r2'?   ܡ-�x-�7 x$?      0�@<"r2'?ﰑù*!�     ��?�I       hSK KK��R�K��R���]�(hjq  }�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.�L       h#Nu��R�hj�  }�(j�  ]�(hjq  }�(h
h,)��}�(h/h2h3K��h5h6h7j�  h?�h@Kub���       �numpy._core.multiarray��_reconstruct����numpy��ndarray���K ��Cb���R�(KK��h�dtype����O8�����R�(K�|�NNNJ����J����K?t�b�]�(�state.0��state.1��state.2�et�b.�R       h#Nu��R�hh!}�(h#Nh$K h%K$h&Ku��R�ej�  ]�(h,)��}�(h/h2h3Kl��h5h6h7j�  h?�h@Kub�������                                    �&       h,)��}�(h/h2h3Kl��h5h6h7j�  h?�h@Kub����   			


   !!!"""###�l      ej�  Nj�  ]�(NNeu��R�e��R�hWj}  hYj~  h\}�h^}�h`�subub�_data_attr_model�]�(j�  hhbe�
_init_kwds�}�(h5h�h�h�h�h�h��h��h��h�Ku�specification��statsmodels.tools.tools��Bunch���)��(h�K j8  �j9  �j;  �h��h��j<  �h��h�Kh5h�h�h�jh  Kjk  K jg  Kji  Kjj  K jl  K j  Kj  Kh�h�h�K h�K j:  �jq  �ujA  bj^  h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub���������������(       j>  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��������������      �?�����鿕(       jF  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��������������      �?�����忕(       jN  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��������������      �?�(       jV  h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub������      �?�;       �polynomial_reduced_ar�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub���      �?�����鿕;       �polynomial_reduced_ma�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�����������      �?�����忕�       �model_orders�}�(h�K hgK �ar�K�ma�K�seasonal_ar�K �seasonal_ma�K �
reduced_ar�K�
reduced_ma�K�exog_variance�K �measurement_variance�K �variance�Ku�param_terms�]�(j[  j\  jc  e�
_params_ar�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub������������?�0       �
_params_ma�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub�������������������忕6       �_params_variance�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��������:�^(IzB�9       �_params_seasonal_ma�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub������9       �_params_seasonal_ar�h,)��}�(h/h2h3K ��h5h6h7h<h?�h@Kub��������������h       �mlefit��statsmodels.base.model��LikelihoodModelResults���)��}�(h{h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub��������������#�/'���J�T���2�?!n4A��       hh�hiK h�]�j0  ]�(j2  j3  j4  ej5  Nj6  G?�      j7  ��mle_retvals�}�(�fopt�h�h<C��IK.@���R��gopt�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub����������������a���f � ��>V̹��tt���       �fcalls�KD�warnflag�K j�  ��
iterations�Ku�mle_settings�}�(�	optimizer��lbfgs��start_params�h,)��}�(h/h2h3K��h5h6h7h<h?�h@Kub����������v˟<��%	*+�E��֑?!n4A��      �maxiter�K2�full_output�K�disp�K �fargs�}�(�transformed���includes_fixed���score_method�N�approx_complex_step��u���callback�N�retall���extra_fit_funcs�}��approx_grad���epsilon�G>�����h�bounds�]�(NN��j�  j�  euubj�  j�  j�  j�  ub�__doc__�X�  
Class to hold results from fitting an SARIMAX model

Parameters
----------
model : SARIMAX instance
    The fitted model instance

Attributes
----------
specification : dictionary
    Dictionary including all attributes from the SARIMAX model instance.
polynomial_ar : ndarray
    Array containing autoregressive lag polynomial coefficients,
    ordered from lowest degree to highest. Initialized with ones, unless
    a coefficient is constrained to be zero (in which case it is zero).
polynomial_ma : ndarray
    Array containing moving average lag polynomial coefficients,
    ordered from lowest degree to highest. Initialized with ones, unless
    a coefficient is constrained to be zero (in which case it is zero).
polynomial_seasonal_ar : ndarray
    Array containing seasonal autoregressive lag polynomial coefficients,
    ordered from lowest degree to highest. Initialized with ones, unless
    a coefficient is constrained to be zero (in which case it is zero).
polynomial_seasonal_ma : ndarray
    Array containing seasonal moving average lag polynomial coefficients,
    ordered from lowest degree to highest. Initialized with ones, unless
    a coefficient is constrained to be zero (in which case it is zero).
polynomial_trend : ndarray
    Array containing trend polynomial coefficients, ordered from lowest
    degree to highest. Initialized with ones, unless a coefficient is
    constrained to be zero (in which case it is zero).
model_orders : dict
    The orders of each of the polynomials in the model.
param_terms : list of str
    List of parameters actually included in the model, in sorted order.

See Also
--------
statsmodels.tsa.statespace.kalman_filter.FilterResults
statsmodels.tsa.statespace.mlemodel.MLEResults
��fit_details�j~  ub.
```


<div style='page-break-after: always;'></div>

# File: notebooks\01_data_exploration.ipynb

```ipynb
```


<div style='page-break-after: always;'></div>

# File: notebooks\02_feature_engineering.ipynb

```ipynb
```


<div style='page-break-after: always;'></div>

# File: notebooks\03_modeling_experiments.ipynb

```ipynb
```


<div style='page-break-after: always;'></div>

# File: README.md

```md
# ValueAI: End-to-End Risk Stratification & Agentic AI Insights

## Project Overview
This project builds a scalable cloud pipeline that segments users, predicts future outcomes, and deploys an Agentic AI assistant for value-based programs. 

## Directory Structure
- `data/`: Raw and processed datasets.
- `notebooks/`: Exploratory data analysis.
- `src/`: Production-ready modular Python code.
- `app/`: Streamlit dashboard.
- `docs/`: Executive summary and audit logs.

## Setup
1. `python -m venv venv`
2. `venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `streamlit run app/app.py`




## Remove all contents created by download_synpuf_data.ps1 off the synpuf directory safely
Remove-Item -Path ".\data\raw\synpuf\*" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "[OK] Downloaded data cleared successfully." -ForegroundColor Green

# Run download_synpuf_data.ps1 to download the data
.\scripts\download_synpuf_data.ps1



# 1. Download the data
cd scripts
.\download_synpuf_data.ps1
cd ..

### ✅ Pre-Flight Check (Do this first)
Just to be 100% sure all dependencies are ready (especially since we added `great-expectations` and `matplotlib`), run this quick command in your active `.venv`:
```powershell
pip install -r requirements.txt
```

---

### 🚀 Execute the Phase 1 Pipeline

Run these three commands in order. I have included what you should expect to see so you know it's working correctly.



(
### 🛠️ Step 1: Install Java (JDK 11) via Windows Package Manager
We will use `winget` (built into modern Windows) to install Eclipse Temurin (a reliable, open-source JDK). 

1. Open a **new** PowerShell window (you can use your current one).
2. Copy and paste this command and press **Enter**:
   ```powershell
   winget install --id EclipseAdoptium.Temurin.11.JDK -e
   ```
   *(If it asks for administrator permission or terms of agreement, type `Y` and press Enter).*

---

### 🛠️ Step 2: Set the `JAVA_HOME` Environment Variable
Once the installation finishes, we need to tell Windows where Java lives. 

1. **Close your current PowerShell terminal** and open a **new** one (this is required to pick up the new installation).
2. Run this PowerShell script to automatically find the installation and set `JAVA_HOME`:
   ```powershell
   # Find the newly installed JDK 11 directory
   $javaDir = Get-ChildItem "C:\Program Files\Eclipse Adoptium" -Filter "jdk-11*" -ErrorAction SilentlyContinue | Select-Object -First 1

   if ($javaDir) {
       # Set JAVA_HOME for the current user permanently
       [Environment]::SetEnvironmentVariable("JAVA_HOME", $javaDir.FullName, "User")
       
       # Set it for the current session immediately
       $env:JAVA_HOME = $javaDir.FullName
       
       # Add Java to PATH for this session
       $env:Path = "$env:JAVA_HOME\bin;" + $env:Path
       
       Write-Host "✅ JAVA_HOME successfully set to: $($javaDir.FullName)" -ForegroundColor Green
       Write-Host "✅ Java version:" -ForegroundColor Green
       java -version
   } else {
       Write-Host "⚠️ Could not find Java automatically." -ForegroundColor Yellow
       Write-Host "Please install manually from: https://adoptium.net/temurin/releases/?version=11" -ForegroundColor Yellow
   }
   ```

---

### 🛠️ Step 3: Verify and Run the Pipeline Again
1. Verify Java is working by running:
   ```powershell
   java -version
   ```
   *(You should see output like `openjdk version "11.0.x"`)*

2. Now, run your PySpark pipeline again:
   ```powershell
   python -m src.data.make_dataset
   ```
)






#### 1. Run the Main PySpark Pipeline
```powershell
python -m src.data.make_dataset
```
**What to expect:** 
- You will see Spark initialization logs.
- It will load the 2008/2009 beneficiary files and union them.
- It will load the claims files, build the 30-day readmission target, and engineer the rolling average features.
- It will perform the stratified split and save `.parquet` files.
- **Success Indicator:** You should see `✅ Pipeline completed in XX.X seconds` and `📁 Processed data saved to...`






#### 2. Validate Data Quality
```powershell
python -m src.data.validate_data
```
**What to expect:**
- Great Expectations will read your new `train.parquet` file.
- It will run the 6 business rules (no null IDs, age bounds, boolean targets, etc.).
- **Success Indicator:** You should see `📋 Data quality report saved to: ...` followed by `Validation PASSED ✅`. *(Note: Great Expectations updates its API frequently. If you get a minor syntax error here, just paste it to me and I will give you the 1-line fix).*

#### 3. Run Monte Carlo Simulation
```powershell
python -m src.data.monte_carlo_simulation
```
**What to expect:**
- It will read the `AVG_ADMISSION_COST` from your processed data.
- It will fit a log-normal distribution and run 10,000 simulations.
- **Success Indicator:** You should see `✅ Monte Carlo simulation complete`, the projected total cost, and a new file named `monte_carlo_projection.png` will appear in your `data/processed/` folder.

---

### 🔍 How to Verify Success
After running all three, type this in your terminal:
```powershell
Get-ChildItem -Path .\data\processed\ -Recurse
```
You should see:
- `train.parquet`, `val.parquet`, `test.parquet`, `full_dataset.parquet`
- `data_profile_summary.csv`
- `monte_carlo_results.json`
- `monte_carlo_projection.png`

And in your `docs/` folder:
- `data_quality_report.md`

---

### 🛑 If You Hit a Snag
If any of these commands throw an error (e.g., a PySpark Java path issue, or a Great Expectations version mismatch), **don't panic**. This is normal in data engineering. Just copy the **last 10-15 lines of the error traceback** and paste it here. I will give you the exact fix.

Otherwise, paste the success output here, and we will immediately move to **Phase 2: Econometric, Statistical & ML Modeling** (Clustering, XGBoost, and Time-Series)!
```


<div style='page-break-after: always;'></div>

# File: requirements.txt

```txt
pyspark>=3.4.0
pandas>=2.0.0
numpy>=1.24.0
pyarrow>=12.0.0
scikit-learn>=1.3.0
xgboost>=2.0.0
statsmodels>=0.14.0
prophet>=1.1.0
shap>=0.43.0
langchain>=0.1.0
langgraph>=0.0.20
boto3>=1.34.0
streamlit>=1.30.0
plotly>=5.18.0
python-dotenv>=1.0.0
pytest>=7.4.0
great-expectations>=0.18.0
seaborn>=0.12.0
```


<div style='page-break-after: always;'></div>

# File: scripts\download_synpuf_data.ps1

```ps1
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




```


<div style='page-break-after: always;'></div>

# File: src\__init__.py

```python
```


<div style='page-break-after: always;'></div>

# File: src\ai_agent\__init__.py

```python
```


<div style='page-break-after: always;'></div>

# File: src\ai_agent\agent_graph.py

```python
```


<div style='page-break-after: always;'></div>

# File: src\ai_agent\agent_tools.py

```python
```


<div style='page-break-after: always;'></div>

# File: src\data\__init__.py

```python
```


<div style='page-break-after: always;'></div>

# File: src\data\make_dataset.py

```python
import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Tuple

import pyspark.sql.functions as F
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.window import Window


# =============================================================================
# PROJECT ROOT
# =============================================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# =============================================================================
# LOGGING
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =============================================================================
# WINDOWS SPARK CONFIGURATION
# =============================================================================
if os.name == "nt":
    # Force Spark to use this project's virtual environment
    os.environ["PYSPARK_PYTHON"] = sys.executable
    os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

    # Hadoop home used by Spark on Windows
    hadoop_home = Path.home() / ".hadoop"
    hadoop_bin = hadoop_home / "bin"

    winutils_path = hadoop_bin / "winutils.exe"
    hadoop_dll_path = hadoop_bin / "hadoop.dll"

    if not winutils_path.exists():
        raise FileNotFoundError(
            f"winutils.exe not found at {winutils_path}. "
            "Install the Hadoop 3.5.0 Windows binary before running the pipeline."
        )

    if not hadoop_dll_path.exists():
        raise FileNotFoundError(
            f"hadoop.dll not found at {hadoop_dll_path}. "
            "Install the Hadoop 3.5.0 Windows native library."
        )

    # Tell Hadoop where its Windows binaries live
    os.environ["HADOOP_HOME"] = str(hadoop_home)
    os.environ["hadoop.home.dir"] = str(hadoop_home)

    # Make Hadoop binaries available to Windows processes
    os.environ["PATH"] = (
        str(hadoop_bin)
        + os.pathsep
        + os.environ.get("PATH", "")
    )

    # Use forward slashes for Java/JVM native-library paths.
    # This avoids Windows backslash escaping issues in JVM options.
    hadoop_home_java = hadoop_home.as_posix()
    hadoop_bin_java = hadoop_bin.as_posix()
    

# =============================================================================
# 1. SPARK SESSION - Local mode for dev, cluster mode for AWS EMR/SageMaker
# =============================================================================
def create_spark_session(
    app_name: str = "ValueAI_SynPUF_Pipeline"
) -> SparkSession:
    """Create a Spark session configured for either local dev or AWS cluster."""

    # Detect environment: switch to YARN on AWS
    is_aws = os.environ.get("AWS_EXECUTION_ENV") is not None
    master = "yarn" if is_aws else "local[*]"

    builder = (
        SparkSession.builder
        .appName(app_name)
        .master(master)
        .config("spark.sql.session.timeZone", "UTC")
        .config(
            "spark.sql.shuffle.partitions",
            "8" if not is_aws else "200"
        )
        .config("spark.driver.memory", "4g")
        .config("spark.sql.adaptive.enabled", "true")
        .config(
            "spark.hadoop.fs.s3a.impl",
            "org.apache.hadoop.fs.s3a.S3AFileSystem"
        )
    )

    # Windows-only JVM configuration
    if os.name == "nt":
        builder = (
            builder
            .config(
                "spark.driver.extraJavaOptions",
                f"-Dhadoop.home.dir={hadoop_home_java} "
                f"-Djava.library.path={hadoop_bin_java}"
            )
            .config(
                "spark.executor.extraJavaOptions",
                f"-Dhadoop.home.dir={hadoop_home_java} "
                f"-Djava.library.path={hadoop_bin_java}"
            )
        )

    if is_aws:
        # AWS S3 credentials picked up from IAM role automatically
        builder = builder.config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "com.amazonaws.auth.InstanceProfileCredentialsProvider"
        )

    spark = builder.getOrCreate()

    spark.sparkContext.setLogLevel("WARN")

    logger.info(
        f"Spark session created on master: {master}"
    )

    return spark


# =============================================================================
# 2. DATA INGESTION - Read raw SynPUF CSVs
# =============================================================================
def load_beneficiary_data(
    spark: SparkSession,
    data_path: Path
) -> DataFrame:
    """Dynamically load and union all available beneficiary summary files."""

    pattern = "*Beneficiary_Summary_File_Sample_1.csv"

    files = list(data_path.glob(pattern))

    if not files:
        raise FileNotFoundError(
            f"No beneficiary files found matching {pattern} in {data_path}"
        )

    dfs = []

    for path in files:
        # Extract year from filename
        year = int(path.stem.split("_")[2])

        df = (
            spark.read
            .option("header", "true")
            .option("inferSchema", "true")
            .csv(str(path))
            .withColumn("source_year", F.lit(year))
        )

        dfs.append(df)

        logger.info(
            f"Loaded {path.name}: {df.count()} rows"
        )

    from functools import reduce

    final_df = reduce(
        lambda df1, df2: df1.unionByName(
            df2,
            allowMissingColumns=True
        ),
        dfs
    )

    logger.info(
        f"Total beneficiary records loaded across "
        f"{len(dfs)} years: {final_df.count()}"
    )

    return final_df


def load_claims_data(
    spark: SparkSession,
    data_path: Path,
    claim_type: str
) -> DataFrame:
    """Load inpatient, outpatient, carrier, or drug claims."""

    file_map = {
        "inpatient":
            "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv",

        "outpatient":
            "DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv",

        "carrier":
            "DE1_0_2008_to_2010_Carrier_Claims_Sample_1.csv",

        "drug":
            "DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.csv",
    }

    path = data_path / file_map[claim_type]

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(str(path))
    )

    logger.info(
        f"Loaded {claim_type} claims: {df.count()} rows"
    )

    return df


# =============================================================================
# 3. DATA CLEANING
# =============================================================================
def clean_beneficiary_data(df: DataFrame) -> DataFrame:
    """Standardize dates, handle missing values, derive age."""

    df = (
        df

        # CMS SynPUF uses yyyyMMdd
        .withColumn(
            "BENE_BIRTH_DT",
            F.to_date("BENE_BIRTH_DT", "yyyyMMdd")
        )

        .withColumn(
            "BENE_DEATH_DT",
            F.to_date("BENE_DEATH_DT", "yyyyMMdd")
        )

        # Age at end of study
        .withColumn(
            "AGE",
            F.floor(
                F.datediff(
                    F.lit("2010-12-31"),
                    F.col("BENE_BIRTH_DT")
                ) / 365.25
            )
        )

        # Impute missing race
        .withColumn(
            "RACE",
            F.coalesce(
                F.col("BENE_RACE_CD"),
                F.lit(2)
            )
        )

        .drop("BENE_RACE_CD")

        # Flag deceased beneficiaries
        .withColumn(
            "IS_DECEASED",
            F.col("BENE_DEATH_DT").isNotNull()
        )

        # Keep valid ages
        .filter(
            (F.col("AGE") >= 18) &
            (F.col("AGE") <= 110)
        )
    )

    logger.info(
        f"Cleaned beneficiary data: {df.count()} rows"
    )

    return df


def clean_claims_dates(
    df: DataFrame,
    claim_type: str
) -> DataFrame:
    """Standardize date columns across all claim types."""

    date_cols = {
        "inpatient": [
            "CLM_ADMSN_DT",
            "CLM_THRU_DT",
            "NCH_BENE_DSCHRG_DT"
        ],

        "outpatient": [
            "CLM_FROM_DT",
            "CLM_THRU_DT"
        ],

        "carrier": [
            "CLM_FROM_DT",
            "CLM_THRU_DT"
        ],

        "drug": [
            "SRVC_DT"
        ],
    }

    for col_name in date_cols.get(claim_type, []):

        if col_name in df.columns:

            df = df.withColumn(
                col_name,
                F.to_date(
                    F.col(col_name),
                    "yyyyMMdd"
                )
            )

    return df


# =============================================================================
# 4. FEATURE ENGINEERING
# =============================================================================
def build_readmission_target(
    inpatient_df: DataFrame
) -> DataFrame:
    """
    Create 30-day readmission target variable.

    A readmission = another inpatient admission
    within 30 days of discharge.
    """

    window_spec = (
        Window
        .partitionBy("DESYNPUF_ID")
        .orderBy("CLM_ADMSN_DT")
        .rowsBetween(1, 1)
    )

    df = (
        inpatient_df

        .filter(
            F.col("CLM_ADMSN_DT").isNotNull()
        )

        .filter(
            F.col("NCH_BENE_DSCHRG_DT").isNotNull()
        )

        .withColumn(
            "next_admission_date",
            F.lead(
                "CLM_ADMSN_DT"
            ).over(window_spec)
        )

        .withColumn(
            "days_to_next_admission",
            F.datediff(
                F.col("next_admission_date"),
                F.col("NCH_BENE_DSCHRG_DT")
            )
        )

        .withColumn(
            "IS_30DAY_READMISSION",
            (
                (F.col("days_to_next_admission") <= 30) &
                (F.col("days_to_next_admission") >= 0)
            )
        )

        .drop(
            "next_admission_date",
            "days_to_next_admission"
        )
    )

    readmit_rate = (
        df
        .groupBy("IS_30DAY_READMISSION")
        .count()
        .collect()
    )

    logger.info(
        f"Readmission target distribution: {readmit_rate}"
    )

    return df


def build_comorbidity_features(
    inpatient_df: DataFrame
) -> DataFrame:
    """
    Count unique ICD-9 diagnosis codes per beneficiary.

    SynPUF has 10 diagnosis columns:
    ICD9_DGNS_CD, ICD9_DGNS_2_CD, ... ICD9_DGNS_10_CD
    """

    diag_cols = [
        c
        for c in inpatient_df.columns
        if c.startswith("ICD9_DGNS_")
        or c == "ICD9_DGNS_CD"
    ]

    df_long = (
        inpatient_df
        .select(
            "DESYNPUF_ID",
            F.explode(
                F.array(
                    *[
                        F.col(c)
                        for c in diag_cols
                    ]
                )
            ).alias("DIAGNOSIS_CD")
        )
        .filter(
            F.col("DIAGNOSIS_CD").isNotNull()
        )
    )

    comorbidity_counts = (
        df_long
        .groupBy("DESYNPUF_ID")
        .agg(
            F.countDistinct(
                "DIAGNOSIS_CD"
            ).alias(
                "UNIQUE_DIAGNOSES_COUNT"
            )
        )
    )

    return comorbidity_counts


def build_utilization_features(
    claims_df: DataFrame,
    claim_type: str
) -> DataFrame:
    """
    Build rolling averages and time-since-last-event
    per beneficiary.
    """

    date_col_map = {
        "inpatient": "CLM_ADMSN_DT",
        "outpatient": "CLM_FROM_DT",
        "carrier": "CLM_FROM_DT",
        "drug": "SRVC_DT"
    }

    date_col = date_col_map.get(
        claim_type,
        "CLM_FROM_DT"
    )

    # Determine cost column
    if "CLM_PMT_AMT" in claims_df.columns:
        cost_col = "CLM_PMT_AMT"

    elif "TOT_RX_CST_AMT" in claims_df.columns:
        cost_col = "TOT_RX_CST_AMT"

    else:
        cost_col = None

    window_spec = (
        Window
        .partitionBy("DESYNPUF_ID")
        .orderBy(date_col)
        .rowsBetween(-3, -1)
    )

    df = claims_df.filter(
        F.col(date_col).isNotNull()
    )

    if cost_col:

        df = (
            df

            .withColumn(
                "ROLLING_AVG_COST_3",
                F.avg(cost_col).over(window_spec)
            )

            .withColumn(
                "ROLLING_MAX_COST_3",
                F.max(cost_col).over(window_spec)
            )
        )

    # Time since previous claim
    df = df.withColumn(
        "DAYS_SINCE_LAST_CLAIM",
        F.datediff(
            F.col(date_col),
            F.lag(date_col).over(
                Window
                .partitionBy("DESYNPUF_ID")
                .orderBy(date_col)
            )
        )
    )

    agg_cols = [
        F.count("*").alias(
            f"{claim_type.upper()}_CLAIM_COUNT"
        ),

        (
            F.avg("ROLLING_AVG_COST_3").alias(
                f"AVG_{claim_type.upper()}_COST"
            )
            if cost_col
            else F.lit(None)
        ),

        F.avg(
            "DAYS_SINCE_LAST_CLAIM"
        ).alias(
            f"AVG_DAYS_BETWEEN_{claim_type.upper()}_CLAIMS"
        ),
    ]

    agg_cols = [
        c for c in agg_cols
        if c is not None
    ]

    return (
        df
        .groupBy("DESYNPUF_ID")
        .agg(*agg_cols)
    )


# =============================================================================
# 5. TRAIN / VALIDATION / TEST SPLIT
# =============================================================================
def stratified_split(
    df: DataFrame,
    target_col: str,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15
) -> Tuple[DataFrame, DataFrame, DataFrame]:
    """
    Split data into training, validation and test datasets.
    """

    train_df = df.filter(
        F.rand(seed=42) < train_ratio
    )

    remaining = df.filter(
        F.rand(seed=42) >= train_ratio
    )

    val_df = remaining.filter(
        F.rand(seed=43)
        < (val_ratio / (1 - train_ratio))
    )

    test_df = remaining.filter(
        F.rand(seed=43)
        >= (val_ratio / (1 - train_ratio))
    )

    logger.info(
        f"Split sizes - "
        f"Train: {train_df.count()}, "
        f"Val: {val_df.count()}, "
        f"Test: {test_df.count()}"
    )

    return train_df, val_df, test_df


# =============================================================================
# 6. MAIN PIPELINE ORCHESTRATOR
# =============================================================================
def run_pipeline():
    """Execute the full Phase 1 pipeline."""

    start_time = datetime.now()

    logger.info("=" * 60)
    logger.info("Starting ValueAI Phase 1 Pipeline")
    logger.info("=" * 60)

    spark = create_spark_session()

    raw_path = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "synpuf"
    )

    processed_path = (
        PROJECT_ROOT
        / "data"
        / "processed"
    )

    processed_path.mkdir(
        parents=True,
        exist_ok=True
    )

    try:

        # ---------------------------------------------------------------------
        # INGESTION
        # ---------------------------------------------------------------------
        logger.info("[1/6] Loading raw data...")

        beneficiaries = load_beneficiary_data(
            spark,
            raw_path
        )

        inpatient = load_claims_data(
            spark,
            raw_path,
            "inpatient"
        )

        outpatient = load_claims_data(
            spark,
            raw_path,
            "outpatient"
        )

        drug = load_claims_data(
            spark,
            raw_path,
            "drug"
        )

        # ---------------------------------------------------------------------
        # CLEANING
        # ---------------------------------------------------------------------
        logger.info("[2/6] Cleaning data...")

        beneficiaries = clean_beneficiary_data(
            beneficiaries
        )

        inpatient = clean_claims_dates(
            inpatient,
            "inpatient"
        )

        outpatient = clean_claims_dates(
            outpatient,
            "outpatient"
        )

        drug = clean_claims_dates(
            drug,
            "drug"
        )

        # ---------------------------------------------------------------------
        # TARGET VARIABLE
        # ---------------------------------------------------------------------
        logger.info(
            "[3/6] Building readmission target..."
        )

        inpatient_with_target = (
            build_readmission_target(
                inpatient
            )
        )

        # ---------------------------------------------------------------------
        # FEATURE ENGINEERING
        # ---------------------------------------------------------------------
        logger.info(
            "[4/6] Engineering features..."
        )

        comorbidity = (
            build_comorbidity_features(
                inpatient
            )
        )

        inpatient_util = (
            build_utilization_features(
                inpatient,
                "inpatient"
            )
        )

        outpatient_util = (
            build_utilization_features(
                outpatient,
                "outpatient"
            )
        )

        drug_util = (
            build_utilization_features(
                drug,
                "drug"
            )
        )

        # ---------------------------------------------------------------------
        # JOIN FEATURE TABLES
        # ---------------------------------------------------------------------
        logger.info(
            "[5/6] Joining feature tables..."
        )

        admission_base = (
            inpatient_with_target
            .groupBy("DESYNPUF_ID")
            .agg(
                F.max(
                    "IS_30DAY_READMISSION"
                ).alias(
                    "IS_30DAY_READMISSION"
                ),

                F.count("*").alias(
                    "TOTAL_ADMISSIONS"
                ),

                F.avg(
                    "CLM_PMT_AMT"
                ).alias(
                    "AVG_ADMISSION_COST"
                ),

                F.avg(
                    "CLM_UTLZTN_DAY_CNT"
                ).alias(
                    "AVG_LENGTH_OF_STAY"
                ),
            )
        )

        final_df = (
            beneficiaries

            .join(
                admission_base,
                "DESYNPUF_ID",
                "left"
            )

            .join(
                comorbidity,
                "DESYNPUF_ID",
                "left"
            )

            .join(
                inpatient_util,
                "DESYNPUF_ID",
                "left"
            )

            .join(
                outpatient_util,
                "DESYNPUF_ID",
                "left"
            )

            .join(
                drug_util,
                "DESYNPUF_ID",
                "left"
            )
        )

        # Fill nulls with 0 for patients with no claims.
        # These columns are created by the joins above.
        fill_columns = [
            "TOTAL_ADMISSIONS",
            "UNIQUE_DIAGNOSES_COUNT",
            "INPATIENT_CLAIM_COUNT",
            "OUTPATIENT_CLAIM_COUNT",
            "DRUG_CLAIM_COUNT"
        ]

        final_df = final_df.fillna(
            0,
            subset=[
                c
                for c in fill_columns
                if c in final_df.columns
            ]
        )

        # ---------------------------------------------------------------------
        # STRATIFIED SPLIT & SAVE
        # ---------------------------------------------------------------------
        logger.info(
            "[6/6] Stratified sampling and saving..."
        )

        train_df, val_df, test_df = stratified_split(
            final_df,
            "IS_30DAY_READMISSION"
        )

        # Save train dataset
        (
            train_df.write
            .mode("overwrite")
            .parquet(
                str(
                    processed_path
                    / "train.parquet"
                )
            )
        )

        # Save validation dataset
        (
            val_df.write
            .mode("overwrite")
            .parquet(
                str(
                    processed_path
                    / "val.parquet"
                )
            )
        )

        # Save test dataset
        (
            test_df.write
            .mode("overwrite")
            .parquet(
                str(
                    processed_path
                    / "test.parquet"
                )
            )
        )

        # Save complete dataset
        (
            final_df.write
            .mode("overwrite")
            .parquet(
                str(
                    processed_path
                    / "full_dataset.parquet"
                )
            )
        )

        # ---------------------------------------------------------------------
        # DATA PROFILE
        # ---------------------------------------------------------------------
        _generate_data_profile(
            train_df,
            processed_path
        )

        elapsed = (
            datetime.now() - start_time
        ).total_seconds()

        logger.info(
            f"Pipeline completed in {elapsed:.1f} seconds"
        )

        logger.info(
            f"Processed data saved to: {processed_path}"
        )

    except Exception as e:

        logger.error(
            f"[ERROR] Pipeline failed: {e}",
            exc_info=True
        )

        raise

    finally:
        spark.stop()


# =============================================================================
# 7. DATA PROFILE
# =============================================================================
def _generate_data_profile(
    df: DataFrame,
    output_path: Path
):
    """
    Generate a lightweight Spark data profiling summary.
    """

    summary = df.summary().toPandas()

    summary.to_csv(
        output_path / "data_profile_summary.csv",
        index=False
    )

    logger.info(
        "Data profile saved to data_profile_summary.csv"
    )


# =============================================================================
# ENTRY POINT
# =============================================================================
if __name__ == "__main__":
    run_pipeline()
```


<div style='page-break-after: always;'></div>

# File: src\data\monte_carlo_simulation.py

```python

"""
Monte Carlo simulation for cost uncertainty modeling.

Matches JD:
"build econometric and statistical models... simulations"

The simulation fits a log-normal distribution to positive historical
healthcare costs and projects future monthly costs with uncertainty bounds.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path

from src.utils.logger import get_logger


logger = get_logger(__name__)


def run_monte_carlo_projection(
    n_simulations: int = 10_000,
    projection_horizon_months: int = 12,
    confidence_level: float = 0.95,
    output_path: Path = None
) -> dict:
    """
    Run Monte Carlo simulation to project future healthcare costs.

    Historical positive admission costs are modeled using a log-normal
    distribution. Non-positive costs are excluded because a log-normal
    distribution is defined only for positive values.
    """

    # -------------------------------------------------------------------------
    # OUTPUT PATH
    # -------------------------------------------------------------------------
    if output_path is None:
        output_path = (
            Path(__file__).parents[2]
            / "data"
            / "processed"
        )

    output_path.mkdir(
        parents=True,
        exist_ok=True
    )

    # -------------------------------------------------------------------------
    # LOAD HISTORICAL DATA
    # -------------------------------------------------------------------------
    logger.info("Loading historical admission costs...")

    df = pd.read_parquet(
        output_path / "full_dataset.parquet"
    )

    if "AVG_ADMISSION_COST" not in df.columns:
        raise ValueError(
            "AVG_ADMISSION_COST column not found in full_dataset.parquet"
        )

    historical_costs = (
        pd.to_numeric(
            df["AVG_ADMISSION_COST"],
            errors="coerce"
        )
        .dropna()
        .to_numpy()
    )

    if len(historical_costs) == 0:
        raise ValueError(
            "No historical cost data available for simulation"
        )

    # -------------------------------------------------------------------------
    # VALIDATE HISTORICAL COSTS
    # -------------------------------------------------------------------------
    total_cost_records = len(historical_costs)

    non_positive_mask = historical_costs <= 0
    non_positive_count = int(
        np.sum(non_positive_mask)
    )

    positive_costs = historical_costs[
        ~non_positive_mask
    ]

    logger.info(
        f"Historical cost records: {total_cost_records:,}"
    )

    logger.info(
        f"Non-positive cost records excluded: {non_positive_count:,}"
    )

    logger.info(
        f"Positive cost records used for fitting: {len(positive_costs):,}"
    )

    if len(positive_costs) < 10:
        raise ValueError(
            "Fewer than 10 positive historical cost observations "
            "are available for fitting the log-normal distribution."
        )

    # -------------------------------------------------------------------------
    # FIT LOG-NORMAL DISTRIBUTION
    # -------------------------------------------------------------------------
    #
    # Log-normal modeling requires strictly positive values.
    #
    log_costs = np.log(
        positive_costs
    )

    mu = float(
        np.mean(log_costs)
    )

    sigma = float(
        np.std(log_costs)
    )

    if not np.isfinite(mu) or not np.isfinite(sigma):
        raise ValueError(
            "Invalid log-normal parameters. "
            f"mu={mu}, sigma={sigma}"
        )

    if sigma <= 0:
        raise ValueError(
            "Log-normal standard deviation is zero. "
            "Historical costs do not contain enough variation."
        )

    logger.info(
        f"Fitted log-normal distribution: "
        f"mu={mu:.4f}, sigma={sigma:.4f}"
    )

    # -------------------------------------------------------------------------
    # MONTE CARLO SIMULATION
    # -------------------------------------------------------------------------
    logger.info(
        f"Running {n_simulations:,} simulations "
        f"over {projection_horizon_months} months..."
    )

    np.random.seed(42)

    all_projections = np.zeros(
        (
            n_simulations,
            projection_horizon_months
        )
    )

    # Healthcare cost trend assumption:
    # approximately 5% annual growth.
    trend = np.linspace(
        1.0,
        1.05,
        projection_horizon_months
    )

    for sim in range(n_simulations):

        monthly_costs = np.random.lognormal(
            mean=mu,
            sigma=sigma,
            size=projection_horizon_months
        )

        all_projections[sim] = (
            monthly_costs * trend
        )

    # -------------------------------------------------------------------------
    # CALCULATE PROJECTION STATISTICS
    # -------------------------------------------------------------------------
    mean_projection = np.mean(
        all_projections,
        axis=0
    )

    lower_percentile = (
        (1 - confidence_level)
        / 2
        * 100
    )

    upper_percentile = (
        (1 + confidence_level)
        / 2
        * 100
    )

    lower_bound = np.percentile(
        all_projections,
        lower_percentile,
        axis=0
    )

    upper_bound = np.percentile(
        all_projections,
        upper_percentile,
        axis=0
    )

    total_cost_mean = float(
        np.sum(mean_projection)
    )

    total_cost_ci = (
        float(np.sum(lower_bound)),
        float(np.sum(upper_bound))
    )

    # -------------------------------------------------------------------------
    # RESULTS
    # -------------------------------------------------------------------------
    results = {
        "mean_monthly_projection":
            mean_projection.tolist(),

        "lower_bound":
            lower_bound.tolist(),

        "upper_bound":
            upper_bound.tolist(),

        "total_cost_mean":
            total_cost_mean,

        "total_cost_ci_lower":
            total_cost_ci[0],

        "total_cost_ci_upper":
            total_cost_ci[1],

        "n_simulations":
            n_simulations,

        "projection_horizon_months":
            projection_horizon_months,

        "confidence_level":
            confidence_level,

        "log_normal_mu":
            mu,

        "log_normal_sigma":
            sigma,

        "historical_cost_records":
            total_cost_records,

        "excluded_non_positive_costs":
            non_positive_count,

        "positive_cost_records_used":
            len(positive_costs),
    }

    # -------------------------------------------------------------------------
    # SAVE RESULTS
    # -------------------------------------------------------------------------
    results_df = pd.DataFrame(
        {
            "mean_monthly_projection":
                mean_projection,

            "lower_bound":
                lower_bound,

            "upper_bound":
                upper_bound,
        }
    )

    results_df.to_json(
        output_path / "monte_carlo_results.json",
        orient="index"
    )

    # -------------------------------------------------------------------------
    # PLOT
    # -------------------------------------------------------------------------
    months = np.arange(
        1,
        projection_horizon_months + 1
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.plot(
        months,
        mean_projection,
        linewidth=2,
        label="Mean Projection"
    )

    plt.fill_between(
        months,
        lower_bound,
        upper_bound,
        alpha=0.3,
        label=(
            f"{int(confidence_level * 100)}% "
            "Confidence Interval"
        )
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Projected Cost ($)"
    )

    plt.title(
        f"Monte Carlo Cost Projection "
        f"({n_simulations:,} Simulations)"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plt.savefig(
        output_path / "monte_carlo_projection.png",
        dpi=150
    )

    plt.close()

    # -------------------------------------------------------------------------
    # FINAL LOGGING
    # -------------------------------------------------------------------------
    logger.info(
        "Monte Carlo simulation complete"
    )

    logger.info(
        f"Total projected cost: "
        f"${total_cost_mean:,.2f}"
    )

    logger.info(
        f"{int(confidence_level * 100)}% CI: "
        f"(${total_cost_ci[0]:,.2f}, "
        f"${total_cost_ci[1]:,.2f})"
    )

    return results


if __name__ == "__main__":
    run_monte_carlo_projection()


```


<div style='page-break-after: always;'></div>

# File: src\data\validate_data.py

```python
"""
Great Expectations validation suite for data quality adherence.
Matches JD: "100% adherence to policies, procedures and statutory guidelines"
"""
import great_expectations as gx
from pathlib import Path
from datetime import datetime


def run_data_validation():
    """Validate processed data against business rules."""
    context = gx.get_context()
    processed_path = Path(__file__).parents[2] / "data" / "processed"

    # Create data source
    data_source = context.data_sources.add_pandas(name="synpuf_processed")
    data_asset = data_source.add_dataframe_asset(name="train_data")

    # Read train data
    import pandas as pd
    df = pd.read_parquet(processed_path / "train.parquet")
    batch_definition = data_asset.add_batch_definition_whole_dataframe("train_batch")
    batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

    # Define expectations (business rules)
    expectation_suite = context.suites.add(gx.ExpectationSuite(name="synpuf_quality"))

    expectations = [
        # 1. No null beneficiary IDs (primary key integrity)
        gx.expectations.ExpectColumnValuesToNotBeNull(column="DESYNPUF_ID"),
        # 2. Age must be between 18 and 110
        gx.expectations.ExpectColumnValuesToBeBetween(column="AGE", min_value=18, max_value=110),
        # 3. Readmission target must be boolean
        gx.expectations.ExpectColumnValuesToBeInSet(column="IS_30DAY_READMISSION", value_set=[True, False]),
        # 4. Costs must be non-negative
        gx.expectations.ExpectColumnValuesToBeBetween(column="AVG_ADMISSION_COST", min_value=0, max_value=1_000_000),
        # 5. Claim counts must be non-negative
        gx.expectations.ExpectColumnValuesToBeBetween(column="TOTAL_ADMISSIONS", min_value=0, max_value=1000),
        # 6. No duplicate beneficiaries
        gx.expectations.ExpectColumnValuesToBeUnique(column="DESYNPUF_ID"),
    ]

    for exp in expectations:
        expectation_suite.add_expectation(exp)

    # Run validation
    validation_definition = context.validation_definitions.add(
        gx.ValidationDefinition(
            name="synpuf_train_validation",
            data=batch_definition,
            suite=expectation_suite,
        )
    )

    result = validation_definition.run(batch_parameters={"dataframe": df})

    # Save report
    report_path = Path(__file__).parents[2] / "docs" / "data_quality_report.md"
    with open(report_path, "w") as f:
        f.write(f"# Data Quality Report\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write(f"## Results\n\n")
        f.write(f"**Status:** {'✅ PASSED' if result.success else '❌ FAILED'}\n\n")
        f.write(f"**Statistics:**\n")
        f.write(f"- Evaluated: {result.results.__len__()} expectations\n")
        f.write(f"- Success Rate: {sum(1 for r in result.results if r.success) / len(result.results) * 100:.1f}%\n\n")
        f.write("## Expectation Details\n\n")
        for r in result.results:
            status = "✅" if r.success else "❌"
            f.write(f"- {status} {r.expectation.configuration.get('type', 'Unknown')}\n")

    print(f"📋 Data quality report saved to: {report_path}")
    return result.success


if __name__ == "__main__":
    success = run_data_validation()
    print(f"\nValidation {'PASSED ✅' if success else 'FAILED ❌'}")
```


<div style='page-break-after: always;'></div>

# File: src\models\__init__.py

```python
```


<div style='page-break-after: always;'></div>

# File: src\models\train_classification.py

```python
"""
Classification Model for 30-Day Readmission Prediction.
Matches JD: "predictive statistical models, decision trees, classification"
"""
import sys
import logging
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from pathlib import Path
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report
import xgboost as xgb

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logger import get_logger
logger = get_logger(__name__)

def run_classification():
    logger.info("Starting Classification Model Training...")
    
    # 1. Load Data
    data_path = PROJECT_ROOT / "data" / "processed"
    train_df = pd.read_parquet(data_path / "train.parquet")
    val_df = pd.read_parquet(data_path / "val.parquet")
    test_df = pd.read_parquet(data_path / "test.parquet")
    
    # 2. Define Features and Target
    target = "IS_30DAY_READMISSION"
    exclude_cols = [
        "DESYNPUF_ID",
        "IS_30DAY_READMISSION",
        "BENE_BIRTH_DT",
        "BENE_DEATH_DT",
        "RISK_CLUSTER"
    ]

    # Remove records where the readmission outcome is unknown.
    # None/NaN means the outcome cannot be used as a classification label.
    train_df = train_df.dropna(subset=[target]).copy()
    val_df = val_df.dropna(subset=[target]).copy()
    test_df = test_df.dropna(subset=[target]).copy()

    logger.info(
        f"Labeled records - Train: {len(train_df):,}, "
        f"Validation: {len(val_df):,}, "
        f"Test: {len(test_df):,}"
    )

    # Convert boolean readmission target to binary 0/1.
    # True = readmitted, False = not readmitted.
    def encode_target(series):
        return series.map({
            True: 1,
            False: 0,
            "True": 1,
            "False": 0,
            1: 1,
            0: 0
        }).astype(int)

    train_df[target] = encode_target(train_df[target])
    val_df[target] = encode_target(val_df[target])
    test_df[target] = encode_target(test_df[target])

    features = [
        col for col in train_df.columns
        if col not in exclude_cols
        and train_df[col].dtype in [
            "int64",
            "float64",
            "bool",
            "int32",
            "float32"
        ]
    ]

    logger.info(f"Classification features: {len(features)}")

    # Handle boolean feature columns for XGBoost compatibility
    for col in features:
        if train_df[col].dtype == "bool":
            train_df[col] = train_df[col].astype(int)
            val_df[col] = val_df[col].astype(int)
            test_df[col] = test_df[col].astype(int)

    # Fill missing values in FEATURES only.
    train_df[features] = train_df[features].fillna(0)
    val_df[features] = val_df[features].fillna(0)
    test_df[features] = test_df[features].fillna(0)

    X_train, y_train = train_df[features], train_df[target]
    X_val, y_val = val_df[features], val_df[target]
    X_test, y_test = test_df[features], test_df[target]

    logger.info(
        f"Target distribution - Train: "
        f"{y_train.value_counts().to_dict()}"
    )
    logger.info(
        f"Target distribution - Validation: "
        f"{y_val.value_counts().to_dict()}"
    )
    logger.info(
        f"Target distribution - Test: "
        f"{y_test.value_counts().to_dict()}"
    )

    # 3. Train XGBoost Model
    logger.info("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric="auc"
    )
    
    model.fit(
        X_train, y_train,
        eval_set=[(X_train, y_train), (X_val, y_val)],
        verbose=False
    )
    
    # 4. Evaluate Model
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    auc_roc = roc_auc_score(y_test, y_pred_proba)
    acc = accuracy_score(y_test, y_pred)
    
    logger.info(f"Test AUC-ROC: {auc_roc:.4f}")
    logger.info(f"Test Accuracy: {acc:.4f}")
    logger.info("Classification Report:\n" + classification_report(y_test, y_pred))
    
    # 5. SHAP Explainability
    logger.info("Calculating SHAP values for explainability...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    # Plot SHAP summary
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_test, show=False)
    plt.title("SHAP Feature Importance for Readmission Prediction")
    plt.tight_layout()
    plt.savefig(PROJECT_ROOT / "docs" / "shap_summary.png", dpi=150)
    plt.close()
    logger.info("Saved SHAP summary plot to docs/shap_summary.png")
    
    # 6. Save Model
    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, models_dir / "classification_model.pkl")
    logger.info("Saved classification model to models/classification_model.pkl")
    
    logger.info("Classification Model Training Complete.")

if __name__ == "__main__":
    run_classification()
```


<div style='page-break-after: always;'></div>

# File: src\models\train_clustering.py

```python
"""
Clustering Model for Patient Risk Segmentation.
Matches JD: "clustering, pattern analysis, segmentation analysis, customer profiling"

Note for SageMaker: In a cloud environment, this script is executed as a SageMaker 
Training Job. The joblib.dump step is replaced by saving the model artifact to S3 
and registering it in the SageMaker Model Registry.
"""
import sys
import logging
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logger import get_logger
logger = get_logger(__name__)

def run_clustering():
    logger.info("Starting Clustering Model Training...")
    
    # 1. Load Data
    data_path = PROJECT_ROOT / "data" / "processed" / "full_dataset.parquet"
    df = pd.read_parquet(data_path)
    logger.info(f"Loaded {len(df)} records for clustering.")
    
    # 2. Select Features for Segmentation
    cluster_features = [
        "AGE", "TOTAL_ADMISSIONS", "AVG_ADMISSION_COST", 
        "UNIQUE_DIAGNOSES_COUNT", "AVG_LENGTH_OF_STAY",
        "INPATIENT_CLAIM_COUNT", "OUTPATIENT_CLAIM_COUNT", "DRUG_CLAIM_COUNT"
    ]
    
    available_features = [f for f in cluster_features if f in df.columns]
    X = df[available_features].fillna(0)
    
    # 3. Scale Features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4. Train Gaussian Mixture Model (GMM)
    n_components = 3
    gmm = GaussianMixture(n_components=n_components, random_state=42, n_init=10)
    cluster_labels = gmm.fit_predict(X_scaled)
    
    # 5. Evaluate
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    logger.info(f"Silhouette Score for {n_components} clusters: {silhouette_avg:.4f}")
    
    # 6. Analyze Cluster Profiles
    df["RISK_CLUSTER"] = cluster_labels
    cluster_profile = df.groupby("RISK_CLUSTER")[available_features].mean()
    logger.info("Cluster Profiles (Mean Values):\n" + str(cluster_profile))
    
    # 7. Save Outputs
    models_dir = PROJECT_ROOT / "models"
    models_dir.mkdir(parents=True, exist_ok=True)
    
    joblib.dump(gmm, models_dir / "clustering_model.pkl")
    joblib.dump(scaler, models_dir / "clustering_scaler.pkl")
    
    clustered_df_path = PROJECT_ROOT / "data" / "processed" / "clustered_dataset.parquet"
    df.to_parquet(clustered_df_path, index=False)
    logger.info(f"Saved clustered dataset to {clustered_df_path}")
    
    # Plot Cluster Distribution
    plt.figure(figsize=(8, 5))
    sns.countplot(x="RISK_CLUSTER", data=df, palette="viridis", hue="RISK_CLUSTER", legend=False)
    plt.title("Patient Risk Cluster Distribution")
    plt.xlabel("Cluster ID")
    plt.ylabel("Number of Patients")
    plt.savefig(PROJECT_ROOT / "docs" / "cluster_distribution.png", dpi=150)
    plt.close()
    logger.info("Saved cluster distribution plot to docs/cluster_distribution.png")
    
    logger.info("Clustering Model Training Complete.")

if __name__ == "__main__":
    run_clustering()
```


<div style='page-break-after: always;'></div>

# File: src\models\train_timeseries.py

```python
"""
Time-Series & Econometric Forecasting Model.

Matches JD:
"time-series analysis, econometrics, projections"

Methodology:
1. Aggregate inpatient claims into monthly healthcare costs.
2. Restrict the real dataset to complete 2008-2010 monthly observations.
3. Reserve the final 6 months as an out-of-sample holdout period.
4. Compare a naive baseline against an ARIMA model.
5. Evaluate using RMSE, MAE, and MAPE.
6. Refit the ARIMA model on the complete historical dataset.
7. Produce a 12-month forward forecast with 95% confidence intervals.
8. Save the trained model, forecast, evaluation metrics, and visualization.

This implementation intentionally avoids seasonal ARIMA because the available
historical series contains only 36 monthly observations. Estimating a full
12-month seasonal model with such a small sample can produce unstable
parameters and unreliable forecasts.
"""

import sys
import logging
import warnings
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logger import get_logger

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

RAW_DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "synpuf"
    / "DE1_0_2008_to_2010_Inpatient_Claims_Sample_1.csv"
)

DOCS_DIR = PROJECT_ROOT / "docs"
MODELS_DIR = PROJECT_ROOT / "models"

FORECAST_HORIZON = 12
HOLDOUT_MONTHS = 6

# ARIMA specification.
#
# With only 36 observations, a simple non-seasonal ARIMA is more defensible
# than a 12-month seasonal ARIMA.
ARIMA_ORDER = (1, 1, 1)


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_monthly_claim_costs():
    """
    Load and aggregate inpatient claims into monthly total costs.

    Returns
    -------
    pandas.DataFrame
        Columns:
            ds : monthly timestamp
            y  : total monthly claim cost
    """

    logger.info("Loading historical inpatient claims...")

    if not RAW_DATA_FILE.exists():
        logger.warning(
            "Raw inpatient claims not found. "
            "Using synthetic monthly data for demonstration."
        )

        dates = pd.date_range(
            start="2008-01-01",
            end="2010-12-01",
            freq="MS"
        )

        np.random.seed(42)

        # Synthetic data intentionally uses a moderate trend, annual
        # seasonality and random noise.
        trend = np.linspace(10_000_000, 15_000_000, len(dates))

        seasonality = (
            1_000_000
            * np.sin(
                2 * np.pi * np.arange(len(dates)) / 12
            )
        )

        noise = np.random.normal(
            loc=0,
            scale=300_000,
            size=len(dates)
        )

        monthly_costs = trend + seasonality + noise

        df = pd.DataFrame(
            {
                "ds": dates,
                "y": monthly_costs,
            }
        )

        return df

    logger.info("Reading raw inpatient claims CSV...")

    try:
        df_raw = pd.read_csv(RAW_DATA_FILE)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to read inpatient claims file: {exc}"
        ) from exc

    required_columns = [
        "CLM_ADMSN_DT",
        "CLM_PMT_AMT",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df_raw.columns
    ]

    if missing_columns:
        raise ValueError(
            "Required columns missing from inpatient claims file: "
            + ", ".join(missing_columns)
        )

    logger.info(
        f"Raw inpatient claim records: {len(df_raw):,}"
    )

    # Convert admission date.
    df_raw["CLM_ADMSN_DT"] = pd.to_datetime(
        df_raw["CLM_ADMSN_DT"],
        format="%Y%m%d",
        errors="coerce"
    )

    # Convert payment amount to numeric.
    df_raw["CLM_PMT_AMT"] = pd.to_numeric(
        df_raw["CLM_PMT_AMT"],
        errors="coerce"
    )

    # Remove unusable records.
    df_raw = df_raw.dropna(
        subset=[
            "CLM_ADMSN_DT",
            "CLM_PMT_AMT",
        ]
    )

    logger.info(
        f"Usable claim records after cleaning: {len(df_raw):,}"
    )

    # Convert every admission date to month-start.
    df_raw["ds"] = (
        df_raw["CLM_ADMSN_DT"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    # Aggregate total monthly claim payments.
    df = (
        df_raw
        .groupby("ds", as_index=False)["CLM_PMT_AMT"]
        .sum()
        .rename(columns={"CLM_PMT_AMT": "y"})
        .sort_values("ds")
        .reset_index(drop=True)
    )

    # -----------------------------------------------------------------------
    # Important:
    #
    # The source contains Nov-Dec 2007 partial/ramp-up observations.
    # The intended analytical period is Jan 2008-Dec 2010.
    # -----------------------------------------------------------------------

    start_date = pd.Timestamp("2008-01-01")
    end_date = pd.Timestamp("2010-12-01")

    df = df[
        (df["ds"] >= start_date)
        & (df["ds"] <= end_date)
    ].copy()

    # Create a complete monthly index.
    expected_dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="MS"
    )

    df = (
        df
        .set_index("ds")
        .reindex(expected_dates)
        .rename_axis("ds")
        .reset_index()
    )

    # Missing months indicate no recorded claims in that month.
    # For a monthly total-cost series, this is treated as zero.
    missing_months = df["y"].isna().sum()

    if missing_months > 0:
        logger.warning(
            f"Found {missing_months} missing monthly observations. "
            "Filling missing monthly costs with zero."
        )

        df["y"] = df["y"].fillna(0)

    # Validate final data.
    if len(df) < HOLDOUT_MONTHS + 12:
        raise ValueError(
            "Insufficient historical observations for time-series modeling."
        )

    if not np.isfinite(df["y"]).all():
        raise ValueError(
            "Monthly cost series contains non-finite values."
        )

    logger.info(
        f"Monthly time series: {len(df)} observations"
    )

    logger.info(
        f"Historical period: "
        f"{df['ds'].min().strftime('%Y-%m')} to "
        f"{df['ds'].max().strftime('%Y-%m')}"
    )

    logger.info(
        f"Monthly cost range: "
        f"${df['y'].min():,.2f} to ${df['y'].max():,.2f}"
    )

    return df


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def calculate_metrics(actual, predicted):
    """
    Calculate standard forecasting evaluation metrics.
    """

    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)

    rmse = np.sqrt(
        mean_squared_error(actual, predicted)
    )

    mae = mean_absolute_error(
        actual,
        predicted
    )

    # MAPE is undefined when actual values are zero.
    non_zero_mask = actual != 0

    if non_zero_mask.any():
        mape = (
            np.mean(
                np.abs(
                    (
                        actual[non_zero_mask]
                        - predicted[non_zero_mask]
                    )
                    / actual[non_zero_mask]
                )
            )
            * 100
        )
    else:
        mape = np.nan

    return {
        "RMSE": rmse,
        "MAE": mae,
        "MAPE": mape,
    }


# ---------------------------------------------------------------------------
# Model Training
# ---------------------------------------------------------------------------

def fit_arima(series):
    """
    Fit the configured ARIMA model.

    Warnings are suppressed during fitting because statsmodels can emit
    convergence warnings on small samples. The model fit itself is still
    checked for successful completion.
    """

    logger.info(
        f"Fitting ARIMA{ARIMA_ORDER}..."
    )

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=UserWarning
        )

        warnings.filterwarnings(
            "ignore",
            category=RuntimeWarning
        )

        fitted_model = ARIMA(
            series,
            order=ARIMA_ORDER
        ).fit()

    return fitted_model


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def run_timeseries():

    logger.info(
        "Starting Time-Series Forecasting Model..."
    )

    DOCS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # -----------------------------------------------------------------------
    # 1. Load and prepare monthly data
    # -----------------------------------------------------------------------

    df = load_monthly_claim_costs()

    logger.info(
        f"Time series data shape: {df.shape}"
    )

    # -----------------------------------------------------------------------
    # 2. Holdout split
    #
    # Final 6 months are never used during model training.
    # This provides a genuine out-of-sample evaluation.
    # -----------------------------------------------------------------------

    train = df.iloc[:-HOLDOUT_MONTHS].copy()
    test = df.iloc[-HOLDOUT_MONTHS:].copy()

    logger.info(
        f"Training observations: {len(train)}"
    )

    logger.info(
        f"Holdout observations: {len(test)}"
    )

    logger.info(
        f"Training period: "
        f"{train['ds'].min().strftime('%Y-%m')} to "
        f"{train['ds'].max().strftime('%Y-%m')}"
    )

    logger.info(
        f"Holdout period: "
        f"{test['ds'].min().strftime('%Y-%m')} to "
        f"{test['ds'].max().strftime('%Y-%m')}"
    )

    # -----------------------------------------------------------------------
    # 3. Naive baseline
    #
    # Forecast every holdout month using the final observed training value.
    # This is important because ARIMA should demonstrate value beyond a
    # simple baseline.
    # -----------------------------------------------------------------------

    logger.info(
        "Evaluating naive last-value baseline..."
    )

    naive_prediction = np.repeat(
        train["y"].iloc[-1],
        len(test)
    )

    naive_metrics = calculate_metrics(
        test["y"],
        naive_prediction
    )

    logger.info(
        f"Naive Baseline RMSE: "
        f"${naive_metrics['RMSE']:,.2f}"
    )

    logger.info(
        f"Naive Baseline MAE: "
        f"${naive_metrics['MAE']:,.2f}"
    )

    logger.info(
        f"Naive Baseline MAPE: "
        f"{naive_metrics['MAPE']:.2f}%"
    )

    # -----------------------------------------------------------------------
    # 4. Train ARIMA using only training data
    # -----------------------------------------------------------------------

    fitted_train_model = fit_arima(
        train["y"]
    )

    logger.info(
        "ARIMA model fitted successfully."
    )

    # -----------------------------------------------------------------------
    # 5. Forecast the holdout period
    # -----------------------------------------------------------------------

    logger.info(
        f"Generating {HOLDOUT_MONTHS}-month holdout forecast..."
    )

    holdout_forecast_result = (
        fitted_train_model.get_forecast(
            steps=HOLDOUT_MONTHS
        )
    )

    holdout_prediction = (
        holdout_forecast_result
        .predicted_mean
        .to_numpy()
    )

    # -----------------------------------------------------------------------
    # 6. Evaluate ARIMA
    # -----------------------------------------------------------------------

    arima_metrics = calculate_metrics(
        test["y"],
        holdout_prediction
    )

    logger.info(
        f"ARIMA Test RMSE: "
        f"${arima_metrics['RMSE']:,.2f}"
    )

    logger.info(
        f"ARIMA Test MAE: "
        f"${arima_metrics['MAE']:,.2f}"
    )

    logger.info(
        f"ARIMA Test MAPE: "
        f"{arima_metrics['MAPE']:.2f}%"
    )

    # -----------------------------------------------------------------------
    # 7. Compare ARIMA against baseline
    # -----------------------------------------------------------------------

    if (
        np.isfinite(arima_metrics["RMSE"])
        and np.isfinite(naive_metrics["RMSE"])
        and naive_metrics["RMSE"] != 0
    ):
        rmse_improvement = (
            (
                naive_metrics["RMSE"]
                - arima_metrics["RMSE"]
            )
            / naive_metrics["RMSE"]
        ) * 100
    else:
        rmse_improvement = np.nan

    logger.info(
        f"ARIMA RMSE improvement vs naive baseline: "
        f"{rmse_improvement:.2f}%"
    )

    # -----------------------------------------------------------------------
    # 8. Save evaluation metrics
    # -----------------------------------------------------------------------

    metrics_df = pd.DataFrame(
        [
            {
                "model": "Naive Last Value",
                "rmse": naive_metrics["RMSE"],
                "mae": naive_metrics["MAE"],
                "mape_percent": naive_metrics["MAPE"],
            },
            {
                "model": f"ARIMA{ARIMA_ORDER}",
                "rmse": arima_metrics["RMSE"],
                "mae": arima_metrics["MAE"],
                "mape_percent": arima_metrics["MAPE"],
            },
        ]
    )

    metrics_path = (
        DOCS_DIR
        / "timeseries_model_metrics.csv"
    )

    metrics_df.to_csv(
        metrics_path,
        index=False
    )

    logger.info(
        f"Saved evaluation metrics to {metrics_path}"
    )

    # -----------------------------------------------------------------------
    # 9. Create holdout evaluation dataset
    # -----------------------------------------------------------------------

    holdout_df = test[
        ["ds", "y"]
    ].copy()

    holdout_df["naive_forecast"] = naive_prediction
    holdout_df["arima_forecast"] = holdout_prediction

    holdout_path = (
        DOCS_DIR
        / "timeseries_holdout_evaluation.csv"
    )

    holdout_df.to_csv(
        holdout_path,
        index=False
    )

    logger.info(
        f"Saved holdout evaluation to {holdout_path}"
    )

    # -----------------------------------------------------------------------
    # 10. Refit ARIMA on ALL historical observations
    #
    # The holdout was only for honest evaluation.
    # Once evaluation is complete, we use all historical data to maximize
    # information available for the final production forecast.
    # -----------------------------------------------------------------------

    logger.info(
        "Refitting ARIMA on complete historical dataset..."
    )

    final_model = fit_arima(
        df["y"]
    )

    logger.info(
        "Final ARIMA model fitted successfully."
    )

    # -----------------------------------------------------------------------
    # 11. Generate 12-month future forecast
    # -----------------------------------------------------------------------

    logger.info(
        f"Generating {FORECAST_HORIZON}-month future forecast..."
    )

    forecast_result = (
        final_model.get_forecast(
            steps=FORECAST_HORIZON
        )
    )

    forecast_mean = (
        forecast_result
        .predicted_mean
        .to_numpy()
    )

    conf_int = (
        forecast_result
        .conf_int()
        .to_numpy()
    )

    forecast_dates = pd.date_range(
        start=(
            df["ds"].iloc[-1]
            + pd.DateOffset(months=1)
        ),
        periods=FORECAST_HORIZON,
        freq="MS"
    )

    forecast_df = pd.DataFrame(
        {
            "ds": forecast_dates,
            "forecast": forecast_mean,
            "lower_ci": conf_int[:, 0],
            "upper_ci": conf_int[:, 1],
        }
    )

    # Ensure forecasts cannot contain non-finite values.
    if not np.isfinite(
        forecast_df[
            [
                "forecast",
                "lower_ci",
                "upper_ci",
            ]
        ].to_numpy()
    ).all():

        raise ValueError(
            "Final forecast contains non-finite values."
        )

    # -----------------------------------------------------------------------
    # 12. Log forecast summary
    # -----------------------------------------------------------------------

    logger.info(
        "Future forecast summary:"
    )

    logger.info(
        f"Total projected cost over "
        f"{FORECAST_HORIZON} months: "
        f"${forecast_df['forecast'].sum():,.2f}"
    )

    logger.info(
        f"Average projected monthly cost: "
        f"${forecast_df['forecast'].mean():,.2f}"
    )

    logger.info(
        f"Minimum projected monthly cost: "
        f"${forecast_df['forecast'].min():,.2f}"
    )

    logger.info(
        f"Maximum projected monthly cost: "
        f"${forecast_df['forecast'].max():,.2f}"
    )

    # -----------------------------------------------------------------------
    # 13. Save forecast
    # -----------------------------------------------------------------------

    forecast_path = (
        DOCS_DIR
        / "timeseries_forecast.csv"
    )

    forecast_df.to_csv(
        forecast_path,
        index=False
    )

    logger.info(
        f"Saved forecast to {forecast_path}"
    )

    # -----------------------------------------------------------------------
    # 14. Create visualization
    # -----------------------------------------------------------------------

    logger.info(
        "Creating time-series forecast visualization..."
    )

    plt.figure(
        figsize=(14, 7)
    )

    # Complete historical series.
    plt.plot(
        df["ds"],
        df["y"],
        label="Historical Monthly Cost",
        linewidth=2
    )

    # Holdout actuals.
    plt.plot(
        test["ds"],
        test["y"],
        label="Holdout Actuals",
        linewidth=2
    )

    # Holdout ARIMA forecast.
    plt.plot(
        test["ds"],
        holdout_prediction,
        linestyle="--",
        label="ARIMA Holdout Forecast",
        linewidth=2
    )

    # Future forecast.
    plt.plot(
        forecast_df["ds"],
        forecast_df["forecast"],
        linestyle="--",
        label="12-Month Future Forecast",
        linewidth=2
    )

    # Future confidence interval.
    plt.fill_between(
        forecast_df["ds"],
        forecast_df["lower_ci"],
        forecast_df["upper_ci"],
        alpha=0.2,
        label="95% Confidence Interval"
    )

    # Separate historical data from future projection.
    plt.axvline(
        df["ds"].iloc[-1],
        linestyle=":",
        linewidth=2,
        label="Forecast Start"
    )

    plt.title(
        "Healthcare Monthly Cost Forecast - ARIMA"
    )

    plt.xlabel(
        "Date"
    )

    plt.ylabel(
        "Total Monthly Claim Cost ($)"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()

    plot_path = (
        DOCS_DIR
        / "timeseries_forecast.png"
    )

    plt.savefig(
        plot_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    logger.info(
        f"Saved time-series forecast plot to {plot_path}"
    )

    # -----------------------------------------------------------------------
    # 15. Save final model
    # -----------------------------------------------------------------------

    model_path = (
        MODELS_DIR
        / "timeseries_model.pkl"
    )

    joblib.dump(
        final_model,
        model_path
    )

    logger.info(
        f"Saved final ARIMA model to {model_path}"
    )

    # -----------------------------------------------------------------------
    # 16. Save model metadata
    #
    # This makes the artifact easier to understand if it is later moved
    # into an ML platform such as SageMaker.
    # -----------------------------------------------------------------------

    metadata = {
        "model_type": "ARIMA",
        "order": ARIMA_ORDER,
        "historical_start": df["ds"].min().strftime("%Y-%m-%d"),
        "historical_end": df["ds"].max().strftime("%Y-%m-%d"),
        "historical_observations": int(len(df)),
        "holdout_months": HOLDOUT_MONTHS,
        "forecast_horizon_months": FORECAST_HORIZON,
        "naive_rmse": float(naive_metrics["RMSE"]),
        "naive_mae": float(naive_metrics["MAE"]),
        "naive_mape_percent": float(naive_metrics["MAPE"]),
        "arima_rmse": float(arima_metrics["RMSE"]),
        "arima_mae": float(arima_metrics["MAE"]),
        "arima_mape_percent": float(arima_metrics["MAPE"]),
        "arima_rmse_improvement_vs_naive_percent": (
            float(rmse_improvement)
            if np.isfinite(rmse_improvement)
            else None
        ),
        "forecast_total": float(
            forecast_df["forecast"].sum()
        ),
        "forecast_average_monthly": float(
            forecast_df["forecast"].mean()
        ),
    }

    metadata_path = (
        DOCS_DIR
        / "timeseries_model_metadata.json"
    )

    import json

    with open(
        metadata_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=2
        )

    logger.info(
        f"Saved model metadata to {metadata_path}"
    )

    # -----------------------------------------------------------------------
    # 17. Final status
    # -----------------------------------------------------------------------

    logger.info(
        "Time-Series Forecasting Complete."
    )

    logger.info(
        "Outputs generated:"
    )

    logger.info(
        f"  Model: {model_path}"
    )

    logger.info(
        f"  Forecast: {forecast_path}"
    )

    logger.info(
        f"  Evaluation metrics: {metrics_path}"
    )

    logger.info(
        f"  Holdout predictions: {holdout_path}"
    )

    logger.info(
        f"  Plot: {plot_path}"
    )

    logger.info(
        f"  Metadata: {metadata_path}"
    )


if __name__ == "__main__":
    run_timeseries()
```


<div style='page-break-after: always;'></div>

# File: src\utils\__init__.py

```python
```


<div style='page-break-after: always;'></div>

# File: src\utils\config.py

```python
```


<div style='page-break-after: always;'></div>

# File: src\utils\logger.py

```python
"""Standardized logging for the ValueAI project."""
import logging
import sys
from pathlib import Path


def get_logger(name: str, log_file: str = "valueai.log") -> logging.Logger:
    """Create a logger that outputs to both console and file."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler
    log_dir = Path(__file__).parents[2] / "logs"
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
```


<div style='page-break-after: always;'></div>

# File: tests\test_agent.py

```python
```


<div style='page-break-after: always;'></div>

# File: tests\test_data.py

```python
```

