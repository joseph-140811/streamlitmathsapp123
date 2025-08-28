import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats

# ==========================
# 🎨 Custom Page Config
# ==========================
st.set_page_config(
    page_title="All-in-One Maths App",
    page_icon="📘",
    layout="wide"
)

# Apply custom CSS for mature UI
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background: linear-gradient(135deg, #001f3f, #003366);
        color: white;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: black;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    /* Input boxes */
    .stTextInput input {
        background-color: #1e2b47;
        color: white;
        border-radius: 10px;
        padding: 8px;
    }
    /* Result cards */
    .stAlert {
        background-color: #0d1b2a;
        border-radius: 12px;
        padding: 15px;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📘 All-in-One Maths App")

# ==========================
# Sidebar for Topics
# ==========================
level = st.sidebar.radio("📚 Select Level:", ["Junior Secondary", "Senior Secondary"])

if level == "Junior Secondary":
    topic = st.sidebar.selectbox("Choose a topic:", [
        "Arithmetic", "Algebra", "Geometry", "Statistics", "Trigonometry"
    ])
else:
    topic = st.sidebar.selectbox("Choose a topic:", [
        "Quadratic Equations", "Calculus", "Matrices", "Probability", "Trigonometry"
    ])

# ==========================
# Topic Functions
# ==========================

if topic == "Arithmetic":
    st.subheader("Arithmetic Calculator")
    expr = st.text_input("Enter an arithmetic expression (e.g. 5*(2+3)):")
    if st.button("Solve Arithmetic"):
        try:
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Algebra":
    st.subheader("Algebra Solver")
    expr = st.text_input("Enter an algebraic expression (e.g. x^2 + 2*x + 1):")
    var = st.text_input("Enter the variable (e.g. x):")
    if st.button("Simplify Algebra"):
        try:
            x = sp.symbols(var)
            result = sp.simplify(expr)
            st.success(f"Simplified: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Geometry":
    st.subheader("Geometry - Area & Perimeter")
    shape = st.selectbox("Select a shape:", ["Circle", "Rectangle", "Triangle"])
    if shape == "Circle":
        r = st.number_input("Enter radius:")
        if st.button("Calculate Circle"):
            area = np.pi * r**2
            perimeter = 2 * np.pi * r
            st.success(f"Area: {area:.2f}, Perimeter: {perimeter:.2f}")
    elif shape == "Rectangle":
        l = st.number_input("Length:")
        b = st.number_input("Breadth:")
        if st.button("Calculate Rectangle"):
            area = l * b
            perimeter = 2 * (l + b)
            st.success(f"Area: {area}, Perimeter: {perimeter}")
    elif shape == "Triangle":
        b = st.number_input("Base:")
        h = st.number_input("Height:")
        if st.button("Calculate Triangle"):
            area = 0.5 * b * h
            st.success(f"Area: {area}")

elif topic == "Statistics":
    st.subheader("Statistics Calculator")
    nums = st.text_area("Enter numbers separated by commas:")
    if st.button("Calculate Statistics"):
        try:
            numbers = [float(n) for n in nums.split(",")]
            mean = stats.mean(numbers)
            median = stats.median(numbers)
            mode = stats.mode(numbers)
            st.success(f"Mean: {mean}, Median: {median}, Mode: {mode}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Trigonometry":
    st.subheader("Trigonometry Solver")
    expr = st.text_input("Enter trig expression (e.g. sin(30), cos(pi/4), tan(60)):")
    if st.button("Solve Trigonometry"):
        try:
            # Auto-convert degrees to radians
            expr = expr.replace("sin(", "sp.sin(sp.rad(")
            expr = expr.replace("cos(", "sp.cos(sp.rad(")
            expr = expr.replace("tan(", "sp.tan(sp.rad(")
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Quadratic Equations":
    st.subheader("Quadratic Equation Solver (ax²+bx+c=0)")
    a = st.number_input("Enter a:", value=1.0)
    b = st.number_input("Enter b:", value=0.0)
    c = st.number_input("Enter c:", value=0.0)
    if st.button("Solve Quadratic"):
        x = sp.symbols('x')
        roots = sp.solve(a*x**2 + b*x + c, x)
        st.success(f"Roots: {roots}")

elif topic == "Calculus":
    st.subheader("Calculus")
    expr = st.text_input("Enter a function (e.g. x^2 + 3*x):")
    var = st.text_input("Enter the variable (e.g. x):")
    choice = st.radio("Choose:", ["Differentiate", "Integrate"])
    if st.button("Solve Calculus"):
        try:
            x = sp.symbols(var)
            if choice == "Differentiate":
                result = sp.diff(expr, x)
            else:
                result = sp.integrate(expr, x)
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Matrices":
    st.subheader("Matrix Operations")
    st.write("Enter rows separated by semicolons. Example: `1 2; 3 4`")
    mat1 = st.text_input("Matrix A:")
    mat2 = st.text_input("Matrix B:")
    if st.button("Add Matrices"):
        try:
            A = np.matrix(mat1)
            B = np.matrix(mat2)
            st.success(f"Result:\n{A+B}")
        except Exception as e:
            st.error(f"Error: {e}")
    if st.button("Multiply Matrices"):
        try:
            A = np.matrix(mat1)
            B = np.matrix(mat2)
            st.success(f"Result:\n{A*B}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Probability":
    st.subheader("Probability Calculator")
    fav = st.number_input("Favourable outcomes:")
    total = st.number_input("Total outcomes:")
    if st.button("Calculate Probability"):
        try:
            prob = fav / total
            st.success(f"Probability: {prob:.2f}")
        except Exception as e:
            st.error(f"Error: {e}")
