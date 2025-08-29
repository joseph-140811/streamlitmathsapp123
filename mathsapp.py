import streamlit as st
import sympy as sp
import math

# ----------------- Utility Functions ----------------- #
def parse_equation(eq_str):
    try:
        eq_str = eq_str.replace("^", "**")
        if "=" in eq_str:
            left, right = eq_str.split("=")
            return sp.Eq(sp.sympify(left), sp.sympify(right))
        return sp.sympify(eq_str)
    except Exception as e:
        return str(e)

def solve_expression(expr):
    try:
        return sp.simplify(expr)
    except Exception:
        return "Invalid Expression"

def solve_equation(equation):
    try:
        x = sp.symbols("x")
        eq = parse_equation(equation)
        return sp.solve(eq, x)
    except Exception:
        return "Invalid Equation"

def solve_simultaneous(eq1, eq2):
    try:
        x, y = sp.symbols("x y")
        eq1 = parse_equation(eq1)
        eq2 = parse_equation(eq2)
        return sp.solve([eq1, eq2], (x, y))
    except Exception:
        return "Invalid Simultaneous Equations"

def trig_function(func, angle):
    try:
        angle_rad = math.radians(angle)  # Convert degrees → radians
        if func == "sin":
            return math.sin(angle_rad)
        elif func == "cos":
            return math.cos(angle_rad)
        elif func == "tan":
            return math.tan(angle_rad)
    except Exception:
        return "Invalid Trigonometric Function"

# ----------------- Page Config ----------------- #
st.set_page_config(page_title="Math Mastery Hub", page_icon="📘", layout="centered")

