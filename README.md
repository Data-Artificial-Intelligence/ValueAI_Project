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