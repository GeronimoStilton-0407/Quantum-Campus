import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page Setup & Branding Configuration
st.set_page_config(
    page_title="Quantum Campus - Centralized Faculty & Student Hub",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File Paths
DATAFILE = r"C:\Users\jerom\Downloads\Certificates\Design_Thinking_Prototype_Dataset-2.xlsx"
LOGO_PATH = r"C:\Users\jerom\Downloads\Untitled design.png"  # Place "Untitled design.png" in the same directory as app.py

@st.cache_data
def load_initial_data():
    records = pd.read_excel(DATAFILE, sheet_name='Student_Records')
    achievements = pd.read_excel(DATAFILE, sheet_name='Student_Achievements')
    time_log = pd.read_excel(DATAFILE, sheet_name='Faculty_Admin_Time_Log')
    return records, achievements, time_log

# Initialize Session State
if 'records_df' not in st.session_state:
    try:
        r_df, a_df, l_df = load_initial_data()
        st.session_state.records_df = r_df
        st.session_state.achievements_df = a_df
        st.session_state.log_df = l_df
    except Exception as e:
        st.error(f"Error loading dataset from {DATAFILE}: {e}")
        st.stop()

records_df = st.session_state.records_df
achievements_df = st.session_state.achievements_df
log_df = st.session_state.log_df

# Sidebar Header & Quantum Campus Logo Integration
st.sidebar.markdown("<h2 style='text-align: center; color: #4FACFE;'>QUANTUM CAMPUS</h2>", unsafe_allow_html=True)

if os.path.exists(LOGO_PATH):
    st.sidebar.image(LOGO_PATH, use_container_width=True)
else:
    st.sidebar.info("💡 Place 'Untitled design.png' in your project folder to display the custom Quantum Campus logo.")

st.sidebar.title("📌 Navigation & Controls")
page = st.sidebar.radio(
    "Select Module",
    [
        "📊 Interactive Dashboard", 
        "🔍 Centralized Student Explorer", 
        "🤝 Opportunity & Skill Matcher", 
        "⏱️ Admin Workload & Time Simulator",
        "➕ Live Data Entry Portal"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("🌌 **Quantum Campus Platform:** Automating administrative overhead and connecting student talent with research and industry opportunities.")

# ---------------------------------------------------------
# HEADER WITH QUANTUM CAMPUS BRANDING
# ---------------------------------------------------------
header_col1, header_col2 = st.columns([1, 4])
with header_col1:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=140)
with header_col2:
    st.title("Quantum Campus - Academic & Research Hub")
    st.caption("Empowering Faculty Research & Student Academic Growth through Data Centralization")

st.markdown("---")

# ---------------------------------------------------------
# MODULE 1: INTERACTIVE DASHBOARD
# ---------------------------------------------------------
if page == "📊 Interactive Dashboard":
    st.subheader("🎓 Quantum Campus Analytics Overview")

    # Key Performance Metrics
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Students Tracked", len(records_df))
    kpi2.metric("Total Achievements Logged", len(achievements_df))
    kpi3.metric("Average Department CGPA", f"{records_df['CGPA'].mean():.2f}")
    kpi4.metric("Active Faculty Mentors", records_df['Mentor_Faculty'].nunique())

    st.markdown("---")

    col_left, col_right = st.columns(2)

    with col_left:
        st.write("#### Student Core Competency Distribution")
        strength_counts = records_df['Key_Strength_Area'].value_counts().reset_index()
        strength_counts.columns = ['Strength Area', 'Student Count']
        
        fig_strength = px.bar(
            strength_counts, 
            x='Student Count', 
            y='Strength Area', 
            orientation='h',
            color='Student Count',
            color_continuous_scale='Electric',
            title="Technical Skills Breakdown Across Campus"
        )
        fig_strength.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_strength, use_container_width=True)

    with col_right:
        st.write("#### Verified Student Achievements")
        ach_counts = achievements_df['Achievement_Type'].value_counts().reset_index()
        ach_counts.columns = ['Achievement Type', 'Count']
        
        fig_ach = px.pie(
            ach_counts, 
            names='Achievement Type', 
            values='Count', 
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_ach.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_ach, use_container_width=True)

# ---------------------------------------------------------
# MODULE 2: CENTRALIZED STUDENT EXPLORER
# ---------------------------------------------------------
elif page == "🔍 Centralized Student Explorer":
    st.subheader("🔍 Centralized Quantum Student Profiles")
    st.write("Eliminates fragmented Google Forms by consolidating academic records and extra-curricular achievements.")

    # Interactive Search & Filters
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        search_query = st.text_input("Search Name / Reg No:")
    with f_col2:
        dept_options = ["All"] + list(records_df['Department'].unique())
        selected_dept = st.selectbox("Department Filter", dept_options)
    with f_col3:
        skills_options = list(records_df['Key_Strength_Area'].unique())
        selected_skills = st.multiselect("Core Skills", skills_options, default=[])
    with f_col4:
        min_cgpa = st.slider("Minimum CGPA Filter", 0.0, 10.0, 0.0, step=0.1)

    # Corrected string filtering logic using .str.contains()
    filtered_df = records_df.copy()
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Student_Name'].str.contains(search_query, case=False, na=False) |
            filtered_df['Register_Number'].astype(str).str.contains(search_query, na=False)
        ]
    if selected_dept != "All":
        filtered_df = filtered_df[filtered_df['Department'] == selected_dept]
    if selected_skills:
        filtered_df = filtered_df[filtered_df['Key_Strength_Area'].isin(selected_skills)]
    filtered_df = filtered_df[filtered_df['CGPA'] >= min_cgpa]

    st.write(f"Showing **{len(filtered_df)}** matching student record(s):")
    st.dataframe(filtered_df, use_container_width=True)

    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export Filtered Student Records (CSV)",
        data=csv_data,
        file_name="Quantum_Campus_Student_Records.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.write("#### Detailed Interactive Student Inspection")
    if not filtered_df.empty:
        selected_student_id = st.selectbox("Select Student ID to view full profile:", filtered_df['Student_ID'].unique())
        stu_info = records_df[records_df['Student_ID'] == selected_student_id].iloc[0]
        stu_achievements = achievements_df[achievements_df['Student_ID'] == selected_student_id]

        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Student Name:** {stu_info['Student_Name']}")
            st.write(f"**Register Number:** {stu_info['Register_Number']}")
            st.write(f"**Department:** {stu_info['Department']} (Semester {stu_info['Semester']})")
        with c2:
            st.success(f"**CGPA:** {stu_info['CGPA']}")
            st.write(f"**Key Technical Strength:** {stu_info['Key_Strength_Area']}")
            st.write(f"**Assigned Mentor:** {stu_info['Mentor_Faculty']}")

        st.write("##### Verified Extra-Curricular Achievements")
        if not stu_achievements.empty:
            st.dataframe(stu_achievements[['Achievement_Type', 'Achievement_Title', 'Organization', 'Date', 'Level']], use_container_width=True)
        else:
            st.warning("No achievements logged yet for this student.")

