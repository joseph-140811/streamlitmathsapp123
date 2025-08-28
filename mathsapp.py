import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats
import re

# ---- CUSTOM CSS THEME ----
st.markdown(
    """
    <style>
    body {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    .stSidebar {
        background-color: #000000 !important;
    }
    .stMarkdown, .stTextInput, .stNumberInput, .stSelectbox, .stButton>button, textarea, input, .stTextArea textarea {
        background-color: #1E3A8A !important;
        color: #E2E8F0 !important;
        border-radius: 10px;
        padding: 5px;
    }
    .stButton>button {
        background-color: #1E90FF !important;
        color: white !important;
        font-weight: bold;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---- APP TITLE ----
st.title("📘 All-in-One Maths App")
st.write("Solve Junior & Senior Secondary School Math Problems — with a clean, mature theme.")

# Sidebar navigation
level = st.sidebar.selectbox("Select Level", ["Junior Secondary", "Senior Secondary"])

# ------------------ JUNIOR SECONDARY ------------------
if level == "Junior Secondary":
    topic = st.sidebar.selectbox("Choose a Topic", [
        "Arithmetic", "Algebra", "Geometry", "Statistics", 
        "Fractions & Decimals", "Simple Interest & Percentage", "Ratio & Proportion"
    ])

    if topic == "Arithmetic":
        st.subheader("Arithmetic Solver")
        expr = st.text_input("Enter an arithmetic expression (e.g., 12/4 + 3*2 or 5(2+3)):")
        if st.button("Solve Arithmetic"):
            try:
                expr_fixed = re.sub(r'(\d)(\()', r'\1*\2', expr)
                result = sp.sympify(expr_fixed)
                st.success(f"Result = {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Algebra":
        st.subheader("Algebra Solver")
        expr = st.text_input("Enter algebraic expression (e.g., x^2 + 3*x + 2):")
        if st.button("Factorize"):
            try:
                x = sp.symbols('x')
                factored = sp.factor(sp.sympify(expr))
                st.success(f"Factorized: {factored}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Geometry":
        st.subheader("Geometry Calculator")
        shape = st.selectbox("Choose a shape", ["Circle", "Rectangle", "Triangle"])
        if shape == "Circle":
            r = st.number_input("Radius", value=1.0)
            if st.button("Calculate Circle"):
                st.success(f"Area = {np.pi*r**2:.2f}, Perimeter = {2*np.pi*r:.2f}")
        elif shape == "Rectangle":
            l = st.number_input("Length", value=1.0)
            w = st.number_input("Width", value=1.0)
            if st.button("Calculate Rectangle"):
                st.success(f"Area = {l*w}, Perimeter = {2*(l+w)}")
        elif shape == "Triangle":
            b = st.number_input("Base", value=1.0)
            h = st.number_input("Height", value=1.0)
            if st.button("Calculate Triangle"):
                st.success(f"Area = {0.5*b*h}")

    elif topic == "Statistics":
        st.subheader("Statistics Calculator")
        numbers = st.text_area("Enter numbers separated by commas")
        if st.button("Calculate Stats"):
            try:
                data = [float(x.strip()) for x in numbers.split(",") if x.strip()]
                if not data:
                    raise ValueError("No valid numbers entered")
                mean_val = stats.mean(data)
                median_val = stats.median(data)
                try:
                    mode_val = stats.mode(data)
                except:
                    mode_val = "No unique mode"
                st.success(f"Mean = {mean_val}, Median = {median_val}, Mode = {mode_val}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Fractions & Decimals":
        st.subheader("Fractions & Decimals")
        expr = st.text_input("Enter fraction/decimal (e.g., 3/4 or 0.75):")
        if st.button("Convert"):
            try:
                frac = sp.Rational(expr)
                st.success(f"Fraction: {frac}, Decimal: {float(frac)}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Simple Interest & Percentage":
        st.subheader("Simple Interest & Percentage")
        p = st.number_input("Principal", value=100.0)
        r = st.number_input("Rate (%)", value=5.0)
        t = st.number_input("Time (years)", value=1.0)
        if st.button("Calculate SI"):
            si = (p*r*t)/100
            st.success(f"Simple Interest = {si}, Total Amount = {p+si}")
        value = st.number_input("Enter Value", value=50.0)
        percent = st.number_input("Percentage", value=10.0)
        if st.button("Percentage of Value"):
            st.success(f"{percent}% of {value} = {(percent/100)*value}")

    elif topic == "Ratio & Proportion":
        st.subheader("Ratio & Proportion")
        a = st.number_input("a", value=1.0)
        b = st.number_input("b", value=2.0)
        c = st.number_input("c", value=3.0)
        if st.button("Find d in a:b = c:d"):
            try:
                d = (b*c)/a
                st.success(f"d = {d}")
            except Exception as e:
                st.error(f"Error: {e}")

# ------------------ SENIOR SECONDARY ------------------
if level == "Senior Secondary":
    topic = st.sidebar.selectbox("Choose a Topic", [
        "Quadratic Equations", "Trigonometry", "Calculus", 
        "Logarithms & Indices", "Probability", "Matrices"
    ])

    if topic == "Quadratic Equations":
        st.subheader("Quadratic Equation Solver")
        a = st.number_input("Coefficient a", value=1)
        b = st.number_input("Coefficient b", value=0)
        c = st.number_input("Coefficient c", value=0)
        if st.button("Solve Quadratic"):
            x = sp.symbols('x')
            eq = a*x**2 + b*x + c
            solutions = sp.solve(eq, x)
            st.success(f"Solutions: {solutions}")

    elif topic == "Trigonometry":
        st.subheader("Trigonometry Evaluator")
        expr = st.text_input("Enter trig expression (e.g., sin(pi/6) + cos(pi/3)): ")
        if st.button("Evaluate Trig"):
            try:
                result = sp.simplify(sp.sympify(expr))
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Calculus":
        st.subheader("Calculus")
        expr = st.text_input("Enter function in x (e.g., x**3 + 2*x):")
        if st.button("Differentiate"):
            try:
                x = sp.symbols('x')
                diff = sp.diff(sp.sympify(expr), x)
                st.success(f"Derivative: {diff}")
            except Exception as e:
                st.error(f"Error: {e}")
        if st.button("Integrate"):
            try:
                x = sp.symbols('x')
                integ = sp.integrate(sp.sympify(expr), x)
                st.success(f"Integral: {integ}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Logarithms & Indices":
        st.subheader("Logarithms & Indices")
        expr = st.text_input("Enter expression (e.g., log(100,10) or 2**5):")
        if st.button("Evaluate Log/Index"):
            try:
                result = sp.simplify(sp.sympify(expr))
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Probability":
        st.subheader("Probability Calculator")
        favorable = st.number_input("Favorable Outcomes", value=1)
        total = st.number_input("Total Outcomes", value=6)
        if st.button("Calculate Probability"):
            try:
                if total <= 0:
                    raise ValueError("Total outcomes must be greater than 0")
                prob = favorable/total
                st.success(f"Probability = {prob}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Matrices":
        st.subheader("Matrix Calculator")
        matA = st.text_area("Enter Matrix A (rows separated by ;, elements by space) e.g. 1 2;3 4")
        matB = st.text_area("Enter Matrix B (same format)")
        operation = st.selectbox("Choose Operation", ["Add", "Subtract", "Multiply", "Determinant A", "Inverse A"])
        if st.button("Calculate Matrix"):
            try:
                A = sp.Matrix([[float(num) for num in row.split()] for row in matA.split(";")])
                if matB:
                    B = sp.Matrix([[float(num) for num in row.split()] for row in matB.split(";")])
                if operation == "Add":
                    st.success(f"A + B = {A+B}")
                elif operation == "Subtract":
                    st.success(f"A - B = {A-B}")
                elif operation == "Multiply":
                    st.success(f"A * B = {A*B}")
                elif operation == "Determinant A":
                    st.success(f"det(A) = {A.det()}")
                elif operation == "Inverse A":
                    if A.det() == 0:
                        st.error("Matrix A is singular and cannot be inverted")
                    else:
                        st.success(f"A^(-1) = {A.inv()}")
            except Exception as e:
                st.error(f"Error: {e}")
