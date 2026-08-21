import streamlit as st
import pandas as pd
import numpy as np
import random

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Geo-Chakshu", layout="wide", page_icon="🛰️", initial_sidebar_state="expanded")

# --- INITIALIZE DATA (Session State) ---
# Added fixed latitudes, longitudes, and color codes for a better map experience
if 'projects' not in st.session_state:
    st.session_state.projects = [
        {"id": 1, "name": "House #A-104, Kotturu", "score": 91, "status": "Verified", "claimed": "12 Mar 2026", "lat": 16.18, "lon": 81.14, "color": "#00cc96"},
        {"id": 2, "name": "House #A-118, Kotturu", "score": 12, "status": "Flagged", "claimed": "12 Mar 2026", "lat": 16.16, "lon": 81.12, "color": "#ff4b4b"},
        {"id": 3, "name": "House #A-121, Kotturu", "score": 76, "status": "Review", "claimed": "28 Feb 2026", "lat": 16.17, "lon": 81.15, "color": "#ffa421"},
        {"id": 4, "name": "Village Road, Ch. 4–6 km", "score": 8, "status": "Flagged", "claimed": "05 Apr 2026", "lat": 16.15, "lon": 81.13, "color": "#ff4b4b"}
    ]

# --- APP HEADER ---
st.title("🛰️ Geo-Chakshu")
st.markdown("**Autonomous Infrastructure & Welfare Audit Engine** | *Smart India Hackathon Prototype*")

df = pd.DataFrame(st.session_state.projects)

# --- TOP METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Projects Tracked", value=len(st.session_state.projects))
with col2:
    flagged_count = len(df[df['status'] == 'Flagged']) if not df.empty else 0
    st.metric(label="🚨 Flagged for Review", value=flagged_count)
with col3:
    avg_score = f"{int(df['score'].mean())}%" if not df.empty else "0%"
    st.metric(label="📊 Average Confidence", value=avg_score)

st.divider()

# --- ADMIN PANEL (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Admin Controls")
    st.markdown("Simulate new data entry from the State MIS portal.")
    
    with st.form("add_form"):
        new_name = st.text_input("Project Name", placeholder="e.g. House #C-302")
        new_date = st.date_input("Claimed Completion Date")
        submitted = st.form_submit_button("Run Radar Scan & Add", use_container_width=True)
        
        if submitted and new_name:
            new_score = random.randint(5, 95)
            if new_score >= 80:
                new_status, new_color = "Verified", "#00cc96"
            elif new_score >= 50:
                new_status, new_color = "Review", "#ffa421"
            else:
                new_status, new_color = "Flagged", "#ff4b4b"
                
            new_project = {
                "id": len(st.session_state.projects) + 1,
                "name": new_name,
                "score": new_score,
                "status": new_status,
                "claimed": new_date.strftime("%d %b %Y"),
                "lat": 16.17 + random.uniform(-0.03, 0.03),
                "lon": 81.13 + random.uniform(-0.03, 0.03),
                "color": new_color
            }
            st.session_state.projects.append(new_project)
            st.rerun()
            
    st.divider()
    st.write("**Remove a Project:**")
    if len(st.session_state.projects) > 0:
        project_names = [p['name'] for p in st.session_state.projects]
        remove_target = st.selectbox("Select project to delete", project_names, label_visibility="collapsed")
        if st.button("Delete Selected", use_container_width=True):
            st.session_state.projects = [p for p in st.session_state.projects if p['name'] != remove_target]
            st.rerun()

# --- MAIN LAYOUT & FILTER ---
# Add a filter to make the dashboard interactive
filter_choice = st.radio("Filter Dashboard View:", ["All Projects", "🚨 Flagged Only", "✅ Verified Only"], horizontal=True)

# Apply the filter to our dataframe
if filter_choice == "🚨 Flagged Only":
    filtered_df = df[df['status'] == 'Flagged']
elif filter_choice == "✅ Verified Only":
    filtered_df = df[df['status'] == 'Verified']
else:
    filtered_df = df

left_pane, right_pane = st.columns([1.5, 1], gap="large")

with left_pane:
    st.subheader("📍 Satellite Map Overview")
    st.caption("Sample block: **Machilipatnam Mandal cluster**")
    
    if not filtered_df.empty:
        # Render map with colored dots based on status
        st.map(filtered_df, latitude='lat', longitude='lon', color='color', size=150)
    else:
        st.info("No projects match the current filter.")

with right_pane:
    st.subheader("📋 Audit List")
    
    if filtered_df.empty:
        st.write("No projects found.")
        
    # Convert filtered dataframe back to list of dicts for easy iteration
    display_projects = filtered_df.to_dict('records')
    
    for proj in display_projects:
        # Create a clean header for each dropdown
        status_icon = "🚨" if proj['status'] == "Flagged" else "⚠️" if proj['status'] == "Review" else "✅"
        
        with st.expander(f"{status_icon} {proj['name']} - Score: {proj['score']}"):
            
            # Use columns inside the expander for cleaner layout
            c1, c2 = st.columns(2)
            c1.markdown(f"**Claimed Date:**\n{proj['claimed']}")
            c2.markdown(f"**Status:**\n{proj['status']}")
            
            if proj['status'] == 'Flagged':
                st.error("No construction signature detected. Likely fraudulent.")
                # Fake flatline data
                base_pattern = [40, 42, 39, 41, 40, 38, 41, 39] 
            elif proj['status'] == 'Review':
                st.warning("Weak signature detected. Secondary check required.")
                # Fake weak curve
                base_pattern = [36, 33, 25, 29, 44, 58, 70, 76]
            else:
                st.success("Strong construction signature detected. Verified.")
                # Fake successful build curve (dip then huge jump)
                base_pattern = [40, 38, 20, 18, 85, 88, 90, 91]
            
            # Add slight random noise so the charts look like real organic data
            noise = np.random.normal(0, 2, 8)
            final_pattern = [max(0, min(100, val + n)) for val, n in zip(base_pattern, noise)]
            
            chart_data = pd.DataFrame(
                final_pattern,
                index=['M-7', 'M-6', 'M-5', 'M-4', 'M-3', 'M-2', 'M-1', 'Now'],
                columns=['Radar Intensity']
            )
            
            st.caption("Satellite Backscatter Signature (Last 8 Months)")
            st.line_chart(chart_data)








