import streamlit as st
import sympy as sp
import math
import fractions
import numpy as np
from scipy import stats

# Page config
st.set_page_config(page_title="Maths App 📘", page_icon="📘", layout="wide")

# Theme styling
st.markdown(
    """
    <style>
        .main {
            background-color: #2B4A9B; /* Distinct mature blue for main content */
            color: white;
        }
        .stTextInput>div>div>input, .stNumberInput>div>div>input {
            background-color: black;
            color: white;
        }
        section[data-testid="stSidebar"] {
            background-color: #123456; /* Keep sidebar blue as is */
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

# Helper: Trigonometry with degrees
def evaluate_trig(expr):
    try:
        # Define degree symbol
        deg = sp.deg
        # Replace trig functions with SymPy versions that handle degrees
        expr = expr.replace("sin", "sp.sin(sp.deg") \
                   .replace("cos", "sp.cos(sp.deg") \
                   .replace("tan", "sp.tan(sp.deg")
        expr = expr.replace(")", "))")
        result = eval(expr, {"sp": sp, "deg": deg})
        return round(float(result), 4)  # Convert to float and round to 4 decimal places
    except Exception as e:
        return f"Error: Invalid trig expression ({str(e)})"

# Helper: Fraction operations
def fraction_operation(num1, den1, num2, den2, operation):
    try:
        f1 = fractions.Fraction(num1, den1)
        f2 = fractions.Fraction(num2, den2)
        if operation == "Add":
            result = f1 + f2
        elif operation == "Subtract":
            result = f1 - f2
        elif operation == "Multiply":
            result = f1 * f2
        elif operation == "Divide":
            if f2 == 0:
                return "Error: Division by zero"
            result = f1 / f2
        return f"{result.numerator}/{result.denominator}"
    except:
        return "Invalid fraction input"

# Helper: Decimal operations
def decimal_operation(num1, num2, operation):
    try:
        if operation == "Add":
            return round(num1 + num2, 4)
        elif operation == "Subtract":
            return round(num1 - num2, 4)
        elif operation == "Multiply":
            return round(num1 * num2, 4)
        elif operation == "Divide":
            if num2 == 0:
                return "Error: Division by zero"
            return round(num1 / num2, 4)
    except:
        return "Invalid decimal input"

# Helper: Percentage calculations
def percentage_operation(value, percentage, operation):
    try:
        if operation == "Percentage of":
            return round((value * percentage) / 100, 4)
        elif operation == "Increase by":
            return round(value + (value * percentage) / 100, 4)
        elif operation == "Decrease by":
            return round(value - (value * percentage) / 100, 4)
    except:
        return "Invalid percentage input"

# Helper: Matrix operations (for 2x2 matrices)
def matrix_operation(mat1, mat2, operation):
    try:
        m1 = np.array(mat1)
        m2 = np.array(mat2)
        if operation == "Add":
            return m1 + m2
        elif operation == "Subtract":
            return m1 - m2
        elif operation == "Multiply":
            return np.dot(m1, m2)
    except:
        return "Invalid matrix input"

# Helper: Vector operations
def vector_operation(vec1, vec2, operation):
    try:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        if len(v1) != len(v2):
            return "Vectors must be of same dimension"
        if operation == "Dot Product":
            return np.dot(v1, v2)
        elif operation == "Cross Product" and len(v1) == 3:
            return np.cross(v1, v2)
        else:
            return "Cross product only for 3D vectors"
    except:
        return "Invalid vector input"

# Helper: Probability calculations
def probability_operation(n, k, operation):
    try:
        if operation == "Permutation":
            return math.perm(n, k)
        elif operation == "Combination":
            return math.comb(n, k)
    except:
        return "Invalid input"

# Helper: Statistics calculations
def statistics_operation(data, operation):
    try:
        arr = np.array(data)
        if operation == "Mean":
            return np.mean(arr)
        elif operation == "Median":
            return np.median(arr)
        elif operation == "Mode":
            mode = stats.mode(arr)
            return mode.mode if mode.count > 1 else "No unique mode"
        elif operation == "Standard Deviation":
            return np.std(arr)
    except:
        return "Invalid data input"

# Helper: Sequences and Series
def series_operation(first_term, common_diff_ratio, n_terms, series_type):
    try:
        if series_type == "Arithmetic Sum":
            return n_terms / 2 * (2 * first_term + (n_terms - 1) * common_diff_ratio)
        elif series_type == "Geometric Sum":
            if common_diff_ratio == 1:
                return first_term * n_terms
            return first_term * (1 - common_diff_ratio ** n_terms) / (1 - common_diff_ratio)
    except:
        return "Invalid input"

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
        "Logarithms", "Calculus", "Matrices", "Vectors",
        "Probability", "Statistics", "Sequences and Series"
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

elif topic == "Fractions":
    num1 = st.number_input("Enter first numerator:", step=1, format="%.f")
    den1 = st.number_input("Enter first denominator:", step=1, format="%.f", min_value=1)
    num2 = st.number_input("Enter second numerator:", step=1, format="%.f")
    den2 = st.number_input("Enter second denominator:", step=1, format="%.f", min_value=1)
    operation = st.selectbox("Choose operation:", ["Add", "Subtract", "Multiply", "Divide"])
    if st.button("Calculate"):
        result = fraction_operation(int(num1), int(den1), int(num2), int(den2), operation)
        st.success(result)

elif topic == "Decimals":
    num1 = st.number_input("Enter first decimal number:", step=0.1)
    num2 = st.number_input("Enter second decimal number:", step=0.1)
    operation = st.selectbox("Choose operation:", ["Add", "Subtract", "Multiply", "Divide"])
    if st.button("Calculate"):
        result = decimal_operation(num1, num2, operation)
        st.success(result)

elif topic == "Percentages":
    value = st.number_input("Enter value:", step=1.0, min_value=0.0)
    percentage = st.number_input("Enter percentage:", step=1.0, min_value=0.0)
    operation = st.selectbox("Choose operation:", ["Percentage of", "Increase by", "Decrease by"])
    if st.button("Calculate"):
        result = percentage_operation(value, percentage, operation)
        st.success(result)

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
    expr = st.text_input("Enter trig expression in degrees (e.g. sin(30), cos(60), tan(45)):")
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
    val = st.number_input("Enter value:", min_value=0.0001, step=0.1)
    base = st.number_input("Enter base (default 10):", value=10, step=1, format="%.f", min_value=1)
    if st.button("Calculate Log"):
        try:
            result = math.log(val, base)
            st.success(round(result, 4))
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

elif topic == "Matrices":
    st.write("Enter 2x2 matrices as comma-separated values (e.g., 1,2,3,4 for [[1,2],[3,4]])")
    mat1_str = st.text_input("Enter first matrix:")
    mat2_str = st.text_input("Enter second matrix:")
    operation = st.selectbox("Choose operation:", ["Add", "Subtract", "Multiply"])
    if st.button("Calculate"):
        try:
            mat1 = [[float(x) for x in mat1_str.split(',')[:2]], [float(x) for x in mat1_str.split(',')[2:]]]
            mat2 = [[float(x) for x in mat2_str.split(',')[:2]], [float(x) for x in mat2_str.split(',')[2:]]]
            result = matrix_operation(mat1, mat2, operation)
            st.success(result)
        except:
            st.error("Invalid matrix input")

elif topic == "Vectors":
    st.write("Enter vectors as comma-separated values (e.g., 1,2,3)")
    vec1_str = st.text_input("Enter first vector:")
    vec2_str = st.text_input("Enter second vector:")
    operation = st.selectbox("Choose operation:", ["Dot Product", "Cross Product"])
    if st.button("Calculate"):
        try:
            vec1 = [float(x) for x in vec1_str.split(',')]
            vec2 = [float(x) for x in vec2_str.split(',')]
            result = vector_operation(vec1, vec2, operation)
            st.success(result)
        except:
            st.error("Invalid vector input")

elif topic == "Probability":
    n = st.number_input("Enter n:", step=1, format="%.f", min_value=0)
    k = st.number_input("Enter k:", step=1, format="%.f", min_value=0)
    operation = st.selectbox("Choose operation:", ["Permutation", "Combination"])
    if st.button("Calculate"):
        result = probability_operation(int(n), int(k), operation)
        st.success(result)

elif topic == "Statistics":
    data_str = st.text_input("Enter data as comma-separated values (e.g., 1,2,3,4):")
    operation = st.selectbox("Choose operation:", ["Mean", "Median", "Mode", "Standard Deviation"])
    if st.button("Calculate"):
        try:
            data = [float(x) for x in data_str.split(',')]
            result = statistics_operation(data, operation)
            st.success(result)
        except:
            st.error("Invalid data input")

elif topic == "Sequences and Series":
    first_term = st.number_input("Enter first term:")
    common = st.number_input("Enter common difference/ratio:")
    n_terms = st.number_input("Enter number of terms:", step=1, format="%.f", min_value=1)
    series_type = st.selectbox("Choose series type:", ["Arithmetic Sum", "Geometric Sum"])
    if st.button("Calculate"):
        result = series_operation(first_term, common, int(n_terms), series_type)
        st.success(result)
