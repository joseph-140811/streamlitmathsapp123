import streamlit as st
import sympy as sp
import math

# Page config
st.set_page_config(page_title="Maths App 📘", page_icon="📘", layout="wide")

# Theme styling
st.markdown(
    """
    <style>
        .main {
            background-color: #0A1A44; /* Mature dark blue */
            color: white;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: black;
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #123456; /* Sidebar another type of mature blue */
        }
        .stSelectbox>div>div>select {
            background-color: black;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📘 Maths App")
st.sidebar.title("📘 Topics")

# Helper: Algebra equation parser
def parse_equation(eq):
    x = sp.symbols("x")
    try:
        expr = sp.sympify(eq)
        return sp.simplify(expr)
    except:
        return "Invalid equation"

# Helper: Solve simultaneous equations
def solve_simultaneous(eq1, eq2):
    x, y = sp.symbols("x y")
    try:
        sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
        return sol
    except:
        return "Invalid equations"

# Trigonometry with degrees
def evaluate_trig(expr):
    try:
        expr = expr.replace("sin", "math.sin(math.radians") \
                           .replace("cos", "math.cos(math.radians") \
                           .replace("tan", "math.tan(math.radians")
        expr = expr.replace(")", "))")
        return eval(expr)
    except:
        return "Invalid trig expression"

# Sidebar
level = st.sidebar.radio("Select Level", ["JSS", "SSS"])
if level == "JSS":
    topic = st.sidebar.radio("Select Topic", [
        "Arithmetic", "Fractions", "Decimals", "Percentages",
        "Algebra", "Simultaneous Equations", "Trigonometry"
    ])
else:
    topic = st.sidebar.radio("Select Topic", [
        "Quadratic Equations", "Simultaneous Equations", "Trigonometry",
        "Logarithms", "Calculus"
    ])

# Main Logic
if topic == "Arithmetic":
    num1 = st.number_input("Enter first number:", step=1.0, format="%.f")
    num2 = st.number_input("Enter second number:", step=1.0, format="%.f")
    operation = st.selectbox("Choose operation:", ["Add", "Subtract", "Multiply", "Divide"])
    if st.button("Calculate"):
        if operation == "Add":
            st.success(int(num1 + num2))
        elif operation == "Subtract":
            st.success(int(num1 - num2))
        elif operation == "Multiply":
            st.success(int(num1 * num2))
        elif operation == "Divide":
            st.success(num1 / num2 if num2 != 0 else "Error: Division by zero")

elif topic == "Algebra":
    eq = st.text_input("Enter algebraic expression (e.g. 2*x + 2*x):")
    if st.button("Simplify"):
        result = parse_equation(eq)
        st.success(result)

elif topic == "Simultaneous Equations":
    eq1 = st.text_input("Enter first equation (e.g. 2*x + y - 5):")
    eq2 = st.text_input("Enter second equation (e.g. x - y - 1):")
    if st.button("Solve"):
        result = solve_simultaneous(eq1, eq2)
        st.success(result)

elif topic == "Trigonometry":
    expr = st.text_input("Enter trig expression (e.g. sin(30), cos(60), tan(45)):")
    if st.button("Evaluate"):
        result = evaluate_trig(expr)
        st.success(result)

elif topic == "Quadratic Equations":
    eq = st.text_input("Enter quadratic equation (e.g. x**2 + 5*x + 6):")
    if st.button("Solve"):
        x = sp.symbols("x")
        try:
            result = sp.solve(sp.sympify(eq), x)
            st.success(result)
        except:
            st.error("Invalid quadratic equation")

elif topic == "Logarithms":
    val = st.number_input("Enter value:")
    base = st.number_input("Enter base (default 10):", value=10, step=1, format="%.f")
    if st.button("Calculate Log"):
        try:
            result = math.log(val, base)
            st.success(result)
        except:
            st.error("Invalid log input")

elif topic == "Calculus":
    expr = st.text_input("Enter expression (e.g. x**2 + 3*x):")
    if st.button("Differentiate"):
        x = sp.symbols("x")
        try:
            result = sp.diff(sp.sympify(expr), x)
            st.success(result)
        except:
            st.error("Invalid expression")
