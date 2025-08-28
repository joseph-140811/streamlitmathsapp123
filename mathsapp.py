import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats

st.set_page_config(page_title="All-in-One Maths App", layout="wide")

# Sidebar for navigation
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

# ---------------- TOPICS ----------------

# Arithmetic
if topic == "Arithmetic":
    st.subheader("Arithmetic Solver")
    expr = st.text_input("Enter arithmetic expression (e.g. 5*(2+3)):")
    if st.button("Solve Arithmetic"):
        try:
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# Algebra
elif topic == "Algebra":
    st.subheader("Algebra Solver")
    expr = st.text_input("Enter algebraic expression (e.g. expand((x+2)**2)):")
    if st.button("Solve Algebra"):
        try:
            x = sp.symbols('x')
            result = sp.sympify(expr)
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# Geometry
elif topic == "Geometry":
    st.subheader("Geometry Solver")
    st.write("Coming soon...")

# Statistics
elif topic == "Statistics":
    st.subheader("Statistics Calculator")
    data = st.text_input("Enter numbers separated by commas (e.g. 2,4,6,8):")
    if st.button("Calculate Stats"):
        try:
            nums = list(map(float, data.split(",")))
            mean = stats.mean(nums)
            median = stats.median(nums)
            st.success(f"Mean: {mean}, Median: {median}")
        except Exception as e:
            st.error(f"Error: {e}")

# Trigonometry
elif topic == "Trigonometry":
    st.subheader("Trigonometry Solver")
    expr = st.text_input("Enter trig expression (e.g. sin(30), cos(pi/4), tan(60)):")
    mode_angle = st.radio("Select Angle Mode", ["Degrees", "Radians"])
    if st.button("Solve Trigonometry"):
        try:
            parsed = sp.sympify(expr, evaluate=False)
            if mode_angle == "Degrees":
                parsed = parsed.xreplace({
                    arg: arg * sp.pi/180 for arg in parsed.atoms(sp.Number)
                })
            result = parsed.evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# Calculus
elif topic == "Calculus":
    st.subheader("Calculus Solver")
    expr = st.text_input("Enter function (e.g. x**2 + 3*x):")
    x = sp.symbols('x')
    if st.button("Differentiate"):
        try:
            result = sp.diff(sp.sympify(expr), x)
            st.success(f"Derivative: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
    if st.button("Integrate"):
        try:
            result = sp.integrate(sp.sympify(expr), x)
            st.success(f"Integral: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# Matrices
elif topic == "Matrices":
    st.subheader("Matrix Calculator")
    matA = st.text_area("Enter Matrix A (e.g. 1,2;3,4):")
    matB = st.text_area("Enter Matrix B (optional for addition/multiplication):")
    operation = st.selectbox("Operation", ["Determinant", "Inverse", "Add", "Multiply", "Subtract"])
    if st.button("Solve Matrix"):
        try:
            A = sp.Matrix([[float(num) for num in row.split(",")] for row in matA.split(";")])
            B = None
            if matB.strip():
                B = sp.Matrix([[float(num) for num in row.split(",")] for row in matB.split(";")])
            if operation == "Determinant":
                result = A.det()
            elif operation == "Inverse":
                result = A.inv()
            elif operation == "Add":
                result = A + B
            elif operation == "Subtract":
                result = A - B
            elif operation == "Multiply":
                result = A * B
            st.success(f"Result:\n{result}")
        except Exception as e:
            st.error(f"Error: {e}")

# Calculator
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
