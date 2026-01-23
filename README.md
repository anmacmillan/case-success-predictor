# Employment Tribunal Case Success Predictor

Interactive 4-factor weighted model for predicting employment tribunal case success probability.

## Features

- **Historical Success Rates**: Calibrated with official ET statistics 2020-21
- **4-Factor Assessment**:
  1. **Historical Baseline** - Success rate by claim type
  2. **Limitation Issues** - Time bars, jurisdiction
  3. **Legal Basis** - Quality of legal arguments
  4. **Evidence Quality** - Documentary and witness evidence
- **Flexible Weighting**: Adjust factor importance per case
- **Interactive Visualizations**: Charts and breakdowns
- **Detailed Analysis**: Factor contributions and interpretations

## Methodology

Inspired by **Deloitte's macroeconomic risk assessment framework**, this tool applies multi-factor weighted modeling to legal case prediction.

**Calculation:**
```
P(success) = Historical_Rate + Σ(weight_i × (score_i - 50) / 100)
```

Where:
- Historical_Rate: Baseline from ET statistics
- weight_i: Normalized importance weight (0-1)
- score_i: Factor assessment (0-100, 50=neutral)

## Data Source

Employment Tribunal and Employment Appeal Tribunal Statistics 2020-21
- Covers 15 major claim types
- Based on actual tribunal outcomes
- Success rates range from 19.55% (age discrimination) to 67.31% (unlawful deductions)

## About

Created by [Alex MacMillan](https://alexmacmillan.co.uk), Employment Law Barrister at St Philips Chambers.

**Disclaimer:** This is an educational tool providing indicative estimates only. Not legal advice.

## Usage

Visit the deployed app at: https://case-success-predictor.streamlit.app

Or run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Claim Types Supported

- Unfair Dismissal
- Breach of Contract
- Unlawful Deduction from Wages
- Disability Discrimination
- Equal Pay
- Race Discrimination
- Sex Discrimination
- Age Discrimination
- Protected Disclosure (Whistleblowing)
- And 6 more...

## License

Copyright © 2025 Alex MacMillan. Educational use only.
