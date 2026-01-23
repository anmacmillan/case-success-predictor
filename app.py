"""
Employment Tribunal Case Success Predictor
4-Factor Weighted Model inspired by Deloitte's macroeconomic risk assessment framework

Factors:
1. Historical Success Rate (baseline by claim type)
2. Limitation/Jurisdictional Issues
3. Legal Basis Strength
4. Evidence Quality

Author: Alex MacMillan
Based on official Employment Tribunal statistics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="ET Case Success Predictor | Alex MacMillan",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Force light mode for consistency */
    .stApp {
        background-color: white;
        color: #262730;
    }

    .main-header {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #262730;
    }
    .disclaimer {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
        color: #856404 !important;
    }
    .disclaimer strong {
        color: #856404 !important;
    }
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        text-align: center;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .factor-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .metric-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin: 0.5rem;
    }
    .strength-high { background: #4caf50; color: white; }
    .strength-moderate { background: #ff9800; color: white; }
    .strength-low { background: #f44336; color: white; }
</style>
""", unsafe_allow_html=True)

# Historical success rates from ET statistics 2020-21
HISTORICAL_RATES = {
    'Unfair Dismissal': 50.00,
    'Breach of Contract': 66.18,
    'Unlawful Deduction from Wages': 67.31,
    'Disability Discrimination': 26.04,
    'Equal Pay': 46.45,
    'National Minimum Wage': 54.91,
    'Race Discrimination': 28.41,
    'Redundancy Pay': 51.95,
    'Religion/Belief Discrimination': 55.17,
    'Sex Discrimination': 31.43,
    'Sexual Orientation Discrimination': 46.96,
    'Age Discrimination': 19.55,
    'Protected Disclosure (Whistleblowing)': 44.69,
    'Working Time': 50.88,
    'Other Claims': 56.49
}

# Header
st.markdown('<div class="main-header">📊 Employment Tribunal Case Success Predictor</div>', unsafe_allow_html=True)
st.markdown("**4-Factor Weighted Model | Calibrated with Official ET Statistics**")

# Disclaimer
st.markdown("""
<div class="disclaimer">
    <strong>⚠️ Important Notice</strong><br>
    This tool provides <strong>indicative probability estimates</strong> based on historical data and case factors.
    It is <strong>not legal advice</strong> and should not replace proper legal analysis by a qualified barrister or solicitor.
    Success depends on many case-specific factors not captured by this model.
    <br><br>
    <strong>Methodology:</strong> 4-factor weighted model inspired by Deloitte's macroeconomic risk assessment framework,
    calibrated with Employment Tribunal statistics 2020-21.
</div>
""", unsafe_allow_html=True)

# Sidebar - Model explanation
st.sidebar.title("About This Model")
st.sidebar.markdown("""
### 4-Factor Framework

**1. Historical Success Rate (H)**
Baseline probability from ET statistics by claim type

**2. Limitation Issues (L)**
Time bars, jurisdictional problems, procedural defects

**3. Legal Basis Strength (B)**
Quality of legal arguments, precedent, statutory interpretation

**4. Evidence Quality (E)**
Witness credibility, documentation, burden of proof

### Calculation

Each factor receives:
- **Score** (0-100): Your assessment
- **Weight** (0-100): Importance to this case

Final probability combines weighted factors with historical baseline.

### Inspiration

Adapted from **Deloitte's macroeconomic risk modeling** methodology,
applying multi-factor weighted analysis to legal case assessment.

---

**Created by:**
[Alex MacMillan](https://alexmacmillan.co.uk)
Employment Law Barrister
St Philips Chambers
""")

