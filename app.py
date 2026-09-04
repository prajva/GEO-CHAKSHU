import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Geo-Chakshu Pro", layout="wide", page_icon="🛰️", initial_sidebar_state="expanded")

# --- INITIALIZE PRO DATA ---
if 'projects' not in st.session_state or (len(st.session_state.projects) > 0 and 'budget' not in st.session_state.projects[0]):
    st.session_state.projects = [
        {"id": 1, "name": "House #A-104, Kotturu", "score": 91, "status": "Verified", "claimed": "12 Mar 2026", "lat": 16.18, "lon": 81.14, "color": "#00cc96", "budget": 120000},
        {"id": 2, "name": "House #A-118, Kotturu", "score": 12, "status": "Flagged", "claimed": "12 Mar 2026", "lat": 16.16, "lon": 81.12, "color": "#ff4b4b", "budget": 120000},
        {"id": 3, "name": "House #A-121, Kotturu", "score": 76, "status": "Review", "claimed": "28 Feb 2026", "lat": 16.17, "lon": 81.15, "color": "#ffa421", "budget": 120000},
        {"id": 4, "name": "Village Road, Ch. 4–6 km", "score": 8, "status": "Flagged", "claimed": "05 Apr 2026", "lat": 16.15, "lon": 81.13, "color": "#ff4b4b", "budget": 4500000}
    ]

# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- APP HEADER ---
st.title("🛰️ Geo-Chakshu Enterprise")
st.markdown("**Autonomous Infrastructure & Welfare Audit Engine** | *Advanced Analytics Module*")

