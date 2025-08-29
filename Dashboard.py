import streamlit as st
import pandas as pd

# -------------------------------
# Streamlit Dashboard
# -------------------------------
st.set_page_config(page_title="Student Allotment Dashboard", layout="wide")

st.title("🎓 Student Allotment Dashboard")
st.markdown("Upload your **final output file** and explore student allotments & matching scores.")

# -------------------------------
# File Upload
# -------------------------------
uploaded_file = st.file_uploader("📂 Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read CSV or Excel
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Ensure required columns exist
    required_cols = {"UniqueID", "StudentName", "CourseAllotted", "Score"}
    if not required_cols.issubset(df.columns):
        st.error(f"❌ Uploaded file must contain columns: {required_cols}")
    else:
        # -------------------------------
        # Search by Unique ID
        # -------------------------------
        st.sidebar.header("🔍 Search Student")
        unique_id = st.sidebar.text_input("Enter Student Unique ID:")

        if unique_id:
            try:
                unique_id = int(unique_id)
                student_data = df[df["UniqueID"] == unique_id]

                if not student_data.empty:
                    st.success(f"✅ Student Found: {student_data.iloc[0]['StudentName']}")
                    st.table(student_data)

                    # Matching Score Chart for Student
                    st.subheader("📈 Matching Score (Selected Student)")
                    st.bar_chart(student_data.set_index("StudentName")["Score"])
                else:
                    st.error("❌ No record found for this Unique ID.")
            except ValueError:
                st.warning("⚠️ Please enter a valid numeric Unique ID.")

        # -------------------------------
        # Filters Section
        # -------------------------------
        st.sidebar.header("⚙️ Filters")

        # Course Filter
        courses = ["All"] + sorted(df["CourseAllotted"].unique().tolist())
        selected_course = st.sidebar.selectbox("Filter by Course", courses)

        # Minimum Score Filter
        min_score = st.sidebar.slider("Minimum Matching Score", 
                                    int(df["Score"].min()), 
                                    int(df["Score"].max()), 
                                    int(df["Score"].min()))

        # Apply Filters
        filtered_df = df.copy()
        if selected_course != "All":
            filtered_df = filtered_df[filtered_df["CourseAllotted"] == selected_course]

        filtered_df = filtered_df[filtered_df["Score"] >= min_score]

        # -------------------------------
        # Display Filtered Results
        # -------------------------------
        st.subheader("📊 Filtered Student Allotments")
        st.dataframe(filtered_df)

        # Overall Distribution Chart
        st.subheader("📊 Matching Score Distribution (Filtered)")
        st.bar_chart(filtered_df.set_index("StudentName")["Score"])

        # -------------------------------
        # Expandable Full Data
        # -------------------------------
        with st.expander("📂 View Complete Dataset"):
            st.dataframe(df)

else:
    st.info("👆 Please upload a **CSV or Excel file** to get started.")
