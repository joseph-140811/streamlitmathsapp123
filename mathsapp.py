import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats

# ================== THEME (Mature Dark Blue) ==================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0A1A2F; /* Dark mature blue */
        color: #E0E0E0; /* Soft white text */
    }
    .stSidebar {
        background-color: #000000; /* Sidebar black */
        color: #FFFFFF;
    }
    .stSidebar .stRadio label, .stSidebar .stSelectbox label, .stSidebar .stTextInput label {
        color: #FFFFFF !important;
    }
    .stButton button {
        background-color: #004080;
        color: white;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================== MAIN APP ==================
st.title("📘 MathCore – All-in-One Maths App")

# Sidebar menu
level = st.sidebar.radio("Choose Level:", ["Junior Secondary", "Senior Secondary", "Calculator"])

# ------------------ TRIGONOMETRY FIX ------------------
def trig_solver(expr, mode):
    try:
        if mode == "Degrees":
            # Wrap numeric arguments in radians conversion
            expr = expr.replace("sin(", "sp.sin(sp.rad(")
            expr = expr.replace("cos(", "sp.cos(sp.rad(")
            expr = expr.replace("tan(", "sp.tan(sp.rad(")
            result = eval(expr)
        else:
            result = sp.sympify(expr).evalf()
        return result
    except Exception as e:
        return f"Error: {e}"

# ------------------ CONTENT BASED ON LEVEL ------------------
if level == "Junior Secondary":
    topic = st.sidebar.radio("Select Topic:", [
        "Arithmetic", "Algebra", "Simultaneous Equations", "Geometry", "Statistics", "Trigonometry"
    ])

    if topic == "Arithmetic":
        expr = st.text_input("Enter arithmetic expression (e.g. 5*(2+3)):")
        if st.button("Solve Arithmetic"):
            try:
                result = sp.sympify(expr).evalf()
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Algebra":
        eqn = st.text_input("Enter an equation (e.g. x + 2 - 5):")
        if st.button("Solve Algebra"):
            try:
                x = sp.symbols('x')
                result = sp.solve(sp.sympify(eqn), x)
                st.success(f"Solution: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Simultaneous Equations":
        st.write("Enter two equations:")
        eq1 = st.text_input("Equation 1 (e.g. 2*x + y - 5)")
        eq2 = st.text_input("Equation 2 (e.g. x - y - 1)")
        if st.button("Solve Simultaneous Equations"):
            try:
                x, y = sp.symbols('x y')
                sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
                st.success(f"Solution: {sol}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Geometry":
        st.write("Geometry formulas coming soon! (Areas, Volumes, etc.)")

    elif topic == "Statistics":
        nums = st.text_input("Enter numbers separated by commas:")
        if st.button("Calculate Statistics"):
            try:
                data = list(map(float, nums.split(",")))
                mean = stats.mean(data)
                median = stats.median(data)
                st.success(f"Mean: {mean}, Median: {median}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Trigonometry":
        mode = st.radio("Mode:", ["Degrees", "Radians"])
        expr = st.text_input("Enter trig expression (e.g. sin(30), cos(pi/4)):")
        if st.button("Solve Trigonometry"):
            result = trig_solver(expr, mode)
            st.success(f"Result: {result}")

elif level == "Senior Secondary":
    topic = st.sidebar.radio("Select Topic:", [
        "Calculus", "Complex Numbers", "Matrices", "Trigonometry"
    ])

    if topic == "Trigonometry":
        mode = st.radio("Mode:", ["Degrees", "Radians"])
        expr = st.text_input("Enter trig expression (e.g. sin(60), tan(pi/3)):")
        if st.button("Solve Trigonometry"):
            result = trig_solver(expr, mode)
            st.success(f"Result: {result}")

    else:
        st.write("More Senior Secondary features coming soon!")

elif level == "Calculator":
    expr = st.text_input("Enter any math expression (e.g. 2+3*4, sin(pi/6)):")
    if st.button("Calculate"):
        try:
            result = sp.sympify(expr).evalf()
            st.success(f"Result: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
