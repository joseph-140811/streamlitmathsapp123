import streamlit as st
import sympy as sp
import math
import fractions
import numpy as np
import statistics

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
        .stButton>button {
            background-color: #4B5EAA; /* Lighter blue for buttons */
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
        expr = sp.sympify(eq, evaluate=True)
        simplified = sp.simplify(expr)
        return sp.pretty(simplified, use_unicode=False)  # Clean output like 4x, not 4*x
    except:
        return "Invalid equation. Use format like 2x + 2x or x**2 - 4."

# Helper: Solve simultaneous equations
def solve_simultaneous(eq1, eq2):
    x, y = sp.symbols("x y")
    try:
        sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
        return {str(k): str(v) for k, v in sol.items()}  # Clean string output
    except:
        return "Invalid equations. Use format like 2x + y = 5."

# Helper: Trigonometry with degrees
def evaluate_trig(expr):
    try:
        deg = sp.deg
        expr = expr.replace("sin", "sp.sin(sp.deg") \
                   .replace("cos", "sp.cos(sp.deg") \
                   .replace("tan", "sp.tan(sp.deg")
        expr = expr.replace(")", "))")
        result = eval(expr, {"sp": sp, "deg": deg})
        return round(float(result), 4)
    except Exception as e:
        return f"Error: Invalid trig expression. Use format like sin(30) or cos(45). ({str(e)})"

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
        return "Invalid fraction input. Ensure non-zero denominators."

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
        return "Invalid decimal input."

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
        return "Invalid percentage input. Use non-negative numbers."

# Helper: Matrix operations (for 2x2 matrices)
def matrix_operation(mat1, mat2, operation):
    try:
        m1 = np.array(mat1)
        m2 = np.array(mat2)
        if m1.shape != (2, 2) or m2.shape != (2, 2):
            return "Matrices must be 2x2."
        if operation == "Add":
            return m1 + m2
        elif operation == "Subtract":
            return m1 - m2
        elif operation == "Multiply":
            return np.dot(m1, m2)
    except:
        return "Invalid matrix input. Use 4 comma-separated numbers per matrix."

# Helper: Vector operations
def vector_operation(vec1, vec2, operation):
    try:
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        if len(v1) != len(v2):
            return "Vectors must be of same dimension."
        if operation == "Dot Product":
            return round(np.dot(v1, v2), 4)
        elif operation == "Cross Product" and len(v1) == 3:
            return np.round(np.cross(v1, v2), 4)
        else:
            return "Cross product only for 3D vectors."
    except:
        return "Invalid vector input. Use comma-separated numbers."

# Helper: Probability calculations
def probability_operation(n, k, operation):
    try:
        if n < k or n < 0 or k < 0:
            return "Invalid input. Ensure n >= k >= 0."
        if operation == "Permutation":
            return math.perm(n, k)
        elif operation == "Combination":
            return math.comb(n, k)
    except:
        return "Invalid input. Use non-negative integers."

# Helper: Statistics calculations
def statistics_operation(data, operation):
    try:
        arr = np.array(data)
        if len(arr) == 0:
            return "Data cannot be empty."
        if operation == "Mean":
            return round(np.mean(arr), 4)
        elif operation == "Median":
            return round(np.median(arr), 4)
        elif operation == "Mode":
            return round(statistics.mode(arr), 4)
        elif operation == "Standard Deviation":
            return round(np.std(arr), 4)
    except statistics.StatisticsError:
        return "No unique mode."
    except:
        return "Invalid data input. Use comma-separated numbers."

# Helper: Sequences and Series
def series_operation(first_term, common_diff_ratio, n_terms, series_type):
    try:
        if n_terms < 1:
            return "Number of terms must be positive."
        if series_type == "Arithmetic Sum":
            return round(n_terms / 2 * (2 * first_term + (n_terms - 1) * common_diff_ratio), 4)
        elif series_type == "Geometric Sum":
            if common_diff_ratio == 1:
                return round(first_term * n_terms, 4)
            return round(first_term * (1 - common_diff_ratio ** n_terms) / (1 - common_diff_ratio), 4)
    except:
        return "Invalid input. Use valid numbers."

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
    st.write("Enter two integers for basic operations.")
    num1 = st.number_input("Enter first number:", step=1, format="%.f")
    num2 = st.number_input("Enter second number:", step=1, format="%.f")
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
    st.write("Enter numerators and denominators for fraction operations.")
    num1 = st.number_input("Enter first numerator:", step=1, format="%.f")
    den1 = st.number_input("Enter first denominator:", step=1, format="%.f", min_value=1)
    num2 = st.number_input("Enter second numerator:", step=1, format="%.f")
    den2 = st.number_input("Enter second denominator:", step=1, format="%.f", min_value=1)
    operation = st.selectbox("Choose operation:", ["Add", "Subtract", "Multiply", "Divide"])
    if st.button("Calculate"):
        result = fraction_operation(int(num1), int(den1), int(num2), int(den2), operation)
        st.success(result)

elif topic == "Decimals":
    st.write("Enter two decimal numbers for operations.")
    num1 = st.number_input("Enter first decimal number:", step=0.1)
    num2 = st.number_input("Enter second decimal number:", step=0.1)
    operation = st.selectbox("Choose operation:", ["Add", "Subtract", "Multiply", "Divide"])
    if st.button("Calculate"):
        result = decimal_operation(num1, num2, operation)
        st.success(result)

elif topic == "Percentages":
    st.write("Enter a value and percentage for calculations.")
    value = st.number_input("Enter value:", step=1.0, min_value=0.0)
    percentage = st.number_input("Enter percentage:", step=1.0, min_value=0.0)
    operation = st.selectbox("Choose operation:", ["Percentage of", "Increase by", "Decrease by"])
    if st.button("Calculate"):
        result = percentage_operation(value, percentage, operation)
        st.success(result)

elif topic == "Algebra":
    st.write("Enter an algebraic expression to simplify (e.g., 2x + 2x).")
    eq = st.text_input("Enter algebraic expression:")
    if st.button("Simplify"):
        result = parse_equation(eq)
        st.success(result)

elif topic == "Simultaneous Equations":
    st.write("Enter two linear equations (e.g., 2x + y = 5, x - y = 1).")
    eq1 = st.text_input("Enter first equation:")
    eq2 = st.text_input("Enter second equation:")
    if st.button("Solve"):
        result = solve_simultaneous(eq1, eq2)
        st.success(result)

elif topic == "Trigonometry":
    st.write("Enter a trigonometric expression in degrees (e.g., sin(30), cos(60), tan(45)).")
    expr = st.text_input("Enter trig expression in degrees:")
    if st.button("Evaluate"):
        result = evaluate_trig(expr)
        st.success(result)

elif topic == "Quadratic Equations":
    st.write("Enter a quadratic equation (e.g., x^2 + 5x + 6 = 0).")
    eq = st.text_input("Enter quadratic equation:")
    if st.button("Solve"):
        x = sp.symbols("x")
        try:
            result = sp.solve(sp.sympify(eq), x)
            st.success([str(sp.pretty(r, use_unicode=False)) for r in result])
        except:
            st.error("Invalid quadratic equation. Use format like x^2 + 5x + 6 = 0.")

elif topic == "Logarithms":
    st.write("Enter a value and base for logarithm calculation.")
    val = st.number_input("Enter value:", min_value=0.0001, step=0.1)
    base = st.number_input("Enter base (default 10):", value=10, step=1, format="%.f", min_value=1)
    if st.button("Calculate Log"):
        try:
            result = math.log(val, base)
            st.success(round(result, 4))
        except:
            st.error("Invalid log input. Value must be positive, base > 1.")

elif topic == "Calculus":
    st.write("Enter an expression to differentiate (e.g., x^2 + 3x).")
    expr = st.text_input("Enter expression:")
    if st.button("Differentiate"):
        x = sp.symbols("x")
        try:
            result = sp.diff(sp.sympify(expr), x)
            st.success(sp.pretty(result, use_unicode=False))
        except:
            st.error("Invalid expression. Use format like x^2 + 3x.")

elif topic == "Matrices":
    st.write("Enter 2x2 matrices as comma-separated values (e.g., 1,2,3,4 for [[1,2],[3,4]])")
    mat1_str = st.text_input("Enter first matrix:")
    mat2_str = st.text_input("Enter second matrix:")
    operation = st.selectbox("Choose operation:", ["Add", "Subtract", "Multiply"])
    if st.button("Calculate"):
        try:
            mat1 = [[float(x) for x in mat1_str.split(',')[:2]], [float(x) for x in mat1_str.split(',')[2:4]]]
            mat2 = [[float(x) for x in mat2_str.split(',')[:2]], [float(x) for x in mat2_str.split(',')[2:4]]]
            result = matrix_operation(mat1, mat2, operation)
            st.success(result.tolist())
        except:
            st.error("Invalid matrix input. Enter 4 numbers per matrix.")

elif topic == "Vectors":
    st.write("Enter vectors as comma-separated values (e.g., 1,2,3 for a 3D vector).")
    vec1_str = st.text_input("Enter first vector:")
    vec2_str = st.text_input("Enter second vector:")
    operation = st.selectbox("Choose operation:", ["Dot Product", "Cross Product"])
    if st.button("Calculate"):
        try:
            vec1 = [float(x) for x in vec1_str.split(',')]
            vec2 = [float(x) for x in vec2_str.split(',')]
            result = vector_operation(vec1, vec2, operation)
            st.success(str(result))
        except:
            st.error("Invalid vector input. Use comma-separated numbers.")

elif topic == "Probability":
    st.write("Enter n and k for permutation or combination calculations.")
    n = st.number_input("Enter n:", step=1, format="%.f", min_value=0)
    k = st.number_input("Enter k:", step=1, format="%.f", min_value=0)
    operation = st.selectbox("Choose operation:", ["Permutation", "Combination"])
    if st.button("Calculate"):
        result = probability_operation(int(n), int(k), operation)
        st.success(result)

elif topic == "Statistics":
    st.write("Enter data as comma-separated values (e.g., 1,2,3,4).")
    data_str = st.text_input("Enter data:")
    operation = st.selectbox("Choose operation:", ["Mean", "Median", "Mode", "Standard Deviation"])
    if st.button("Calculate"):
        try:
            data = [float(x) for x in data_str.split(',')]
            result = statistics_operation(data, operation)
            st.success(result)
        except:
            st.error("Invalid data input. Use comma-separated numbers.")

elif topic == "Sequences and Series":
    st.write("Enter parameters for arithmetic or geometric series sum.")
    first_term = st.number_input("Enter first term:")
    common = st.number_input("Enter common difference (arithmetic) or ratio (geometric):")
    n_terms = st.number_input("Enter number of terms:", step=1, format="%.f", min_value=1)
    series_type = st.selectbox("Choose series type:", ["Arithmetic Sum", "Geometric Sum"])
    if st.button("Calculate"):
        result = series_operation(first_term, common, int(n_terms), series_type)
        st.success(result)
