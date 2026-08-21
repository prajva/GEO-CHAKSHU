import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Geo-Chakshu", layout="wide", page_icon="🛰️")

# App Header
st.title("Geo-Chakshu 🛰️")
st.subheader("Autonomous Infrastructure & Welfare Audit Engine[cite: 1]")

# Dummy Data based on your HTML[cite: 1]
projects = [
    {"id": 1, "name": "House #A-104, Kotturu", "score": 91, "status": "Verified", "claimed": "12 Mar 2026"},
    {"id": 2, "name": "House #A-118, Kotturu", "score": 12, "status": "Flagged", "claimed": "12 Mar 2026"},
    {"id": 3, "name": "House #A-121, Kotturu", "score": 76, "status": "Review", "claimed": "28 Feb 2026"},
    {"id": 4, "name": "Village Road, Ch. 4–6 km", "score": 8, "status": "Flagged", "claimed": "05 Apr 2026"}
]
df = pd.DataFrame(projects)

# Top Metrics[cite: 1]
col1, col2, col3 = st.columns(3)
col1.metric(label="Projects tracked", value=len(projects)) #[cite: 1]
col2.metric(label="Flagged for review", value=len(df[df['status'] == 'Flagged'])) #[cite: 1]
col3.metric(label="Avg confidence", value=f"{int(df['score'].mean())}%") #[cite: 1]

st.divider()

# Layout: Map on left, Sidebar list on right
left_pane, right_pane = st.columns([2, 1])

with left_pane:
    st.write("### Map Overview")
    st.write("Sample block: **Machilipatnam Mandal cluster** — PMAY-G houses, radar-derived confidence score[cite: 1]")
    
    # Streamlit can render a simple map if you provide lat/lon data
    map_data = pd.DataFrame(
        np.random.randn(4, 2) / [50, 50] + [16.17, 81.13],
        columns=['lat', 'lon']
    )
    st.map(map_data)

with right_pane:
    st.write("### Claimed Projects[cite: 1]")
    for proj in projects:
        with st.expander(f"{proj['name']} - {proj['status']}"):
            st.write(f"**Claimed Date:** {proj['claimed']}")
            st.write(f"**Confidence Score:** {proj['score']}/100") #[cite: 1]
            
            if proj['status'] == 'Flagged':
                st.error("Likely fraudulent (below 50)[cite: 1]")
            elif proj['status'] == 'Review':
                st.warning("Needs review (50–79)[cite: 1]")
            else:
                st.success("Verified pattern (80–100)[cite: 1]")
            
            # Mock Time-series data chart[cite: 1]
            chart_data = pd.DataFrame(
                np.random.randn(8, 1) * 10 + proj['score'],
                columns=['Signature']
            )
            st.line_chart(chart_data)