# --- SIDEBAR: ADMIN LOCK & CONTROLS ---
with st.sidebar:
    st.header("⚙️ System Controls")
    
    # Check if the user is logged in
    if not st.session_state.authenticated:
        st.info("🔒 Admin access required to run scans or alter thresholds.")
        
        # Checkbox to toggle showing the password
        show_password = st.checkbox("Show password")
        
        # Switch the input type based on the checkbox
        pass_type = "default" if show_password else "password"
        entered_password = st.text_input("Enter Admin Password", type=pass_type)
        
        if st.button("Login", use_container_width=True):
            if entered_password == "Terraria":
                st.session_state.authenticated = True
                st.success("Access Granted!")
                time.sleep(0.5)
                st.rerun() # Refresh to show admin panel
            else:
                st.error("Access Denied. Password is case-sensitive.")
                
    # Show this ONLY if they are logged in!
    if st.session_state.authenticated:
        if st.button("🔓 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
            
        st.divider()
        
        st.write("**AI Risk Threshold**")
        fraud_threshold = st.slider("Flag projects scoring below:", min_value=10, max_value=80, value=50, step=5)
        
        st.divider()
        
        st.write("**📡 Trigger Manual Satellite Scan:**")
        with st.form("add_form"):
            new_name = st.text_input("Project ID (e.g. House #C-302)")
            new_budget = st.number_input("Sanctioned Budget (₹)", min_value=50000, max_value=5000000, value=120000, step=10000)
            new_date = st.date_input("Claimed Date")
            submitted = st.form_submit_button("Launch InSAR Scan", use_container_width=True)
            
            if submitted and new_name:
                with st.spinner("Aligning Sentinel-1 Satellite Trajectory..."):
                    time.sleep(1)
                with st.spinner("Downloading and processing SAR data..."):
                    time.sleep(1.5)
                    
                new_score = random.randint(5, 95)
                
                new_project = {
                    "id": len(st.session_state.projects) + 1,
                    "name": new_name,
                    "score": new_score,
                    "claimed": new_date.strftime("%d %b %Y"),
                    "lat": 16.17 + random.uniform(-0.03, 0.03),
                    "lon": 81.13 + random.uniform(-0.03, 0.03),
                    "budget": new_budget
                }
                st.session_state.projects.append(new_project)
                st.toast(f"Scan complete for {new_name}! Confidence: {new_score}%", icon="✅")
                time.sleep(0.5)
                st.rerun()
    else:
        # Default threshold if admin is locked out
        fraud_threshold = 50

# --- RECALCULATE STATUS BASED ON SLIDER ---
for p in st.session_state.projects:
    if p['score'] >= 80:
        p['status'], p['color'] = "Verified", "#00cc96"
    elif p['score'] >= fraud_threshold:
        p['status'], p['color'] = "Review", "#ffa421"
    else:
        p['status'], p['color'] = "Flagged", "#ff4b4b"

df = pd.DataFrame(st.session_state.projects)

# --- TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric(label="Total Assets Scanned", value=len(st.session_state.projects))
flagged_df = df[df['status'] == 'Flagged']
col2.metric(label="🚨 Fraud Alerts", value=len(flagged_df))
col3.metric(label="📊 Network Accuracy", value=f"{int(df['score'].mean()) if not df.empty else 0}%")
money_saved = flagged_df['budget'].sum() if not flagged_df.empty else 0
col4.metric(label="💰 Public Funds Protected", value=f"₹{money_saved:,}")

st.divider()

# --- MAIN DASHBOARD TABS ---
tab1, tab2, tab3 = st.tabs(["🌍 Geospatial View", "📋 Audit Database", "📥 Export & Reports"])

with tab1:
    st.subheader("Live Satellite Monitoring Network")
    st.caption("Map updates dynamically based on the Admin AI Risk Threshold.")
    if not df.empty:
        st.map(df, latitude='lat', longitude='lon', color='color', size=200)

with tab2:
    filter_choice = st.radio("Filter Database:", ["All Assets", "🚨 Flagged", "⚠️ Review", "✅ Verified"], horizontal=True)
    if filter_choice != "All Assets":
        display_df = df[df['status'] == filter_choice.split(" ")[1]]
    else:
        display_df = df
        
    for proj in display_df.to_dict('records'):
        status_icon = "🚨" if proj['status'] == "Flagged" else "⚠️" if proj['status'] == "Review" else "✅"
        
        with st.expander(f"{status_icon} {proj['name']} | Confidence: {proj['score']}% | Budget: ₹{proj['budget']:,}"):
            sub_tab1, sub_tab2, sub_tab3 = st.tabs(["📡 SAR Signature", "📸 Optical Data", "⚡ Take Action"])
            
            with sub_tab1:
                st.markdown(f"**Claimed Completion:** {proj['claimed']}")
                base_pattern = [40, 42, 39, 41, 40, 38, 41, 39] if proj['status'] == 'Flagged' else ([36, 33, 25, 29, 44, 58, 70, 76] if proj['status'] == 'Review' else [40, 38, 20, 18, 85, 88, 90, 91])
                noise = np.random.normal(0, 2, 8)
                chart_data = pd.DataFrame([max(0, min(100, val + n)) for val, n in zip(base_pattern, noise)], index=['M-7', 'M-6', 'M-5', 'M-4', 'M-3', 'M-2', 'M-1', 'Now'], columns=['Backscatter Intensity'])
                st.line_chart(chart_data, height=200)
            
            with sub_tab2:
                st.info("Sentinel-2 Optical validation requires cloud-free imagery. Feature available in Tier 2 Audit.")
                st.button("Request High-Res Drone Flyover", key=f"drone_{proj['id']}")
                
            with sub_tab3:
                if proj['status'] == 'Flagged':
                    st.error("Fraud protocol activated. Recommended action: Halt payment.")
                    if st.button("Generate Show-Cause Notice", key=f"notice_{proj['id']}"):
                        st.success(f"Official notice drafted for {proj['name']} and sent to Block Development Officer.")
                else:
                    st.success("Asset verified. Clear for DBT payment release.")

with tab3:
    st.subheader("Generate Compliance Reports")
    st.write("Download the current audit findings as a CSV for offline review or to upload to the state MIS portal.")
    
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Audit Data (CSV)",
        data=csv,
        file_name='geochakshu_audit_report.csv',
        mime='text/csv',
    )
