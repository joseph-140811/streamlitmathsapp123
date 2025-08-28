import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats
import math

# =========================
# APP CONFIG
# =========================
st.set_page_config(page_title="Math Master", layout="wide")

# Dark blue theme CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #0A1D37;
            color: #EAEAEA;
        }
        .css-1d391kg {  /* Sidebar */
            background-color: #000000 !important;
            color: #FFFFFF !important;
        }
        .css-1d391kg * {
            color: #FFFFFF !important;
        }
        h1, h2, h3, h4 {
            color: #4DB8FF !important;
        }
        .stTextInput, .stNumberInput, .stSelectbox, .stTextArea {
            background-color: #133B5C;
            color: white;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# =========================
# MAIN APP STRUCTURE
# =========================
st.title("📘 Math Master – JSS & SSS All-in-One")

level = st.sidebar.radio("Select Level:", ["Junior Secondary", "Senior Secondary", "Calculator"])

# =========================
# JSS SECTION
# =========================
if level == "Junior Secondary":
    topic = st.sidebar.selectbox("Choose a JSS Topic:", [
        "Arithmetic",
        "Fractions & Decimals",
        "Algebra",
        "Simultaneous Equations",
        "Geometry",
        "Trigonometry",
        "Statistics"
    ])

    # Arithmetic
    if topic == "Arithmetic":
        st.subheader("➕ Arithmetic")
        a = st.number_input("Enter first number:")
        b = st.number_input("Enter second number:")
        op = st.selectbox("Operation", ["+", "-", "×", "÷"])
        if st.button("Calculate"):
            if op == "+": st.write("Result:", a+b)
            elif op == "-": st.write("Result:", a-b)
            elif op == "×": st.write("Result:", a*b)
            elif op == "÷": st.write("Result:", a/b if b != 0 else "Error: Division by zero")

    # Fractions
    elif topic == "Fractions & Decimals":
        st.subheader("➗ Fractions & Decimals")
        num = st.number_input("Numerator:", step=1)
        den = st.number_input("Denominator:", step=1)
        if st.button("Convert"):
            if den != 0:
                st.write("Decimal:", num/den)
                st.write("Simplified Fraction:", sp.Rational(num, den))
            else:
                st.error("Denominator cannot be zero!")

    # Algebra
    elif topic == "Algebra":
        st.subheader("🔢 Algebra")
        expr = st.text_input("Enter expression (e.g. 2*x + 3*x - 4):")
        if st.button("Simplify"):
            try:
                x = sp.symbols("x")
                st.write("Simplified:", sp.simplify(expr))
            except Exception as e:
                st.error(e)

    # Simultaneous Equations
    elif topic == "Simultaneous Equations":
        st.subheader("🧮 Simultaneous Equations")
        st.markdown("Solve system: a1x + b1y = c1 ; a2x + b2y = c2")
        a1 = st.number_input("a1:", step=1)
        b1 = st.number_input("b1:", step=1)
        c1 = st.number_input("c1:", step=1)
        a2 = st.number_input("a2:", step=1)
        b2 = st.number_input("b2:", step=1)
        c2 = st.number_input("c2:", step=1)
        if st.button("Solve"):
            x, y = sp.symbols("x y")
            sol = sp.solve([a1*x+b1*y-c1, a2*x+b2*y-c2], (x, y))
            st.write("Solution:", sol)

    # Geometry
    elif topic == "Geometry":
        st.subheader("📐 Geometry")
        shape = st.selectbox("Choose shape", ["Circle", "Rectangle", "Triangle"])
        if shape == "Circle":
            r = st.number_input("Radius:", step=1.0)
            if st.button("Solve"):
                st.write("Area:", math.pi*r**2)
                st.write("Perimeter:", 2*math.pi*r)
        elif shape == "Rectangle":
            l = st.number_input("Length:")
            w = st.number_input("Width:")
            if st.button("Solve"):
                st.write("Area:", l*w)
                st.write("Perimeter:", 2*(l+w))
        elif shape == "Triangle":
            b = st.number_input("Base:")
            h = st.number_input("Height:")
            if st.button("Solve"):
                st.write("Area:", 0.5*b*h)

    # Trigonometry
    elif topic == "Trigonometry":
        st.subheader("📐 Trigonometry")
        func = st.selectbox("Function", ["sin", "cos", "tan"])
        angle = st.number_input("Enter angle:", step=1.0)
        mode = st.radio("Mode", ["Degrees", "Radians"])
        if st.button("Compute"):
            ang = math.radians(angle) if mode == "Degrees" else angle
            if func == "sin": st.write("Result:", math.sin(ang))
            elif func == "cos": st.write("Result:", math.cos(ang))
            elif func == "tan": 
                st.write("Result:", math.tan(ang) if math.cos(ang)!=0 else "Undefined")

    # Statistics
    elif topic == "Statistics":
        st.subheader("📊 Statistics")
        nums = st.text_area("Enter numbers separated by commas (e.g. 2,4,6,8):")
        if st.button("Analyze"):
            try:
                data = [float(n) for n in nums.split(",")]
                st.write("Mean:", stats.mean(data))
                st.write("Median:", stats.median(data))
                st.write("Mode:", stats.mode(data))
                st.write("Variance:", stats.variance(data))
            except Exception as e:
                st.error("Invalid input or not enough data")


# =========================
# SSS SECTION
# =========================
elif level == "Senior Secondary":
    topic = st.sidebar.selectbox("Choose an SSS Topic:", [
        "Algebra",
        "Quadratic Equations",
        "Simultaneous Equations",
        "Geometry",
        "Trigonometry",
        "Calculus",
        "Statistics & Probability"
    ])

    # Algebra
    if topic == "Algebra":
        st.subheader("🔢 Advanced Algebra")
        expr = st.text_input("Enter expression (e.g. (x+1)*(x+2)):")
        if st.button("Expand & Factorize"):
            x = sp.symbols("x")
            try:
                st.write("Expanded:", sp.expand(expr))
                st.write("Factorized:", sp.factor(expr))
            except Exception as e:
                st.error(e)

    # Quadratic
    elif topic == "Quadratic Equations":
        st.subheader("🧩 Quadratic Equations")
        a = st.number_input("a:", step=1.0)
        b = st.number_input("b:", step=1.0)
        c = st.number_input("c:", step=1.0)
        if st.button("Solve"):
            x = sp.symbols("x")
            sol = sp.solve(a*x**2 + b*x + c, x)
            st.write("Solutions:", sol)

    # Simultaneous
    elif topic == "Simultaneous Equations":
        st.subheader("🧮 2 Vars Simultaneous Equations")
        st.markdown("a1x + b1y = c1 ; a2x + b2y = c2")
        a1 = st.number_input("a1:", step=1)
        b1 = st.number_input("b1:", step=1)
        c1 = st.number_input("c1:", step=1)
        a2 = st.number_input("a2:", step=1)
        b2 = st.number_input("b2:", step=1)
        c2 = st.number_input("c2:", step=1)
        if st.button("Solve"):
            x, y = sp.symbols("x y")
            sol = sp.solve([a1*x+b1*y-c1, a2*x+b2*y-c2], (x, y))
            st.write("Solution:", sol)

    # Geometry
    elif topic == "Geometry":
        st.subheader("📐 2D & 3D Geometry")
        shape = st.selectbox("Choose shape", ["Circle", "Rectangle", "Triangle", "Sphere", "Cylinder"])
        if shape == "Sphere":
            r = st.number_input("Radius:")
            if st.button("Solve"):
                st.write("Surface Area:", 4*math.pi*r**2)
                st.write("Volume:", (4/3)*math.pi*r**3)
        elif shape == "Cylinder":
            r = st.number_input("Radius:")
            h = st.number_input("Height:")
            if st.button("Solve"):
                st.write("Surface Area:", 2*math.pi*r*(h+r))
                st.write("Volume:", math.pi*r**2*h)
        # reuse JSS shapes
        elif shape == "Circle":
            r = st.number_input("Radius:")
            if st.button("Solve"):
                st.write("Area:", math.pi*r**2)
                st.write("Perimeter:", 2*math.pi*r)
        elif shape == "Rectangle":
            l = st.number_input("Length:")
            w = st.number_input("Width:")
            if st.button("Solve"):
                st.write("Area:", l*w)
                st.write("Perimeter:", 2*(l+w))
        elif shape == "Triangle":
            b = st.number_input("Base:")
            h = st.number_input("Height:")
            if st.button("Solve"):
                st.write("Area:", 0.5*b*h)

    # Trigonometry
    elif topic == "Trigonometry":
        st.subheader("📐 Trigonometry")
        func = st.selectbox("Function", ["sin", "cos", "tan"])
        angle = st.number_input("Enter angle:", step=1.0)
        mode = st.radio("Mode", ["Degrees", "Radians"])
        if st.button("Compute"):
            ang = math.radians(angle) if mode == "Degrees" else angle
            if func == "sin": st.write("Result:", math.sin(ang))
            elif func == "cos": st.write("Result:", math.cos(ang))
            elif func == "tan": 
                st.write("Result:", math.tan(ang) if math.cos(ang)!=0 else "Undefined")

    # Calculus
    elif topic == "Calculus":
        st.subheader("📈 Calculus")
        expr = st.text_input("Enter expression in x (e.g. x**2 + 3*x):")
        x = sp.symbols("x")
        if st.button("Differentiate"):
            try:
                st.write("dy/dx:", sp.diff(expr, x))
            except Exception as e:
                st.error(e)
        if st.button("Integrate"):
            try:
                st.write("∫ f(x) dx:", sp.integrate(expr, x))
            except Exception as e:
                st.error(e)

    # Statistics
    elif topic == "Statistics & Probability":
        st.subheader("📊 Statistics & Probability")
        nums = st.text_area("Enter data (comma-separated):")
        if st.button("Analyze"):
            try:
                data = [float(n) for n in nums.split(",")]
                st.write("Mean:", stats.mean(data))
                st.write("Median:", stats.median(data))
                st.write("Mode:", stats.mode(data))
                st.write("Variance:", stats.variance(data))
            except Exception as e:
                st.error("Invalid input")
        prob_event = st.number_input("Favourable outcomes:", step=1)
        prob_total = st.number_input("Total outcomes:", step=1)
        if st.button("Find Probability"):
            if prob_total>0:
                st.write("Probability:", prob_event/prob_total)

# =========================
# CALCULATOR MODE
# =========================
elif level == "Calculator":
    st.subheader("🧮 General Calculator")
    expr = st.text_input("Enter any math expression (e.g. 5*(2+3), sin(pi/2)):")
    if st.button("Evaluate"):
        try:
            x = sp.symbols("x")
            result = sp.sympify(expr)
            st.write("Result:", result.evalf())
        except Exception as e:
            st.error(e)
