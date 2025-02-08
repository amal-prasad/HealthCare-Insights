import base64
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import warnings
import json
warnings.filterwarnings("ignore")

def load_lottie(filepath: str):
    """
    Load a Lottie animation from a JSON file.

    This function opens the specified JSON file, which contains the data defining a Lottie animation.
    Lottie files include details such as animation frames, vector paths, and other configuration
    information that allows libraries like streamlit_lottie to render smooth, scalable animations.
    """
    with open(filepath, 'r') as f:
        return json.load(f)

def SQL_query(query):
    """
    Connect to the SQL database 'health', execute the provided SQL query,
    and return the fetched results as a pandas DataFrame.
    """
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="health",
        cursorclass=pymysql.cursors.DictCursor  
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)  
            results = cursor.fetchall()  
    finally:
        connection.close()  

    # Ensure results are properly converted into a DataFrame
    df = pd.DataFrame(results)
    
    return df

# Set the Streamlit page configuration, including the page title, icon, layout, and initial sidebar state.
st.set_page_config(
    page_title="Health Care Insights",
    page_icon="🩺",
    layout="centered",  # Options: "centered" or "wide"
    initial_sidebar_state="expanded"
)

# CSS Styling for the Dashboard
st.markdown("""
<style>
    /* Modern Card Styling with Understated Dotted Background */

    .stApp {
        background-color: #C7D2E8; /* Lightened muted blue-silver background */
        background-image: radial-gradient(circle, rgba(255,255,255,0.5) 1px, transparent 1px);
        background-size: 20px 20px; /* Increased space between the dots */
        filter: drop-shadow(2px 2px 2px rgba(0, 0, 0, 0.3)); /* Added shadow to the dots */
    }
    
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Section Headers with a Static Background */
    .section-header {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
    }
    
    /* Hover Effects for Cards */
    .hover-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .hover-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Progress Bars with Static Background */
    .stProgress > div > div > div > div {
        background-image: linear-gradient(45deg, #1e3c72, #2a5298);
    }
    
    /* Pulsing Effect for Important Elements */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Smooth Transitions */
    * {
        transition: all 0.3s ease-in-out;
    }
    
    /* Pulsing Animation */
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    /* Modern Sidebar Styling */
    .css-1d391kg {
        background-color: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Custom Button Styling */
    .stButton>button {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Metric Card Styling */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px 0;
    }
    
    /* Chart Container Styling */
    .chart-container {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 20px 0;
    }
    
    /* Loading Animation */
    .stSpinner {
        animation: spin 1s linear infinite;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #1e3c72;
        border-radius: 50%;
        width: 40px;
        height: 40px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Modify the sidebar radio to include icons
st.markdown("""
    <style>
    .css-1p2iens {
        font-size: 1.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Add custom CSS for the sidebar
st.markdown("""
    <style>
    /* Sidebar styling with added pattern overlay on a dark blue background */
    [data-testid="stSidebar"] {
        position: relative;
        background-color: #1e3c72; /* Dark blue base */
        background-image: 
            repeating-linear-gradient(45deg, rgba(255,255,255,0.05), rgba(255,255,255,0.05) 5px, transparent 5px, transparent 10px);
        background-blend-mode: overlay;
        color: white;
        overflow: hidden;
    }
    
    /* Navigation item styling */
    [data-testid="stSidebar"] .css-1v3fvcr {
        color: white !important;
        position: relative;
        z-index: 1;
    }
    
    /* Radio button styling */
    [data-testid="stSidebar"] .css-1v3fvcr [role="radiogroup"] > label {
        color: white !important;
        position: relative;
        z-index: 1;
    }
    </style>
    """, unsafe_allow_html=True)
st.sidebar.markdown("""
    <style>
        /* Add text shadow to sidebar title, navigation items, and radio button labels to create a pop-out effect */
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] .css-1v3fvcr,
        [data-testid="stSidebar"] label {
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
        }
    </style>
""", unsafe_allow_html=True)

# Add sidebar title
st.sidebar.title("Contents")

rd = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📈 Admit and Discharge Trends", 
        "💰 Billing Amount and Health Insurance Analysis",
        "🏥 Diagnosis Statistics",
        "🛏️ Bed Occupancy Statistics", 
        "⏱️ Length of Stay",
        "👨‍⚕️ Doctor's Statistics",
        "📋 Follow-up Statistics",
        "🚨 Patients in Critical Condition",
        "🔬 Test Analysis",
        "💡 Suggestions for the Hospital"
    ],
    label_visibility="visible"
)

# This effectively removes any prefix (like an icon) preceding the first space.
rd = rd.split(" ", 1)[1] if " " in rd else rd

