import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats

# ============ APP CONFIG ============
st.set_page_config(page_title="All-in-One Maths App", layout="wide")

# Custom CSS for UI polish
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
        }
        .stSidebar {
            background-color: black !important;
        }
        .stTextInput > div > div > input {
            background-color: #1e1e2f;
            color: white;
        }
        .stButton > button {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
        }
        .stSuccess {
            background-color: #004080;
            padding: 10px;
            border-radius: 10px;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ============ SIDEBAR ============
st.sidebar.title("📘 Maths App")
mode = st.sidebar.selectbox("Select Mode", ["Junior Secondary", "Senior Secondary", "Calculator"])

if mode == "Junior Secondary":
    topic = st.sidebar.radio("Choose Topic", ["Arithmetic", "Algebra", "Geometry", "Statistics", "Trigonometry"])
elif mode == "Senior Secondary":
    topic = st.sidebar.radio("Choose Topic", ["Algebra", "Calculus", "Trigonometry", "Matrices", "Probability"])
else:
    topic = "Calculator"

# ============ TOPIC LOGIC ============

# 1. Arithmetic
if topic == "Arithmetic":
    st.subheader("Arithmetic Solver")
    expr = st.text_input("Enter an arithmetic expression (e.g. 5*(2+3)):")

    if st.button("Solve Arithmetic"):
        try:
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# 2. Algebra
elif topic == "Algebra":
    st.subheader("Algebra Solver")
    expr = st.text_input("Enter algebraic expression (e.g. expand((x+2)**2)):")

    if st.button("Solve Algebra"):
        try:
            x = sp.symbols('x')
            result = sp.sympify(expr)
            st.success(f"Result: {sp.simplify(result)}")
        except Exception as e:
            st.error(f"Error: {e}")

# 3. Geometry (placeholder)
elif topic == "Geometry":
    st.subheader("Geometry Solver")
    st.info("More geometry tools coming soon...")

# 4. Statistics
elif topic == "Statistics":
    st.subheader("Statistics Solver")
    data = st.text_input("Enter numbers separated by commas (e.g. 2,4,6,8):")

    if st.button("Calculate Stats"):
        try:
            nums = list(map(float, data.split(",")))
            mean = stats.mean(nums)
            median = stats.median(nums)
            mode = stats.mode(nums)
            st.success(f"Mean: {mean}, Median: {median}, Mode: {mode}")
        except Exception as e:
            st.error(f"Error: {e}")

# 5. Trigonometry
elif topic == "Trigonometry":
    st.subheader("Trigonometry Solver")

    expr = st.text_input("Enter trig expression (e.g. sin(30), cos(pi/4), tan(60)):")
    mode_angle = st.radio("Select Angle Mode", ["Degrees", "Radians"])

    if st.button("Solve Trigonometry"):
        try:
            if mode_angle == "Degrees":
                expr_deg = expr.replace("sin(", ")sp.sin(sp.rad(")
                expr_deg = expr_deg.replace("cos(", ")sp.cos(sp.rad(")
                expr_deg = expr_deg.replace("tan(", ")sp.tan(sp.rad(")
                result = eval(expr_deg)
            else:  # Radians
                result = sp.sympify(expr).evalf()

            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# 6. Calculus
elif topic == "Calculus":
    st.subheader("Calculus Solver")
    expr = st.text_input("Enter expression (e.g. x**2 + 2*x):")
    option = st.radio("Choose Operation", ["Differentiate", "Integrate"])

    if st.button("Solve Calculus"):
        try:
            x = sp.symbols('x')
            parsed_expr = sp.sympify(expr)
            if option == "Differentiate":
                result = sp.diff(parsed_expr, x)
            else:
                result = sp.integrate(parsed_expr, x)
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# 7. Matrices
elif topic == "Matrices":
    st.subheader("Matrix Calculator")
    matA = st.text_area("Enter Matrix A (comma-separated rows, e.g. 1 2; 3 4):")
    matB = st.text_area("Enter Matrix B (optional, same format):")
    operation = st.radio("Choose Operation", ["Add", "Subtract", "Multiply", "Determinant A", "Inverse A"])

    if st.button("Solve Matrix"):
        try:
            A = sp.Matrix([[float(num) for num in row.split()] for row in matA.split(";")])

            if operation in ["Add", "Subtract", "Multiply"] and matB.strip():
                B = sp.Matrix([[float(num) for num in row.split()] for row in matB.split(";")])

            if operation == "Add":
                result = A + B
            elif operation == "Subtract":
                result = A - B
            elif operation == "Multiply":
                result = A * B
            elif operation == "Determinant A":
                result = A.det()
            elif operation == "Inverse A":
                result = A.inv()

            st.success(f"Result:\n{result}")
        except Exception as e:
            st.error(f"Error: {e}")

# 8. Probability
elif topic == "Probability":
    st.subheader("Probability Solver")
    st.info("Probability tools coming soon...")

# 9. Calculator (New!)
elif topic == "Calculator":
    st.subheader("🧮 General Calculator")
    expr = st.text_input("Enter any expression (e.g. 2+3*5, sin(pi/3), sqrt(25)):")

    if st.button("Calculate"):
        try:
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

