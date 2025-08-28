import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import statistics as stats
import re
import math

# ================== PAGE & THEME ==================
st.set_page_config(page_title="MathCore – All-in-One Maths App", layout="wide", page_icon="🧮")

st.markdown(
    """
    <style>
      .stApp { background-color:#0A1A2F; color:#E6EAF0; }
      section[data-testid="stSidebar"] { background-color:#0B0B0B !important; }
      section[data-testid="stSidebar"] * { color:#F5F5F5 !important; }
      .stButton>button { background:#1C2D4A !important; color:#FFFFFF !important; border:1px solid #3E5C96; border-radius:12px; }
      .stTextInput>div>div>input, textarea { background:#102544 !important; color:#E6EAF0 !important; border-radius:10px; }
      .stNumberInput input { background:#102544 !important; color:#E6EAF0 !important; }
      .stSelectbox>div>div { background:#102544 !important; color:#E6EAF0 !important; border-radius:10px; }
      .metric-card { background:#0F233F; padding:12px 16px; border-radius:12px; border:1px solid #264B7F; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧮 MathCore – All‑in‑One Maths App (JSS & SSS)")
st.caption("No API keys. SymPy + NumPy + Pandas under the hood. Mature dark‑blue theme + black sidebar.")

# ================== HELPERS ==================
# Allowed names for sympy parsing (so users can type sin(30) without 'sp.')
ALLOWED = {
    'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
    'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
    'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
    'sqrt': sp.sqrt, 'log': sp.log, 'ln': sp.log, 'exp': sp.exp,
    'pi': sp.pi, 'E': sp.E, 'Abs': sp.Abs, 'abs': sp.Abs, 'floor': sp.floor, 'ceiling': sp.ceiling
}

# Regex helpers for implicit multiplication (5(2+3) -> 5*(2+3), 2x -> 2*x, )(2 -> )*2 )
_num = re.compile(r"(\d)\s*(?=\(")")
_alpha = re.compile(r"(\d)([a-zA-Z])")
_paren_num = re.compile(r"\)\s*(\d)")

def implicit_mul(expr: str) -> str:
    if not expr:
        return expr
    # insert * between number and opening paren: 5( -> 5*(
    expr = _num.sub(r"\1*", expr)
    # insert * between number and variable/letter: 2x -> 2*x
    expr = _alpha.sub(r"\1*\2", expr)
    # insert * between closing paren and number: )2 -> )*2
    expr = _paren_num.sub(r")*\1", expr)
    return expr

# Convert numeric trig arguments to radians for Degrees mode

def convert_trig_degrees(sym_expr: sp.Expr) -> sp.Expr:
    # matches sin/cos/tan with a single numeric argument that does not contain pi
    def cond(node):
        try:
            return (hasattr(node, 'func')
                    and node.func in (sp.sin, sp.cos, sp.tan)
                    and len(node.args) == 1
                    and getattr(node.args[0], 'is_number', False)
                    and not node.args[0].has(sp.pi))
        except Exception:
            return False

    def repl(node):
        return node.func(node.args[0] * sp.pi / 180)

    return sym_expr.replace(cond, repl)

# Parse an input string into a SymPy equation or expression using ALLOWED locals

def parse_equation(text: str):
    text = implicit_mul(text)
    if '=' in text:
        L, R = text.split('=', 1)
        return sp.Eq(sp.sympify(L, locals=ALLOWED), sp.sympify(R, locals=ALLOWED))
    return sp.sympify(text, locals=ALLOWED)

# ================== SIDEBAR ==================
st.sidebar.title("📘 MathCore")
level = st.sidebar.selectbox("Select Level", ["Junior Secondary", "Senior Secondary", "Calculator"], index=0)

if level == "Junior Secondary":
    topic = st.sidebar.radio("Choose a topic:", [
        "Arithmetic", "Fractions & Decimals", "GCD & LCM", "Simple Interest & Percentage",
        "Ratio & Proportion", "Pythagoras", "Algebra", "Simultaneous Equations (2×2)",
        "Geometry", "Statistics", "Trigonometry"
    ], index=0)

elif level == "Senior Secondary":
    topic = st.sidebar.radio("Choose a topic:", [
        "Algebra (Factor/Solve)", "Quadratic Equations", "Trigonometry",
        "Calculus", "Probability", "Matrices", "Logarithms & Indices", "Graphs"
    ], index=0)

else:
    topic = "Calculator"

# ================== TOPICS ==================
# ---- JSS topics ----
if topic == "Arithmetic":
    st.subheader("Arithmetic")
    expr = st.text_input("Enter expression (supports implicit multiplication like 5(2+3))")
    if st.button("Compute", key="arith"):
        try:
            val = sp.sympify(implicit_mul(expr), locals=ALLOWED).evalf()
            st.success(f"Result: {val}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Fractions & Decimals":
    st.subheader("Fractions & Decimals")
    col1, col2 = st.columns(2)
    with col1:
        dec = st.text_input("Decimal → Fraction (e.g. 0.75)")
        if st.button("To Fraction"):
            try:
                r = sp.Rational(dec).limit_denominator()
                st.success(f"{dec} = {r} (≈ {float(r)})")
            except Exception as e:
                st.error(e)
    with col2:
        frac = st.text_input("Fraction → Decimal (e.g. 5/8)")
        if st.button("To Decimal"):
            try:
                r = sp.nsimplify(frac)
                st.success(f"{frac} ≈ {float(r)}")
            except Exception as e:
                st.error(e)

elif topic == "GCD & LCM":
    st.subheader("GCD (HCF) & LCM")
    nums = st.text_input("Enter integers separated by commas", "12, 18, 30")
    if st.button("Compute GCD/LCM"):
        try:
            arr = [int(s) for s in nums.replace(';', ',').split(',') if s.strip()]
            g = int(sp.igcd(*arr))
            l = int(sp.ilcm(*arr))
            st.success(f"GCD/HCF = {g}, LCM = {l}")
        except Exception as e:
            st.error(e)

elif topic == "Simple Interest & Percentage":
    st.subheader("Simple Interest & Percentage")
    P = st.number_input("Principal (₦)", value=10000.0, step=100.0)
    R = st.number_input("Rate (% per annum)", value=10.0)
    T = st.number_input("Time (years)", value=2.0)
    if st.button("Compute Simple Interest"):
        SI = (P*R*T)/100
        A = P + SI
        st.success(f"Simple Interest = ₦{SI}, Amount = ₦{A}")
    st.divider()
    base = st.number_input("Base value", value=200.0)
    p = st.number_input("Percentage %", value=15.0)
    if st.button("% of base"):
        st.success(f"{p}% of {base} = {(p/100)*base}")

elif topic == "Ratio & Proportion":
    st.subheader("Ratio & Proportion")
    a = st.number_input("a", value=2.0)
    b = st.number_input("b", value=3.0)
    total = st.number_input("Total to share", value=100.0)
    if st.button("Share by a:b"):
        s = a+b
        st.success(f"Portion A = {total*(a/s)}, Portion B = {total*(b/s)}")

elif topic == "Pythagoras":
    st.subheader("Pythagoras (Right Triangle)")
    tab1, tab2 = st.tabs(["Find hypotenuse", "Find a leg"])
    with tab1:
        A = st.number_input("Leg a", value=3.0)
        B = st.number_input("Leg b", value=4.0)
        if st.button("Hypotenuse"):
            st.success(f"c = sqrt(a^2 + b^2) = {float(np.hypot(A,B))}")
    with tab2:
        C = st.number_input("Hypotenuse c", value=13.0)
        known = st.number_input("Known leg", value=5.0)
        if st.button("Other leg"):
            val = max(C**2 - known**2, 0)
            st.success(f"Other leg = {float(np.sqrt(val))}")

elif topic == "Algebra":
    st.subheader("Algebra (JSS)")
    eq = st.text_input("Enter equation or expression in x (e.g. 2*x + 3 = 11 or x^2-5*x+6)")
    if st.button("Solve/Factor"):
        try:
            obj = parse_equation(eq)
            x = sp.Symbol('x')
            if isinstance(obj, sp.Equality):
                sol = sp.solve(obj, x)
                st.success(f"Solutions: {sol}")
            else:
                st.write(f"Simplified: {sp.simplify(obj)}")
                st.write(f"Factored: {sp.factor(obj)}")
        except Exception as e:
            st.error(e)

elif topic == "Simultaneous Equations (2×2)":
    st.subheader("Simultaneous Equations (2×2)")
    st.caption("Form: a1*x + b1*y = c1 and a2*x + b2*y = c2")
    c1, c2 = st.columns(2)
    with c1:
        a1 = st.number_input("a1", value=1.0)
        b1 = st.number_input("b1", value=2.0)
        c1v = st.number_input("c1", value=5.0)
    with c2:
        a2 = st.number_input("a2", value=3.0)
        b2 = st.number_input("b2", value=-1.0)
        c2v = st.number_input("c2", value=4.0)
    if st.button("Solve 2×2"):
        try:
            x, y = sp.symbols('x y')
            sol = sp.solve([sp.Eq(a1*x + b1*y, c1v), sp.Eq(a2*x + b2*y, c2v)], (x, y), dict=True)
            if sol:
                st.success(f"x = {sp.N(sol[0][x])}, y = {sp.N(sol[0][y])}")
            else:
                st.warning("No unique solution (parallel or coincident lines).")
        except Exception as e:
            st.error(e)

# ---- Geometry & JSS shapes ----
elif topic == "Geometry":
    st.subheader("Geometry")
    shape = st.selectbox("Shape", ["Rectangle", "Triangle", "Parallelogram", "Trapezium", "Circle", "Cuboid", "Cylinder", "Sphere", "Cone"])
    if shape == "Rectangle":
        L = st.number_input("Length", value=8.0)
        W = st.number_input("Width", value=5.0)
        if st.button("Compute Rectangle"):
            st.success(f"Perimeter = {2*(L+W)}, Area = {L*W}")
    elif shape == "Triangle":
        B = st.number_input("Base", value=10.0)
        H = st.number_input("Height", value=6.0)
        if st.button("Compute Triangle"):
            st.success(f"Area = 1/2 * b * h = {0.5*B*H}")
    elif shape == "Parallelogram":
        B = st.number_input("Base", value=10.0, key="pb")
        H = st.number_input("Height", value=6.0, key="ph")
        if st.button("Compute Parallelogram"):
            st.success(f"Area = b*h = {B*H}")
    elif shape == "Trapezium":
        A = st.number_input("a (top)", value=8.0)
        Bt = st.number_input("b (bottom)", value=12.0)
        H = st.number_input("height", value=5.0)
        if st.button("Compute Trapezium"):
            st.success(f"Area = 1/2*(a+b)*h = {0.5*(A+Bt)*H}")
    elif shape == "Circle":
        r = st.number_input("Radius r", value=7.0)
        if st.button("Compute Circle"):
            st.success(f"Diameter = {2*r}; Circumference ≈ {2*sp.pi*r:.5f}; Area ≈ {sp.pi*r*r:.5f}")
    elif shape == "Cuboid":
        l = st.number_input("Length", value=4.0)
        w = st.number_input("Width", value=3.0)
        h = st.number_input("Height", value=2.0)
        if st.button("Compute Cuboid"):
            st.success(f"Volume = {l*w*h}; Surface Area = {2*(l*w + l*h + w*h)}")
    elif shape == "Cylinder":
        r = st.number_input("Radius", value=3.0, key="cr")
        h = st.number_input("Height", value=5.0, key="ch")
        if st.button("Compute Cylinder"):
            st.success(f"Volume ≈ {sp.pi*r*r*h:.5f}; Curved Surface Area ≈ {2*sp.pi*r*h:.5f}")
    elif shape == "Sphere":
        r = st.number_input("Radius", value=3.0, key="sr")
        if st.button("Compute Sphere"):
            st.success(f"Volume ≈ {(4*sp.pi*r**3)/3:.5f}; Surface Area ≈ {4*sp.pi*r**2:.5f}")
    elif shape == "Cone":
        r = st.number_input("Radius", value=3.0, key="cor")
        h = st.number_input("Height", value=5.0, key="coh")
        if st.button("Compute Cone"):
            st.success(f"Volume ≈ {(sp.pi*r*r*h)/3:.5f}")

# ---- Statistics ----
elif topic == "Statistics":
    st.subheader("Statistics")
    raw = st.text_input("Enter numbers (comma‑separated)", "2, 3, 5, 7, 11, 13, 13")
    if st.button("Compute Stats"):
        try:
            data = [float(s) for s in raw.replace('\n', ',').replace(';', ',').split(',') if s.strip()]
            arr = np.array(data)
            mean = float(np.mean(arr)); median = float(np.median(arr))
            srs = pd.Series(arr).value_counts()
            modes = srs[srs == srs.max()].index.tolist()
            st.write({"Mean": mean, "Median": median, "Mode(s)": modes})
        except Exception as e:
            st.error(e)

# ---- Trigonometry ----
elif topic == "Trigonometry":
    st.subheader("Trigonometry Evaluator")
    expr = st.text_input("Enter trig expression (e.g. sin(30), cos(pi/3), tan(45))")
    angle_mode = st.radio("Angle Mode", ["Degrees", "Radians"], horizontal=True)
    if st.button("Evaluate trig"):
        try:
            parsed = sp.sympify(implicit_mul(expr), locals=ALLOWED)
            if angle_mode == "Degrees":
                parsed = convert_trig_degrees(parsed)
            st.success(f"Result: {sp.N(parsed)}")
        except Exception as e:
            st.error(e)

# ----------------- SSS -----------------
elif topic == "Algebra (Factor/Solve)":
    st.subheader("Algebra (SSS)")
    expr = st.text_input("Expression or equation in x (e.g. 2*x**2 - 5*x - 3 or 2*x+3=11)")
    if st.button("Go", key="alg_sss"):
        try:
            obj = parse_equation(expr)
            x = sp.Symbol('x')
            if isinstance(obj, sp.Equality):
                st.success(f"Solutions: {sp.solve(obj, x)}")
            else:
                st.write(f"Simplified: {sp.simplify(obj)}")
                st.write(f"Factored: {sp.factor(obj)}")
        except Exception as e:
            st.error(e)

elif topic == "Quadratic Equations":
    st.subheader("Quadratic Solver: ax² + bx + c = 0")
    a = st.number_input("a (≠0)", value=1.0)
    b = st.number_input("b", value=-3.0)
    c = st.number_input("c", value=2.0)
    if st.button("Solve Quadratic"):
        try:
            x = sp.Symbol('x')
            D = b**2 - 4*a*c
            r1 = (-b + sp.sqrt(D)) / (2*a)
            r2 = (-b - sp.sqrt(D)) / (2*a)
            st.write({"Discriminant": D, "Roots": [sp.N(r1), sp.N(r2)]})
        except Exception as e:
            st.error(e)

elif topic == "Calculus":
    st.subheader("Calculus")
    expr = st.text_input("f(x) =", "3*x**4 - 5*x**2 + 7*x - 9")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Differentiate"):
            try:
                x = sp.Symbol('x')
                f = sp.sympify(expr, locals=ALLOWED)
                st.success(f"f'(x) = {sp.diff(f, x)}")
            except Exception as e:
                st.error(e)
    with col2:
        if st.button("Integrate"):
            try:
                x = sp.Symbol('x')
                f = sp.sympify(expr, locals=ALLOWED)
                st.success(f"∫ f(x) dx = {sp.integrate(f, x)} + C")
            except Exception as e:
                st.error(e)
    with col3:
        a_val = st.number_input("Limit as x → a", value=1.0)
        if st.button("Limit"):
            try:
                x = sp.Symbol('x')
                f = sp.sympify(expr, locals=ALLOWED)
                st.success(f"limₓ→{a_val} f(x) = {sp.limit(f, x, a_val)}")
            except Exception as e:
                st.error(e)

elif topic == "Probability":
    st.subheader("Probability (Simple)")
    favorable = st.number_input("Favorable outcomes", value=1)
    total = st.number_input("Total outcomes", value=6)
    if st.button("Compute Probability"):
        try:
            st.success(f"P = {favorable}/{total} = {favorable/total}")
        except Exception as e:
            st.error(e)

elif topic == "Matrices":
    st.subheader("Matrices")
    A_str = st.text_area("Matrix A (rows by ';', elements by space)", "1 2; 3 4")
    B_str = st.text_area("Matrix B (optional, same format)", "5 6; 7 8")
    op = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Determinant A", "Inverse A"]) 
    if st.button("Compute Matrix"):
        try:
            A = sp.Matrix([[float(n) for n in row.split()] for row in A_str.split(';')])
            B = sp.Matrix([[float(n) for n in row.split()] for row in B_str.split(';')]) if B_str.strip() else None
            if op == "Add": st.success(f"A + B =\n{A + B}")
            elif op == "Subtract": st.success(f"A - B =\n{A - B}")
            elif op == "Multiply": st.success(f"A * B =\n{A * B}")
            elif op == "Determinant A": st.success(f"det(A) = {A.det()}")
            elif op == "Inverse A": st.success(f"A⁻¹ =\n{A.inv()}")
        except Exception as e:
            st.error(e)

elif topic == "Logarithms & Indices":
    st.subheader("Logarithms & Indices")
    ex = st.text_input("Enter expression (e.g., log(100,10), 2**5, sqrt(49))", "log(100,10)")
    if st.button("Evaluate log/index"):
        try:
            st.success(f"Result: {sp.sympify(implicit_mul(ex), locals=ALLOWED).evalf()}")
        except Exception as e:
            st.error(e)

elif topic == "Graphs":
    st.subheader("Graph of y = f(x)")
    fx = st.text_input("f(x) =", "x**2 - 3*x + 2")
    xmin, xmax = st.number_input("x min", value=-5.0), st.number_input("x max", value=5.0)
    npts = st.slider("Number of points", 20, 500, 101)
    if st.button("Plot f(x)"):
        try:
            x = sp.Symbol('x')
            f = sp.lambdify(x, sp.sympify(fx, locals=ALLOWED), 'numpy')
            X = np.linspace(xmin, xmax, npts)
            Y = f(X)
            df = pd.DataFrame({"x": X, "f(x)": Y})
            st.line_chart(df.set_index("x"))
            st.caption("Tip: Zoom by dragging over the chart.")
        except Exception as e:
            st.error(e)

# ----------------- CALCULATOR -----------------
elif topic == "Calculator":
    st.subheader("🧮 General Calculator")
    expr = st.text_input("Enter any expression (e.g. 2+3*5, sin(30), sqrt(25), log(100,10))")
    angle_mode = st.radio("Angle Mode (for trig)", ["Degrees", "Radians"], horizontal=True)
    if st.button("Calculate", key="calc"):
        try:
            parsed = sp.sympify(implicit_mul(expr), locals=ALLOWED)
            if angle_mode == "Degrees":
                parsed = convert_trig_degrees(parsed)
            st.success(f"Result: {sp.N(parsed)}")
        except Exception as e:
            st.error(e)
