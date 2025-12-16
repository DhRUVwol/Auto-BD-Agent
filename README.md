# Auto-BD: Lead Generation & Scoring Agent

A Streamlit-based prototype that identifies, enriches, and ranks B2B leads for 3D In-Vitro Models based on "Propensity to Buy."

## Project Overview
This tool automates the sales research process by:
* **Identifying** leads based on specific buyer personas (e.g., Toxicologists).
* **Enriching** data with location and publication history.
* **Ranking** leads using a weighted scoring engine (0-100).

## The Scoring Logic
Implemented exactly per the assignment requirements:
* **+40 Scientific Intent:** Recent papers on "Drug-Induced Liver Injury".
* **+30 Role Fit:** Titles containing "Toxicology", "Safety", etc.
* **+20 Company Intent:** Series A/B funding.
* **+10 Location:** Key Biotech Hubs (Boston, Cambridge, etc.).

## Technical Implementation
* **Stack:** Python, Streamlit, Pandas.
* **Data Source:** For this prototype, I implemented a **Mock Data Generator** to ensure a stable, reproducible demo without hitting LinkedIn anti-bot measures. The architecture is designed to swap this generator with a real scraping module (e.g., Proxycurl or Selenium) for production.

## How to Run
1. Clone the repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
