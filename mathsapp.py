import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats
import re

st.set_page_config(page_title="MathCore", layout="wide")

# Sidebar
st.sidebar.title("MathCore")
level = st.sidebar.selectbox("Select Level", ["Junior Secondary", "Senior Secondary", "Calculator"])

if level == "Junior Secondary":
    topic = st.sidebar.radio("Select Topic", ["Arithmetic", "Algebra", "Geometry", "Statistics", "Simultaneous Equations (2x2)"])

elif level == "Senior Secondary":
    topic = st.sidebar.radio("Select Topic", ["Algebra", "Trigonometry", "Calculus", "Probability", "Statistics"])

else:
    topic = "Calculator"

st.title("🧮 MathCore - All-in-One Mathematics App")

# Junior Secondary
if level == "Junior Secondary":
    if topic == "Arithmetic":
        expr = st.text_input("Enter arithmetic expression (e.g., 5*(2+3)):")
        if st.button("Solve Arithmetic"):
            try:
                result = sp.sympify(expr).evalf()
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Algebra":
        equation = st.text_input("Enter algebraic equation (e.g., x^2 - 5*x + 6 = 0):")
        if st.button("Solve Algebra"):
            try:
                x = sp.symbols('x')
                sol = sp.solve(equation, x)
                st.success(f"Solutions: {sol}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Geometry":
        st.info("Geometry solver coming soon...")

    elif topic == "Statistics":
        data = st.text_input("Enter numbers separated by commas:")
        if st.button("Calculate Statistics"):
            try:
                nums = [float(n) for n in data.split(",")]
                mean = stats.mean(nums)
                median = stats.median(nums)
                st.success(f"Mean: {mean}, Median: {median}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Simultaneous Equations (2x2)":
        st.subheader("Solve Simultaneous Equations")
        st.latex(r"a1*x + b1*y = c1")
        st.latex(r"a2*x + b2*y = c2")

        a1 = st.number_input("a1", value=1.0)
        b1 = st.number_input("b1", value=1.0)
        c1 = st.number_input("c1", value=1.0)
        a2 = st.number_input("a2", value=1.0)
        b2 = st.number_input("b2", value=1.0)
        c2 = st.number_input("c2", value=1.0)

        if st.button("Solve 2x2 System"):
            try:
                x, y = sp.symbols('x y')
                eq1 = sp.Eq(a1*x + b1*y, c1)
                eq2 = sp.Eq(a2*x + b2*y, c2)
                sol = sp.solve((eq1, eq2), (x, y))
                st.success(f"Solution: {sol}")
            except Exception as e:
                st.error(f"Error: {e}")

# Senior Secondary
elif level == "Senior Secondary":
    if topic == "Algebra":
        equation = st.text_input("Enter algebraic equation (e.g., x^2 - 5*x + 6 = 0):")
        if st.button("Solve Algebra"):
            try:
                x = sp.symbols('x')
                sol = sp.solve(equation, x)
                st.success(f"Solutions: {sol}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Trigonometry":
        st.subheader("Trigonometry Solver")
        mode = st.radio("Select mode:", ["Degrees", "Radians"])
        expr = st.text_input("Enter trig expression (e.g. sin(30), cos(pi/4), tan(60)):")

        if st.button("Solve Trigonometry"):
            try:
                if mode == "Degrees":
                    expr_deg = expr.replace("sin(", "sp.sin(sp.rad(")
                    expr_deg = expr_deg.replace("cos(", "sp.cos(sp.rad(")
                    expr_deg = expr_deg.replace("tan(", "sp.tan(sp.rad(")
                    result = eval(expr_deg)
                else:
                    result = sp.sympify(expr).evalf()

                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Calculus":
        function = st.text_input("Enter function (e.g., x^2 + 3*x):")
        if st.button("Differentiate"):
            try:
                x = sp.symbols('x')
                diff = sp.diff(function, x)
                st.success(f"Derivative: {diff}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Probability":
        st.info("Probability solver coming soon...")

    elif topic == "Statistics":
        data = st.text_input("Enter numbers separated by commas:")
        if st.button("Calculate Statistics"):
            try:
                nums = [float(n) for n in data.split(",")]
                mean = stats.mean(nums)
                median = stats.median(nums)
                st.success(f"Mean: {mean}, Median: {median}")
            except Exception as e:
                st.error(f"Error: {e}")

# Calculator
elif level == "Calculator":
    expr = st.text_input("Enter any expression (supports +, -, *, /, sin, cos, tan, etc.):")
    if st.button("Calculate"):
        try:
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
