import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="🚀 Data Sweeper", layout='wide')

#custom css
st.markdown("""
      <style>
      .stApp{
          background-color:black;
          color:white;
          }    
          </style>
           """,
           unsafe_allow_html=True   
)

# Sidebar for user input and file upload
st.sidebar.title("User Input")
user_name = st.sidebar.text_input("Enter Your Name")

uploaded_files = st.sidebar.file_uploader(
    "Upload your files (CSV or Excel):", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

if user_name:
    st.sidebar.success(f"Welcome, {user_name}!")

st.title("🚀 DataSweeper Sterling Integrator By Abdullah Raees Khan ")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization creating the project For quater3.")

if uploaded_files:
    st.subheader(f"Uploaded Files by {user_name}")
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported File Type: {file_ext}")
            continue  # Skip unsupported files

        st.write(f"📂 **File Name:** {file.name}")
        st.write(f"📏 **File Size:** {file.size / 1024:.2f} KB")

        # Show 5 rows of the dataframe
        st.write("📊 **Preview of the DataFrame**")
        st.dataframe(df, height=300)

        # Data Cleaning Options
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ **Duplicates Removed!**")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include={'number'}).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ **Missing Values Have Been Filled!**")

        # Select columns to keep
        st.subheader("📝 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data Visualization
        st.subheader("📈 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # **Conversion Options**
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"Convert {file.name} to {conversion_type}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            # Download button
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer.getvalue(),
                file_name=file_name,
                mime=mime_type
            )

st.success("✅ All files processed successfully!")