# Main interface
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## Case Details")

    # Claim type selection
    claim_type = st.selectbox(
        "Primary Claim Type",
        options=sorted(HISTORICAL_RATES.keys()),
        help="Select the primary cause of action. Historical success rate will be used as baseline."
    )

    historical_rate = HISTORICAL_RATES[claim_type]

    st.info(f"📈 Historical success rate for **{claim_type}**: **{historical_rate:.1f}%**  \n"
            f"*Based on Employment Tribunal statistics 2020-21*")

    st.markdown("---")
    st.markdown("## Factor Assessment")
    st.markdown("*Rate each factor on a 0-100 scale and assign its importance weight*")

    # Factor 1: Historical (read-only, just show weight)
    st.markdown("### 1️⃣ Historical Success Rate")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.metric("Baseline Rate", f"{historical_rate:.1f}%")
    with col_h2:
        weight_H = st.slider(
            "Weight",
            0, 100, 10,
            key="weight_h",
            help="How much should historical rates influence prediction? Lower if case is unusual."
        )

    st.markdown("---")

    # Factor 2: Limitation Issues
    st.markdown("### 2️⃣ Limitation / Jurisdictional Issues")
    st.caption("Time bars, early conciliation, continuous employment, etc.")

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        score_L = st.slider(
            "Strength Score",
            0, 100, 80,
            key="score_l",
            help="100 = No limitation issues. 0 = Clear time bar or jurisdictional defect."
        )
    with col_l2:
        weight_L = st.slider(
            "Weight",
            0, 100, 30,
            key="weight_l",
            help="Importance of limitation issues in this case"
        )

    limitation_status = "Strong" if score_L >= 70 else "Moderate" if score_L >= 40 else "Weak"
    st.progress(score_L / 100)
    st.caption(f"Status: {limitation_status} ({score_L}/100)")

    st.markdown("---")

    # Factor 3: Legal Basis
    st.markdown("### 3️⃣ Legal Basis Strength")
    st.caption("Quality of legal arguments, precedent support, statutory interpretation")

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        score_B = st.slider(
            "Strength Score",
            0, 100, 70,
            key="score_b",
            help="100 = Strong precedent, clear statute. 0 = Weak legal basis, adverse authority."
        )
    with col_b2:
        weight_B = st.slider(
            "Weight",
            0, 100, 30,
            key="weight_b",
            help="Importance of legal arguments in this case"
        )

    legal_status = "Strong" if score_B >= 70 else "Moderate" if score_B >= 40 else "Weak"
    st.progress(score_B / 100)
    st.caption(f"Status: {legal_status} ({score_B}/100)")

    st.markdown("---")

    # Factor 4: Evidence
    st.markdown("### 4️⃣ Evidence Quality")
    st.caption("Witness credibility, documentation, contemporaneous records, burden of proof")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        score_E = st.slider(
            "Strength Score",
            0, 100, 60,
            key="score_e",
            help="100 = Strong documentary evidence, credible witnesses. 0 = No evidence, incredible witnesses."
        )
    with col_e2:
        weight_E = st.slider(
            "Weight",
            0, 100, 30,
            key="weight_e",
            help="Importance of evidence in this case"
        )

    evidence_status = "Strong" if score_E >= 70 else "Moderate" if score_E >= 40 else "Weak"
    st.progress(score_E / 100)
    st.caption(f"Status: {evidence_status} ({score_E}/100)")

