# AI Data Analysis Assistant

A stunning, feature‑rich data analysis app built for the **AI Data Analysis Challenge**.  
Upload any CSV, get instant stats, ask natural‑language questions, generate beautiful charts, and receive AI‑powered explanations.

## Features

- Drag‑and‑drop CSV upload (or use sample data)
- Dataset overview, missing values, data types
- Descriptive statistics
- 4 predefined judge questions + custom Q&A
- 5 chart types (Bar, Pie, Histogram, Scatter, Line)
- Download chart as PNG
- Optional AI explanation (Groq/OpenAI) with fallback
- Dark theme with smooth animations

## How to Run

1. Install dependencies: `pip install -r requirements.txt`
2. Run: `streamlit run app.py` or `streamlit run main.py`
3. Open http://localhost:8501

## Project Structure

- app.py: main Streamlit app
- main.py: simple entry-point wrapper
- sample_data.csv: built-in sample dataset
- charts/: exported chart images are saved here

## API Key (Optional)

Set environment variable `GROQ_API_KEY` or `OPENAI_API_KEY` to enable LLM‑generated explanations.
