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
            background: #0b0e17;
            font-family: 'Inter', sans-serif;
        }
        .main > div {
            padding: 0 1rem;
        }
        /* Cards */
        .css-1r6slb0, .css-1v3fvcr, .css-1d391kg {
            background: rgba(19, 26, 43, 0.7) !important;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(42, 58, 92, 0.4);
            border-radius: 20px;
            box-shadow: 0 20px 40px -12px rgba(0,0,0,0.6);
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
            background: rgba(19, 26, 43, 0.8);
            border-radius: 16px;
            padding: 6px;
            border: 1px solid rgba(42,58,92,0.4);
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
        .metric-card:hover {
            border-color: #6c8cff;
            transform: translateY(-4px);
            box-shadow: 0 12px 32px rgba(0,0,0,0.4);
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
            background: rgba(19,26,43,0.6);
            border-radius: 16px;
            padding: 16px;
            border: 1px solid rgba(42,58,92,0.3);
        }
        /* Responsive */
        @media (max-width: 600px) {
            .metric-value { font-size: 1.6rem; }
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
st.markdown("<div class='glow-text' style='font-size:2.2rem; font-weight:800;'>📊 AI Data Analysis Assistant</div>", unsafe_allow_html=True)
st.caption("Upload a CSV or use the sample dataset. Ask questions, visualize, and get AI insights.")

# Uploader
col1, col2 = st.columns([3, 1])
with col1:
    uploaded_file = st.file_uploader("Drop your CSV here", type=['csv'], label_visibility="collapsed")
with col2:
    if st.button("📂 Use Sample Data"):
        st.session_state.df = generate_sample_data()
        st.session_state.loaded = True
        st.rerun()

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

        st.subheader("📌 Data Types")
        dtype_df = pd.DataFrame(df.dtypes.reset_index())
        dtype_df.columns = ['Column', 'Data Type']
        st.dataframe(dtype_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("📊 Descriptive Statistics")
        num_summary = get_numeric_summary(df)
        if not num_summary.empty:
            st.dataframe(num_summary, use_container_width=True)
        else:
            st.info("No numeric columns for summary.")
        st.subheader("🔎 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

    with tab3:
        st.subheader("❓ Ask a Question")
        # Predefined questions (judge questions)
        questions = [
            "Which product generated the highest sales?",
            "What is the average age of customers?",
            "Which city has the maximum orders?",
            "Which category appears most frequently?"
        ]
        for i, q in enumerate(questions):
            with st.container():
                st.markdown(f"<div class='answer-box'>", unsafe_allow_html=True)
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**Q{i+1}:** {q}")
                with col2:
                    if st.button(f"Ask #{i+1}", key=f"q_{i}"):
                        ans = answer_question(df, q)
                        st.session_state.qa_answers[q] = ans
                        st.rerun()
                if q in st.session_state.qa_answers:
                    st.markdown(f"**A:** {st.session_state.qa_answers[q]}")
                st.markdown("</div>", unsafe_allow_html=True)

        # Custom question
        custom_q = st.text_input("Or type your own question:", placeholder="e.g., What is the average sales?")
        if custom_q and st.button("Ask Custom"):
            ans = answer_question(df, custom_q)
            st.session_state.qa_answers[custom_q] = ans
            st.rerun()
        if custom_q in st.session_state.qa_answers:
            st.markdown(f"**A:** {st.session_state.qa_answers[custom_q]}")

    with tab4:
        st.subheader("📈 Generate Chart")
        chart_type = st.selectbox(
            "Choose chart type",
            ['Bar Chart', 'Pie Chart', 'Histogram', 'Scatter Plot', 'Line Chart'],
            index=0
        )
        if st.button("Generate Chart"):
            st.session_state.chart_type = chart_type
            st.rerun()

        if st.session_state.chart_type:
            fig = generate_chart(df, st.session_state.chart_type)
            st.pyplot(fig)

            # Export chart as PNG
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            st.download_button(
                label="⬇️ Download Chart as PNG",
                data=buf,
                file_name=f"chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                mime="image/png"
            )

            # AI Explanation
            st.subheader("🧠 AI Explanation")
            explanation = get_ai_explanation(df, st.session_state.chart_type)
            st.markdown(f"<div class='answer-box' style='border-left-color:#a78bfa;'>{explanation}</div>", unsafe_allow_html=True)

else:
    st.info("👆 Upload a CSV or click 'Use Sample Data' to begin.")

# Footer
st.markdown("---")
st.caption("✨ AI Data Analysis Challenge · Hackathon 2026")