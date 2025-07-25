
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Paragliding LC Lead Zone Calculator")

# Ввід параметрів таску
task_distance = st.number_input("Task distance (km)", min_value=10.0, max_value=300.0, value=41.6, step=0.1)
lead_cut_km = st.number_input("Non-leading final segment (km)", min_value=0.0, max_value=20.0, value=5.0, step=0.1)

effective_distance = task_distance - lead_cut_km

# Побудова кривої ваги
x = np.linspace(0, effective_distance, 500)
center = effective_distance / 2
width = effective_distance / 2
weights = np.exp(-((x - center)**2) / (2 * (width / 2.5)**2))

threshold = 0.9 * np.max(weights)
lead_zone = x[(weights >= threshold)]
lead_zone_start = np.min(lead_zone)
lead_zone_end = np.max(lead_zone)

st.subheader("Optimal leading zone")
st.markdown(f"**Maximum lead points accrue between:**  
:orange[**{lead_zone_start:.1f} km**] and :orange[**{lead_zone_end:.1f} km**] of the task")

# Побудова графіка
fig, ax = plt.subplots(figsize=(8, 3))
ax.plot(x, weights, label='Leading Weight Curve')
ax.axvspan(lead_zone_start, lead_zone_end, color='orange', alpha=0.4,
            label=f'Max Lead Zone: {lead_zone_start:.1f}–{lead_zone_end:.1f} km')
ax.set_xlabel("Distance in task (km)")
ax.set_ylabel("Relative weight")
ax.set_title("Leading Coefficient Weight Curve")
ax.grid(True)
ax.legend()
st.pyplot(fig)

st.markdown("""
This calculator estimates where in the task distance the maximum LC weight is applied.
Values are based on a Gaussian model used in GAP scoring.
""")
