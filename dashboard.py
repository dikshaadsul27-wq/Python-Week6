# dashboard.py
# Interactive Sales Dashboard using Seaborn + Plotly with sales_data.csv

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------
# Step 0: Load Your CSV
# -----------------------------
df = pd.read_csv("sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# Step 1: Seaborn Basics
# -----------------------------
sns.set_style("whitegrid")
sns.set_palette("muted")

plt.figure(figsize=(6,4))
sns.boxplot(x='Product', y='Price', data=df)
plt.title('Price Distribution by Product')
plt.savefig("visualizations/boxplot.png")
plt.close()

# -----------------------------
# Step 2: Statistical Visualizations
# -----------------------------
plt.figure(figsize=(6,4))
sns.violinplot(x='Region', y='Total_Sales', data=df, inner='quartile')
plt.title('Sales Distribution by Region')
plt.savefig("visualizations/violinplot.png")
plt.close()

# -----------------------------
# Step 3: Heatmaps & Correlation
# -----------------------------
corr = df[['Quantity','Price','Total_Sales']].corr()
plt.figure(figsize=(6,4))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title('Feature Correlation Heatmap')
plt.savefig("visualizations/heatmap.png")
plt.close()

# -----------------------------
# Step 4: Multi-plot Dashboard (Static)
# -----------------------------
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

sns.lineplot(x='Date', y='Total_Sales', data=df, ax=axes[0,0])
axes[0,0].set_title("Sales Trend Over Time")

sns.barplot(x='Product', y='Total_Sales', data=df, ax=axes[0,1])
axes[0,1].set_title("Sales by Product")

sns.boxplot(x='Region', y='Total_Sales', data=df, ax=axes[1,0])
axes[1,0].set_title("Regional Sales Distribution")

sns.scatterplot(x='Quantity', y='Total_Sales', data=df, ax=axes[1,1])
axes[1,1].set_title("Quantity vs Total Sales")

plt.tight_layout()
plt.savefig("visualizations/multi_dashboard.png")
plt.close()

# -----------------------------
# Step 5: Interactive Visualizations (Plotly)
# -----------------------------
fig_line = px.line(df, x="Date", y="Total_Sales", color="Region",
                   title="Interactive Sales Trends")
fig_line.update_layout(hovermode="x unified")
fig_line.write_html("visualizations/interactive_line.html")

# Dropdown Example
fig_dropdown = make_subplots(rows=1, cols=1)
fig_dropdown.add_trace(go.Bar(x=df["Product"], y=df["Total_Sales"], name="Total Sales"))
fig_dropdown.add_trace(go.Bar(x=df["Product"], y=df["Price"], name="Price"))

fig_dropdown.update_layout(
    updatemenus=[{
        "buttons": [
            {"method": "update", "label": "Total Sales", "args": [{"visible": [True, False]}]},
            {"method": "update", "label": "Price", "args": [{"visible": [False, True]}]}
        ]
    }],
    title="Interactive Dropdown Example"
)
fig_dropdown.write_html("visualizations/interactive_dropdown.html")

# -----------------------------
# Step 6: Dashboard Integration
# -----------------------------
fig_dashboard = make_subplots(rows=2, cols=2,
    subplot_titles=("Sales Trend", "Sales by Product", "Regional Sales", "Quantity vs Sales"))

fig_dashboard.add_trace(go.Scatter(x=df["Date"], y=df["Total_Sales"], mode="lines", name="Sales Trend"), row=1, col=1)
fig_dashboard.add_trace(go.Bar(x=df["Product"], y=df["Total_Sales"], name="Product Sales"), row=1, col=2)
fig_dashboard.add_trace(go.Box(y=df["Total_Sales"], x=df["Region"], name="Regional Sales"), row=2, col=1)
fig_dashboard.add_trace(go.Scatter(x=df["Quantity"], y=df["Total_Sales"], mode="markers", name="Quantity vs Sales"), row=2, col=2)

fig_dashboard.update_layout(title="Integrated Interactive Sales Dashboard", showlegend=False)
fig_dashboard.write_html("visualizations/final_dashboard.html")

# -----------------------------
# Step 7: Polish & Presentation
# -----------------------------
print("Dashboard generation complete. Check 'visualizations/' folder for outputs.")
