import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats
import math

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="All-in-One Maths App", layout="wide")

# --------- THEME ---------
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
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #0a0a0a !important;
            color: #f5f5f5 !important;
        }
        section[data-testid="stSidebar"] * {
            color: #f5f5f5 !important;
        }
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
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --------- SIDEBAR ---------
st.sidebar.title("📘 Maths App")
level = st.sidebar.selectbox("Select Level", ["Junior Secondary", "Senior Secondary", "Calculator"])

if level == "Junior Secondary":
    topic = st.sidebar.radio("Choose a topic:", ["Arithmetic", "Algebra", "Geometry", "Statistics", "Trigonometry"])

elif level == "Senior Secondary":
    topic = st.sidebar.radio("Choose a topic:", ["Algebra", "Calculus", "Matrices", "Trigonometry", "Statistics"])

else:
    topic = "Calculator"

# Allowed functions for sympy
allowed_funcs = {
    "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
    "sqrt": sp.sqrt, "log": sp.log, "exp": sp.exp,
    "pi": sp.pi, "e": sp.E
}

# --------- TOPIC HANDLERS ---------
if topic == "Arithmetic":
    st.subheader("Arithmetic Solver")
    expr = st.text_input("Enter arithmetic expression (e.g. 5*(2+3)):")
    if st.button("Solve Arithmetic"):
        try:
            result = sp.sympify(expr, locals=allowed_funcs).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Algebra":
    st.subheader("Algebra Solver")
    equation = st.text_input("Enter equation (e.g. x**2 - 4 = 0):")
    variable = st.text_input("Variable to solve for:", "x")
    if st.button("Solve Algebra"):
        try:
            var = sp.Symbol(variable)
            sol = sp.solve(sp.sympify(equation, locals=allowed_funcs), var)
            st.success(f"Solutions: {sol}")
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

elif topic == "Trigonometry":
    st.subheader("Trigonometry Solver")
    expr = st.text_input("Enter expression (e.g. sin(30), cos(pi/3)):")
    angle_mode = st.radio("Angle Mode", ["Degrees", "Radians"])
    if st.button("Solve Trigonometry"):
        try:
            parsed = sp.sympify(expr, locals=allowed_funcs)
            if angle_mode == "Degrees":
                parsed = parsed.xreplace({
                    arg: arg * sp.pi/180 for arg in parsed.atoms(sp.Number)
                })
            result = parsed.evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Statistics":
    st.subheader("Statistics Calculator")
    data = st.text_input("Enter numbers separated by commas (e.g. 1,2,3,4,5):")
    if st.button("Calculate Stats"):
        try:
            nums = [float(x) for x in data.split(",")]
            st.write(f"Mean: {stats.mean(nums)}")
            st.write(f"Median: {stats.median(nums)}")
            st.write(f"Variance: {stats.pvariance(nums)}")
            st.write(f"Standard Deviation: {stats.pstdev(nums)}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Calculus":
    st.subheader("Calculus Solver")
    expr = st.text_input("Enter expression (e.g. x**2 + 2*x + 1):")
    variable = st.text_input("Variable:", "x")
    action = st.radio("Choose:", ["Differentiate", "Integrate"])
    if st.button("Solve Calculus"):
        try:
            var = sp.Symbol(variable)
            parsed = sp.sympify(expr, locals=allowed_funcs)
            if action == "Differentiate":
                result = sp.diff(parsed, var)
            else:
                result = sp.integrate(parsed, var)
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Matrices":
    st.subheader("Matrix Solver")
    matrix_str = st.text_area("Enter matrix rows separated by ';' (e.g. 1 2; 3 4):")
    if st.button("Solve Matrix"):
        try:
            rows = [[float(num) for num in row.split()] for row in matrix_str.split(";")]
            M = sp.Matrix(rows)
            st.write(f"Matrix: {M}")
            st.write(f"Determinant: {M.det()}")
            if M.det() != 0:
                st.write(f"Inverse: {M.inv()}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Calculator":
    st.subheader("🧮 General Calculator")
    expr = st.text_input("Enter any expression (e.g. 2+3*5, sin(pi/3), sqrt(25)):")
    angle_mode = st.radio("Angle Mode (for trig)", ["Degrees", "Radians"])
    if st.button("Calculate"):
        try:
            parsed = sp.sympify(expr, locals=allowed_funcs)
            if angle_mode == "Degrees":
                parsed = parsed.xreplace({
                    arg: arg * sp.pi/180 for arg in parsed.atoms(sp.Number)
                })
            result = parsed.evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
