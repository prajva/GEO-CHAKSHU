import streamlit as st
import pandas as pd
import numpy as np
import random

# Page config
st.set_page_config(page_title="Geo-Chakshu", layout="wide", page_icon="🛰️")

# --- INITIALIZE DATA (Session State) ---
# This ensures the website remembers our list when we add or remove items
if 'projects' not in st.session_state:
    st.session_state.projects = [
        {"id": 1, "name": "House #A-104, Kotturu", "score": 91, "status": "Verified", "claimed": "12 Mar 2026"},
        {"id": 2, "name": "House #A-118, Kotturu", "score": 12, "status": "Flagged", "claimed": "12 Mar 2026"},
        {"id": 3, "name": "House #A-121, Kotturu", "score": 76, "status": "Review", "claimed": "28 Feb 2026"},
        {"id": 4, "name": "Village Road, Ch. 4–6 km", "score": 8, "status": "Flagged", "claimed": "05 Apr 2026"}
    ]

# App Header
st.title("Geo-Chakshu 🛰️")
st.subheader("Autonomous Infrastructure & Welfare Audit Engine")

# Top Metrics
df = pd.DataFrame(st.session_state.projects)

col1, col2, col3 = st.columns(3)
col1.metric(label="Projects tracked", value=len(st.session_state.projects))
if not df.empty:
    col2.metric(label="Flagged for review", value=len(df[df['status'] == 'Flagged']))
    col3.metric(label="Avg confidence", value=f"{int(df['score'].mean())}%")
else:
    col2.metric(label="Flagged for review", value=0)
    col3.metric(label="Avg confidence", value="0%")

st.divider()

# --- ADMIN PANEL (Add/Remove) ---
with st.sidebar:
    st.header("⚙️ Admin Controls")
    
    st.write("**Add a New Claim:**")
    with st.form("add_form"):
        new_name = st.text_input("Project Name (e.g. House #C-302)")
        new_date = st.date_input("Claimed Completion Date")
        submitted = st.form_submit_button("Run Radar Scan & Add")
        
        if submitted and new_name:
            # Simulate the AI running a scan and generating a random confidence score
            new_score = random.randint(5, 95)
            if new_score >= 80:
                new_status = "Verified"
            elif new_score >= 50:
                new_status = "Review"
            else:
                new_status = "Flagged"
                
            new_project = {
                "id": len(st.session_state.projects) + 1,
                "name": new_name,
                "score": new_score,
                "status": new_status,
                "claimed": new_date.strftime("%d %b %Y")
            }
            st.session_state.projects.append(new_project)
            st.rerun() # Refreshes the page to show the new data
            
    st.divider()
    
    st.write("**Remove a Project:**")
    if len(st.session_state.projects) > 0:
        project_names = [p['name'] for p in st.session_state.projects]
        remove_target = st.selectbox("Select project to delete", project_names)
        if st.button("Delete Project"):
            st.session_state.projects = [p for p in st.session_state.projects if p['name'] != remove_target]
            st.rerun()

# --- MAIN LAYOUT ---
left_pane, right_pane = st.columns([2, 1])

with left_pane:
    st.write("### Map Overview")
    st.write("Sample block: **Machilipatnam Mandal cluster** — PMAY-G houses, radar-derived confidence score")
    
    # Generate random map coordinates based on how many projects exist
    if not df.empty:
        map_data = pd.DataFrame(
            np.random.randn(len(st.session_state.projects), 2) / [50, 50] + [16.17, 81.13],
            columns=['lat', 'lon']
        )
        st.map(map_data)
    else:
        st.info("No projects currently tracked on the map.")

with right_pane:
    st.write("### Claimed Projects")
    
    if len(st.session_state.projects) == 0:
        st.write("No projects found.")
        
    for proj in st.session_state.projects:
        with st.expander(f"{proj['name']} - {proj['status']}"):
            st.write(f"**Claimed Date:** {proj['claimed']}")
            st.write(f"**Confidence Score:** {proj['score']}/100")
            
            if proj['status'] == 'Flagged':
                st.error("Likely fraudulent (below 50)")
            elif proj['status'] == 'Review':
                st.warning("Needs review (50–79)")
            else:
                st.success("Verified pattern (80–100)")
            
            # Mock Time-series data chart
            chart_data = pd.DataFrame(
                np.random.randn(8, 1) * 10 + proj['score'],
                columns=['Signature']
            )
            st.line_chart(chart_data)
