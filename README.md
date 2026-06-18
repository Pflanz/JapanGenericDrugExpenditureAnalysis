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

* Annual expenditure shares of generic and brand-name drugs
* Trends by therapeutic category
* Trends by healthcare setting
* Trends by dosage form
* Trends by geographic region

### Regional Analysis

* Comparison among prefectures
* Regional summaries across Japan
* Prefecture-level tables

### Spatial Analysis

* Choropleth maps
* Global Moran's I
* Local Indicators of Spatial Association (LISA)
* Spatial cluster identification

### Interactive Filtering

Analyses can be customized by:

* Fiscal year
* Prefecture
* Geographic region
* Therapeutic category
* Healthcare setting
* Dosage form

---

## Dashboard Pages

### Trend Analysis

Explore temporal changes in generic expenditure shares and compare patterns across therapeutic categories, healthcare settings, dosage forms, and geographic regions.

Outputs:

* Line charts
* Summary tables

### Regional Analysis

Evaluate regional variation in generic expenditure shares among prefectures and major regions of Japan.

Outputs:

* Regional trend plots
* Prefecture-level summary tables

### Spatial Analysis

Investigate spatial patterns of generic drug expenditure.

Outputs:

* Choropleth maps
* Global Moran's I statistics
* LISA cluster maps

Spatial clusters are classified following the GeoDa convention:

* High–High
* Low–Low
* Low–High
* High–Low
* Island (excluded)

### Dataset Explorer

Inspect database structure and randomly sampled records.

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

| File             | Description                      |
| ---------------- | -------------------------------- |
| dashboard.py     | Streamlit dashboard              |
| sample_data.csv  | Sample dataset for demonstration |
| jp.json          | Prefecture boundary file         |
| requirements.txt | Python dependencies              |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Pflanz/JapanGenericDrugExpenditureAnalysis.git
cd JapanGenericDrugExpenditureAnalysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard.py
```

---

## Example Research Applications

This framework can be used to:

* Monitor generic drug policy outcomes
* Compare generic utilization across therapeutic categories
* Evaluate regional disparities in pharmaceutical expenditure
* Investigate spatial clustering of healthcare utilization patterns
* Support pharmacoepidemiological and health services research

---

## Data Availability

The complete analytical dataset (2015–2023) is archived in Zenodo.

DOI: 10.5281/zenodo.20657214

A sample dataset containing 1,000 randomly selected records is provided in this repository for demonstration and testing purposes.

---

## Citation

If you use this code or analytical framework, please cite:

Fan D. Generic Drug Expenditure Analysis in Japan. GitHub repository.

---

## Acknowledgements

This work is based on publicly available NDB Open Data released by the Ministry of Health, Labour and Welfare of Japan.

The interpretations and conclusions presented in this repository are solely those of the author and do not represent the official views of the Ministry of Health, Labour and Welfare.

---

## License

MIT License
