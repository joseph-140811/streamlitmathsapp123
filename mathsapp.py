import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats
import re

# --- PAGE CONFIG ---
st.set_page_config(page_title="Math Core", layout="wide")

# Custom CSS Theme
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0b1e39;
            color: #ffffff;
        }
        section[data-testid="stSidebar"] {
            background-color: #000000;
        }
        section[data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        .stTextInput > div > div > input {
            background-color: #1a2b4d;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #1f3a66;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 8px 16px;
        }
        .stButton>button:hover {
            background-color: #335c99;
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Helper function: handle implicit multiplication
implicit_mul_patterns = [
    re.compile(r"(\d)\s*(?=\()"),       # 2(3+4) → 2*(3+4)
    re.compile(r"(\))\s*(?=\d)"),       # (3+4)2 → (3+4)*2
    re.compile(r"(\))\s*(?=\()"),       # (2+3)(4+5) → (2+3)*(4+5)
    re.compile(r"(\d)([a-zA-Z])")       # 2x → 2*x
]

TRIG_FUNCS = {
    "sin": sp.sin,
    "cos": sp.cos,
    "tan": sp.tan,
    "asin": sp.asin,
    "acos": sp.acos,
    "atan": sp.atan,
}

# Function to safely evaluate expressions
def safe_eval(expr, angle_mode="Radians"):
    if not expr:
        return ""
    expr = expr.replace("^", "**")

    # Fix implicit multiplication
    for pattern in implicit_mul_patterns:
        expr = pattern.sub(r"\\1*", expr)

    # Trigonometry handling
    for name, func in TRIG_FUNCS.items():
        regex = re.compile(rf"(?<![a-zA-Z_]){name}\\((.*?)\\)")
        while regex.search(expr):
            expr = regex.sub(lambda m: f"{name}(sp.rad({m.group(1)}))" if angle_mode=="Degrees" else f"{name}({m.group(1)})", expr)

    try:
        return sp.sympify(expr, locals={**TRIG_FUNCS, "pi": sp.pi, "e": sp.E}).evalf()
    except Exception as e:
        return f"Error: {e}"

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Math Core Navigation")
section = st.sidebar.radio("Select Level", ["Junior Secondary", "Senior Secondary", "Calculator"])

# --- JUNIOR SECONDARY ---
if section == "Junior Secondary":
    topic = st.sidebar.selectbox("Choose Topic", [
        "Arithmetic", "Fractions & Decimals", "GCD & LCM", "Simple & Compound Interest",
        "Ratio & Proportion", "Pythagoras Theorem", "Algebra (JSS)", "Simultaneous Equations",
        "Geometry", "Statistics", "Trigonometry"
    ])

    st.header(f"Junior Secondary - {topic}")
    expr = st.text_input("Enter expression:")
    angle_mode = st.radio("Angle Mode", ["Degrees", "Radians"], horizontal=True)
    if st.button("Solve"):
        st.success(safe_eval(expr, angle_mode))

# --- SENIOR SECONDARY ---
elif section == "Senior Secondary":
    topic = st.sidebar.selectbox("Choose Topic", [
        "Algebra (SSS)", "Quadratic Equations", "Calculus", "Probability",
        "Matrices", "Logarithms & Indices", "Graphs", "Trigonometry"
    ])

    st.header(f"Senior Secondary - {topic}")
    expr = st.text_input("Enter expression:")
    angle_mode = st.radio("Angle Mode", ["Degrees", "Radians"], horizontal=True)
    if st.button("Solve"):
        st.success(safe_eval(expr, angle_mode))

# --- CALCULATOR ---
else:
    st.header("General Calculator")
    expr = st.text_input("Enter calculation:")
    angle_mode = st.radio("Angle Mode", ["Degrees", "Radians"], horizontal=True)
    if st.button("Calculate"):
        st.success(safe_eval(expr, angle_mode))
