# GTC Virtual Lab App

A **Streamlit-based interactive virtual lab** for GTC (Gas Turbine Combustion / General Theory of Combustion) experiments.

## 🚀 Features

- 11 interactive experiments (exp1 – exp11)
- Built-in Python code editor and executor per experiment
- Experiment-wise theory viewer (Markdown + PDF-style content)
- Graph/plot output rendered inline
- Sidebar navigation with logo branding

## 📁 Project Structure

```
app/
├── app.py              # Main Streamlit application
├── logo.png            # App logo
├── th.zip              # Theory resources archive
└── theory/             # Markdown theory files
    ├── exp1.md – exp11.md         # Short experiment descriptions
    └── gtc_exp1.md – gtc_exp11.md # Detailed GTC theory content
```

## 🛠️ Setup & Run

### 1. Install dependencies

```bash
pip install streamlit
```

### 2. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501` in your browser.

## 📋 Requirements

- Python 3.8+
- Streamlit

## 📄 License

This project is for educational purposes.
