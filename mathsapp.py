import streamlit as st
import sympy as sp
import math

# --- THEME SETUP ---
st.markdown(
    """
    <style>
    .main {
        background-color: #0A1A2F; /* Mature dark blue background */
        color: white;
    }
    .stTextInput textarea {
        background-color: black !important;
        color: white !important;
    }
    .stTextInput input {
        background-color: black !important;
        color: white !important;
    }
    .sidebar .sidebar-content {
        background-color: #15294B !important; /* Different shade of mature blue */
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- APP TITLE ---
st.title("📘 SmartMaths - JSS & SSS Learning Hub")

# --- HELPER FUNCTIONS ---
def solve_equation(equation_str):
    """Solve a simple algebraic equation like 2*x + 3 = 7"""
    x = sp.Symbol("x")
    try:
        left, right = equation_str.split("=")
        eq = sp.Eq(sp.sympify(left), sp.sympify(right))
        solution = sp.solve(eq, x)
        return solution
    except Exception as e:
        return f"Error: {e}"

def solve_simultaneous(eq1_str, eq2_str):
    """Solve 2 simultaneous equations"""
    x, y = sp.symbols("x y")
    try:
        left1, right1 = eq1_str.split("=")
        left2, right2 = eq2_str.split("=")
        eq1 = sp.Eq(sp.sympify(left1), sp.sympify(right1))
        eq2 = sp.Eq(sp.sympify(left2), sp.sympify(right2))
        solution = sp.solve((eq1, eq2), (x, y))
        return solution
    except Exception as e:
        return f"Error: {e}"

def evaluate_expression(expr_str):
    """Evaluate math expression safely with degrees for trig"""
    try:
        expr_str = expr_str.replace("^", "**")  
        expr_str = expr_str.replace("sin", "math.sin(math.radians")
        expr_str = expr_str.replace("cos", "math.cos(math.radians")
        expr_str = expr_str.replace("tan", "math.tan(math.radians")

        # Close the parentheses automatically
        expr_str = expr_str.replace(")", "))")

        result = eval(expr_str, {"math": math, "sqrt": math.sqrt})
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result
    except Exception as e:
        return f"Error: {e}"

# --- SIDEBAR SELECTION ---
level = st.sidebar.selectbox("Choose Level", ["Junior Secondary (JSS)", "Senior Secondary (SSS)", "Calculator"])

# --- JSS TOPICS ---
if level == "Junior Secondary (JSS)":
    topic = st.selectbox("Choose a JSS Topic", [
        "Fractions",
        "Decimals",
        "Percentages",
        "Simple Equations",
        "Simultaneous Equations",
        "Geometry",
        "Probability",
        "Word Problems",
        "Algebra",
        "Trigonometry"
    ])

    if topic == "Fractions":
        expr = st.text_input("Enter fraction expression (e.g., 1/2 + 3/4):")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

    elif topic == "Decimals":
        expr = st.text_input("Enter decimal expression (e.g., 2.5 * 3.2):")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

    elif topic == "Percentages":
        expr = st.text_input("Enter percentage problem (e.g., 20% of 50):")
        if st.button("Calculate"):
            try:
                if "%" in expr:
                    num, of_val = expr.split(" of ")
                    percent = float(num.replace("%", ""))
                    result = (percent / 100) * float(of_val)
                    st.write("Result:", int(result) if result.is_integer() else result)
                else:
                    st.write("Result:", evaluate_expression(expr))
            except Exception as e:
                st.write("Error:", e)

    elif topic == "Simple Equations":
        eq = st.text_input("Enter an equation (e.g., 2*x + 3 = 7):")
        if st.button("Solve"):
            st.write("Solution:", solve_equation(eq))

    elif topic == "Simultaneous Equations":
        eq1 = st.text_input("Enter first equation (e.g., 2*x + y = 10):")
        eq2 = st.text_input("Enter second equation (e.g., x - y = 2):")
        if st.button("Solve"):
            st.write("Solution:", solve_simultaneous(eq1, eq2))

    elif topic == "Geometry":
        expr = st.text_input("Enter geometry formula (e.g., Area of circle: 3.14*5^2):")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

    elif topic == "Probability":
        expr = st.text_input("Enter probability expression (e.g., 1/6 + 1/6):")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

    elif topic == "Word Problems":
        st.info("Type word problems in math expressions format. Example: (2+3)*4")

    elif topic == "Algebra":
        eq = st.text_input("Enter algebra equation (e.g., 3*x + 2 = 11):")
        if st.button("Solve"):
            st.write("Solution:", solve_equation(eq))

    elif topic == "Trigonometry":
        expr = st.text_input("Enter trig expression in degrees (e.g., sin(30) + cos(60)):")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

# --- SSS TOPICS ---
elif level == "Senior Secondary (SSS)":
    topic = st.selectbox("Choose an SSS Topic", [
        "Algebra",
        "Calculus",
        "Quadratic Equations",
        "Simultaneous Equations",
        "Trigonometry",
        "Logarithms",
        "Sequences & Series",
        "Matrices",
        "Vectors",
        "Probability & Statistics"
    ])

    if topic == "Algebra":
        eq = st.text_input("Enter algebra equation (e.g., 5*x - 3 = 7):")
        if st.button("Solve"):
            st.write("Solution:", solve_equation(eq))

    elif topic == "Calculus":
        expr = st.text_input("Enter expression to differentiate (e.g., x**2 + 3*x):")
        x = sp.Symbol("x")
        if st.button("Differentiate"):
            try:
                diff_expr = sp.diff(expr, x)
                st.write("Result:", diff_expr)
            except Exception as e:
                st.write("Error:", e)

    elif topic == "Quadratic Equations":
        eq = st.text_input("Enter quadratic equation (e.g., x**2 - 5*x + 6 = 0):")
        if st.button("Solve"):
            st.write("Solution:", solve_equation(eq))

    elif topic == "Simultaneous Equations":
        eq1 = st.text_input("Enter first equation (e.g., 2*x + y = 10):")
        eq2 = st.text_input("Enter second equation (e.g., x - y = 4):")
        if st.button("Solve"):
            st.write("Solution:", solve_simultaneous(eq1, eq2))

    elif topic == "Trigonometry":
        expr = st.text_input("Enter trig expression in degrees (e.g., sin(45) + cos(30)):")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

    elif topic == "Logarithms":
        expr = st.text_input("Enter logarithm expression (e.g., log(100,10)):")
        if st.button("Calculate"):
            try:
                if "log" in expr:
                    base_expr = expr.replace("log", "math.log")
                    st.write("Result:", eval(base_expr, {"math": math}))
                else:
                    st.write("Result:", evaluate_expression(expr))
            except Exception as e:
                st.write("Error:", e)

    elif topic == "Sequences & Series":
        expr = st.text_input("Enter sequence formula (e.g., sum of first 5 natural numbers: (5*6)/2):")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

    elif topic == "Matrices":
        st.info("Matrix operations coming soon!")

    elif topic == "Vectors":
        st.info("Vector operations coming soon!")

    elif topic == "Probability & Statistics":
        expr = st.text_input("Enter probability/statistics expression (e.g., (1/6) + (1/6)):")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

# --- GENERAL CALCULATOR ---
elif level == "Calculator":
    expr = st.text_input("Enter any math expression:")
    if st.button("Calculate"):
        st.write("Result:", evaluate_expression(expr))