if rd == "Home":
    st.markdown("""
    <style>
        /* Elegant styling for boxes: Trends, Utilization, and Decision Making with a blue theme and pop-out shadow effect */
        .content-box {
            border: 2px solid #2980b9; /* Elegant blue border */
            background: linear-gradient(135deg, #d6eaf8, #aed6f1); /* Soft, elegant blue gradient */
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3); /* Pop-out shadow effect */
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .content-box:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        }
        .subheader.trends {
            background-color: #2980b9; /* Blue shade for trends */
            color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Pop-out shadow effect */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
        }
        .subheader.utilization {
            background-color: #3498db; /* Elegant blue */
            color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Pop-out shadow effect */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
        }
        .subheader.decision-making {
            background-color: #2471a3; /* Blue shade for decision-making */
            color: #ffffff;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Pop-out shadow effect */
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
        }
        /* Added spacing and pop out animation for the subheader (title box within the content box) */
        .content-box .subheader {
            margin-bottom: 15px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .content-box .subheader:hover {
            transform: translateY(-5px) scale(1.03);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the animated title
    st.markdown("""
    <div class="title">Healthcare Insights</div>
    """, unsafe_allow_html=True)

    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Display the animated sub-title with a permanent gradient animation effect
    st.markdown("""
    <style>
        .subtitle-objective {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(-45deg, #1e3c72, #2a5298, #1a75bb, #0d3a8b);
            background-size: 400% 400%;
            padding: 10px;
            border-radius: 10px;
            animation: gradientShift 10s ease infinite;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.7);
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
    <div class="subtitle-objective">Objective</div>
    """, unsafe_allow_html=True)   

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        /* Animated Title with enhanced pulse intensity */
        .title {
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.6);
        }
        /* Section Box with hover animation */
        .section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            margin: 20px 0px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .section:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        }
        .section h2 {
            color: #1e3c72;
            font-size: 28px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        /* Divider styling */
        .divider {
            border-top: 2px solid #2a5298;
            margin: 20px 0;
        }
        /* Image styling with hover effect */
        .image-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 20px 0;
        }
        .image {
            border-radius: 15px;
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .image:hover {
            transform: scale(1.05);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
        }
        /* Keyframe for the pulse animation with increased intensity */
        @keyframes pulse {
            0%   { transform: scale(1); }
            50%  { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        /* 3D effect for paragraph texts in content boxes */
        .content-box p {
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Treatment & Service Trends Section
    st.markdown("""
    <div class="content-box">
        <div class="subheader trends">
            <h2>📊 Treatment & Service Trends</h2>
        </div>
        <p><b>💡 Identify the most common procedures</b> and <b>treatment frequencies</b> in your hospital.</p>
        <p><b>📅 Detect peak patient visit times</b> and <b>seasonal trends</b> to enhance hospital workflow.</p>
        <p><b>🔄 Adapt to changing patient needs</b> by tracking emerging healthcare patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the First Image
    st.markdown("""
    <div class="image-container">
        <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
    </div>
    """.format(base64.b64encode(open("E:\\vscode\\H1.png", "rb").read()).decode()), unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Healthcare Facility Utilization Section
    st.markdown("""
    <div class="content-box">
        <div class="subheader utilization">
            <h2>🏥 Healthcare Facility Utilization</h2>
        </div>
        <p><b>📌 Understand which departments are overburdened</b> and <b>which are underutilized</b>.</p>
        <p><b>🛏 Optimize bed occupancy</b>, <b>staff allocation</b>, and <b>consultation schedules</b>.</p>
        <p><b>📉 Minimize patient wait times</b> and <b>improve hospital efficiency</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the Second Image
    st.markdown("""
    <div class="image-container">
        <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
    </div>
    """.format(base64.b64encode(open("E:\\vscode\\H2.png", "rb").read()).decode()), unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Data-Driven Decision Making Section
    st.markdown("""
    <div class="content-box">
        <div class="subheader decision-making">
            <h2>🧠 Data-Driven Decision Making</h2>
        </div>
        <p><b>🛠 Empower hospital administrators</b> with actionable insights.</p>
        <p><b>📈 Forecast future trends</b> to plan ahead and streamline hospital operations.</p>
        <p><b>❤️ Improve patient care</b> and healthcare outcomes with data-backed strategies.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the Third Image
    st.markdown("""
    <div class="image-container">
        <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
    </div>
    """.format(base64.b64encode(open("E:\\vscode\\H3.png", "rb").read()).decode()), unsafe_allow_html=True)
if rd == "Admit and Discharge Trends":
    
    # Inject CSS styling for the dashboard with updated background colours for the boxes
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Render the dashboard title
    st.markdown('<div class="dashboard-title">Admit and Discharge Trends</div>', unsafe_allow_html=True)
    
    # ------------------------- Admission Trends Section -------------------------
    try:
        # Query admission trends data
        df_admit = SQL_query("""
            SELECT 
                DATE_FORMAT(Admit_Date, '%Y-%m') AS admit_month_year,
                COUNT(DISTINCT Patient_ID) AS patient_count
            FROM 
                healthcare_insights
            GROUP BY 
                DATE_FORMAT(Admit_Date, '%Y-%m')
            ORDER BY 
                DATE_FORMAT(Admit_Date, '%Y-%m')
        """)
        
        if df_admit.empty:
            st.warning("No admission data available.")
        else:
            st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Admission Trends Over Time</strong></div>
            ''', unsafe_allow_html=True)
            
            # Generate the admission trends plot
            fig, ax = plt.subplots(figsize=(15, 7))
            ax.plot(df_admit["admit_month_year"], df_admit["patient_count"], 
                    color="green", marker="o", linestyle="--")
            ax.set_title("Monthly Patient Admissions", fontsize=20)
            ax.set_xlabel("Month/Year", fontsize=14)
            ax.set_ylabel("Number of Patients", fontsize=14)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Display the plot within a styled container
            st.markdown('<div class="graph-box">', unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown('</div></div>', unsafe_allow_html=True)
            plt.close()
    
    except Exception as e:
        st.error(f"Error loading admission data: {str(e)}")
    
    # ------------------------- Seasonal Admission Patterns (Observation) -------------------------
    st.markdown('''
    <div class="content-box">
        <div class="subheader deemphasized">Seasonal Admission Patterns</div>
        <ul>
            <li><b>Winter (Dec-Feb):</b> Peak admissions from respiratory illnesses</li>
            <li><b>Summer (Mar-May):</b> Moderate admissions with heat-related cases</li>
            <li><b>Monsoon (Jun-Sep):</b> Consistent admissions from seasonal diseases</li>
            <li><b>Autumn (Oct-Nov):</b> Lower admissions as weather stabilizes</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # ------------------------- Discharge Trends Section -------------------------
    try:
        # Query discharge trends data
        df_discharge = SQL_query("""
            SELECT 
                DATE_FORMAT(Discharge_Date, '%Y-%m') AS discharge_month_year,
                COUNT(DISTINCT Patient_ID) AS patient_count
            FROM 
                healthcare_insights
            GROUP BY 
                DATE_FORMAT(Discharge_Date, '%Y-%m')
            ORDER BY 
                DATE_FORMAT(Discharge_Date, '%Y-%m')
        """)
        
        if df_discharge.empty:
            st.warning("No discharge data available.")
        else:
            st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Discharge Trends Over Time</strong></div>
            ''', unsafe_allow_html=True)
            
            # Generate the discharge trends plot
            fig, ax = plt.subplots(figsize=(15, 7))
            ax.plot(df_discharge["discharge_month_year"], df_discharge["patient_count"], 
                    color="red", marker="o", linestyle="--")
            ax.set_title("Monthly Patient Discharges", fontsize=20)
            ax.set_xlabel("Month/Year", fontsize=14)
            ax.set_ylabel("Number of Patients", fontsize=14)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            
            # Display the plot within a styled container
            st.markdown('<div class="graph-box">', unsafe_allow_html=True)
            st.pyplot(fig)
            st.markdown('</div></div>', unsafe_allow_html=True)
            plt.close()
    
    except Exception as e:
        st.error(f"Error loading discharge data: {str(e)}")
    
    # ------------------------- Admission-Discharge Relationship Analysis (Observation) -------------------------
    st.markdown('''
    <div class="content-box">
        <div class="subheader deemphasized">Admission-Discharge Relationship</div>
        <ul>
            <li><b>Winter:</b> High admissions in Dec-Jan lead to increased discharges by late January</li>
            <li><b>Summer:</b> Lower activity with steady decline in both admissions and discharges</li>
            <li><b>Monsoon:</b> Stable patterns due to seasonal illnesses</li>
            <li><b>Autumn:</b> Balanced hospital inflow-outflow with moderate activity</li>
        </ul>
    </div>
    ''', unsafe_allow_html=True)
if rd == "Billing Amount and Health Insurance Analysis":

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Title
    st.markdown('<div class="dashboard-title">Billing Amount and Health Insurance Analysis</div>', unsafe_allow_html=True)
    
    # =============================================================================
    # Section 1: Bill Amount Analysis
    # =============================================================================
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Bill Amount Analysis</strong></div>
            ''', unsafe_allow_html=True)
    
    df_bill = SQL_query("""
        SELECT MIN(`Billing Amount`) AS Min_Billing_Amount,
               MAX(`Billing Amount`) AS Max_Billing_Amount,
               AVG(`Billing Amount`) AS Average_Billing_Amount
        FROM healthcare_insights
    """)
    df_bill_melted = df_bill.melt(var_name="Metric", value_name="Billing Amount")
    fig_bill, ax_bill = plt.subplots(figsize=(8, 6))
    sns.barplot(x="Metric", y="Billing Amount", data=df_bill_melted, palette="viridis", ax=ax_bill)
    ax_bill.set_title("Bill Amount Analysis", fontsize=20)
    ax_bill.set_ylabel("Billing Amount", fontsize=15)
    st.pyplot(fig_bill)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Observations for Bill Amount Analysis
    st.markdown('''
        <div class="content-box">
            <div class="subheader deemphasized">Observations on Bill Amount Analysis</div>
        <ul>
            <li><b>Minimum Billing Amount</b> is very low, close to zero.</li>
            <li><b>Maximum Billing Amount</b> is significantly high, reaching around 90,000+.</li>
            <li><b>Average Billing Amount</b> is much lower than the maximum but still notable.</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # =============================================================================
    # Section 2: Billing Amount per Day
    # =============================================================================
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Billing Amount per Day</strong></div>
            ''', unsafe_allow_html=True)
    
    df_day = SQL_query("""
        WITH AmountStay AS (
            SELECT `Billing Amount` / Admit_Stay AS BillingAmount_per_Day
            FROM healthcare_insights
        )
        SELECT AVG(BillingAmount_per_Day) AS Average_BillingAmount_per_Day,
               MAX(BillingAmount_per_Day) AS Max_BillingAmount_per_Day,
               MIN(BillingAmount_per_Day) AS Min_BillingAmount_per_Day
        FROM AmountStay
    """)
    df_day_melted = df_day.melt(var_name="Category", value_name="Billing Amount")
    x_day = np.arange(len(df_day_melted))
    width_day = 0.5
    plt.figure(figsize=(10, 7))
    plt.bar(x_day, df_day_melted["Billing Amount"], width=width_day, tick_label=df_day_melted["Category"], color=['blue', 'green', 'red'])
    plt.yscale('log')
    plt.ylabel("Billing Amount (log scale) per Day", fontsize=15)
    plt.title("Billing Amount per Day Statistics", fontsize=20)
    st.pyplot(plt)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Observations for Billing Amount per Day
    st.markdown('''
        <div class="content-box">
            <div class="subheader deemphasized">Observations on Billing Amount per Day</div>
        <ul>
            <li><b>Maximum Billing Amount per Day</b> is the highest and significantly larger than the average.</li>
            <li><b>Average Billing Amount per Day</b> is notably lower than the maximum but still substantial.</li>
            <li><b>Minimum Billing Amount per Day</b> is very low compared to the other two values.</li>
            <li>The <b>logarithmic scale</b> is used to highlight the difference between lower and higher daily amounts.</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # =============================================================================
    # Section 3: Billing Amount Room Typewise
    # =============================================================================
    
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Billing Amount Room Typewise</strong></div>
            ''', unsafe_allow_html=True)
    
    df_room = SQL_query("""
        WITH AmountStay AS (
    
            SELECT Bed_Occupancy, `Billing Amount` / Admit_Stay AS BillingAmount_per_Room
            FROM healthcare_insights
        )
        SELECT Bed_Occupancy,
               AVG(BillingAmount_per_Room) AS Average_BillingAmount_per_Room,
               MAX(BillingAmount_per_Room) AS Max_BillingAmount_per_Room,
               MIN(BillingAmount_per_Room) AS Min_BillingAmount_per_Room
        FROM AmountStay
        GROUP BY Bed_Occupancy
    """)
    df_room_melted = df_room.melt(id_vars=["Bed_Occupancy"], var_name="Billing_Type", value_name="BillingAmount")
    fig_room, ax_room = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Bed_Occupancy", y="BillingAmount", hue="Billing_Type", data=df_room_melted, ax=ax_room)
    ax_room.set_xlabel("Bed Occupancy", fontsize=16)
    ax_room.set_ylabel("Billing Amount per Room", fontsize=16)
    ax_room.set_title("Billing Amount Per Room by Bed Occupancy", fontsize=20)
    plt.xticks(rotation=45)
    ax_room.legend(title="Billing Type")
    plt.grid()
    st.pyplot(fig_room)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Observations for Billing Amount Room Typewise
    st.markdown('''
        <div class="content-box">
            <div class="subheader deemphasized">Observations on Billing Amount Room Typewise</div>
        <ul>
            <li>Billing amounts vary significantly across different room types (<b>General, ICU, Private</b>).</li>
            <li><b>Maximum billing amount</b> is highest across all room types compared to average and minimum values.</li>
            <li><b>Average billing amount</b> is notably lower than the maximum but still varies across room types.</li>
            <li><b>Minimum billing amount</b> is the lowest across all categories.</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # =============================================================================
    # Section 4: Billing Amount per Test
    # =============================================================================
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Billing Amount per Test</strong></div>
            ''', unsafe_allow_html=True)
    
    
    df_test = SQL_query("""
        WITH AmountStay AS (
            SELECT Test, `Billing Amount` AS BillingAmount_per_Test
            FROM healthcare_insights
        )
        SELECT Test,
               AVG(BillingAmount_per_Test) AS Average_BillingAmount_per_Test,
               MAX(BillingAmount_per_Test) AS Max_BillingAmount_per_Test,
               MIN(BillingAmount_per_Test) AS Min_BillingAmount_per_Test
        FROM AmountStay
        GROUP BY Test
    """)
    df_test_melted = df_test.melt(id_vars=["Test"], var_name="Billing_Type", value_name="Billing_Amount")
    fig_test = plt.figure(figsize=(12, 6))
    sns.barplot(x="Test", y="Billing_Amount", hue="Billing_Type", data=df_test_melted, palette="Set2")
    plt.title("Billing Amount by Test Type", fontsize=24, fontweight='bold')
    plt.xlabel("Test Type", fontsize=20)
    plt.ylabel("Billing Amount", fontsize=20)
    plt.xticks(rotation=45)
    plt.grid()
    st.pyplot(fig_test)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Observations for Billing Amount per Test
    st.markdown('''
        <div class="content-box">
            <div class="subheader deemphasized">Observations on Billing Amount per Test</div>
        <ul>
            <li>Billing amounts vary across different test types (<b>MRI, CT Scan, X-ray, Blood Test, Ultrasound</b>).</li>
            <li><b>Maximum billing amount</b> is highest for MRI, CT Scan, and Ultrasound compared to other tests.</li>
            <li><b>Average billing amount</b> follows a similar trend, with MRI, CT Scan, and Ultrasound being higher.</li>
            <li><b>Minimum billing amount</b> remains significantly lower across all test types.</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # =============================================================================
    # Section 5: Actual Amount paid by the Patient
    # =============================================================================
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Actual Amount paid by the Patient</strong></div>
            ''', unsafe_allow_html=True)
    
    
    df_paid = SQL_query("""
        WITH Datedifference AS (
            SELECT `Billing Amount` AS Billing_Amount,
                   `Health Insurance Amount` AS Insurance_Amount,
                   (`Billing Amount` - `Health Insurance Amount`) AS Amt_Paid
            FROM healthcare_insights
        )
        SELECT AVG(Amt_Paid) AS Average_Amount_Paid,
               MAX(Amt_Paid) AS Max_Amount_Paid,
               MIN(Amt_Paid) AS Min_Amount_Paid
        FROM Datedifference
    """)
    df_paid_melted = df_paid.melt(var_name="Metric", value_name="Billing Amount")
    fig_paid, ax_paid = plt.subplots(figsize=(8, 6))
    sns.barplot(x="Metric", y="Billing Amount", data=df_paid_melted, palette="viridis", ax=ax_paid)
    ax_paid.set_title("Amount paid Analysis", fontsize=18)
    ax_paid.set_ylabel("Billing Amount", fontsize=13)
    st.pyplot(fig_paid)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Observations for Actual Amount paid by the Patient
    st.markdown('''
        <div class="content-box">
            <div class="subheader deemphasized">Observations on Actual Amount paid by the Patient</div>
        <ul>
            <li><b>Max Amount Paid</b> is significantly higher than the Average and Min Amount Paid.</li>
            <li><b>Average Amount Paid</b> is considerably lower than the Max Amount Paid.</li>
            <li><b>Min Amount Paid</b> is very close to zero.</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    
    # =============================================================================
    # Section 6: Health Insurance Amount Analysis
    # =============================================================================
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Health Insurance Amount Analysis</strong></div>
            ''', unsafe_allow_html=True)
    
    df_ins = SQL_query("""
        SELECT MIN(`Health Insurance Amount`) AS Min_Insurance_Amount,
               MAX(`Health Insurance Amount`) AS Max_Insurance_Amount,
               AVG(`Health Insurance Amount`) AS Average_Insurance_Amount
        FROM healthcare_insights
    """)
    df_ins_melted = df_ins.melt(var_name="Metric", value_name="Health Insurance Amount")
    fig_ins = plt.figure(figsize=(8, 6))
    sns.barplot(x="Metric", y="Health Insurance Amount", data=df_ins_melted, palette="viridis")
    plt.title("Health Insurance Amount Analysis", fontsize=18, fontweight='bold')
    plt.ylabel("Health Insurance Amount", fontsize=14)
    st.pyplot(fig_ins)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Observations for Health Insurance Amount Analysis
    st.markdown('''
        <div class="content-box">
            <div class="subheader deemphasized">Observations on Health Insurance Amount Analysis</div>
        <ul>
            <li><b>Max Insurance Amount</b> is significantly higher than the Average Insurance Amount.</li>
            <li><b>Average Insurance Amount</b> is considerably lower than the Max Insurance Amount.</li>
            <li><b>Min Insurance Amount</b> is very close to zero.</li>
            </ul>
        </div>
    ''', unsafe_allow_html=True)
if rd == "Diagnosis Statistics":

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)

    # Page Title
    st.markdown('<div class="dashboard-title">Diagnosis Statistics</div>', unsafe_allow_html=True)
    
    
    # Sub header for Occurences of Diseases
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Occurences of Diseases</strong></div>
            ''', unsafe_allow_html=True)
    
    st.write("")
    
    # Occurences of Diseases Stats 
    df_ = SQL_query("""
                    WITH FormattedData AS (
                        SELECT 
                            DATE_FORMAT(Admit_Date, '%Y-%m') AS Month_Year,
                            Diagnosis
                        FROM 
                            healthcare_insights
                    )
                    SELECT 
                        Month_Year,
                        Diagnosis,
                        COUNT(*) AS Patient_Count
                    FROM 
                        FormattedData
                    GROUP BY 
                        Month_Year, Diagnosis
                    ORDER BY 
                        Month_Year
            """)
    
    g = sns.catplot(x='Month_Year', y='Patient_Count', hue='Diagnosis', data=df_, height=6, aspect=2, kind='point')
    g.set_xlabels("Month Year", fontsize=20)
    g.set_ylabels("Patient Count", fontsize=20)
    st.pyplot(plt)
    
    # Observations for Occurences of Diseases using the same design as before
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Observations on Occurences of Diseases</div>
            <ul>
                <li><strong>Consistent trends:</strong> Viral infections show the highest patient count, indicating seasonal or environmental impact.</li>
                <li><strong>Fluctuations:</strong> Diseases like the flu and malaria exhibit cyclic peaks, possibly during monsoon or winter seasons.</li>
                <li><strong>Stable conditions:</strong> Fractures remain steady over time, indicating non-seasonal factors.</li>
                <li><strong>Season transition:</strong> We also see the jump in the cases of all the diagnoses in the month of March, which is due to the seasonal changes.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Sub header for Patient Distribution by Diagnosis
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Patient Distribution by Diagnosis</strong></div>
            ''', unsafe_allow_html=True)
    
    df_ = SQL_query("""
                    SELECT 
                        Diagnosis,
                        COUNT(Patient_ID) AS Patients
                    FROM 
                        healthcare_insights
                    GROUP BY
                        Diagnosis
                """)
    
    # Pie Chart
    plt.figure(figsize=(8, 8))
    plt.pie(df_["Patients"], labels=df_["Diagnosis"], autopct='%1.1f%%', startangle=120)
    plt.title("Patient Distribution by Diagnosis", fontsize=14, fontweight='bold')
    st.pyplot(plt)
    
    # Observations for Patient Distribution by Diagnosis (Pie Chart Observations) using the same design as before
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Pie Chart Observations</div>
            <ul>
                <li><strong>High proportion:</strong> Viral infections dominate with 28% of cases, highlighting their widespread nature.</li>
                <li><strong>Second largest:</strong> Flu and malaria together account for ~44% of cases, emphasizing the need for preventive measures.</li>
                <li><strong>Rare cases:</strong> Fractures and pneumonia have the least shares, suggesting they are less common in the observed period.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


if rd == "Bed Occupancy Statistics":

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Title
    st.markdown('<div class="dashboard-title">Bed Occupancy Statistics</div>', unsafe_allow_html=True)
    
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Bed Occupancy over Time</strong></div>
            ''', unsafe_allow_html=True)

    st.write("")
    
    # Bed Occupancy Stats

    df_ = SQL_query("""
            SELECT 
                Admit_Month_Year,
                Bed_Occupancy,
                COUNT(Bed_Occupancy) AS Occupancy_Count
                
            FROM 
                healthcare_insights
            WHERE
                Admit_Month_Year LIKE '%2023%'
            GROUP BY
                Bed_Occupancy, Admit_Month_Year
            ORDER BY
                STR_TO_DATE(Admit_Month_Year, '%M-%Y')
                """)


    sns.catplot(x= 'Admit_Month_Year', y = 'Occupancy_Count', hue = 'Bed_Occupancy', data = df_, height=3, aspect=2, kind = 'point')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Observations for the Line Chart
    line_chart_insights = """
    <li><strong>Private</strong> beds consistently have the highest occupancy, fluctuating between 250 and 320.</li>
    <li><strong>General</strong> bed occupancy shows a steady trend around 150–220, peaking in March.</li>
    <li><strong>ICU</strong> beds maintain the lowest count, staying below 100 with minor fluctuations.</li>
    <li>Peaks in March indicate increased overall demand, while a dip in April shows reduced occupancy across categories.</li>
    """

    # Display insights for Line Chart
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Line Chart Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Private</strong> beds consistently have the highest occupancy, fluctuating between 250 and 320.</li>
                <li><strong>General</strong> bed occupancy shows a steady trend around 150–220, peaking in March.</li>
                <li><strong>ICU</strong> beds maintain the lowest count, staying below 100 with minor fluctuations.</li>
                <li>Peaks in March indicate increased overall demand, while a dip in April shows reduced occupancy across categories.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Bed Occupancy Distribution</strong></div>
            ''', unsafe_allow_html=True)

    df_ = SQL_query(
                    """ 
                    SELECT 
                        Bed_Occupancy,
                        COUNT(Bed_Occupancy) AS Occupancy_Count    
                    FROM 
                        healthcare_insights    
                    GROUP BY
                        Bed_Occupancy
                    
                    """
                    )

    # Pie Chart

    plt.figure(figsize=(8, 8))  # Set figure size
    plt.pie(df_["Occupancy_Count"], labels=df_["Bed_Occupancy"], autopct='%1.1f%%', startangle=120)

    # Title
    plt.title("Bed Occupancy Distribution", fontsize=14, fontweight='bold')

    # Show plot
    st.pyplot(plt)

    # Observations for the Pie Chart
    pie_chart_insights = """
    <li><strong>Private beds</strong> account for the majority of the occupancy (50%).</li>
    <li><strong>General beds</strong> contribute 33.3%.</li>
    <li><strong>ICU beds</strong> form the smallest share, at 16.7%.</li>
    """
    # Display insights for Pie Chart
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Pie Chart Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Private beds</strong> account for the majority of the occupancy (50%).</li>
                <li><strong>General beds</strong> contribute 33.3%.</li>
                <li><strong>ICU beds</strong> form the smallest share, at 16.7%.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

