import streamlit as st
import sympy as sp
import math

# Set page config with a book icon
st.set_page_config(page_title="mathsapp", page_icon="📘", layout="wide")

# Apply custom CSS for mature dark blue theme and sidebar with different blue
st.markdown(
    """
    <style>
    body {
        background-color: #0A1D37;
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #102542;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("📘 maths learning hub")

# Sidebar navigation
level = st.sidebar.selectbox("Choose Level", ["Junior Secondary (JSS)", "Senior Secondary (SSS)", "Calculator"])

# Junior Secondary Topics
if level == "Junior Secondary (JSS)":
    topic = st.selectbox("Choose a Topic", [
        "Fractions", 
        "Decimals", 
        "Percentages", 
        "Algebra", 
        "Simultaneous Equations",
        "Geometry", 
        "Mensuration",
        "Probability",
        "Statistics",
        "Indices (Coming Soon)",
        "Logarithms (Coming Soon)",
        "Quadratic Equations (Coming Soon)",
        "Simple Interest (Coming Soon)",
        "Matrices (Coming Soon)"
    ])
    
    if topic == "Fractions":
        expr = st.text_input("Enter a fraction expression (e.g., 1/2 + 3/4):")
        if st.button("Calculate"):
            try:
                result = eval(expr)
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Decimals":
        expr = st.text_input("Enter a decimal expression (e.g., 2.5 + 3.1):")
        if st.button("Calculate"):
            try:
                result = eval(expr)
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Percentages":
        expr = st.text_input("Enter percentage (e.g., 20% of 50):")
        if st.button("Calculate"):
            try:
                if "of" in expr:
                    parts = expr.split("of")
                    percent = float(parts[0].replace("%", "").strip())
                    number = float(parts[1].strip())
                    result = (percent / 100) * number
                else:
                    result = eval(expr)
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Algebra":
        expr = st.text_input("Enter an algebraic expression (e.g., 2*x + 3*x):")
        if st.button("Simplify"):
            try:
                x = sp.symbols("x")
                simplified = sp.simplify(expr)
                st.success(f"Simplified: {simplified}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Simultaneous Equations":
        st.write("Solve equations (e.g., 2*x + y = 10, x - y = 2)")
        eq1 = st.text_input("Equation 1:")
        eq2 = st.text_input("Equation 2:")
        if st.button("Solve"):
            try:
                x, y = sp.symbols("x y")
                sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
                st.success(f"Solution: {sol}")
            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.info(f"{topic} will be available soon.")

# Senior Secondary Topics
elif level == "Senior Secondary (SSS)":
    topic = st.selectbox("Choose a Topic", [
        "Trigonometry", 
        "Differentiation", 
        "Integration", 
        "Sequences and Series", 
        "Vectors",
        "Complex Numbers",
        "Further Probability",
        "Further Statistics",
        "Differential Equations (Coming Soon)",
        "Loci (Coming Soon)",
        "Linear Programming (Coming Soon)",
        "Permutation & Combination (Coming Soon)",
        "Binomial Expansion (Coming Soon)"
    ])
    
    if topic == "Trigonometry":
        expr = st.text_input("Enter a trig expression (e.g., sin(30) + cos(60)):")
        if st.button("Calculate"):
            try:
                result = eval(expr, {"__builtins__": None}, {
                    "sin": lambda x: math.sin(math.radians(x)),
                    "cos": lambda x: math.cos(math.radians(x)),
                    "tan": lambda x: math.tan(math.radians(x)),
                    "pi": math.pi
                })
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Differentiation":
        expr = st.text_input("Enter an expression to differentiate (e.g., x**2 + 3*x):")
        if st.button("Differentiate"):
            try:
                x = sp.symbols("x")
                diff = sp.diff(expr, x)
                st.success(f"Differentiated: {diff}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Integration":
        expr = st.text_input("Enter an expression to integrate (e.g., x**2):")
        if st.button("Integrate"):
            try:
                x = sp.symbols("x")
                integ = sp.integrate(expr, x)
                st.success(f"Integrated: {integ}")
            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.info(f"{topic} will be available soon.")

# Calculator
elif level == "Calculator":
    expr = st.text_input("Enter any expression (supports sin, cos, tan in degrees):")
    if st.button("Calculate"):
        try:
            result = eval(expr, {"__builtins__": None}, {
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "sqrt": math.sqrt,
                "log": math.log10,
                "pi": math.pi
            })
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
