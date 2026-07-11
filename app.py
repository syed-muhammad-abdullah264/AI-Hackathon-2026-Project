import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import os
import re
from datetime import datetime
import base64

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="AI Data Analysis Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- CUSTOM CSS --------------------
def load_css():
    st.markdown("""
    <style>
        /* ---------- GLOBAL ---------- */
        .stApp {
            background: radial-gradient(circle at top left, rgba(108,140,255,0.14), transparent 28%), radial-gradient(circle at bottom right, rgba(167,139,250,0.12), transparent 24%), #0b0e17;
            font-family: 'Inter', sans-serif;
        }
        .main > div {
            padding: 0 1rem;
        }
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2.2rem;
            max-width: 1400px;
        }
        /* Cards */
        .css-1r6slb0, .css-1v3fvcr, .css-1d391kg {
            background: rgba(19, 26, 43, 0.74) !important;
            backdrop-filter: blur(14px);
            border: 1px solid rgba(42, 58, 92, 0.38);
            border-radius: 20px;
            box-shadow: 0 18px 40px -16px rgba(0,0,0,0.65);
        }
        /* Buttons */
        .stButton button {
            background: linear-gradient(135deg, #6c8cff, #a78bfa);
            color: white;
            border: none;
            border-radius: 14px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 6px 20px rgba(108,140,255,0.3);
        }
        .stButton button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 10px 30px rgba(108,140,255,0.5);
        }
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(19, 26, 43, 0.82);
            border-radius: 16px;
            padding: 6px;
            border: 1px solid rgba(42,58,92,0.4);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 12px;
            padding: 10px 24px;
            font-weight: 600;
            color: #8899bb;
            transition: 0.3s;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #6c8cff, #a78bfa);
            color: white;
            box-shadow: 0 6px 24px rgba(108,140,255,0.3);
        }
        /* Headers */
        h1, h2, h3 {
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        .glow-text {
            background: linear-gradient(135deg, #6c8cff, #a78bfa, #ff7eb3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        /* Metrics */
        .metric-card {
            background: rgba(19,26,43,0.6);
            border-radius: 16px;
            padding: 16px 20px;
            border: 1px solid rgba(42,58,92,0.3);
            transition: 0.3s;
        }
        .metric-card {
            animation: cardFadeIn 0.6s ease both;
        }
        .metric-card:hover {
            border-color: #6c8cff;
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.4);
        }
        .analysis-panel {
            background: rgba(19,26,43,0.66);
            border: 1px solid rgba(42,58,92,0.36);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            margin-top: 0.85rem;
            box-shadow: 0 12px 30px rgba(0,0,0,0.2);
            animation: panelSlideIn 0.55s ease both;
        }
        .panel-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #f2f6ff;
            margin-bottom: 0.55rem;
        }
        .panel-subtitle {
            color: #8ea0c7;
            font-size: 0.92rem;
            margin-bottom: 0.8rem;
        }
        .info-pill {
            display: inline-block;
            padding: 0.35rem 0.6rem;
            margin-right: 0.4rem;
            margin-bottom: 0.4rem;
            border-radius: 999px;
            background: rgba(108,140,255,0.12);
            color: #d8e3ff;
            font-size: 0.8rem;
            border: 1px solid rgba(108,140,255,0.2);
        }
        .insight-card {
            background: linear-gradient(135deg, rgba(108,140,255,0.12), rgba(167,139,250,0.1));
            border: 1px solid rgba(108,140,255,0.22);
            border-radius: 16px;
            padding: 1rem;
            height: 100%;
        }
        .insight-title {
            font-size: 0.9rem;
            color: #aebbd7;
            margin-bottom: 0.35rem;
            font-weight: 600;
        }
        .insight-value {
            font-size: 1.15rem;
            font-weight: 700;
            color: #f5f8ff;
            margin-bottom: 0.25rem;
        }
        .insight-desc {
            font-size: 0.85rem;
            color: #8fa2c9;
        }
        .health-score {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6c8cff, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        .health-bar {
            height: 8px;
            background: rgba(255,255,255,0.08);
            border-radius: 999px;
            overflow: hidden;
            margin-top: 0.55rem;
        }
        .health-bar > div {
            height: 100%;
            border-radius: inherit;
            background: linear-gradient(90deg, #6c8cff, #a78bfa);
        }
        .recommendation-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(108,140,255,0.18);
            border-radius: 14px;
            padding: 0.8rem 0.9rem;
            margin-bottom: 0.6rem;
        }
        .recommendation-icon {
            color: #8fb8ff;
            font-weight: 700;
            margin-right: 0.35rem;
        }
        .story-card {
            background: linear-gradient(135deg, rgba(108,140,255,0.14), rgba(167,139,250,0.1));
            border: 1px solid rgba(108,140,255,0.22);
            border-radius: 16px;
            padding: 1rem 1.1rem;
            margin-bottom: 0.8rem;
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }
        .story-text {
            color: #e9f0ff;
            line-height: 1.6;
            font-size: 0.95rem;
        }
        .section-hero {
            background: linear-gradient(135deg, rgba(108,140,255,0.16), rgba(167,139,250,0.11));
            border: 1px solid rgba(108,140,255,0.24);
            border-radius: 16px;
            padding: 0.8rem 0.95rem;
            margin-bottom: 0.7rem;
        }
        .section-hero-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: #f4f7ff;
        }
        .section-hero-subtitle {
            font-size: 0.82rem;
            color: #9fb0d7;
            margin-top: 0.2rem;
        }
        .qa-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(108,140,255,0.16);
            border-radius: 14px;
            padding: 0.8rem 0.9rem;
            margin-bottom: 0.7rem;
        }
        .prompt-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 0.4rem 0 0.8rem;
        }
        .prompt-chip {
            display: inline-block;
            padding: 0.38rem 0.62rem;
            border-radius: 999px;
            background: rgba(108,140,255,0.12);
            border: 1px solid rgba(108,140,255,0.18);
            color: #dce8ff;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .tip-card {
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(108,140,255,0.16);
            border-radius: 14px;
            padding: 0.8rem 0.9rem;
            margin-top: 0.7rem;
            color: #dce8ff;
        }
        .empty-state-card {
            background: linear-gradient(135deg, rgba(108,140,255,0.12), rgba(167,139,250,0.08));
            border: 1px solid rgba(108,140,255,0.24);
            border-radius: 20px;
            padding: 1.2rem 1.3rem;
            margin-top: 0.8rem;
            box-shadow: 0 12px 30px rgba(0,0,0,0.16);
        }
        .step-badge {
            display: inline-block;
            margin: 0.3rem 0.35rem 0.3rem 0;
            padding: 0.34rem 0.6rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.1);
            color: #dce8ff;
            font-size: 0.8rem;
            font-weight: 600;
        }
        .chart-shell {
            background: linear-gradient(135deg, rgba(108,140,255,0.08), rgba(167,139,250,0.06));
            border: 1px solid rgba(108,140,255,0.18);
            border-radius: 18px;
            padding: 0.85rem;
            margin-top: 0.5rem;
        }
        .metric-value {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #6c8cff, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        /* Upload zone */
        .upload-zone {
            border: 2px dashed rgba(108,140,255,0.4);
            border-radius: 20px;
            padding: 3rem 1rem;
            text-align: center;
            background: rgba(19,26,43,0.4);
            transition: 0.3s;
            cursor: pointer;
        }
        .upload-zone:hover {
            border-color: #6c8cff;
            background: rgba(108,140,255,0.05);
            transform: scale(1.01);
        }
        /* Answer boxes */
        .answer-box {
            background: rgba(108,140,255,0.06);
            border-left: 4px solid #6c8cff;
            border-radius: 12px;
            padding: 16px 20px;
            margin: 10px 0;
            animation: fadeIn 0.6s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes floatGlow {
            0%, 100% { transform: translateY(0px) scale(1); opacity: 0.7; }
            50% { transform: translateY(-16px) scale(1.08); opacity: 1; }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(108,140,255,0.12); }
            50% { transform: scale(1.02); box-shadow: 0 0 0 6px rgba(108,140,255,0.02); }
        }
        @keyframes cardFadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes panelSlideIn {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes heroRise {
            from { opacity: 0; transform: translateY(-8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        /* Dark/Light toggle (manual) */
        .theme-toggle {
            display: flex;
            align-items: center;
            gap: 8px;
            background: rgba(19,26,43,0.8);
            padding: 6px 14px 6px 10px;
            border-radius: 100px;
            border: 1px solid rgba(42,58,92,0.4);
            cursor: pointer;
            transition: 0.3s;
        }
        .theme-toggle:hover {
            border-color: #6c8cff;
        }
        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0b0e17; }
        ::-webkit-scrollbar-thumb { background: #6c8cff; border-radius: 10px; }
        /* Chart container */
        .chart-box {
            background: rgba(19,26,43,0.64);
            border-radius: 18px;
            padding: 16px;
            border: 1px solid rgba(42,58,92,0.32);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04), 0 10px 24px rgba(0,0,0,0.16);
        }
        /* Widget polish */
        [data-testid="stFileUploader"] > div {
            background: rgba(19,26,43,0.65);
            border: 1px solid rgba(108,140,255,0.25);
            border-radius: 16px;
            padding: 0.35rem;
        }
        .stTextInput > div > div > input,
        .stSelectbox > div > div > div {
            background: rgba(19,26,43,0.7);
            border: 1px solid rgba(42,58,92,0.45);
            border-radius: 12px;
            color: #f5f7ff;
        }
        .stDataFrame, .stTable {
            border-radius: 14px;
            overflow: hidden;
        }
        /* Hero / action cards */
        .hero-card {
            background: linear-gradient(135deg, rgba(108,140,255,0.18), rgba(167,139,250,0.16));
            border: 1px solid rgba(108,140,255,0.35);
            border-radius: 24px;
            padding: 1.4rem 1.6rem;
            margin-bottom: 1rem;
            box-shadow: 0 18px 35px rgba(0,0,0,0.25);
            position: relative;
            overflow: hidden;
            animation: heroRise 0.7s ease both;
        }
        .hero-card::before {
            content: "";
            position: absolute;
            inset: -30% 60% auto auto;
            width: 220px;
            height: 220px;
            background: radial-gradient(circle, rgba(255,255,255,0.16), transparent 70%);
            animation: floatGlow 6s ease-in-out infinite;
            pointer-events: none;
        }
        .hero-badge {
            display: inline-block;
            padding: 6px 12px;
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 999px;
            color: #c8d4ff;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 0.7rem;
        }
        .hero-title {
            font-size: 2rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }
        .hero-subtitle {
            color: #aab7d1;
            font-size: 1rem;
        }
        .action-card {
            background: rgba(19,26,43,0.72);
            border: 1px solid rgba(42,58,92,0.45);
            border-radius: 18px;
            padding: 1rem 1.2rem;
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
        }
        .action-card::after {
            content: "";
            position: absolute;
            inset: auto auto -20px -20px;
            width: 90px;
            height: 90px;
            background: radial-gradient(circle, rgba(108,140,255,0.22), transparent 70%);
            pointer-events: none;
        }
        .section-title {
            font-size: 1rem;
            font-weight: 700;
            color: #f2f6ff;
            margin-bottom: 0.2rem;
        }
        .section-subtitle {
            color: #8ea0c7;
            font-size: 0.95rem;
        }
        .upload-card {
            background: rgba(19,26,43,0.6);
            border: 1px solid rgba(42,58,92,0.35);
            border-radius: 22px;
            padding: 1rem 1rem 0.8rem;
            margin-bottom: 1rem;
            box-shadow: 0 16px 38px rgba(0,0,0,0.2);
            animation: cardFadeIn 0.7s ease both;
        }
        .pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.6rem;
            margin: 0.8rem 0 1rem;
        }
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.42rem 0.7rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.09);
            color: #dce7ff;
            font-size: 0.84rem;
            font-weight: 600;
            transition: transform 0.25s ease, border-color 0.25s ease;
        }
        .pill:hover {
            transform: translateY(-2px);
            border-color: rgba(108,140,255,0.45);
        }
        .status-ribbon {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 0.6rem;
            padding: 0.4rem 0.7rem;
            border-radius: 999px;
            background: rgba(108,140,255,0.12);
            border: 1px solid rgba(108,140,255,0.22);
            color: #dbe8ff;
            font-size: 0.8rem;
            font-weight: 700;
            animation: pulse 2.2s ease-in-out infinite;
        }
        .stDownloadButton button {
            background: linear-gradient(135deg, #6c8cff, #a78bfa);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 600;
        }
        /* Responsive */
        @media (max-width: 600px) {
            .metric-value { font-size: 1.6rem; }
            .hero-title { font-size: 1.6rem; }
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# -------------------- SESSION STATE --------------------
if 'df' not in st.session_state:
    st.session_state.df = None
if 'loaded' not in st.session_state:
    st.session_state.loaded = False
if 'qa_answers' not in st.session_state:
    st.session_state.qa_answers = {}
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = 'Bar Chart'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# -------------------- SAMPLE DATA GENERATOR --------------------
def generate_sample_data():
    np.random.seed(42)
    categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Toys']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    data = {
        'Product': [f'Product {i}' for i in range(1, 101)],
        'Category': np.random.choice(categories, 100),
        'Sales': np.random.randint(200, 2000, 100),
        'Quantity': np.random.randint(1, 50, 100),
        'City': np.random.choice(cities, 100),
        'Customer_Age': np.random.randint(18, 70, 100)
    }
    return pd.DataFrame(data)

# -------------------- DATA LOADING --------------------
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return None
    else:
        # Use sample data if no file
        if st.session_state.df is None:
            st.session_state.df = generate_sample_data()
        return st.session_state.df

# -------------------- STATISTICS --------------------
def get_stats(df):
    stats = {
        'Rows': df.shape[0],
        'Columns': df.shape[1],
        'Missing': df.isnull().sum().sum(),
        'Numerical': len(df.select_dtypes(include=np.number).columns),
        'Categorical': len(df.select_dtypes(include='object').columns)
    }
    return stats

def get_numeric_summary(df):
    num_cols = df.select_dtypes(include=np.number).columns
    if len(num_cols) == 0:
        return pd.DataFrame()
    return df[num_cols].describe().T

def get_smart_insights(df):
    insights = []

    if 'Category' in df.columns:
        top_category = df['Category'].value_counts().idxmax()
        top_category_count = df['Category'].value_counts().max()
        insights.append(("Top category", f"{top_category} ({top_category_count})", "Most frequent segment"))

    if 'Sales' in df.columns:
        top_product = df.loc[df['Sales'].idxmax(), 'Product'] if 'Product' in df.columns else "N/A"
        top_sales = int(df['Sales'].max())
        insights.append(("Best seller", f"{top_product} • {top_sales}", "Highest sales performer"))

    if 'City' in df.columns:
        top_city = df['City'].value_counts().idxmax()
        insights.append(("Top city", top_city, "Most active region"))

    if 'Customer_Age' in df.columns:
        age_range = f"{int(df['Customer_Age'].min())}–{int(df['Customer_Age'].max())}"
        insights.append(("Age range", age_range, "Customer age spread"))

    missing_ratio = df.isnull().mean().mean()
    health_score = max(0, min(100, int(round(100 - (missing_ratio * 100)))))
    health_label = "Excellent" if health_score >= 90 else "Good" if health_score >= 75 else "Needs review"

    return insights, health_score, health_label

def get_recommendations(df):
    recommendations = []

    if 'Category' in df.columns and 'Sales' in df.columns:
        category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        top_category = category_sales.index[0]
        recommendations.append(f"Focus on {top_category} because it drives the strongest sales volume.")

    if 'City' in df.columns and 'Sales' in df.columns:
        city_sales = df.groupby('City')['Sales'].sum().sort_values(ascending=False)
        top_city = city_sales.index[0]
        recommendations.append(f"{top_city} looks like your strongest market and may deserve more attention.")

    if df.isnull().sum().sum() > 0:
        recommendations.append("Missing values are present; cleaning them will improve the reliability of your analysis.")

    if len(recommendations) == 0:
        recommendations.append("Your data looks balanced, so you can move straight to deeper analysis.")

    return recommendations

def get_data_story(df):
    parts = []
    if 'Category' in df.columns:
        top_category = df['Category'].value_counts().idxmax()
        parts.append(f"The dataset is led by {top_category}, which appears most often.")
    if 'Sales' in df.columns:
        avg_sales = df['Sales'].mean()
        parts.append(f"Average sales are about {avg_sales:,.0f}, giving a sense of the typical transaction size.")
    if 'City' in df.columns:
        top_city = df['City'].value_counts().idxmax()
        parts.append(f"{top_city} contributes the largest share of records.")
    if not parts:
        parts.append("This dataset contains a rich mix of values ready for exploration.")
    return " ".join(parts)

# -------------------- Q&A ENGINE (rule-based) --------------------
def answer_question(df, question):
    q = question.lower()
    # Sales
    if 'highest sales' in q or 'max sales' in q:
        if 'Sales' in df.columns:
            row = df.loc[df['Sales'].idxmax()]
            return f"Product **{row['Product']}** had the highest sales of {row['Sales']} in {row['City']}."
        else:
            return "No 'Sales' column found."
    if 'average age' in q:
        if 'Customer_Age' in df.columns:
            avg = df['Customer_Age'].mean()
            return f"The average customer age is **{avg:.1f}** years."
        else:
            return "No 'Customer_Age' column found."
    if 'city with maximum orders' in q or 'max orders city' in q:
        if 'City' in df.columns:
            city = df['City'].value_counts().idxmax()
            count = df['City'].value_counts().max()
            return f"**{city}** has the maximum orders ({count})."
        else:
            return "No 'City' column found."
    if 'most frequent category' in q or 'category appears most' in q:
        if 'Category' in df.columns:
            cat = df['Category'].value_counts().idxmax()
            cnt = df['Category'].value_counts().max()
            return f"**{cat}** appears most frequently ({cnt} times)."
        else:
            return "No 'Category' column found."
    # Generic fallback
    return "I couldn't parse that question. Please ask about sales, age, city orders, or category frequency."

# -------------------- CHART GENERATION --------------------
def generate_chart(df, chart_type):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.set_style("darkgrid")
    if chart_type == 'Bar Chart':
        if 'Category' in df.columns:
            counts = df['Category'].value_counts()
            sns.barplot(x=counts.index, y=counts.values, palette='viridis', ax=ax)
            ax.set_title('Category Distribution', fontsize=14, fontweight='bold')
            ax.set_xlabel('Category')
            ax.set_ylabel('Count')
        else:
            ax.text(0.5, 0.5, 'No categorical column for bar chart', ha='center', va='center')
    elif chart_type == 'Pie Chart':
        if 'Category' in df.columns:
            counts = df['Category'].value_counts()
            ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette('pastel'))
            ax.set_title('Category Distribution (Pie)')
        else:
            ax.text(0.5, 0.5, 'No categorical column for pie chart', ha='center', va='center')
    elif chart_type == 'Histogram':
        if 'Sales' in df.columns:
            sns.histplot(df['Sales'], bins=20, kde=True, color='#6c8cff', ax=ax)
            ax.set_title('Sales Distribution')
            ax.set_xlabel('Sales')
        else:
            ax.text(0.5, 0.5, 'No "Sales" column for histogram', ha='center', va='center')
    elif chart_type == 'Scatter Plot':
        if 'Sales' in df.columns and 'Quantity' in df.columns:
            sns.scatterplot(data=df, x='Sales', y='Quantity', hue='Category', palette='Set2', ax=ax)
            ax.set_title('Sales vs Quantity')
        else:
            ax.text(0.5, 0.5, 'Need "Sales" and "Quantity" columns', ha='center', va='center')
    else:  # Line chart (if date column)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            grouped = df.groupby('Date')['Sales'].sum().reset_index()
            sns.lineplot(data=grouped, x='Date', y='Sales', marker='o', ax=ax)
            ax.set_title('Sales over Time')
        else:
            ax.text(0.5, 0.5, 'No "Date" column for line chart', ha='center', va='center')
    plt.tight_layout()
    return fig

# -------------------- AI EXPLANATION (optional) --------------------
def get_ai_explanation(df, chart_type):
    # Try to use Groq if API key available, else fallback to template
    api_key = os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            # Simple prompt
            import requests
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            data_preview = df.head(5).to_string()
            prompt = f"""
            Given a dataset with columns: {', '.join(df.columns)}.
            The user generated a {chart_type} chart.
            Provide a short, easy-to-understand explanation (2-3 sentences) of the key insight from this chart.
            Data preview:
            {data_preview}
            """
            # Using Groq API (free)
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5
            }
            response = requests.post(url, json=payload, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content'].strip()
        except Exception:
            pass
    # Fallback template explanation
    if chart_type == 'Bar Chart' and 'Category' in df.columns:
        top = df['Category'].value_counts().idxmax()
        pct = (df['Category'].value_counts().max() / len(df)) * 100
        return f"The **{top}** category has the highest frequency, accounting for approximately {pct:.1f}% of the total records."
    elif chart_type == 'Pie Chart' and 'Category' in df.columns:
        top = df['Category'].value_counts().idxmax()
        pct = (df['Category'].value_counts().max() / len(df)) * 100
        return f"The **{top}** category dominates with {pct:.1f}% of the total."
    elif chart_type == 'Histogram' and 'Sales' in df.columns:
        return f"The sales distribution shows a typical range from {df['Sales'].min()} to {df['Sales'].max()}, with most values clustering around the mean."
    elif chart_type == 'Scatter Plot':
        return f"The scatter plot reveals the relationship between Sales and Quantity, with possible clusters by category."
    else:
        return "This chart provides a visual summary of the dataset's key patterns."

# -------------------- UI LAYOUT --------------------
st.markdown("""
<div class="hero-card">
    <div class="hero-badge">✨ Smart analytics workspace</div>
    <div class="hero-title">AI Data Analysis Assistant</div>
    <div class="hero-subtitle">
        Upload a CSV, ask questions, generate charts, and uncover insights in a polished workspace.
    </div>
    <div class="status-ribbon">⚡ Live insights ready · Smart analysis mode</div>
    <div class="pill-row">
        <span class="pill">📁 CSV Upload</span>
        <span class="pill">❓ Natural Q&A</span>
        <span class="pill">📈 Instant Charts</span>
        <span class="pill">🧠 AI Insights</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="action-card">
    <div class="section-title">Start exploring your data</div>
    <div class="section-subtitle">Choose a CSV file or launch the built-in sample dataset to begin.</div>
</div>
""", unsafe_allow_html=True)

# Uploader
st.markdown("<div class='upload-card'>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Upload your dataset</div>", unsafe_allow_html=True)
st.markdown("<div class='section-subtitle' style='margin-bottom: 0.8rem;'>CSV files are supported and the app will analyze them instantly.</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1.1, 1.1], vertical_alignment="bottom")
with col1:
    uploaded_file = st.file_uploader("Drop your CSV here", type=['csv'], label_visibility="collapsed")
with col2:
    if st.button("📂 Use Sample Data", use_container_width=True):
        st.session_state.df = generate_sample_data()
        st.session_state.loaded = True
        st.rerun()
with col3:
    if st.button("🧹 Clear", use_container_width=True):
        st.session_state.df = None
        st.session_state.loaded = False
        st.session_state.qa_answers = {}
        st.session_state.chart_type = 'Bar Chart'
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# Load data
if uploaded_file is not None:
    df = load_data(uploaded_file)
    if df is not None:
        st.session_state.df = df
        st.session_state.loaded = True
else:
    if st.session_state.df is None:
        st.session_state.df = generate_sample_data()
    df = st.session_state.df

if st.session_state.loaded and df is not None:
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Overview", "🔍 Data Summary", "❓ Q&A", "📈 Chart & Explanation"])

    with tab1:
        stats = get_stats(df)
        insights, health_score, health_label = get_smart_insights(df)
        st.markdown("<div class='section-hero'>", unsafe_allow_html=True)
        st.markdown("<div class='section-hero-title'>📊 Overview dashboard</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-hero-subtitle'>A polished snapshot of your dataset structure, health, and key signals.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>📊 Quick overview</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>A fast snapshot of your dataset structure and quality.</div>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown(f"<div class='metric-card'><div style='font-size:0.9rem; color:#8899bb;'>Rows</div><div class='metric-value'>{stats['Rows']}</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='metric-card'><div style='font-size:0.9rem; color:#8899bb;'>Columns</div><div class='metric-value'>{stats['Columns']}</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='metric-card'><div style='font-size:0.9rem; color:#8899bb;'>Missing</div><div class='metric-value'>{stats['Missing']}</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='metric-card'><div style='font-size:0.9rem; color:#8899bb;'>Numerical</div><div class='metric-value'>{stats['Numerical']}</div></div>", unsafe_allow_html=True)
        with col5:
            st.markdown(f"<div class='metric-card'><div style='font-size:0.9rem; color:#8899bb;'>Categorical</div><div class='metric-value'>{stats['Categorical']}</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>✨ Smart insights</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>Auto-generated highlights make your dataset easier to understand at a glance.</div>", unsafe_allow_html=True)
        health_col, insights_col = st.columns([1, 2])
        with health_col:
            st.markdown(f"""
            <div class='insight-card'>
                <div class='insight-title'>Data quality</div>
                <div class='health-score'>{health_score}</div>
                <div class='insight-desc'>{health_label} · cleaner than most starter datasets</div>
                <div class='health-bar'><div style='width: {health_score}%;'></div></div>
            </div>
            """, unsafe_allow_html=True)
        with insights_col:
            insight_cols = st.columns(2)
            for idx, (title, value, desc) in enumerate(insights[:4]):
                with insight_cols[idx % 2]:
                    st.markdown(f"""
                    <div class='insight-card' style='margin-bottom: 0.7rem;'>
                        <div class='insight-title'>{title}</div>
                        <div class='insight-value'>{value}</div>
                        <div class='insight-desc'>{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>📖 Data story</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>A plain-language summary of what your dataset is saying.</div>", unsafe_allow_html=True)
        story = get_data_story(df)
        st.markdown(f"<div class='story-card'><div class='story-text'>{story}</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>🎯 Actionable recommendations</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>The app turns your data into practical next steps.</div>", unsafe_allow_html=True)
        recommendations = get_recommendations(df)
        for item in recommendations:
            st.markdown(f"<div class='recommendation-card'><span class='recommendation-icon'>➜</span>{item}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>📌 Data types</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>Understand what kind of information each column contains.</div>", unsafe_allow_html=True)
        dtype_df = pd.DataFrame(df.dtypes.reset_index())
        dtype_df.columns = ['Column', 'Data Type']
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<div class='section-hero'>", unsafe_allow_html=True)
        st.markdown("<div class='section-hero-title'>🔍 Deep data summary</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-hero-subtitle'>Explore the stats and preview the data in a cleaner, more insightful layout.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>📊 Descriptive statistics</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>Key statistical insights from the numeric columns in your dataset.</div>", unsafe_allow_html=True)
        num_summary = get_numeric_summary(df)
        if not num_summary.empty:
            st.dataframe(num_summary, use_container_width=True)
        else:
            st.info("No numeric columns for summary.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>🔎 Data preview</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>Preview the first rows of your dataset in a cleaner table layout.</div>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown("<div class='section-hero'>", unsafe_allow_html=True)
        st.markdown("<div class='section-hero-title'>❓ Q&A assistant</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-hero-subtitle'>Ask practical questions and get instant answers from your data.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>❓ Ask a question</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>Try one of the sample questions below or ask your own.</div>", unsafe_allow_html=True)
        st.markdown("<div class='prompt-row'>", unsafe_allow_html=True)
        st.markdown("<span class='prompt-chip'>📌 Sales</span>", unsafe_allow_html=True)
        st.markdown("<span class='prompt-chip'>👥 Customers</span>", unsafe_allow_html=True)
        st.markdown("<span class='prompt-chip'>🏙️ Cities</span>", unsafe_allow_html=True)
        st.markdown("<span class='prompt-chip'>🧺 Categories</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        questions = [
            "Which product generated the highest sales?",
            "What is the average age of customers?",
            "Which city has the maximum orders?",
            "Which category appears most frequently?"
        ]
        for i, q in enumerate(questions):
            with st.container():
                st.markdown(f"<div class='qa-card'>", unsafe_allow_html=True)
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**Q{i+1}:** {q}")
                with col2:
                    if st.button(f"Ask #{i+1}", key=f"q_{i}", use_container_width=True):
                        ans = answer_question(df, q)
                        st.session_state.qa_answers[q] = ans
                        st.rerun()
                if q in st.session_state.qa_answers:
                    st.markdown(f"**A:** {st.session_state.qa_answers[q]}")
                st.markdown("</div>", unsafe_allow_html=True)

        custom_q = st.text_input("Or type your own question:", placeholder="e.g., What is the average sales?")
        if custom_q and st.button("Ask Custom", use_container_width=True):
            ans = answer_question(df, custom_q)
            st.session_state.qa_answers[custom_q] = ans
            st.rerun()
        if custom_q in st.session_state.qa_answers:
            st.markdown(f"**A:** {st.session_state.qa_answers[custom_q]}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        st.markdown("<div class='section-hero'>", unsafe_allow_html=True)
        st.markdown("<div class='section-hero-title'>📈 Visual insights</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-hero-subtitle'>Turn your data into clear visuals and meaningful explanations.</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div class='analysis-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='panel-title'>📈 Generate chart</div>", unsafe_allow_html=True)
        st.markdown("<div class='panel-subtitle'>Choose a chart type and turn your data into a visual story.</div>", unsafe_allow_html=True)
        st.markdown("<div class='tip-card'>💡 Tip: use bar charts for category counts, histograms for sales distributions, and scatter plots for relationships.</div>", unsafe_allow_html=True)
        chart_type = st.selectbox(
            "Choose chart type",
            ['Bar Chart', 'Pie Chart', 'Histogram', 'Scatter Plot', 'Line Chart'],
            index=0
        )
        if st.button("Generate Chart", use_container_width=True):
            st.session_state.chart_type = chart_type
            st.rerun()

        if st.session_state.chart_type:
            fig = generate_chart(df, st.session_state.chart_type)
            st.markdown("<div class='chart-shell'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-box'>", unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            chart_file_name = f"chart_{timestamp}.png"
            charts_dir = os.path.join(os.path.dirname(__file__), 'charts')
            os.makedirs(charts_dir, exist_ok=True)
            chart_path = os.path.join(charts_dir, chart_file_name)
            fig.savefig(chart_path, format='png', dpi=150, bbox_inches='tight')

            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            st.download_button(
                label="⬇️ Download Chart as PNG",
                data=buf,
                file_name=chart_file_name,
                mime="image/png"
            )
            st.caption(f"Saved to: {chart_path}")

            st.markdown("<div class='panel-title' style='margin-top: 1rem;'>🧠 AI explanation</div>", unsafe_allow_html=True)
            explanation = get_ai_explanation(df, st.session_state.chart_type)
            st.markdown(f"<div class='answer-box' style='border-left-color:#a78bfa;'>{explanation}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state-card">
        <div class="section-title">👋 Ready to explore your data?</div>
        <div class="section-subtitle" style="margin-bottom: 0.7rem;">Upload a CSV file, try the sample dataset, or clear the current view to start fresh.</div>
        <div>
            <span class="step-badge">1. Upload CSV</span>
            <span class="step-badge">2. Review insights</span>
            <span class="step-badge">3. Ask questions</span>
            <span class="step-badge">4. Generate charts</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("✨ AI Data Analysis Challenge · Hackathon 2026")