if rd == "Length of Stay":

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Title
    st.markdown('<div class="dashboard-title">Length of Stay</div>', unsafe_allow_html=True)
 

    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Length of Stay Statistics</strong></div>
            ''', unsafe_allow_html=True)


    # Admit Stay Stats

    df_ = SQL_query(""" 
                    SELECT 
                        MIN(Admit_Stay) AS Minimum_Stay,
                        AVG(Admit_Stay) AS Average_Stay,
                        MAX(Admit_Stay) AS Maximum_Stay
                    FROM 
                        healthcare_insights
                """)

    # ✅ Melt the DataFrame correctly (No id_vars needed)
    df__melted = df_.melt(var_name='Stay', value_name='Days')

    # Set bar positions
    x = np.arange(len(df__melted))  # Fix the length
    width = 0.5  # Bar width

    # Create the bar plot
    plt.figure(figsize=(10, 4))
    plt.bar(x, df__melted['Days'], width=width, tick_label=df__melted['Stay'], color=['blue', 'green', 'red'])

    # Labels and title
    plt.ylabel("Days", fontsize = 16)
    plt.title("Length of Stay Statistics", fontsize = 20, fontweight='bold')

    # Show plot
    st.pyplot(plt)

    # Insights for Length of Stay Statistics
    length_of_stay_stats_insights = """
    ### Observations for Length of Stay Statistics
    - **Minimum Stay**: Patients discharged within a day or two are likely undergoing simple procedures or routine care.
    - **Average Stay**: Most patients stay approximately 10-15 days, which indicates the standard recovery period for common illnesses or surgeries.
    - **Maximum Stay**: Extended hospital stays above 40 days suggest critical cases requiring long-term treatment or complications during recovery.
    """

    # Display insights
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Length of Stay Statistics Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Minimum Stay:</strong> Patients discharged within a day or two are likely undergoing simple procedures or routine care.</li>
                <li><strong>Average Stay:</strong> Most patients stay approximately 10-15 days, which indicates the standard recovery period for common illnesses or surgeries.</li>
                <li><strong>Maximum Stay:</strong> Extended hospital stays above 40 days suggest critical cases requiring long-term treatment or complications during recovery.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Length of Stay w.r.t Diagnosis</strong></div>
            ''', unsafe_allow_html=True)

    # Stay per Diagnosis

    df_ = SQL_query(""" 
                        SELECT
                            Diagnosis,
                            AVG(Admit_Stay) AS Average_Stay
                        FROM
                            healthcare_insights
                        GROUP BY
                            Diagnosis 
                """)

    # ✅ Create a barplot
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Diagnosis", y="Average_Stay", data=df_, palette="viridis")

    # Rotate x labels for better readability
    plt.xticks(rotation=45)

    # Titles and labels
    plt.title("Average Hospital Stay per Diagnosis", fontsize = 20, fontweight='bold')
    plt.xlabel("Diagnosis", fontsize = 18)
    plt.ylabel("Average Stay (Days)", fontsize = 18)

    plt.grid()

    # Show plot
    st.pyplot(plt)

    # Insights for Length of Stay w.r.t. Diagnosis
    length_of_stay_diagnosis_insights = """
    ### Observations for Length of Stay w.r.t. Diagnosis
    - **Diagnoses like Typhoid, Malaria, and Pneumonia** result in relatively longer stays, averaging 7-8 days, indicating these illnesses require consistent care.
    - **Flu and Viral Infections** tend to have shorter average stays, around 4-5 days, as they often require less intensive treatment.
    - The consistency in the bar heights implies a balanced treatment protocol across diagnoses.
    """

    # Display insights
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Length of Stay w.r.t Diagnosis Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Diagnoses like Typhoid, Malaria, and Pneumonia</strong> result in relatively longer stays, averaging 7-8 days, indicating these illnesses require consistent care.</li>
                <li><strong>Flu and Viral Infections</strong> tend to have shorter average stays, around 4-5 days, as they often require less intensive treatment.</li>
                <li>The consistency in the bar heights implies a balanced treatment protocol across diagnoses.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

