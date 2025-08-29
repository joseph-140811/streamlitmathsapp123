import streamlit as st
import sympy as sp
import math

# ---------------------------
# Helper function for algebra
# ---------------------------
def parse_equation(equation_str):
    """
    Converts a string like '2*x + 3 = 7' into a SymPy Eq object.
    """
    if "=" in equation_str:
        left, right = equation_str.split("=")
        return sp.Eq(sp.sympify(left.strip()), sp.sympify(right.strip()))
    else:
        # Treat as expression equal to 0
        return sp.Eq(sp.sympify(equation_str.strip()), 0)

# ---------------------------
# Streamlit UI Setup
# ---------------------------
st.set_page_config(page_title="MathsApp", page_icon="📘", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #0A1128; /* Mature dark blue background */
        color: white; /* White text */
    }
    .stTextInput>div>div>input {
        background-color: black;
        color: white;
    }
    section[data-testid="stSidebar"] {
        background-color: #001F54; /* Slightly different mature blue */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📘 Maths Learning Hub")

# ---------------------------
# Choose Level
# ---------------------------
level = st.sidebar.radio("Choose Level", ["Junior Secondary (JSS)", "Senior Secondary (SSS)"])

if level == "Junior Secondary (JSS)":
    topic = st.sidebar.selectbox("Choose a Topic", [
        "Arithmetic", "Algebra", "Geometry", "Trigonometry",
        "Simultaneous Equations", "Calculator"
    ])

elif level == "Senior Secondary (SSS)":
    topic = st.sidebar.selectbox("Choose a Topic", [
        "Algebra", "Calculus", "Trigonometry", "Geometry",
        "Simultaneous Equations", "Statistics", "Calculator"
    ])

# ---------------------------
# Topic Logic
# ---------------------------
if topic == "Arithmetic":
    expr = st.text_input("Enter an arithmetic expression:")
    if st.button("Calculate"):
        try:
            result = eval(expr)
            st.success(f"Result: {int(result)}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Algebra":
    eq_str = st.text_input("Enter an algebraic equation (e.g., 2*x + 3 = 7):")
    if st.button("Solve"):
        try:
            eq = parse_equation(eq_str)
            x = sp.symbols('x')
            sol = sp.solve(eq, x)
            st.success(f"Solution: {sol}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Simultaneous Equations":
    eq1 = st.text_input("Enter first equation (e.g., 2*x + y = 7):")
    eq2 = st.text_input("Enter second equation (e.g., x - y = 1):")
    if st.button("Solve System"):
        try:
            e1 = parse_equation(eq1)
            e2 = parse_equation(eq2)
            x, y = sp.symbols('x y')
            sol = sp.solve([e1, e2], (x, y))
            st.success(f"Solution: {sol}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Trigonometry":
    angle = st.number_input("Enter angle in degrees:", step=1.0)
    function = st.selectbox("Choose function", ["sin", "cos", "tan"])
    if st.button("Calculate"):
        try:
            rad = math.radians(angle)
            if function == "sin":
                result = math.sin(rad)
            elif function == "cos":
                result = math.cos(rad)
            elif function == "tan":
                result = math.tan(rad)
            st.success(f"{function}({int(angle)}) = {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Geometry":
    st.write("📐 Geometry section coming soon!")

elif topic == "Calculus":
    expr = st.text_input("Enter a function of x (e.g., x**2 + 3*x):")
    operation = st.selectbox("Choose operation", ["Differentiate", "Integrate"])
    if st.button("Compute"):
        try:
            x = sp.symbols('x')
            f = sp.sympify(expr)
            if operation == "Differentiate":
                result = sp.diff(f, x)
            else:
                result = sp.integrate(f, x)
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Statistics":
    st.write("📊 Statistics section coming soon!")

elif topic == "Calculator":
    expr = st.text_input("Enter expression:")
    if st.button("Evaluate"):
        try:
            result = eval(expr)
            st.success(f"Result: {int(result)}")
        except Exception as e:
            st.error(f"Error: {e}")