with col2:
    st.markdown("## Prediction")

    # Calculate weighted success probability
    total_weight = weight_H + weight_L + weight_B + weight_E

    if total_weight == 0:
        st.error("Please assign at least some weight to factors")
        success_prob = historical_rate
    else:
        # Normalize weights
        w_h = weight_H / total_weight
        w_l = weight_L / total_weight
        w_b = weight_B / total_weight
        w_e = weight_E / total_weight

        # Calculate weighted probability
        # Historical rate is the baseline
        # Other factors adjust from this baseline
        baseline_adjustment = (
            w_l * (score_L - 50) / 100 +  # Limitation adjustment
            w_b * (score_B - 50) / 100 +  # Legal basis adjustment
            w_e * (score_E - 50) / 100    # Evidence adjustment
        )

        # Combine historical rate with adjustments
        success_prob = historical_rate + (baseline_adjustment * 100)

        # Bound between 0 and 100
        success_prob = max(0, min(100, success_prob))

    # Display result
    st.markdown(f"""
    <div class="result-box">
        <h2 style="margin:0; font-size: 3rem;">{success_prob:.1f}%</h2>
        <p style="margin:0.5rem 0 0 0; font-size: 1.2rem;">Predicted Success Probability</p>
    </div>
    """, unsafe_allow_html=True)

    # Strength assessment
    if success_prob >= 70:
        strength = "Strong"
        strength_class = "strength-high"
        assessment = "Case has strong prospects. Reasonable chance of success at trial."
    elif success_prob >= 40:
        strength = "Moderate"
        strength_class = "strength-moderate"
        assessment = "Case has moderate prospects. Consider settlement alongside litigation."
    else:
        strength = "Weak"
        strength_class = "strength-low"
        assessment = "Case has weak prospects. Significant litigation risk to consider."

    st.markdown(f'<span class="metric-badge {strength_class}">{strength} Case</span>', unsafe_allow_html=True)
    st.caption(assessment)

    st.markdown("---")

    # Factor breakdown
    st.markdown("### Factor Contributions")

    if total_weight > 0:
        factor_data = {
            'Factor': ['Historical', 'Limitation', 'Legal Basis', 'Evidence'],
            'Weight': [w_h * 100, w_l * 100, w_b * 100, w_e * 100],
            'Score': [historical_rate, score_L, score_B, score_E]
        }

        df_factors = pd.DataFrame(factor_data)

        # Weight distribution pie chart
        fig_weights = go.Figure(data=[go.Pie(
            labels=df_factors['Factor'],
            values=df_factors['Weight'],
            hole=0.4,
            marker_colors=['#667eea', '#f093fb', '#4facfe', '#43e97b']
        )])
        fig_weights.update_layout(
            title="Weight Distribution",
            height=300,
            showlegend=True,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_weights, use_container_width=True)

        # Factor scores
        st.markdown("#### Factor Scores")
        for idx, row in df_factors.iterrows():
            st.metric(
                row['Factor'],
                f"{row['Score']:.0f}/100",
                f"{row['Weight']:.0f}% weight"
            )

# Detailed breakdown section
st.markdown("---")
st.markdown("## 📊 Detailed Analysis")

tab1, tab2, tab3 = st.tabs(["Factor Breakdown", "Historical Data", "Methodology"])

with tab1:
    st.markdown("### Factor-by-Factor Analysis")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### Scores")
        fig_scores = go.Figure(data=[
            go.Bar(
                x=['Historical', 'Limitation', 'Legal Basis', 'Evidence'],
                y=[historical_rate, score_L, score_B, score_E],
                marker_color=['#667eea', '#f093fb', '#4facfe', '#43e97b'],
                text=[f"{historical_rate:.0f}", f"{score_L:.0f}", f"{score_B:.0f}", f"{score_E:.0f}"],
                textposition='auto',
            )
        ])
        fig_scores.update_layout(
            title="Factor Scores",
            yaxis_title="Score (0-100)",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_scores, use_container_width=True)

    with col_b:
        st.markdown("#### Weights")
        fig_weights_bar = go.Figure(data=[
            go.Bar(
                x=['Historical', 'Limitation', 'Legal Basis', 'Evidence'],
                y=[weight_H, weight_L, weight_B, weight_E],
                marker_color=['#667eea', '#f093fb', '#4facfe', '#43e97b'],
                text=[f"{weight_H:.0f}", f"{weight_L:.0f}", f"{weight_B:.0f}", f"{weight_E:.0f}"],
                textposition='auto',
            )
        ])
        fig_weights_bar.update_layout(
            title="Factor Weights",
            yaxis_title="Weight (0-100)",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_weights_bar, use_container_width=True)

    st.markdown("### Interpretation")
    st.markdown(f"""
    **Historical Baseline:** {historical_rate:.1f}% (typical success rate for {claim_type})

    **Factor Adjustments:**
    - **Limitation Issues:** {'+' if score_L > 50 else ''}{((score_L - 50) * w_l):.1f} percentage points
    - **Legal Basis:** {'+' if score_B > 50 else ''}{((score_B - 50) * w_b):.1f} percentage points
    - **Evidence Quality:** {'+' if score_E > 50 else ''}{((score_E - 50) * w_e):.1f} percentage points

    **Final Prediction:** {success_prob:.1f}%
    """)

