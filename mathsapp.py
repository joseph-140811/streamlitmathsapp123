import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats
import re

# App title
st.title("📘 Math Mastery Hub")

# Sidebar for navigation
mode = st.sidebar.selectbox("Select Mode", ["Junior Secondary", "Senior Secondary", "Calculator"])

# Function to safely evaluate expressions
def safe_eval(expr):
    try:
        expr = re.sub(r"(\d)\s*\(", r"\1*(", expr)
        return sp.sympify(expr).evalf()
    except Exception:
        return "Invalid Expression"

# JSS Topics
if mode == "Junior Secondary":
    topic = st.sidebar.radio("Select Topic", [
        "Arithmetic", "Algebra", "Geometry", "Statistics", "Simultaneous Equations"
    ])

    if topic == "Arithmetic":
        expr = st.text_input("Enter Arithmetic Expression")
        if st.button("Calculate"):
            if expr:
                st.write("Result:", int(float(safe_eval(expr))))

    elif topic == "Algebra":
        equation = st.text_input("Enter Algebraic Equation (e.g., x+2-5)")
        if st.button("Calculate"):
            if equation:
                x = sp.Symbol('x')
                try:
                    sol = sp.solve(sp.Eq(eval(equation), 0), x)
                    st.write("Solution:", sol)
                except Exception as e:
                    st.write("Error:", e)

    elif topic == "Geometry":
        shape = st.selectbox("Select Shape", ["Circle", "Rectangle", "Triangle"])
        if st.button("Calculate"):
            if shape == "Circle":
                r = st.number_input("Enter radius", 0.0)
                st.write("Area:", round(np.pi * r**2))
                st.write("Perimeter:", round(2 * np.pi * r))
            elif shape == "Rectangle":
                l = st.number_input("Enter length", 0.0)
                b = st.number_input("Enter breadth", 0.0)
                st.write("Area:", round(l * b))
                st.write("Perimeter:", round(2 * (l + b)))
            elif shape == "Triangle":
                b = st.number_input("Enter base", 0.0)
                h = st.number_input("Enter height", 0.0)
                st.write("Area:", round(0.5 * b * h))

    elif topic == "Statistics":
        data = st.text_area("Enter numbers separated by commas")
        if st.button("Calculate"):
            if data:
                try:
                    nums = [float(i) for i in data.split(",")]
                    st.write("Mean:", round(stats.mean(nums)))
                    st.write("Median:", round(stats.median(nums)))
                    st.write("Mode:", stats.mode(nums))
                except Exception:
                    st.write("Invalid input")

    elif topic == "Simultaneous Equations":
        eq1 = st.text_input("Enter first equation (e.g., 2*x + y - 5)")
        eq2 = st.text_input("Enter second equation (e.g., x - y - 1)")
        if st.button("Calculate"):
            if eq1 and eq2:
                x, y = sp.symbols("x y")
                try:
                    sol = sp.solve([eval(eq1), eval(eq2)], (x, y))
                    st.write("Solution:", sol)
                except Exception as e:
                    st.write("Error:", e)

# SSS Topics
elif mode == "Senior Secondary":
    topic = st.sidebar.radio("Select Topic", [
        "Trigonometry", "Calculus", "Probability", "Algebra", "Geometry", "Statistics"
    ])

    if topic == "Trigonometry":
        func = st.text_input("Enter Trigonometric Function (e.g., sin(30), cos(45))")
        if st.button("Calculate"):
            if func:
                try:
                    result = eval(f"np.{func}")
                    st.write("Result:", round(result))
                except Exception as e:
                    st.write("Error:", e)

    elif topic == "Calculus":
        expr = st.text_input("Enter function (e.g., x**2 + 3*x)")
        if st.button("Calculate"):
            if expr:
                x = sp.Symbol("x")
                try:
                    diff = sp.diff(expr, x)
                    integ = sp.integrate(expr, x)
                    st.write("Derivative:", diff)
                    st.write("Integral:", integ)
                except Exception as e:
                    st.write("Error:", e)

    elif topic == "Probability":
        n = st.number_input("Enter total number of outcomes", 1)
        f = st.number_input("Enter number of favorable outcomes", 0)
        if st.button("Calculate"):
            if n > 0:
                st.write("Probability:", round(f / n, 2))

    elif topic == "Algebra":
        equation = st.text_input("Enter Algebraic Equation (e.g., x**2 - 4)")
        if st.button("Calculate"):
            if equation:
                x = sp.Symbol("x")
                try:
                    sol = sp.solve(sp.Eq(eval(equation), 0), x)
                    st.write("Solution:", sol)
                except Exception as e:
                    st.write("Error:", e)

    elif topic == "Geometry":
        shape = st.selectbox("Select Shape", ["Sphere", "Cylinder", "Cone"])
        if st.button("Calculate"):
            if shape == "Sphere":
                r = st.number_input("Enter radius", 0.0)
                st.write("Surface Area:", round(4 * np.pi * r**2))
                st.write("Volume:", round((4/3) * np.pi * r**3))
            elif shape == "Cylinder":
                r = st.number_input("Enter radius", 0.0)
                h = st.number_input("Enter height", 0.0)
                st.write("Surface Area:", round(2 * np.pi * r * (r + h)))
                st.write("Volume:", round(np.pi * r**2 * h))
            elif shape == "Cone":
                r = st.number_input("Enter radius", 0.0)
                h = st.number_input("Enter height", 0.0)
                l = np.sqrt(r**2 + h**2)
                st.write("Surface Area:", round(np.pi * r * (r + l)))
                st.write("Volume:", round((1/3) * np.pi * r**2 * h))

    elif topic == "Statistics":
        data = st.text_area("Enter numbers separated by commas")
        if st.button("Calculate"):
            if data:
                try:
                    nums = [float(i) for i in data.split(",")]
                    st.write("Mean:", round(stats.mean(nums)))
                    st.write("Median:", round(stats.median(nums)))
                    st.write("Mode:", stats.mode(nums))
                except Exception:
                    st.write("Invalid input")

# Calculator
elif mode == "Calculator":
    expr = st.text_input("Enter any Expression")
    if st.button("Calculate"):
        if expr:
            st.write("Result:", int(float(safe_eval(expr))))

# Custom CSS for theme
st.markdown("""
    <style>
    /* Whole app background */
    .stApp {
        background-color: #001f3f !important;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #001f3f !important;
        color: white !important;
    }
    /* Text color */
    .stMarkdown, .stRadio, .stSelectbox, .stTextInput, .stNumberInput, .stTextArea, .stButton > button {
        color: white !important;
    }
    /* Input fields black with white text */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > textarea {
        background-color: black !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)
