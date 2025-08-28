import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats
import math

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="All-in-One Maths App", layout="wide")

# Apply mature dark blue theme styling
st.markdown(
    """
    <style>
        body {
            background-color: #0a1a2f;
            color: #f5f5f5;
        }
        .stApp {
            background-color: #0a1a2f;
            color: #f5f5f5;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stRadio {
            background-color: #1c2d4a !important;
            color: #f5f5f5 !important;
            border-radius: 10px;
        }
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #0a1a2f !important;
            color: #f5f5f5 !important;
        }
        section[data-testid="stSidebar"] .stSelectbox,
        section[data-testid="stSidebar"] .stRadio {
            background-color: #1c2d4a !important;
            color: #f5f5f5 !important;
            border-radius: 8px;
        }
        /* Button styling */
        .stButton>button {
            background-color: #1c2d4a !important;
            color: #ffffff !important;
            border-radius: 12px;
            border: 1px solid #3e5c96;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #3e5c96 !important;
            box-shadow: 0px 0px 12px #3e5c96;
            color: #ffffff !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------- SIDEBAR ---------
st.sidebar.title("📘 Maths App")
level = st.sidebar.selectbox("Select Level", ["Junior Secondary", "Senior Secondary", "Calculator"])

if level == "Junior Secondary":
    topic = st.sidebar.radio("Choose a topic:", 
        ["Arithmetic", "Algebra", "Geometry", "Statistics", "Trigonometry"])

elif level == "Senior Secondary":
    topic = st.sidebar.radio("Choose a topic:", 
        ["Algebra", "Calculus", "Matrices", "Trigonometry", "Statistics"])

else:  # Calculator option
    topic = "Calculator"

# --------- TOPIC HANDLERS (your existing solvers go here) ---------
if topic == "Arithmetic":
    st.subheader("Arithmetic Solver")
    expr = st.text_input("Enter arithmetic expression (e.g. 5*(2+3)):")
    if st.button("Solve Arithmetic"):
        try:
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Geometry":
    st.subheader("Geometry Solver")
    shape = st.selectbox("Choose a shape", ["Circle", "Rectangle", "Triangle"])
    if shape == "Circle":
        r = st.number_input("Radius:", min_value=0.0)
        if st.button("Solve Geometry"):
            area = math.pi * r**2
            perimeter = 2 * math.pi * r
            st.write(f"Area = {area:.2f}, Circumference = {perimeter:.2f}")
    elif shape == "Rectangle":
        l = st.number_input("Length:", min_value=0.0)
        w = st.number_input("Width:", min_value=0.0)
        if st.button("Solve Geometry"):
            st.write(f"Area = {l*w:.2f}, Perimeter = {2*(l+w):.2f}")
    elif shape == "Triangle":
        b = st.number_input("Base:", min_value=0.0)
        h = st.number_input("Height:", min_value=0.0)
        if st.button("Solve Geometry"):
            st.write(f"Area = {0.5*b*h:.2f}")

elif topic == "Calculator":
    st.subheader("🧮 General Calculator")
    expr = st.text_input("Enter any expression (e.g. 2+3*5, sin(pi/3), sqrt(25)):")
    angle_mode = st.radio("Angle Mode (for trig)", ["Degrees", "Radians"])
    if st.button("Calculate"):
        try:
            parsed = sp.sympify(expr, evaluate=False)
            if angle_mode == "Degrees":
                parsed = parsed.xreplace({
                    arg: arg * sp.pi/180 for arg in parsed.atoms(sp.Number)
                })
            result = parsed.evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