with tab2:
    st.markdown("### Employment Tribunal Historical Success Rates")
    st.caption("Source: Employment Tribunal and EAT Statistics 2020-21")

    # Create sorted dataframe
    df_historical = pd.DataFrame(list(HISTORICAL_RATES.items()), columns=['Claim Type', 'Success Rate'])
    df_historical = df_historical.sort_values('Success Rate', ascending=False)

    # Highlight selected claim type
    def highlight_selected(row):
        if row['Claim Type'] == claim_type:
            return ['background-color: #fff3cd; font-weight: bold'] * len(row)
        return [''] * len(row)

    st.dataframe(
        df_historical.style.apply(highlight_selected, axis=1).format({'Success Rate': '{:.1f}%'}),
        use_container_width=True,
        height=400
    )

    # Bar chart
    fig_historical = px.bar(
        df_historical,
        x='Success Rate',
        y='Claim Type',
        orientation='h',
        color='Success Rate',
        color_continuous_scale='RdYlGn',
        title='Historical Success Rates by Claim Type'
    )
    fig_historical.update_layout(height=600)
    st.plotly_chart(fig_historical, use_container_width=True)

    st.markdown("""
    **Key Observations:**
    - **Highest success:** Unlawful deduction from wages (67.3%), Breach of contract (66.2%)
    - **Lowest success:** Age discrimination (19.6%), Disability discrimination (26.0%)
    - **Average:** Approximately 45% across all claim types

    **Note:** These are aggregate statistics. Individual case outcomes depend heavily on specific circumstances.
    """)

with tab3:
    st.markdown("### Methodology")

    st.markdown("""
    #### 4-Factor Weighted Model

    This tool uses a weighted scoring model inspired by **Deloitte's macroeconomic risk assessment framework**,
    adapted for legal case prediction.

    **Mathematical Approach:**

    1. **Baseline:** Historical success rate for claim type (H)
    2. **Adjustments:** Weighted factors (L, B, E) adjust from baseline
    3. **Combination:** `P(success) = H + Σ(weight_i × adjustment_i)`

    **Factor Scoring:**
    - Each factor scored 0-100
    - 50 = neutral (no adjustment)
    - >50 = positive adjustment
    - <50 = negative adjustment

    **Weight Assignment:**
    - User assigns importance weights (0-100)
    - Weights normalized to sum to 1
    - Allows case-specific factor prioritization

    **Calibration:**
    - Historical rates from official Employment Tribunal statistics 2020-21
    - Covers 15 major claim types
    - Based on actual tribunal outcomes

    #### Limitations

    ⚠️ **This model does not account for:**
    - Settlement likelihood
    - Costs risks
    - Tribunal composition
    - Regional variations
    - Case-specific facts beyond the 4 factors
    - Respondent's resources/litigation approach
    - Appeal prospects

    #### Inspiration: Deloitte Framework

    Deloitte's [Global Economic Outlook](https://www.deloitte.com/us/en/insights/topics/economy/global-economic-outlook-2024.html)
    uses multi-factor weighted models to predict complex outcomes. This tool applies similar methodology to legal case assessment.

    **Key Adaptation:**
    - Economic factors → Legal case factors
    - GDP/inflation predictions → Case success predictions
    - Macroeconomic indicators → Case strength indicators
    """)

    st.markdown("---")
    st.markdown("""
    **Academic Basis:**
    - Multi-factor risk modeling
    - Weighted linear combination
    - Empirical calibration with historical data
    - Bayesian updating from baseline priors
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <strong>Employment Tribunal Case Success Predictor</strong> |
    <a href="https://alexmacmillan.co.uk" target="_blank">Alex MacMillan</a> |
    Employment Law Barrister | St Philips Chambers<br>
    Methodology inspired by Deloitte's economic risk modeling framework<br>
    Calibrated with official Employment Tribunal statistics 2020-21<br>
    <em>For educational purposes only - not legal advice</em>
</div>
""", unsafe_allow_html=True)
