import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Bank Churn Dashboard", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f4f7fb 0%, #eef3ff 100%);
    }
    h1 {
        color: #143d6b;
        font-weight: 700;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
    }
    div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stMetric"]) {
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        padding: 0.5rem 0.75rem;
        box-shadow: 0 3px 10px rgba(20, 61, 107, 0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏦 Bank Customer Churn Analysis Dashboard")
st.caption("Customer retention insights across geography and gender segments.")


@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent
    csv_candidates = [
        base_dir / "European_Bank (1).csv",
        base_dir / "data" / "European_Bank.csv",
        base_dir / "European_Bank.csv",
    ]

    for csv_path in csv_candidates:
        if csv_path.exists():
            return pd.read_csv(csv_path)

    raise FileNotFoundError("No bank churn dataset was found in the project folder.")


df = load_data()

if 'Exited' in df.columns:
    df['Churn'] = df['Exited']
else:
    st.error("Churn column not found in the dataset.")
    st.stop()

# Add helper columns
if 'Age' in df.columns:
    df['Age Group'] = pd.cut(
        df['Age'],
        bins=[18, 30, 45, 60, 100],
        labels=["18-30", "30-45", "45-60", "60+"],
        include_lowest=True,
    )

if 'Balance' in df.columns:
    df['Balance Band'] = pd.cut(
        df['Balance'],
        bins=[-1, 10000, 50000, 100000, 200000],
        labels=["Low", "Medium", "High", "Very High"],
        include_lowest=True,
    )

st.sidebar.header("🔍 Filters")

country = st.sidebar.multiselect(
    "Select Geography",
    options=df['Geography'].unique(),
    default=df['Geography'].unique(),
)

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df['Gender'].unique(),
    default=df['Gender'].unique(),
)

filtered_df = df[
    (df['Geography'].isin(country)) &
    (df['Gender'].isin(gender))
].copy()

# KPI section
col1, col2, col3, col4 = st.columns(4)

total_customers = filtered_df.shape[0]
churned = int(filtered_df['Churn'].sum())
churn_rate = (churned / total_customers * 100) if total_customers else 0
retention_rate = 100 - churn_rate
avg_balance = filtered_df['Balance'].mean() if not filtered_df.empty else 0
avg_age = filtered_df['Age'].mean() if not filtered_df.empty else 0
country_churn = filtered_df.groupby('Geography')['Churn'].mean().sort_values(ascending=False)
gender_churn = filtered_df.groupby('Gender')['Churn'].mean().sort_values(ascending=False)

col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned)
col3.metric("Churn Rate (%)", f"{churn_rate:.2f}")
col4.metric("Retention Rate (%)", f"{retention_rate:.2f}")

st.markdown("---")
summary_col1, summary_col2, summary_col3 = st.columns(3)
summary_col1.metric("Avg. Balance", f"${avg_balance:,.0f}")
summary_col2.metric("Avg. Age", f"{avg_age:.1f} years")
summary_col3.metric("Top Churn Country", country_churn.index[0] if not country_churn.empty else "N/A")

# Charts
fig1 = px.bar(
    filtered_df,
    x='Geography',
    y='Churn',
    title='Churn by Country',
    color='Geography',
    barmode='group',
)
st.plotly_chart(fig1, width="stretch")

fig2 = px.pie(
    filtered_df,
    names='Gender',
    values='Churn',
    title='Churn by Gender',
)
st.plotly_chart(fig2, width="stretch")

fig3 = px.histogram(
    filtered_df,
    x='Age Group',
    color='Churn',
    barmode='group',
    title='Churn by Age Group',
)
st.plotly_chart(fig3, width="stretch")

fig4 = px.box(
    filtered_df,
    x='Churn',
    y='Balance',
    title='Balance Distribution by Churn',
)
st.plotly_chart(fig4, width="stretch")

fig5 = px.histogram(
    filtered_df,
    x='CreditScore',
    color='Churn',
    title='Credit Score Distribution',
)
st.plotly_chart(fig5, width="stretch")

st.subheader("📊 Key Insights")
insight_lines = [
    f"- The current filtered dataset has a churn rate of {churn_rate:.2f}% across {total_customers} customers.",
    f"- The highest churn rate among selected countries is in {country_churn.index[0]} with {country_churn.iloc[0] * 100:.2f}% churn.",
    f"- The selected gender split shows {gender_churn.index[0]} with the higher churn rate at {gender_churn.iloc[0] * 100:.2f}%.",
    f"- Average customer balance in the current view is ${avg_balance:,.0f}, while average age is {avg_age:.1f} years.",
]

st.write("\n".join(insight_lines))

st.markdown("---")
st.write("Developed for Data Analytics Project 🚀")