# ---------------------------------------------------------
# MODULE 3: OPPORTUNITY & SKILL MATCHER
# ---------------------------------------------------------
elif page == "🤝 Opportunity & Skill Matcher":
    st.subheader("🤝 Quantum Skill Matcher & Industry Readiness Hub")
    st.write("Match research projects, hackathons, and corporate opportunities directly with high-performing students.")

    target_skill = st.selectbox("Select Target Skill Domain:", records_df['Key_Strength_Area'].unique())
    min_academic_cgpa = st.slider("Select Minimum Target CGPA:", 5.0, 10.0, 7.5, step=0.1)

    matching_students = records_df[
        (records_df['Key_Strength_Area'] == target_skill) & 
        (records_df['CGPA'] >= min_academic_cgpa)
    ]

    st.write(f"Found **{len(matching_students)}** qualified student candidates for **'{target_skill}'**:")

    if not matching_students.empty:
        for idx, row in matching_students.iterrows():
            ach_count = len(achievements_df[achievements_df['Student_ID'] == row['Student_ID']])
            with st.expander(f"⭐ {row['Student_Name']} (CGPA: {row['CGPA']}) - Mentor: {row['Mentor_Faculty']}"):
                st.write(f"**Register Number:** {row['Register_Number']}")
                st.write(f"**Department:** {row['Department']} | **Semester:** {row['Semester']}")
                st.write(f"**Verified Achievements On Record:** {ach_count}")
    else:
        st.warning("No students currently match the specified skill and CGPA criteria.")

