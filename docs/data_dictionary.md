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