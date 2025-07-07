import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- Load and preprocess data ---
@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df['Timestamp'] = pd.to_datetime(df['LastUpdatedDate'] + ' ' + df['LastUpdatedTime'], dayfirst=True)
    df = df.sort_values(['SystemCodeNumber', 'Timestamp']).reset_index(drop=True)
    df['OccupancyRate'] = df['Occupancy'] / df['Capacity']
    return df

# --- Calculate prices dynamically ---
def calculate_prices(df, alpha, base_price=10):
    df = df.copy()
    df['Price'] = base_price
    for lot in df['SystemCodeNumber'].unique():
        lot_idx = df[df['SystemCodeNumber'] == lot].index
        for i in range(1, len(lot_idx)):
            prev_price = df.loc[lot_idx[i - 1], 'Price']
            occupancy_rate = df.loc[lot_idx[i], 'OccupancyRate']
            new_price = prev_price + alpha * occupancy_rate
            new_price = max(5, min(new_price, 30))
            df.loc[lot_idx[i], 'Price'] = new_price
    return df

# --- Simulate competitor prices ---
def simulate_competitor_prices(df):
    competitor_dfs = []
    for lot in df['SystemCodeNumber'].unique():
        lot_data = df[df['SystemCodeNumber'] == lot]
        competitor_prices = np.clip(np.random.normal(lot_data['Price'], 2), 5, 30)
        competitor_dfs.append(
            pd.DataFrame({
                'SystemCodeNumber': lot,
                'Timestamp': lot_data['Timestamp'],
                'CompetitorPrice': competitor_prices
            })
        )
    return pd.concat(competitor_dfs, ignore_index=True)

# --- Plot function using Plotly ---
def plot_prices(df_lot, df_comp_lot, lot):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_lot['Timestamp'], y=df_lot['Price'], mode='lines+markers',
        name='Our Price', line=dict(color='blue')))
    fig.add_trace(go.Scatter(
        x=df_comp_lot['Timestamp'], y=df_comp_lot['CompetitorPrice'], mode='lines+markers',
        name='Competitor Price', line=dict(color='red')))
    fig.update_layout(
        title=f"Dynamic Pricing for Lot: {lot}",
        xaxis_title="Time",
        yaxis_title="Price ($)",
        legend_title="Legend",
        hovermode="x unified"
    )
    return fig

# --- Streamlit UI ---
st.title("🚗 Parking Dynamic Pricing Dashboard")

# Load data
df = load_data("parking.csv")

# User inputs
alpha = st.sidebar.slider("Pricing Sensitivity (alpha)", min_value=0.1, max_value=10.0, value=5.0, step=0.1)
base_price = st.sidebar.number_input("Base Price", min_value=1, max_value=50, value=10)
lot_selected = st.sidebar.selectbox("Select Parking Lot:", df['SystemCodeNumber'].unique())

# Calculate prices with chosen alpha
df_priced = calculate_prices(df, alpha, base_price)
df_comp = simulate_competitor_prices(df_priced)

# Filter data for selected lot
df_lot = df_priced[df_priced['SystemCodeNumber'] == lot_selected]
df_comp_lot = df_comp[df_comp['SystemCodeNumber'] == lot_selected]

# Show latest KPI metrics
latest = df_lot.iloc[-1]
latest_comp = df_comp_lot[df_comp_lot['Timestamp'] == latest['Timestamp']].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${latest['Price']:.2f}")
col2.metric("Occupancy Rate", f"{latest['OccupancyRate']*100:.1f}%")
col3.metric("Competitor Price", f"${latest_comp['CompetitorPrice']:.2f}")

st.markdown("---")

# Plot prices
fig = plot_prices(df_lot, df_comp_lot, lot_selected)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""
---
### How to use this dashboard:
- Adjust the pricing sensitivity slider to see how prices react to occupancy changes.
- Change the base price to simulate different starting points.
- Select different parking lots from the dropdown to analyze their pricing.
""")