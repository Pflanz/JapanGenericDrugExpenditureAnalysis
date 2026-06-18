# Generic Drug Expenditure Analysis in Japan

## Overview

This repository provides an analytical framework for evaluating generic drug utilization and expenditure patterns in Japan using the National Database of Health Insurance Claims and Specific Health Checkups of Japan (NDB) Open Data.

The project integrates longitudinal, regional, and spatial analyses to explore temporal trends and geographic variation in generic drug expenditure shares across multiple therapeutic categories.

An interactive Streamlit dashboard is included to facilitate exploratory analysis and visualization.

---

## Data Source

The analysis is based on publicly available NDB Open Data released by the Ministry of Health, Labour and Welfare (MHLW), Japan.

Data include:

* Fiscal years: 2015–2023
* Top 100 drugs by annual volume for each fiscal year
* Drug expenditure information
* Generic and brand-name classifications
* Prefecture-level aggregation
* Healthcare setting information
* Dosage form information

Original NDB Open Data can be obtained from:

https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177182.html

---

## Features

### Time Trend Analysis

* Annual expenditure shares of brand-name and generic drugs
* Temporal trends by:

  * Therapeutic category
  * Healthcare setting
  * Dosage form
  * Geographic region

### Regional Analysis

* Comparison of generic expenditure shares among prefectures
* Regional summaries across Japan

### Spatial Analysis

* Choropleth maps of generic expenditure shares
* Global Moran's I
* Local Indicators of Spatial Association (LISA)
* Identification of spatial clusters

---

## Project Structure

```text
.
├── dashboard.py
├── sample_data.csv
├── jp.json
├── requirements.txt
├── LICENSE
└── README.md
```

### Main Files

| File                          | Description                  |
| ----------------------------- | ---------------------------- |
| dashboard.py                  | Streamlit dashboard          | 
| sample_data.csv               | Sample of analytical dataset |
| jp.json                       | Prefecture boundary file     |
| requirements.txt              | Python dependencies          |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Pflanz/JapanGenericDrugExpenditureAnalysis.git
cd japan-generic-drug-analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run analyze7_en.py
```

---

## Methodology

### Generic Expenditure Share

Generic expenditure share was calculated as:

Generic Share=Generic Drug Expenditure/Total Drug Expenditure

### Global Spatial Autocorrelation

Spatial clustering was evaluated using Moran's I.

Reference:

Moran PA. Notes on Continuous Stochastic Phenomena. Biometrika. 1950.

### Local Spatial Autocorrelation

Local clustering was assessed using Local Indicators of Spatial Association (LISA).

Reference:

Anselin L. Local Indicators of Spatial Association—LISA. Geographical Analysis. 1995.

---

## Example Research Applications

This framework can be used to:

* Monitor generic drug policy outcomes
* Compare generic utilization across therapeutic categories
* Evaluate regional disparities in pharmaceutical expenditure
* Investigate spatial clustering of healthcare utilization patterns

---

## Limitations

* NDB Open Data does not include all drugs by annual volume for each fiscal year.
* Drug composition varies across fiscal years.
* Analyses are based on aggregated administrative data rather than patient-level records.
* Expenditure-based indicators were used; utilization measures such as DDDs were not included.

---

## Citation

If you use this code or analytical framework, please cite:

Author(s). Generic Drug Expenditure Analysis in Japan. GitHub repository.

---

## Related Manuscript

A manuscript based on this analytical framework is currently under review.

---

## License

MIT License
