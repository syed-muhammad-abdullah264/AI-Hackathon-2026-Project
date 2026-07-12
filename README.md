# AI Data Analysis Assistant

A polished, AI-assisted data analysis web app built for the AI Data Analysis Challenge. It allows users to upload a CSV file, explore the dataset, ask natural-language questions, generate meaningful charts, and receive simple explanations.

## What this project does

This application helps users:

- Load and inspect CSV datasets
- View dataset summary, missing values, and data types
- Explore descriptive statistics
- Answer predefined questions like:
  - Which product generated the highest sales?
  - What is the average age of customers?
  - Which city has the maximum orders?
  - Which category appears most frequently?
- Generate at least one meaningful chart
- Provide a short explanation of the chart insights

## Main features

- CSV upload support
- Built-in sample dataset
- Dataset overview and summary statistics
- Rule-based natural-language Q&A
- Multiple chart options
- Download chart as PNG
- Optional AI explanation using Groq/OpenAI when an API key is available
- Modern dark-themed Streamlit interface

## Tech stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Requests

## Project structure

- app.py: main Streamlit application
- main.py: simple wrapper to launch the app
- sample_data.csv: sample dataset for testing
- requirements.txt: required Python packages
- README.md: project documentation
- charts/: folder for saved chart images

## Installation

1. Open the project folder
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the app

Run either of the following commands:

```bash
streamlit run app.py
```

or

```bash
streamlit run main.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Optional AI explanation setup

To enable AI-generated chart explanations, set one of these environment variables before running the app:

```bash
set GROQ_API_KEY=your_key_here
```

or

```bash
set OPENAI_API_KEY=your_key_here
```

If no API key is set, the app will still work and use a built-in fallback explanation.

## Example questions

Try these questions in the app:

- Which product generated the highest sales?
- What is the average age of customers?
- Which city has the maximum orders?
- Which category appears most frequently?

## Submission notes

This project satisfies the main requirements of the challenge:

- CSV loading
- Basic data analysis
- Natural-language answers
- Chart generation
- Simple explanation
- Clean project structure

## Demo checklist

- [x] Python project created
- [x] CSV dataset used
- [x] requirements.txt added
- [x] README.md added
- [x] Chart generation implemented
- [x] Q&A system implemented
- [x] App runs successfully
