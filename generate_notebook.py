# generate_notebook.py
import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# Notebook cells content
cells = []

# Title
cells.append(new_markdown_cell("# 📊 AI Data Analysis Assistant (Jupyter Notebook)\n*Complete solution for Hackathon 2026*"))

# Cell 1: Imports
cells.append(new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import ipywidgets as widgets
from IPython.display import display, clear_output
import io
%matplotlib inline"""))

# Cell 2: Sample Data Generator
cells.append(new_code_cell("""# Generate sample dataset (100 rows)
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

df = generate_sample_data()
print("✅ Sample Data Loaded! (100 rows)")
display(df.head())"""))

# Cell 3: Dataset Summary
cells.append(new_code_cell("""# Dataset Overview
print(f"📌 Rows: {df.shape[0]}, Columns: {df.shape[1]}")
print(f"📌 Missing Values: {df.isnull().sum().sum()}")
print("\\n📌 Data Types:")
print(df.dtypes)"""))

# Cell 4: Statistics
cells.append(new_code_cell("""# Descriptive Statistics
display(df.describe().T)"""))

# Cell 5: Q&A Function
cells.append(new_code_cell("""# Q&A Engine (Rule-based)
def answer_question(df, q):
    q = q.lower()
    if 'highest sales' in q or 'max sales' in q:
        if 'Sales' in df.columns:
            row = df.loc[df['Sales'].idxmax()]
            return f"✅ Product **{row['Product']}** had the highest sales of {row['Sales']} in {row['City']}."
    if 'average age' in q:
        if 'Customer_Age' in df.columns:
            avg = df['Customer_Age'].mean()
            return f"✅ Average customer age is **{avg:.1f}** years."
    if 'maximum orders' in q or 'city with max orders' in q:
        if 'City' in df.columns:
            city = df['City'].value_counts().idxmax()
            count = df['City'].value_counts().max()
            return f"✅ **{city}** has maximum orders ({count})."
    if 'category appears most' in q or 'most frequent category' in q:
        if 'Category' in df.columns:
            cat = df['Category'].value_counts().idxmax()
            cnt = df['Category'].value_counts().max()
            return f"✅ **{cat}** appears most frequently ({cnt} times)."
    return "❌ Sorry, couldn't parse that question."""))
    
# Cell 6: Run 4 judge questions
cells.append(new_code_cell("""# Judge Questions
questions = [
    "Which product generated the highest sales?",
    "What is the average age of customers?",
    "Which city has the maximum orders?",
    "Which category appears most frequently?"
]

for i, q in enumerate(questions):
    print(f"Q{i+1}: {q}")
    print(f"A: {answer_question(df, q)}\\n")"""))

# Cell 7: Custom question (input)
cells.append(new_code_cell("""# Ask your own question
custom = input("Type your question: ")
if custom:
    print(f"Q: {custom}")
    print(f"A: {answer_question(df, custom)}")"""))

# Cell 8: Chart generation functions
cells.append(new_code_cell("""# Chart Generator
def plot_chart(df, chart_type):
    fig, ax = plt.subplots(figsize=(10,5))
    if chart_type == 'Bar':
        counts = df['Category'].value_counts()
        sns.barplot(x=counts.index, y=counts.values, palette='viridis', ax=ax)
        ax.set_title('Category Distribution', fontsize=14)
        ax.set_xlabel('Category'); ax.set_ylabel('Count')
    elif chart_type == 'Pie':
        counts = df['Category'].value_counts()
        ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Category Distribution (Pie)')
    elif chart_type == 'Hist':
        ax.hist(df['Sales'], bins=20, edgecolor='black', alpha=0.7, color='#6c8cff')
        ax.set_title('Sales Distribution')
        ax.set_xlabel('Sales'); ax.set_ylabel('Frequency')
    elif chart_type == 'Scatter':
        scatter = ax.scatter(df['Sales'], df['Quantity'], 
                             c=df['Category'].astype('category').cat.codes, cmap='Set2')
        ax.set_xlabel('Sales'); ax.set_ylabel('Quantity')
        ax.set_title('Sales vs Quantity')
    plt.tight_layout()
    plt.show()"""))

# Cell 9: Generate all charts
cells.append(new_code_cell("""# Generate all 4 charts
print("📊 Bar Chart")
plot_chart(df, 'Bar')
print("📊 Pie Chart")
plot_chart(df, 'Pie')
print("📊 Histogram")
plot_chart(df, 'Hist')
print("📊 Scatter Plot")
plot_chart(df, 'Scatter')"""))

# Cell 10: Explanation (fallback)
cells.append(new_code_cell("""# AI Explanation (fallback template)
def get_explanation(df, chart_type='Bar'):
    if chart_type == 'Bar' and 'Category' in df.columns:
        top = df['Category'].value_counts().idxmax()
        pct = (df['Category'].value_counts().max() / len(df)) * 100
        return f"🧠 The **{top}** category has the highest frequency, accounting for approximately {pct:.1f}% of the total records."
    return "🧠 This chart provides a visual summary of the dataset."

print("Explanation for Bar Chart:")
print(get_explanation(df))"""))

# Create notebook
nb = new_notebook()
nb['cells'] = cells

# Write to file
with open('AI_Data_Analysis_Assistant.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("✅ Notebook generated successfully! File: AI_Data_Analysis_Assistant.ipynb")