import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats

# ---------------------------- THEME ---------------------------- #
st.markdown(
    """
    <style>
    .stApp { background-color: #0d1b2a; color: #f0f0f0; }
    .css-1d391kg, .css-qbe2hs { background-color: #000000 !important; color: white !important; }
    .css-1d391kg a { color: #f0f0f0 !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("📘 Math Companion")

level = st.sidebar.radio("Select Level", ["Junior Secondary", "Senior Secondary", "Calculator"])

# ---------------------------- FUNCTIONS ---------------------------- #

def arithmetic_calc():
    st.subheader("🧮 Arithmetic Calculator")
    a = st.number_input("Enter first number")
    b = st.number_input("Enter second number")
    op = st.selectbox("Choose operation", ["+", "-", "×", "÷"])
    if st.button("Calculate"):
        if op == "+":
            st.success(f"{a} + {b} = {a+b}")
        elif op == "-":
            st.success(f"{a} - {b} = {a-b}")
        elif op == "×":
            st.success(f"{a} × {b} = {a*b}")
        elif op == "÷":
            if b != 0:
                st.success(f"{a} ÷ {b} = {a/b}")
            else:
                st.error("Division by zero not allowed!")

def fraction_decimal():
    st.subheader("➗ Fractions & Decimals")
    num = st.number_input("Numerator", step=1)
    den = st.number_input("Denominator", step=1)
    if st.button("Simplify Fraction"):
        if den != 0:
            simp = sp.Rational(num, den)
            st.success(f"Simplified: {simp}")
            st.info(f"As Decimal: {float(simp)}")
        else:
            st.error("Denominator cannot be zero!")

def simultaneous_eqns():
    st.subheader("🔗 Simultaneous Equations")
    st.markdown("Solve equations of the form ax + by = c")
    a1 = st.number_input("a1")
    b1 = st.number_input("b1")
    c1 = st.number_input("c1")
    a2 = st.number_input("a2")
    b2 = st.number_input("b2")
    c2 = st.number_input("c2")
    if st.button("Solve Equations"):
        x, y = sp.symbols('x y')
        sol = sp.solve([a1*x + b1*y - c1, a2*x + b2*y - c2], (x, y))
        st.success(f"Solution: {sol}")

def geometry_calc():
    st.subheader("📐 Geometry")
    shape = st.selectbox("Select Shape", ["Circle", "Rectangle", "Triangle"])
    if shape == "Circle":
        r = st.number_input("Radius")
        if st.button("Calculate Area & Circumference"):
            st.success(f"Area = {np.pi*r*r:.2f}, Circumference = {2*np.pi*r:.2f}")
    elif shape == "Rectangle":
        l = st.number_input("Length")
        w = st.number_input("Width")
        if st.button("Calculate Area & Perimeter"):
            st.success(f"Area = {l*w}, Perimeter = {2*(l+w)}")
    elif shape == "Triangle":
        b = st.number_input("Base")
        h = st.number_input("Height")
        if st.button("Calculate Area"):
            st.success(f"Area = {0.5*b*h}")

def trig_calc():
    st.subheader("📏 Trigonometry")
    func = st.selectbox("Function", ["sin", "cos", "tan"])
    angle = st.number_input("Enter angle")
    mode = st.radio("Mode", ["Degrees", "Radians"])
    if st.button("Calculate Trig"):
        ang = np.radians(angle) if mode == "Degrees" else angle
        if func == "sin":
            st.success(f"sin({angle}) = {np.sin(ang):.4f}")
        elif func == "cos":
            st.success(f"cos({angle}) = {np.cos(ang):.4f}")
        elif func == "tan":
            st.success(f"tan({angle}) = {np.tan(ang):.4f}")

def stats_calc():
    st.subheader("📊 Statistics")
    data = st.text_area("Enter numbers separated by commas")
    if st.button("Compute Statistics"):
        try:
            nums = [float(i) for i in data.split(",")]
            st.info(f"Mean = {stats.mean(nums)}")
            st.info(f"Median = {stats.median(nums)}")
            st.info(f"Mode = {stats.mode(nums)}")
            st.info(f"Variance = {stats.variance(nums)}")
        except:
            st.error("Please enter valid numbers!")

# ---------------------------- APP BODY ---------------------------- #

if level == "Junior Secondary":
    topic = st.sidebar.selectbox("Choose Topic", [
        "Arithmetic", "Fractions & Decimals", "Simultaneous Equations", "Geometry", "Trigonometry", "Statistics"
    ])
    if topic == "Arithmetic": arithmetic_calc()
    elif topic == "Fractions & Decimals": fraction_decimal()
    elif topic == "Simultaneous Equations": simultaneous_eqns()
    elif topic == "Geometry": geometry_calc()
    elif topic == "Trigonometry": trig_calc()
    elif topic == "Statistics": stats_calc()

elif level == "Senior Secondary":
    topic = st.sidebar.selectbox("Choose Topic", [
        "Algebra", "Trigonometry", "Geometry", "Statistics"
    ])
    if topic == "Algebra":
        st.subheader("📚 Algebra")
        expr = st.text_input("Enter algebraic expression (e.g., x^2+3x+2)")
        if st.button("Simplify"):
            try:
                x = sp.symbols('x')
                simp = sp.simplify(expr)
                st.success(f"Simplified: {simp}")
            except:
                st.error("Invalid algebraic expression!")
    elif topic == "Trigonometry": trig_calc()
    elif topic == "Geometry": geometry_calc()
    elif topic == "Statistics": stats_calc()

elif level == "Calculator":
    st.subheader("🖩 General Calculator")
    expr = st.text_input("Enter any math expression (e.g., 5*(2+3))")
    if st.button("Evaluate"):
        try:
            x, y = sp.symbols('x y')
            res = sp.sympify(expr)
            st.success(f"Result: {res}")
        except Exception as e:
            st.error(f"Error: {e}")
