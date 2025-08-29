import streamlit as st
import sympy as sp
import math

# ========== STYLING ==========
st.set_page_config(page_title="Scholarly Math Companion", page_icon="📘", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #0A1A2F; /* Main dark blue */
        color: white;
    }
    .stTextInput textarea {
        background-color: black !important;
        color: white !important;
        border-radius: 10px;
    }
    .stTextInput input {
        background-color: black !important;
        color: white !important;
        border-radius: 10px;
    }
    section[data-testid="stSidebar"] {
        background-color: #102542; /* Sidebar different mature blue */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== HELPER FUNCTIONS ==========
def evaluate_expression(expr):
    try:
        # Replace ^ with ** for exponentiation
        expr = expr.replace("^", "**")
        # Convert degrees to radians automatically for trig
        expr = expr.replace("sin(", "math.sin(math.radians(")
        expr = expr.replace("cos(", "math.cos(math.radians(")
        expr = expr.replace("tan(", "math.tan(math.radians(")
        expr = expr.replace("asin(", "math.degrees(math.asin(")
        expr = expr.replace("acos(", "math.degrees(math.acos(")
        expr = expr.replace("atan(", "math.degrees(math.atan(")
        return round(eval(expr, {"math": math, "__builtins__": {}}), 0)  # whole number
    except Exception as e:
        return f"Error: {e}"

# ========== SIDEBAR ==========
st.sidebar.title("📘 Scholarly Math Companion")
level = st.sidebar.selectbox("Select Level", ["Junior Secondary", "Senior Secondary", "Calculator"])

# Topics
jss_topics = [
    "Algebra", "Simultaneous Equations", "Geometry", "Mensuration", "Fractions & Decimals",
    "Percentages", "Simple Interest", "Ratio & Proportion", "Statistics", "Linear Graphs"
]

sss_topics = [
    "Algebra", "Trigonometry", "Simultaneous Equations", "Calculus", "Probability",
    "Matrices", "Vectors", "Logarithms", "Sequence & Series", "Complex Numbers"
]

# ========== MAIN APP ==========
st.title("📘 Scholarly Math Companion")

if level == "Junior Secondary":
    topic = st.selectbox("Select a Topic", jss_topics)

    if topic == "Algebra":
        expr = st.text_input("Enter an algebraic expression (e.g., 2*x + 3*x - 4):", "")
        if st.button("Simplify"):
            try:
                simplified = sp.simplify(expr)
                st.write("Simplified Result:", simplified)
            except Exception as e:
                st.write("Error:", e)

    elif topic == "Simultaneous Equations":
        eq1 = st.text_input("Enter first equation (e.g., 2*x + y - 5):")
        eq2 = st.text_input("Enter second equation (e.g., x - y - 1):")
        if st.button("Solve"):
            try:
                x, y = sp.symbols("x y")
                sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
                st.write("Solution:", sol)
            except Exception as e:
                st.write("Error:", e)

    else:
        expr = st.text_input(f"Enter expression for {topic}:", "")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

elif level == "Senior Secondary":
    topic = st.selectbox("Select a Topic", sss_topics)

    if topic == "Algebra":
        expr = st.text_input("Enter an algebraic expression (e.g., (x^2 + 2*x + 1)/(x+1)):", "")
        if st.button("Simplify"):
            try:
                simplified = sp.simplify(expr)
                st.write("Simplified Result:", simplified)
            except Exception as e:
                st.write("Error:", e)

    elif topic == "Simultaneous Equations":
        eq1 = st.text_input("Enter first equation (e.g., 3*x + 2*y - 12):")
        eq2 = st.text_input("Enter second equation (e.g., 2*x - y - 3):")
        if st.button("Solve"):
            try:
                x, y = sp.symbols("x y")
                sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
                st.write("Solution:", sol)
            except Exception as e:
                st.write("Error:", e)

    else:
        expr = st.text_input(f"Enter expression for {topic}:", "")
        if st.button("Calculate"):
            st.write("Result:", evaluate_expression(expr))

else:  # Calculator
    expr = st.text_input("Enter any expression:", "")
    if st.button("Calculate"):
        st.write("Result:", evaluate_expression(expr))
