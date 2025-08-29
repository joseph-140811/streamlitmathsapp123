import streamlit as st
import sympy as sp
import statistics as stats
import re
import math

# --- Styling (mature theme + white text boxes) ---
st.markdown("""
    <style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #000000; /* Mature black */
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Input boxes */
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.set_page_config(page_title="Maths Master", page_icon="📘")
st.title("📘 Maths Master")
st.write("An all-in-one Junior & Senior Secondary Maths App")

# --- Sidebar Navigation ---
level = st.sidebar.selectbox("Select Level", ["Junior Secondary", "Senior Secondary", "Calculator"])

# --- Utility: clean results ---
def clean_result(result):
    if isinstance(result, (int, float)):
        if float(result).is_integer():
            return int(result)
    return result

# --- JSS Topics ---
if level == "Junior Secondary":
    topic = st.sidebar.radio("Choose Topic", [
        "Arithmetic", "Algebra", "Geometry",
        "Statistics", "Simultaneous Equations"
    ])

    if topic == "Arithmetic":
        expr = st.text_input("Enter arithmetic expression:", value="", placeholder="e.g. 5(2+3) + 10/2")
        if expr:
            try:
                expr = re.sub(r"(\d)\s*\(", r"\1*(", expr)  # handle implicit multiplication
                result = eval(expr, {"__builtins__": None}, {"sqrt": math.sqrt})
                st.success(f"Result: {clean_result(result)}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Algebra":
        expr = st.text_input("Enter algebraic expression:", value="", placeholder="e.g. x^2 + 2x + 1")
        if expr:
            try:
                x = sp.symbols("x")
                result = sp.simplify(expr)
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Geometry":
        shape = st.selectbox("Choose Shape", ["Rectangle", "Circle", "Triangle"])
        if shape == "Rectangle":
            l = st.number_input("Length:", value=0.0, step=1.0)
            w = st.number_input("Width:", value=0.0, step=1.0)
            if l and w:
                st.success(f"Area = {clean_result(l*w)}, Perimeter = {clean_result(2*(l+w))}")
        elif shape == "Circle":
            r = st.number_input("Radius:", value=0.0, step=1.0)
            if r:
                st.success(f"Area = {clean_result(math.pi*r**2)}, Circumference = {clean_result(2*math.pi*r)}")
        elif shape == "Triangle":
            b = st.number_input("Base:", value=0.0, step=1.0)
            h = st.number_input("Height:", value=0.0, step=1.0)
            if b and h:
                st.success(f"Area = {clean_result(0.5*b*h)}")

    elif topic == "Statistics":
        nums = st.text_input("Enter numbers separated by commas:", value="", placeholder="e.g. 2,4,6,8")
        if nums:
            try:
                data = [float(n.strip()) for n in nums.split(",")]
                st.success(f"Mean = {clean_result(stats.mean(data))}, Median = {clean_result(stats.median(data))}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Simultaneous Equations":
        eq1 = st.text_input("Equation 1:", value="", placeholder="e.g. 2*x + y - 5")
        eq2 = st.text_input("Equation 2:", value="", placeholder="e.g. x - y - 1")
        if eq1 and eq2:
            try:
                x, y = sp.symbols("x y")
                sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
                st.success(f"Solution: {sol}")
            except Exception as e:
                st.error(f"Error: {e}")

# --- SSS Topics ---
elif level == "Senior Secondary":
    topic = st.sidebar.radio("Choose Topic", [
        "Trigonometry", "Calculus", "Algebra",
        "Statistics", "Geometry"
    ])

    if topic == "Trigonometry":
        expr = st.text_input("Enter trig expression:", value="", placeholder="e.g. sin(30) + cos(60)")
        if expr:
            try:
                expr = expr.replace("^", "**")
                expr = re.sub(r'(\d+)\(', r'\1*(', expr)  # fix 5(2+3)
                allowed_funcs = {k: getattr(math, k) for k in ["sin", "cos", "tan", "radians", "degrees"]}
                result = eval(expr, {"__builtins__": None}, allowed_funcs)
                st.success(f"Result: {clean_result(result)}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Calculus":
        expr = st.text_input("Enter function of x:", value="", placeholder="e.g. x**2 + 2*x")
        if expr:
            try:
                x = sp.symbols("x")
                deriv = sp.diff(expr, x)
                integ = sp.integrate(expr, x)
                st.success(f"Derivative: {deriv}, Integral: {integ}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Algebra":
        expr = st.text_input("Enter algebraic expression:", value="", placeholder="e.g. (x+1)(x+2)")
        if expr:
            try