# ---------------------------------------------------------
# MODULE 4: ADMIN WORKLOAD & TIME SIMULATOR
# ---------------------------------------------------------
elif page == "⏱️ Admin Workload & Time Simulator":
    st.subheader("⏱️ Faculty Workload & Time Recovery Simulator")
    st.write("Quantifying administrative workload to maximize faculty bandwidth for high-impact research.")

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Workload Distribution by Task Category")
        task_summary = log_df.groupby('Task_Type')['Time_Spent_Minutes'].sum() / 60
        fig_task = px.bar(
            task_summary.reset_index(), 
            x='Task_Type', 
            y='Time_Spent_Minutes',
            labels={'Time_Spent_Minutes': 'Hours Spent', 'Task_Type': 'Task Category'},
            color='Task_Type',
            title="Total Faculty Admin Hours Logged"
        )
        st.plotly_chart(fig_task, use_container_width=True)

    with col2:
        st.write("#### 💡 Interactive Time Recovery Calculator")
        st.write("Adjust task automation sliders to estimate reclaimed faculty research hours:")

        automation_data = st.slider("Data Collection Automation (%)", 0, 100, 85)
        automation_marks = st.slider("Marks Entry Automation (%)", 0, 100, 65)
        automation_records = st.slider("Record Correction Automation (%)", 0, 100, 75)

        data_hrs = log_df[log_df['Task_Type'] == 'Manual Data Collection (Forms/Follow-up)']['Time_Spent_Minutes'].sum() / 60
        marks_hrs = log_df[log_df['Task_Type'] == 'Marks Entry']['Time_Spent_Minutes'].sum() / 60
        records_hrs = log_df[log_df['Task_Type'] == 'Record Correction']['Time_Spent_Minutes'].sum() / 60

        saved_hrs = (data_hrs * automation_data/100) + (marks_hrs * automation_marks/100) + (records_hrs * automation_records/100)

        st.success(f"🚀 **Estimated Reclaimed Research Capacity:** `{saved_hrs:.1f} Hours` saved for faculty members!")

# ---------------------------------------------------------
# MODULE 5: LIVE DATA ENTRY PORTAL
# ---------------------------------------------------------
elif page == "➕ Live Data Entry Portal":
    st.subheader("➕ Quantum Campus Live Data Entry Portal")
    st.write("Log student achievements or faculty administrative time directly into the dynamic system.")

    entry_tab1, entry_tab2 = st.tabs(["Log Student Achievement", "Log Faculty Task Time"])

    with entry_tab1:
        st.write("#### Log a New Student Achievement")
        with st.form("achievement_form", clear_on_submit=True):
            student_id = st.selectbox("Select Student:", records_df['Student_ID'] + " - " + records_df['Student_Name'])
            ach_type = st.selectbox("Achievement Type:", ["Certification", "Publication", "Internship", "Hackathon", "Workshop_Lead", "Competition"])
            title = st.text_input("Achievement Title:")
            org = st.text_input("Issuing Organization / Host:")
            date = st.date_input("Date Received:")
            level = st.selectbox("Level:", ["Department", "State", "National", "International"])

            submitted = st.form_submit_button("Submit Achievement")
            if submitted:
                s_id = student_id.split(" - ")[0]
                new_ach = pd.DataFrame([{
                    "Achievement_ID": f"ACH{len(achievements_df)+1:03d}",
                    "Student_ID": s_id,
                    "Achievement_Type": ach_type,
                    "Achievement_Title": title,
                    "Organization": org,
                    "Date": str(date),
                    "Level": level
                }])
                st.session_state.achievements_df = pd.concat([st.session_state.achievements_df, new_ach], ignore_index=True)
                st.success(f"Successfully logged achievement '{title}' for {student_id} into Quantum Campus DB!")

    with entry_tab2:
        st.write("#### Log Administrative Time Entry")
        with st.form("time_log_form", clear_on_submit=True):
            fac_name = st.selectbox("Faculty Name:", log_df['Faculty_Name'].unique())
            task_type = st.selectbox("Task Category:", log_df['Task_Type'].unique())
            mins_spent = st.number_input("Time Spent (Minutes):", min_value=5, max_value=480, step=5)
            tool = st.selectbox("Tool Used:", ["Quantum Campus Hub", "Knowledge Pro", "Espro", "MS Office", "Email/Verbal Follow-up"])
            count = st.number_input("Students Handled:", min_value=1, max_value=200, step=1)

            log_submitted = st.form_submit_button("Log Administrative Activity")
            if log_submitted:
                new_log = pd.DataFrame([{
                    "Log_ID": f"LOG{len(log_df)+1:03d}",
                    "Faculty_Name": fac_name,
                    "Date": pd.Timestamp.now().strftime('%Y-%m-%d'),
                    "Task_Type": task_type,
                    "Time_Spent_Minutes": mins_spent,
                    "Tool_Used": tool,
                    "Students_Handled_Count": count
                }])
                st.session_state.log_df = pd.concat([st.session_state.log_df, new_log], ignore_index=True)
                st.success("Successfully logged time activity!")