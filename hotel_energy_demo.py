import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Hotel Energy Benchmarking & Optimization Demo")

# Simulated data setup
np.random.seed(42)
hours = pd.date_range("2025-07-01", periods=24, freq="H")
hotel_energy = 100 + 20*np.sin(np.linspace(0, 3*np.pi, 24)) + np.random.normal(0, 5, 24)
benchmark_energy = 90 + 15*np.sin(np.linspace(0, 3*np.pi, 24)) + np.random.normal(0, 4, 24)

# Simulated occupancy: low occupancy from 0-6 and 22-23 hours
occupancy = [0.2 if (h.hour < 7 or h.hour > 21) else 0.9 for h in hours]

df = pd.DataFrame({
    "Hour": hours,
    "Hotel Energy (kWh)": hotel_energy,
    "Benchmark Energy (kWh)": benchmark_energy,
    "Occupancy": occupancy
})

# Show raw data table
st.subheader("Hourly Energy Consumption & Occupancy")
st.dataframe(df.style.format({"Hotel Energy (kWh)": "{:.1f}", "Benchmark Energy (kWh)": "{:.1f}", "Occupancy": "{:.1%}"}))

# Plot energy consumption vs benchmark
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(df["Hour"], df["Hotel Energy (kWh)"], label="Hotel Energy")
ax.plot(df["Hour"], df["Benchmark Energy (kWh)"], label="Benchmark Energy", linestyle='--')
ax.fill_between(df["Hour"], 0, 150, where=(df["Occupancy"] < 0.3), color='orange', alpha=0.2, label="Low Occupancy")
ax.set_ylabel("Energy (kWh)")
ax.set_xlabel("Time")
ax.legend()
ax.set_title("Energy Use vs Benchmark & Occupancy Periods")
st.pyplot(fig)

# Identify inefficiency during low occupancy
low_occ = df[df["Occupancy"] < 0.3]
inefficiency = low_occ[low_occ["Hotel Energy (kWh)"] > low_occ["Benchmark Energy (kWh)"]]

if not inefficiency.empty:
    st.warning("⚠️ Energy inefficiency detected during low occupancy hours!")
    st.write("During these times, your hotel consumes more energy than peers, suggesting potential savings.")
    st.write(inefficiency[["Hour", "Hotel Energy (kWh)", "Benchmark Energy (kWh)"]])
    
    st.markdown("### Recommendation:")
    st.info(
        "Consider reducing heating, cooling, or lighting during low occupancy hours (e.g., 10pm–6am). "
        "Implement automated controls or behavioral nudges to save energy and costs."
    )
else:
    st.success("No significant inefficiency detected during low occupancy periods.")

# Optional user interaction: simulate activating automation
if st.button("Activate Energy Saving Automation for Low Occupancy"):
    st.success("Automation triggered: HVAC and lighting schedules adjusted for low occupancy hours.")
