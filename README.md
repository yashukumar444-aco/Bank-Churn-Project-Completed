# Bank Churn Analysis Dashboard

This project analyzes customer churn for a bank dataset using Python, Streamlit, Pandas, and Plotly.

## Project files
- [Untitled-1.py](Untitled-1.py) – Streamlit dashboard
- [European_Bank (1).csv](European_Bank%20(1).csv) – dataset used for analysis

## Run locally

1. Open a terminal in the project folder.
2. Create and activate a virtual environment (optional but recommended).
3. Install dependencies:

```bash
pip install streamlit pandas plotly
```

4. Start the app:

```bash
streamlit run Untitled-1.py
```

## Deploy on Streamlit Community Cloud

1. Open [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2. Select the repository `yashukumar444-aco/Bank-Churn-Project-Completed`.
3. Select the `main` branch.
4. Set the main file path to `Untitled-1.py`.
5. Click **Deploy**. Streamlit Cloud will install the packages from `requirements.txt`.

The dashboard reads `European_Bank (1).csv` from the repository, so no secrets or extra configuration are required.

## GitHub push steps

```bash
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Bank-Churn-Analysis.git
git push -u origin main
```

Replace `YOUR_USERNAME` and the repository name with your own GitHub details.