if rd == "Doctor's Statistics":

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Title
    st.markdown('<div class="dashboard-title">Doctor\'s Statistics</div>', unsafe_allow_html=True) 


    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Contribution of Doctors to the Hospital</strong></div>
            ''', unsafe_allow_html=True)

    

    # Insights for Graph 1
    graph1_insights = """
    ### Observations from the Graph (Contribution of Doctors)
    - The contributions across all doctors are fairly similar.
    - **Ravi D** has the highest contribution, showing a consistent pattern of excellence.
    - **Jay Sinha** has the lowest contribution, indicating room for improvement.
    """

    # Insights for Graph 2
    graph2_insights = """
    ### Observations from the Graph (Average Feedback of Doctors)
    - The differences in average feedback among doctors are relatively minimal.
    """

    
    # Doctor Contribution Stats


    df_ = SQL_query("""
                    SELECT
                        Doctor,
                        SUM(`Billing Amount`) AS Contribution
                    FROM
                        healthcare_insights
                    GROUP BY
                        Doctor
                    ORDER BY
                        SUM(`Billing Amount`) DESC
                """)

    plt.figure(figsize = (10,7))

    sns.barplot(x = 'Doctor', y='Contribution', data=df_, palette=["red", "blue", "green", "purple", "orange", "magenta", "cyan"])

    # Customize labels
    plt.xlabel("Doctor", fontsize = 16)
    plt.ylabel("Contribution", fontsize = 16)
    plt.title("Contribution of Doctors", fontsize = 20, fontweight='bold')

    # Show plot
    st.pyplot(plt)

        # Display insights for Doctor Contribution
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Doctor Contribution Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li>The contributions across all doctors are fairly similar.</li>
                <li><strong>Ravi D</strong> has the highest contribution, showing a consistent pattern of excellence.</li>
                <li><strong>Jay Sinha</strong> has the lowest contribution, indicating room for improvement.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Doctor\'s Feedback Scores</strong></div>
            ''', unsafe_allow_html=True)


    # Doctor's Feedback Scores

    df_ = SQL_query(""" 
                    SELECT
                        Doctor,
                        AVG(Feedback) AS Average_Feedback
                    FROM
                        healthcare_insights
                    GROUP BY
                        Doctor
                """)

    plt.figure(figsize = (10,7))

    sns.barplot(x = 'Doctor', y='Average_Feedback', data=df_, palette='Greens')

    # Customize labels
    plt.xlabel("Doctor", fontsize = 16)
    plt.ylabel("Average Feedback", fontsize = 16)
    plt.title("Average Feedback of Doctors", fontsize = 20, fontweight='bold')

    # Show plot
    st.pyplot(plt)

    # Display insights for Doctor's Feedback Scores
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Doctor's Feedback Scores Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li>The differences in average feedback among doctors are relatively minimal.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Patients per Doctor</strong></div>
            ''', unsafe_allow_html=True)



    # Patients per Doctor

    df_ = SQL_query(""" 
                    SELECT 
                        Doctor,
                        COUNT(Patient_ID) AS Patient_Count            
                    FROM
                        healthcare_insights
                    GROUP BY
                        Doctor
                """)

    # ✅ Create the barplot
    plt.figure(figsize=(8, 6))
    sns.barplot(x="Doctor", y="Patient_Count", data=df_, palette="viridis")

    # ✅ Labels and title
    plt.title("Patient Count Analysis", fontsize = 18, fontweight='bold')
    plt.xlabel("Doctor", fontsize = 14)
    plt.ylabel("Patient Count", fontsize = 14)

    plt.xticks(rotation=45)

    # ✅ Show plot
    st.pyplot(plt)

    # Display insights for Patients per Doctor
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Patients per Doctor Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li>Almost all doctors have a similar number of patients.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )    




if rd == "Follow-up Statistics":

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Title
    st.markdown('<div class="dashboard-title">Follow-Up Statistics</div>', unsafe_allow_html=True)  
  
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Follow-up Duration Statistics</strong></div>
            ''', unsafe_allow_html=True)


    # Followup Stats
    df_ =  SQL_query(""" 
                SELECT
                    MIN(Followup_Duration) AS Followup_Duration_Minimum,
                    AVG(Followup_Duration) AS Followup_Duration_Average,
                    MAX(Followup_Duration) AS Followup_Duration_Maximum
                FROM
                    healthcare_insights
                """)

    # ✅ Melt the DataFrame correctly (No id_vars needed)
    df__melted = df_.melt(var_name='Followup', value_name='Days')

    # Set bar positions
    x = np.arange(len(df__melted))  # Fix the length
    width = 0.5  # Bar width

    # Create the bar plot
    plt.figure(figsize=(10, 4))
    plt.bar(x, df__melted['Days'], width=width, tick_label=df__melted['Followup'], color=['blue', 'green', 'red'])

    # Labels and title
    plt.ylabel("Days", fontsize = 16)
    plt.title("Length of Followup Statistics", fontsize = 20, fontweight='bold')

    # Show plot
    st.pyplot(plt)

    # Display insights for Length of Followup Statistics
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Length of Followup Statistics Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Minimum Followup Duration</strong> is significantly low, around 5 days, indicating that some cases require minimal attention.</li>
                <li><strong>Average Followup Duration</strong> is approximately 15 days, showing the typical timeline for most follow-ups.</li>
                <li><strong>Maximum Followup Duration</strong> is the highest at around 40 days, indicating long-term follow-ups for critical cases.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Insights for the Length of Followup Statistics graph
    graph1_insights = """
    ### Observations for Length of Followup Statistics
    - **Minimum Followup Duration** is significantly low, around 5 days, indicating that some cases require minimal attention.
    - **Average Followup Duration** is approximately 15 days, showing the typical timeline for most follow-ups.
    - **Maximum Followup Duration** is the highest at around 40 days, indicating long-term follow-ups for critical cases.
    """
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Average Followup Duration by Diagnosis</strong></div>
            ''', unsafe_allow_html=True)


    df_ = SQL_query(""" 
            SELECT
                Diagnosis,
                AVG(Followup_Duration) AS Average_Followup_Duration
            FROM
                healthcare_insights
            GROUP BY
                Diagnosis
            ORDER BY
                Diagnosis
            """)

    plt.figure(figsize = (10,7))

    sns.barplot(x = 'Diagnosis', y='Average_Followup_Duration', data=df_, palette='Greens')

    # Customize labels
    plt.xlabel("Diagnosis", fontsize = 16)
    plt.ylabel("Average Followup Duration", fontsize = 16)
    plt.title("Average Followup Duration of Diagnosis", fontsize = 20, fontweight='bold')

    # Show plot
    st.pyplot(plt)

    graph2_insights = """
    ### Observations for Average Followup Duration of Diagnosis
    - **Malaria and Fractures** have the highest average follow-up duration (~12 days), indicating their longer recovery and monitoring periods.
    - **Pneumonia and Typhoid** follow closely with average durations of around 10–11 days.
    - **Flu** has the shortest follow-up duration (~9 days), reflecting its relatively quick resolution in most cases.
    - **Viral Infection** also has a follow-up duration comparable to Typhoid, emphasizing the need for patient monitoring.
    """

    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Average Followup Duration of Diagnosis Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Malaria and Fractures</strong> have the highest average follow-up duration (~12 days), indicating their longer recovery and monitoring periods.</li>
                <li><strong>Pneumonia and Typhoid</strong> follow closely with average durations of around 10–11 days.</li>
                <li><strong>Flu</strong> has the shortest follow-up duration (~9 days), reflecting its relatively quick resolution in most cases.</li>
                <li><strong>Viral Infection</strong> also has a follow-up duration comparable to Typhoid, emphasizing the need for patient monitoring.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


if rd == "Patients in Critical Condition":

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Title
    st.markdown('<div class="dashboard-title">Patients in Critical Condition</div>', unsafe_allow_html=True)

    # Sub-headerst.markdo
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Patients with distinct diagnosis in ICU</strong></div>
            ''', unsafe_allow_html=True)
    
    # Patients in ICU (Critical Condition)
    df_ = SQL_query(""" 
                        SELECT 
                            Diagnosis,           
                            COUNT(*) AS Diagnosis_Count_To_ICU
                        FROM
                            healthcare_insights
                        WHERE
                            Bed_Occupancy = 'ICU'
                        GROUP BY
                            Diagnosis
                        ORDER BY
                            Diagnosis
                """)


    plt.figure(figsize = (10,7))

    sns.barplot(x = 'Diagnosis', y='Diagnosis_Count_To_ICU', data=df_, palette='Greens')

    # Customize labels
    plt.xlabel("Diagnosis", fontsize = 16)
    plt.ylabel("Patient Count", fontsize = 16)
    plt.title("Patients with distinct diagnosis in ICU", fontsize = 20, fontweight='bold')

    # Show plot
    st.pyplot(plt)

    # Insights for the Patients with distinct diagnosis in ICU graph
    graph1_insights = """
    ### Observations for Patients with distinct diagnosis in ICU
    - **Viral Infection** accounts for the highest number of patients (~320), indicating its widespread impact.
    - **Flu** follows with around 280 patients, reflecting its seasonal prevalence.
    - **Malaria** has a significant count (~240), suggesting it remains a common concern in certain regions.
    - **Typhoid** and **Pneumonia** show moderate counts (~200 and ~160 respectively), highlighting their medical relevance.
    - **Fractures** have the lowest count (~60), as they are less common in ICU compared to diseases.
    """
    
    
    # Display insights for Patients with distinct diagnosis in ICU
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Patients with Distinct Diagnosis in ICU Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Viral Infection</strong> accounts for the highest number of patients (~320), indicating its widespread impact.</li>
                <li><strong>Flu</strong> follows with around 280 patients, reflecting its seasonal prevalence.</li>
                <li><strong>Malaria</strong> has a significant count (~240), suggesting it remains a common concern in certain regions.</li>
                <li><strong>Typhoid</strong> and <strong>Pneumonia</strong> show moderate counts (~200 and ~160 respectively), highlighting their medical relevance.</li>
                <li><strong>Fractures</strong> have the lowest count (~60), as they are less common in ICU compared to diseases.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    # Sub-header
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Patients in ICU over time</strong></div>
            ''', unsafe_allow_html=True)

    df_ = SQL_query(""" 
                    SELECT 
                        Admit_Month_Year,
                        COUNT(Patient_ID) AS Patients_Going_To_ICU
                        
                    FROM 
                        healthcare_insights
                    WHERE
                        Admit_Month_Year LIKE '%2023%'
                        AND Bed_Occupancy = 'ICU'
                    GROUP BY
                        Bed_Occupancy, Admit_Month_Year
                    ORDER BY
                        STR_TO_DATE(Admit_Month_Year, '%M-%Y')
                """)

    plt.figure(figsize = (15,7))
    plt.plot(df_["Admit_Month_Year"], df_["Patients_Going_To_ICU"], color='red')

    plt.title('Patients in ICU over time', fontsize = 28, fontweight='bold')
    plt.xlabel("Time", fontsize = 23)
    plt.ylabel("Patients in ICU", fontsize = 23)

    plt.grid(True)

    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Insights for the Patients in ICU over time graph
    graph2_insights = """
    ### Observations for Patients in ICU over time
    - **March 2023** shows the highest number of ICU patients (~100), potentially due to seasonal illnesses.
    - **June 2023** has the lowest count (~75), possibly indicating a decline in disease outbreaks.
    - The trend shows fluctuating patient counts, with peaks in **January, March, and August**, suggesting periodic spikes.
    - A gradual rise is observed from **November to December 2023**, signaling a potential seasonal pattern.
    """   

    # Display insights for Patients in ICU over time
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Patients in ICU Over Time Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>March 2023</strong> shows the highest number of ICU patients (~100), potentially due to seasonal illnesses.</li>
                <li><strong>June 2023</strong> has the lowest count (~75), possibly indicating a decline in disease outbreaks.</li>
                <li>The trend shows fluctuating patient counts, with peaks in <strong>January, March, and August</strong>, suggesting periodic spikes.</li>
                <li>A gradual rise is observed from <strong>November to December 2023</strong>, signaling a potential seasonal pattern.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

if rd == "Test Analysis":

    # ----------------------------------------------------------------------
    # Inject CSS styling 
    # ----------------------------------------------------------------------
    st.markdown("""
    <style>
        .dashboard-title {
            /* Existing styling remains unchanged */
            font-size: 45px;
            font-weight: bold;
            text-align: center;
            color: white;
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            background-size: 200% auto;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite, gradientShift 3s ease infinite;
            margin-bottom: 30px;
            position: relative;
            /* Added 3D text effect */
            text-shadow: 4px 4px 5px rgba(0, 0, 0, 0.6);
        }
        .dashboard-title::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: inherit;
            opacity: 0.3;
            filter: blur(8px);
            z-index: -1;
            border-radius: 10px;
            animation: shimmer 2s infinite;
        }
        .content-box {
            background-color: #f9f9f9;
            border: 2px solid #ccc;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-weight: bold;
            text-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease-in-out;
        }
        .content-box:hover {
            transform: scale(1.02);
            border-color: #0D47A1;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
        }
        .graph-box {
            animation: zoomIn 0.8s ease-out;
            margin-bottom: 30px;
            transition: transform 0.5s ease;
        }
        .graph-box:hover {
            transform: scale(1.02);
        }
        /* Subheader Styling for boxes above graphs (sub-titles) */
        .subheader {
            font-size: 1.75rem;
            color: #1e3c72;
            margin-bottom: 10px;
            border-bottom: 2px solid #1e3c72;
            padding-bottom: 5px;
            transition: text-shadow 0.3s ease;
        }
        .subheader:hover {
            text-shadow: 2px 2px 8px rgba(30, 60, 114, 0.5);
        }
        /* Text styling for the sub-title and observation headers */
        .subheader.trends {
            font-size: 2rem;
            font-weight: 800;
            color: #1e3c72;
            border-bottom: 3px solid #2c3e50;
        }
        .subheader.deemphasized {
            font-size: 1.6rem;
            font-weight: 500;
            color: #1e3c72;
            border-bottom: 1px solid #7f8c8d;
        }
        /* Updated background-colour for the content boxes based on their child header */
        .content-box:has(> .subheader.trends) {
            background-color: #bbdefb;  /* More pronounced light blue for sub-title boxes */
        }
        .content-box:has(> .subheader.deemphasized) {
            background-color: #e3f2fd;  /* Light blue for observation boxes */
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes shimmer {
            0% { opacity: 0.3; }
            50% { opacity: 0.6; }
            100% { opacity: 0.3; }
        }
        @keyframes zoomIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Page Title
    st.markdown('<div class="dashboard-title">Test Analysis</div>', unsafe_allow_html=True)
    
    # Sub-header
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Patients per test</strong></div>
            ''', unsafe_allow_html=True)


    # Patients per test
    df_ = SQL_query(""" 
                    SELECT
                        Test,
                        COUNT(Patient_ID) AS Patients
                    FROM
                        healthcare_insights
                    GROUP BY
                        Test      
                """)

    plt.figure(figsize = (10,7))

    sns.barplot(x = 'Test', y = 'Patients', data = df_, palette = ['red', 'green', 'blue', 'yellow', 'magenta'])

    # Customize labels
    plt.xlabel("Tests", fontsize = 16)
    plt.ylabel("Patient Count", fontsize = 16)
    plt.title("Patients having different tests", fontsize = 20, fontweight='bold')

    # Show plot
    st.pyplot(plt)

    graph1_insights = """
    ### Observations for Patients Having Different Tests
    - **Blood Tests** are the most common diagnostic procedure, with the highest number of patients.
    - **MRI Scans** follow as the second most frequent test, reflecting its importance in medical diagnostics.
    - **CT Scans and Ultrasounds** are moderately utilized, likely for specific cases.
    - **X-Rays** are the least utilized among the listed tests, possibly due to advancements in other imaging techniques.
    """

    # Display insights for Patients Having Different Tests
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Patients Having Different Tests Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Blood Tests</strong> are the most common diagnostic procedure, with the highest number of patients.</li>
                <li><strong>MRI Scans</strong> follow as the second most frequent test, reflecting its importance in medical diagnostics.</li>
                <li><strong>CT Scans and Ultrasounds</strong> are moderately utilized, likely for specific cases.</li>
                <li><strong>X-Rays</strong> are the least utilized among the listed tests, possibly due to advancements in other imaging techniques.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)

    # Sub-header
    st.markdown('''
            <div class="content-box">
                <div class="subheader trends"><strong>Number of Tests per Diagnosis</strong></div>
            ''', unsafe_allow_html=True)

    # Tests per Diagnosis
    df_ = SQL_query(""" 
                    SELECT
                        Diagnosis,
                        Test AS Test_Type,
                        COUNT(Test) AS Total_Tests
                    FROM
                        healthcare_insights
                    GROUP BY
                        Diagnosis, Test
                    ORDER BY
                        Diagnosis, COUNT(Test) DESC
                """)

    # ✅ Create a grouped barplot
    plt.figure(figsize=(12, 6))
    sns.barplot(x="Diagnosis", y="Total_Tests", hue="Test_Type", data=df_)

    # Rotate x labels for better readability
    plt.xticks(rotation=45)

    plt.xlabel("Diagnosis", fontsize = 19)
    plt.ylabel("Total Tests", fontsize = 19)

    # Show plot
    st.pyplot(plt)

    graph2_insights = """
    ### Observations for Number of Tests per Diagnosis
    - **Flu and Viral Infections** have the highest number of total tests performed, primarily driven by Blood Tests.
    - **Fractures** require a significant number of imaging tests, including X-Rays and MRI scans.
    - **Malaria and Typhoid** heavily rely on Blood Tests for accurate diagnosis.
    - **Pneumonia** shows a balanced usage of CT Scans and Blood Tests.
    """

    # Display insights for Number of Tests per Diagnosis
    st.markdown(
        """
        <div class="content-box">
            <div class="subheader deemphasized">Number of Tests per Diagnosis Observations</div>
            <ul style="list-style-type: disc; margin-left: 20px; color: black;">
                <li><strong>Flu and Viral Infections</strong> have the highest number of total tests performed, primarily driven by Blood Tests.</li>
                <li><strong>Fractures</strong> require a significant number of imaging tests, including X-Rays and MRI scans.</li>
                <li><strong>Malaria and Typhoid</strong> heavily rely on Blood Tests for accurate diagnosis.</li>
                <li><strong>Pneumonia</strong> shows a balanced usage of CT Scans and Blood Tests.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )


if "Suggestions for the Hospital" in rd:
    st.markdown("""
    <style>
        /* Stylized Page Title with Smooth and Bouncy Animation */
        .page-title {
            font-size: 36px;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(45deg, #1e3c72, #2a5298, #1e3c72);
            background-size: 200% 200%;
            animation: gradient 5s ease-in-out infinite, bounce 2s ease infinite;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }
    
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-15px); }
            60% { transform: translateY(-7px); }
        }
    </style>
    """, unsafe_allow_html=True)
    
    
    st.markdown("""
    <style>
        /* Stylized Page Title with Bouncy Animation */
        .page-title {
            font-size: 36px;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(45deg, #1e3c72, #2a5298, #1e3c72);
            background-size: 200% 200%;
            animation: gradient 5s ease-in-out infinite, bounce 2s ease infinite;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
    
        /* Simplified suggestion boxes */
        .suggestion-box {
            border: 2px solid;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            background-color: #fff;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
        }
    
        .suggestion-box:hover {
            transform: translateY(-5px) scale(1.03);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }
    
        /* Simplified suggestion title */
        .suggestion-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            padding: 10px 0;
            color: #2C3E50;
        }

        /* Added 3D text effect for suggestion box text */
        .suggestion-box p, .suggestion-box strong, .suggestion-title {
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
    
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-15px); }
            60% { transform: translateY(-7px); }
        }
    
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <style>
        /* Enhanced CSS for the suggestions page */
        .page-title {
            font-size: 36px;
            font-weight: bold;
            color: #ffffff;
            text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
            text-align: center;
            margin-bottom: 40px;
            background: linear-gradient(45deg, #1e3c72, #2a5298, #1e3c72);
            background-size: 200% 200%;
            animation: gradient 5s ease-in-out infinite, bounce 2s ease infinite;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
    
        /* Simplified suggestion boxes */
        .suggestion-box {
            border: 2px solid;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            background-color: #fff;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.5s ease-in-out;
        }
    
        .suggestion-box:hover {
            transform: translateY(-5px) scale(1.03);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
    
        /* Simplified suggestion title */
        .suggestion-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 15px;
            padding: 10px 0;
            color: #2C3E50;
        }
    
        /* Enhanced horizontal divider */
        .hr {
            border: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #1e3c72, transparent);
            margin: 40px 0;
            animation: glow 2s ease-in-out infinite;
        }
    
        /* Styled paragraphs within suggestion boxes */
        .suggestion-box p {
            line-height: 1.8;
            color: #2C3E50;
            margin-bottom: 15px;
        }
    
        .suggestion-box strong {
            color: #1e3c72;
            font-weight: 600;
        }
    
        /* Added 3D text effect for suggestion box text */
        .suggestion-box p, .suggestion-box strong, .suggestion-title {
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
    
        /* Image container enhancement */
        .image-container {
            position: relative;
            margin: 30px 0;
            transition: all 0.5s ease-in-out;
        }
    
        .image-container:hover {
            transform: scale(1.02);
        }
    
        .image-container img {
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
    
        /* Animations for page title */
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
    
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
            40% { transform: translateY(-15px); }
            60% { transform: translateY(-7px); }
        }
    
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .page-title {
                font-size: 28px;
            }
            .suggestion-title {
                font-size: 20px;
            }
            .suggestion-box {
                padding: 15px;
            }
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Display the bouncy title
    st.markdown('<div class="page-title">Hospital Productivity Enhancement Recommendations</div>', unsafe_allow_html=True)
    
    # Suggestion 1: Align Staffing and Resources with Seasonal Trends
    st.markdown("""
    <div class="suggestion-box" style="border-color: #4CAF50; background-color: #f0fff0;">
    <div class="suggestion-title">Suggestion 1: Align Staffing and Resources</div>
    <p><strong>Observations:</strong> Winter data shows <strong>peak admissions</strong> due to respiratory and cold-related illnesses, with discharges peaking by late January and a sharp decline in February. Summer and monsoon periods are steadier, while post-monsoon shows a dip.</p>
    <p><strong>Recommendations:</strong></p>
    <p><strong>Increase Staffing in Winter:</strong> Enhance staffing levels in emergency, respiratory, and ICU units to manage the winter surge. Ensure an ample supply of medical equipment and medications, and establish <strong>fast-track discharge processes</strong> to free up beds as admissions decline.</p>
    <p><strong>Optimize Summer Utilization:</strong> Use the moderate admission rates during summer to schedule elective procedures, provide staff training, and perform facility maintenance. This ensures that the hospital operates efficiently during slower periods.</p>
    <p><strong>Steady Monsoon Management:</strong> Maintain consistent staffing to manage waterborne and vector-borne diseases during the monsoon season. Emphasize rapid diagnostics and treatment protocols to keep patient flow smooth.</p>
    <p><strong>Post-Monsoon Improvements:</strong> Utilize the stabilized admission numbers in post-monsoon to upgrade systems and refine processes, ensuring the hospital is well-prepared for the next seasonal cycle.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for Styling (Suggestion 1)
    st.markdown(
        """
        <style>
            /* Gradient Title */
            .title {
                font-size: 45px;
                font-weight: bold;
                text-align: center;
                color: white;
                background: linear-gradient(90deg, #1e3c72, #2a5298);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            }
            /* Image Styling */
            .image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px 0;
            }
            .image {
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                transition: transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
            }
            .image:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Display the Image with Inline Style for Size (Suggestion 1)
    st.markdown(
        """
        <div class="image-container">
            <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
        </div>
        """.format(base64.b64encode(open("E:\\vscode\\S1.png", "rb").read()).decode()),
        unsafe_allow_html=True,
    )
    
    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    
    # Suggestion 2: Optimize Bed and Resource Allocation
    st.markdown("""
    <div class="suggestion-box" style="border-color: #2196F3; background-color: #e3f2fd;">
    <div class="suggestion-title">Suggestion 2: Optimize Bed and Resource Allocation</div>
    <p><strong>Observations:</strong> Private beds consistently register the highest occupancy (around 250–320), general beds peak in March (150–220), and ICU beds stay below 100. This reflects a varied demand across bed types.</p>
    <p><strong>Recommendations:</strong></p>
    <p><strong>Adjust Staffing and Capacity:</strong> Analyze bed occupancy trends and adjust staffing levels accordingly. Ensure that general and ICU beds are sufficiently staffed during seasonal peaks.</p>
    <p><strong>Streamline Discharge Processes:</strong> Implement efficient discharge procedures to improve bed turnover. This is crucial during high occupancy periods to accommodate new admissions.</p>
    <p><strong>Resource Rebalancing:</strong> Consider redistributing resources—such as specialized equipment and personnel—to critical areas, especially during periods of anticipated high demand.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for Styling (Suggestion 2)
    st.markdown(
        """
        <style>
            /* Gradient Title */
            .title {
                font-size: 45px;
                font-weight: bold;
                text-align: center;
                color: white;
                background: linear-gradient(90deg, #1e3c72, #2a5298);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            }
            /* Image Styling */
            .image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px 0;
            }
            .image {
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                transition: transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
            }
            .image:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
            }
        </style>
        """, unsafe_allow_html=True)
        
    # Display the Image with Inline Style for Size (Suggestion 2)
    st.markdown(
        """
        <div class="image-container">
            <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
        </div>
        """.format(base64.b64encode(open("E:\\vscode\\S2.png", "rb").read()).decode()),
        unsafe_allow_html=True,
    )
        
    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    
    # Suggestion 3: Improve Billing and Financial Processes
    st.markdown("""
    <div class="suggestion-box" style="border-color: #FFC107; background-color: #fff8e1;">
    <div class="suggestion-title">Suggestion 3: Improve Billing and Financial Processes</div>
    <p><strong>Observations:</strong> Billing amounts show high variability, with occasional peaks in maximum values and very low minimums. This indicates a skewed distribution and potential inconsistencies.</p>
    <p><strong>Recommendations:</strong></p>
    <p><strong>Standardize Billing Procedures:</strong> Develop clear and transparent billing policies. Use standardized billing formats and provide detailed breakdowns to minimize discrepancies.</p>
    <p><strong>Flexible Payment Plans:</strong> Introduce customizable payment options and work closely with insurance providers to streamline claims, thereby reducing financial burdens on patients.</p>
    <p><strong>Regular Financial Reviews:</strong> Conduct periodic audits of billing data to identify and address outliers, ensuring consistent revenue management and cost control.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for Styling (Suggestion 3)
    st.markdown(
        """
        <style>
            /* Gradient Title */
            .title {
                font-size: 45px;
                font-weight: bold;
                text-align: center;
                color: white;
                background: linear-gradient(90deg, #1e3c72, #2a5298);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            }
            /* Image Styling */
            .image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px 0;
            }
            .image {
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                transition: transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
            }
            .image:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Display the Image with Inline Style for Size (Suggestion 3)
    st.markdown(
        """
        <div class="image-container">
            <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
        </div>
        """.format(base64.b64encode(open("E:\\vscode\\S3.png", "rb").read()).decode()),
        unsafe_allow_html=True,
    )
        
    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    
    # Suggestion 4: Enhance Diagnostic and Test Efficiency
    st.markdown("""
    <div class="suggestion-box" style="border-color: #9C27B0; background-color: #f3e5f5;">
    <div class="suggestion-title">Suggestion 4: Enhance Diagnostic and Test Efficiency</div>
    <p><strong>Observations:</strong> Blood tests are the most frequently performed diagnostic procedure, especially for common illnesses like flu and viral infections. This leads to high testing volumes.</p>
    <p><strong>Recommendations:</strong></p>
    <p><strong>Invest in Rapid Diagnostics:</strong> Upgrade laboratory equipment and adopt rapid diagnostic technologies to reduce turnaround times, enabling quicker clinical decisions.</p>
    <p><strong>Implement Standard Testing Protocols:</strong> Create and enforce protocols that minimize redundant tests without compromising diagnostic accuracy. This will improve efficiency and reduce costs.</p>
    <p><strong>Optimize Lab Workflows:</strong> Reorganize lab processes and staff schedules to ensure timely processing of tests, thereby enhancing overall patient management and satisfaction.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for Styling (Suggestion 4)
    st.markdown(
        """
        <style>
            /* Gradient Title */
            .title {
                font-size: 45px;
                font-weight: bold;
                text-align: center;
                color: white;
                background: linear-gradient(90deg, #1e3c72, #2a5298);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            }
            /* Image Styling */
            .image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px 0;
            }
            .image {
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                transition: transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
            }
            .image:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Display the Image with Inline Style for Size (Suggestion 4)
    st.markdown(
        """
        <div class="image-container">
            <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
        </div>
        """.format(base64.b64encode(open("E:\\vscode\\S4.png", "rb").read()).decode()),
        unsafe_allow_html=True,
    )
        
    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    
    # Suggestion 5: Focus on Doctor Performance and Patient Feedback
    st.markdown("""
    <div class="suggestion-box" style="border-color: #E91E63; background-color: #fce4ec;">
    <div class="suggestion-title">Suggestion 5: Focus on Doctor Performance and Feedback</div>
    <p><strong>Observations:</strong> Although overall doctor contributions are similar, certain doctors (e.g., Ravi D) consistently outperform others, while some (e.g., Jay Sinha) could improve.</p>
    <p><strong>Recommendations:</strong></p>
    <p><strong>Benchmark Performance:</strong> Regularly analyze performance metrics and patient feedback to identify high achievers and areas needing improvement.</p>
    <p><strong>Encourage Continuous Training:</strong> Facilitate targeted training sessions and share best practices among doctors to elevate overall care quality.</p>
    <p><strong>Implement Incentive Programs:</strong> Establish reward and recognition programs to motivate doctors and encourage the adoption of innovative treatment protocols.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for Styling (Suggestion 5)
    st.markdown(
        """
        <style>
            /* Gradient Title */
            .title {
                font-size: 45px;
                font-weight: bold;
                text-align: center;
                color: white;
                background: linear-gradient(90deg, #1e3c72, #2a5298);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            }
            /* Image Styling */
            .image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px 0;
            }
            .image {
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                transition: transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
            }
            .image:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Display the Image with Inline Style for Size (Suggestion 5)
    st.markdown(
        """
        <div class="image-container">
            <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
        </div>
        """.format(base64.b64encode(open("E:\\vscode\\S5.png", "rb").read()).decode()),
        unsafe_allow_html=True,
    )
        
    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    
    # Suggestion 6: Optimize Follow-Up and Length of Stay
    st.markdown("""
    <div class="suggestion-box" style="border-color: #FF5722; background-color: #ffebee;">
    <div class="suggestion-title">Suggestion 6: Optimize Follow-Up and Length of Stay</div>
    <p><strong>Observations:</strong> The average length of stay is approximately 10-15 days, with extended stays for illnesses like Malaria and Typhoid. Follow-up durations vary widely from 5 to 40 days.</p>
    <p><strong>Recommendations:</strong></p>
    <p><strong>Streamline Discharge Protocols:</strong> Develop efficient discharge processes to reduce unnecessary prolonged hospital stays, ensuring patients are discharged safely and promptly.</p>
    <p><strong>Tailor Follow-Up Plans:</strong> Create diagnosis-specific follow-up protocols that balance effective patient monitoring with optimal resource utilization. This helps in reducing both follow-up duration and hospital stay.</p>
    <p><strong>Leverage Data Insights:</strong> Use historical data to identify bottlenecks in care pathways and continuously refine treatment strategies to shorten average stays without compromising care quality.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for Styling (Suggestion 6)
    st.markdown(
        """
        <style>
            /* Gradient Title */
            .title {
                font-size: 45px;
                font-weight: bold;
                text-align: center;
                color: white;
                background: linear-gradient(90deg, #1e3c72, #2a5298);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            }
            /* Image Styling */
            .image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px 0;
            }
            .image {
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                transition: transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
            }
            .image:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Display the Image with Inline Style for Size (Suggestion 6)
    st.markdown(
        """
        <div class="image-container">
            <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
        </div>
        """.format(base64.b64encode(open("E:\\vscode\\S6.png", "rb").read()).decode()),
        unsafe_allow_html=True,
    )
        
    st.markdown('<hr class="hr">', unsafe_allow_html=True)
    
    # Suggestion 7: Preventive and Community Outreach Programs
    st.markdown("""
    <div class="suggestion-box" style="border-color: #3F51B5; background-color: #e8eaf6;">
    <div class="suggestion-title">Suggestion 7: Preventive & Community Outreach</div>
    <p><strong>Observations:</strong> Health claims data indicates that viral infections (28%), flu (24.1%), and malaria (20.1%) are highly prevalent, suggesting strong seasonal and environmental influences.</p>
    <p><strong>Recommendations:</strong></p>
    <p><strong>Launch Public Health Initiatives:</strong> Organize vaccination drives, awareness campaigns, and community health screenings to prevent common illnesses. This can help reduce peak admissions and stabilize hospital activity.</p>
    <p><strong>Strengthen Local Partnerships:</strong> Collaborate with community clinics and local health centers to manage minor cases, thus reducing the burden on hospital resources while ensuring widespread healthcare coverage.</p>
    <p><strong>Proactive Monitoring:</strong> Continuously analyze community health data to adjust outreach strategies and quickly address emerging health issues, leading to a healthier overall population.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom CSS for Styling (Suggestion 7)
    st.markdown(
        """
        <style>
            /* Gradient Title */
            .title {
                font-size: 45px;
                font-weight: bold;
                text-align: center;
                color: white;
                background: linear-gradient(90deg, #1e3c72, #2a5298);
                padding: 15px;
                border-radius: 10px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            }
            /* Image Styling */
            .image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 20px 0;
            }
            .image {
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                transition: transform 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
            }
            .image:hover {
                transform: scale(1.05);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5);
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Display the Image with Inline Style for Size (Suggestion 7)
    st.markdown(
        """
        <div class="image-container">
            <img src="data:image/png;base64,{}" class="image" style="width: 80%; max-width: 1000px;" alt="Community Health Diagram">
        </div>
        """.format(base64.b64encode(open("E:\\vscode\\S7.png", "rb").read()).decode()),
        unsafe_allow_html=True,
    )
    
    # Add an eye-catching Thank You section at the bottom with unique animations
    st.markdown("""
    <style>
        .thank-you {
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            color: #ffffff;
            animation: pulse 2s infinite, gradient 3s ease infinite;
            margin: 50px auto 20px auto;
            padding: 20px;
            width: fit-content;
            border: 3px solid #66a6ff;
            border-radius: 10px;
            background: linear-gradient(45deg, #89f7fe, #66a6ff);
            background-size: 200% 200%;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
    </style>
    <div class="thank-you">Thank You!</div>
    """, unsafe_allow_html=True)
# Converts the sidebar text to white color
# ----------------------------------------------------------------------
st.markdown("""
    <style>
        [data-testid="stSidebar"] * {
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        [data-testid="stSidebar"] h1 {
            font-size: 1.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)

    