# ----------------- Custom Styling ----------------- #
st.markdown("""
    <style>
    body {
        background-color: #0A1D37; /* Mature dark blue */
        color: white;
    }
    .sidebar .sidebar-content {
        background-color: #123456; /* Another shade of mature blue */
    }
    textarea, input {
        background-color: black !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------- Sidebar ----------------- #
st.sidebar.title("📘 Math Mastery Hub")
level = st.sidebar.selectbox("Select Level", ["Junior Secondary", "Senior Secondary"])
topic = st.sidebar.selectbox("Select Topic", [
    "Arithmetic",
    "Algebra",
    "Simultaneous Equations",
    "Geometry",
    "Trigonometry",
    "Calculus",
    "Statistics",
    "Probability",
    "Sequences & Series",
    "Quadratic Equations",
    "Matrices",
    "Vectors",
    "Logarithms",
    "Mensuration",
    "Calculator"
])

# ----------------- App Title ----------------- #
st.title("📘 Math Mastery Hub")
st.write("Your all-in-one mathematics learning companion.")

# ----------------- Topic Logic ----------------- #
if topic == "Arithmetic":
    expr = st.text_input("Enter arithmetic expression:", "")
    if st.button("Calculate"):
        st.write("Result:", solve_expression(expr))

elif topic == "Algebra":
    equation = st.text_input("Enter algebraic equation (e.g., 2x + 3 = 7):", "")
    if st.button("Solve"):
        st.write("Solution:", solve_equation(equation))

elif topic == "Simultaneous Equations":
    eq1 = st.text_input("Enter first equation (e.g., 2x + y = 5):", "")
    eq2 = st.text_input("Enter second equation (e.g., x - y = 1):", "")
    if st.button("Solve"):
        st.write("Solution:", solve_simultaneous(eq1, eq2))

elif topic == "Geometry":
    shape = st.selectbox("Choose shape", ["Circle", "Rectangle", "Triangle"])
    if shape == "Circle":
        r = st.number_input("Enter radius:", value=0.0)
        if st.button("Calculate"):
            st.write("Area:", math.pi * r**2)
            st.write("Perimeter:", 2 * math.pi * r)
    elif shape == "Rectangle":
        l = st.number_input("Enter length:", value=0.0)
        b = st.number_input("Enter breadth:", value=0.0)
        if st.button("Calculate"):
            st.write("Area:", l * b)
            st.write("Perimeter:", 2 * (l + b))
    elif shape == "Triangle":
        b = st.number_input("Enter base:", value=0.0)
        h = st.number_input("Enter height:", value=0.0)
        if st.button("Calculate"):
            st.write("Area:", 0.5 * b * h)

elif topic == "Trigonometry":
    func = st.selectbox("Choose function", ["sin", "cos", "tan"])
    angle = st.number_input("Enter angle (degrees):", value=0)
    if st.button("Solve"):
        st.write(f"{func}({angle}°) =", round(trig_function(func, angle), 2))

elif topic == "Calculus":
    expr = st.text_input("Enter function (e.g., x^2 + 3x):", "")
    x = sp.symbols("x")
    if st.button("Differentiate"):
        try:
            st.write("Result:", sp.diff(expr, x))
        except Exception:
            st.write("Invalid Expression")
    if st.button("Integrate"):
        try:
            st.write("Result:", sp.integrate(expr, x))
        except Exception:
            st.write("Invalid Expression")

elif topic == "Statistics":
    numbers = st.text_input("Enter numbers separated by commas:", "")
    if st.button("Analyze"):
        try:
            data = [float(n) for n in numbers.split(",")]
            mean = sum(data) / len(data)
            median = sorted(data)[len(data)//2]
            variance = sum((x - mean)**2 for x in data) / len(data)
            st.write("Mean:", mean)
            st.write("Median:", median)
            st.write("Variance:", variance)
        except Exception:
            st.write("Invalid Input")

elif topic == "Probability":
    success = st.number_input("Number of favorable outcomes:", value=0)
    total = st.number_input("Total possible outcomes:", value=1)
    if st.button("Calculate"):
        try:
            st.write("Probability:", success / total)
        except Exception:
            st.write("Invalid Probability Input")

elif topic == "Sequences & Series":
    st.write("Sequences & Series tools coming soon...")

elif topic == "Quadratic Equations":
    equation = st.text_input("Enter quadratic equation (e.g., x^2 + 5x + 6 = 0):", "")
    if st.button("Solve"):
        st.write("Solution:", solve_equation(equation))

elif topic == "Matrices":
    mat_input = st.text_area("Enter matrix rows separated by ';' (e.g., 1,2;3,4):")
    if st.button("Solve"):
        try:
            rows = [list(map(int, row.split(","))) for row in mat_input.split(";")]
            mat = sp.Matrix(rows)
            st.write("Matrix:", mat)
            st.write("Determinant:", mat.det())
            st.write("Inverse:" if mat.det() != 0 else "No Inverse", mat.inv() if mat.det() != 0 else "")
        except Exception:
            st.write("Invalid Matrix Input")

elif topic == "Vectors":
    v1 = st.text_input("Enter first vector (comma-separated):", "")
    v2 = st.text_input("Enter second vector (comma-separated):", "")
    if st.button("Solve"):
        try:
            v1 = sp.Matrix([float(i) for i in v1.split(",")])
            v2 = sp.Matrix([float(i) for i in v2.split(",")])
            st.write("Dot Product:", v1.dot(v2))
            st.write("Cross Product:", v1.cross(v2) if len(v1) == 3 else "Cross Product only valid for 3D vectors")
        except Exception:
            st.write("Invalid Vector Input")

elif topic == "Logarithms":
    expr = st.text_input("Enter log expression (e.g., log(100,10)):", "")
    if st.button("Calculate"):
        try:
            base_expr = expr.replace("log(", "").replace(")", "")
            value, base = base_expr.split(",")
            st.write("Result:", math.log(float(value), float(base)))
        except Exception:
            st.write("Invalid Logarithmic Expression")

elif topic == "Mensuration":
    st.write("Mensuration tools coming soon...")

elif topic == "Calculator":
    expr = st.text_input("Enter any expression to calculate:", "")
    if st.button("Calculate"):
        try:
            st.write("Result:", eval(expr))
        except Exception:
            st.write("Invalid Expression")
