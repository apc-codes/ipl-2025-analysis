# 🏏 IPL 2025 Data Analysis & Visualization

A complete data analysis project on IPL 2025 using Python, focusing on team performance, player statistics, and match strategy insights.

---

## 📌 Overview

This project analyzes IPL 2025 match and ball-by-ball data to extract meaningful insights such as:

- Team performance and win distribution  
- Player rankings (Orange Cap & Purple Cap)  
- Strike rate and economy rate analysis  
- Chasing vs Defending match outcomes  
- Match trends and scoring patterns  

The project also handles **real-world data issues** like missing values, inconsistent column names, and varying dataset formats.

---

## 🛠️ Tech Stack

- **Python**
- **Pandas** – data cleaning & analysis  
- **Matplotlib & Seaborn** – data visualization  

---

## 📁 Dataset Files

The project uses the following CSV files:

- `matches.csv` → match-level data  
- `deliveries.csv` → ball-by-ball data  
- `orange_cap.csv` → top run scorers  
- `purple_cap.csv` → top wicket takers  

---

## ⚙️ Key Features

### ✅ Data Preprocessing
- Handles missing values and inconsistent data
- Dynamically adapts to different column names (e.g., batter/batsman)
- Removes duplicates and cleans datasets

### 📊 Team Analysis
- Total wins per team
- Win percentage calculation
- Team consistency (wins vs losses)

### 🏆 Match Insights
- Correct champion detection using final match winner
- Toss impact analysis
- Accurate chasing vs defending logic using toss decisions

### 🔥 Player Analysis
- Top run scorers (Orange Cap)
- Top wicket takers (Purple Cap)
- Strike rate calculation
- Economy rate calculation

### 📈 Visualizations
- Team wins bar chart
- Run distribution histogram
- Boundary hitters graph
- Strike rate & economy plots
- Chasing vs defending pie chart

---

## 🧠 Key Learnings

- Handling messy real-world datasets  
- Feature engineering from raw cricket data  
- Importance of correct match logic (toss-based decisions)  
- Building end-to-end data analysis pipelines  

---

## 📊 Sample Outputs

### Team Wins Graph
![Wins Graph](Screenshot 2026-04-19 003555.png)

### Strike Rate Analysis
![Orange Cap](Figure_5.png)

### Economy Rate Analysis
![Economy](Figure_6.png)

---

## 🚀 How to Run

1. Clone the repository:
```bash
git clone https://github.com/apc-codes/ipl-analysis.git
cd ipl-analysis
