# app.py
import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import math
import re

# ============ PAGE CONFIG ============
st.set_page_config(page_title="📘 ScholarlyMath", page_icon="📘", layout="wide")

# ============ THEME (Mature dark blue + black inputs + white text) ============
st.markdown(
    """
    <style>
      /* Main app background + text color */
      .stApp { background-color:#0A1A2F; color:#FFFFFF; }

      /* Sidebar: different mature blue */
      section[data-testid="stSidebar"] { background-color:#13294B !important; }
      section[data-testid="stSidebar"] * { color:#F2F5FA !important; }

      /* Inputs: black with white text */
      .stTextInput input, .stTextArea textarea, .stNumberInput input,
      .stSelectbox div[data-baseweb="select"] > div, .stMultiSelect div[data-baseweb="select"] > div {
        background:#000000 !important; color:#FFFFFF !important; border-radius:10px;
      }
      /* Buttons */
      .stButton>button { background:#1C2D4A !important; color:#FFFFFF !important; border:1px solid #3E5C96; border-radius:10px; }
      /* Cards (metrics) */
      .metric-card { background:#0F233F; padding:12px 16px; border-radius:12px; border:1px solid #264B7F; }
      /* Headings a little brighter */
      h1,h2,h3,h4 { color:#E8EEF8; }
      /* Tables */
      .stDataFrame, .css-1d391kg, .css-1qvj9ah { color:#FFFFFF !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============ TITLE ============
st.title("📘 ScholarlyMath — All-in-One (JSS & SSS)")

# ============ SYMBOLS ============
x, y, z, n, r = sp.symbols('x y z n r', real=True)

# ============ SAFE PARSING & UTILITIES ============
# Allow natural functions without 'sp.'; keep eval safe.
ALLOWED = {
    'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
    'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
    'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
    'sqrt': sp.sqrt, 'log': sp.log, 'ln': sp.log, 'exp': sp.exp,
    'pi': sp.pi, 'E': sp.E, 'Abs': sp.Abs, 'floor': sp.floor, 'ceiling': sp.ceiling,
    'x': x, 'y': y, 'z': z
}

# Implicit multiplication: 2x -> 2*x, 5(2+3) -> 5*(2+3), (x+1)2 -> (x+1)*2
_re_digit_before_paren = re.compile(r"(\d)\s*(?=\()")
_re_digit_before_var   = re.compile(r"(\d)\s*([A-Za-z])")
_re_paren_before_digit = re.compile(r"\)\s*(\d)")
_re_var_before_var     = re.compile(r"([A-Za-z])\s*([A-Za-z])")  # xy -> x*y
_re_var_before_paren   = re.compile(r"([A-Za-z])\s*(?=\()")      # x( -> x*(

def implicit_mul(expr: str) -> str:
    if not expr:
        return expr
    t = expr.replace("^", "**")
    t = _re_digit_before_paren.sub(r"\1*", t)
    t = _re_digit_before_var.sub(r"\1*\2", t)
    t = _re_paren_before_digit.sub(r")*\1", t)
    t = _re_var_before_var.sub(r"\1*\2", t)
    t = _re_var_before_paren.sub(r"\1*", t)
    return t

# Convert numeric sin(30), cos(45) args to radians when in Degree mode
def convert_trig_degrees(sym_expr: sp.Expr) -> sp.Expr:
    from sympy import Number
    def is_trig_numeric(node):
        return (node.func in (sp.sin, sp.cos, sp.tan, sp.asin, sp.acos, sp.atan)
                and len(node.args) == 1
                and isinstance(node.args[0], (Number, sp.Integer, sp.Rational, sp.Float))
                and not node.args[0].has(sp.pi))
    return sym_expr.replace(is_trig_numeric, lambda e: e.func(e.args[0]*sp.pi/180))

# Parse equation possibly containing '='; return Eq or expression
def parse_equation(text: str):
    s = implicit_mul(text)
    if '=' in s:
        L, R = s.split('=', 1)
        return sp.Eq(sp.sympify(L, locals=ALLOWED), sp.sympify(R, locals=ALLOWED))
    return sp.sympify(s, locals=ALLOWED)

# Helper for integer-looking outputs
def pretty_number(val):
    try:
        v = sp.N(val)
        if v.is_real:
            vf = float(v)
            if abs(vf - round(vf)) < 1e-12:
                return int(round(vf))
            return float(vf)
        return v
    except Exception:
        if isinstance(val, (int, float)):
            if isinstance(val, float) and abs(val - round(val)) < 1e-12:
                return int(round(val))
            return val
        return val

def number_input_int(label, value=0, **kwargs):
    return st.number_input(label, value=value, step=1, format="%d", **kwargs)

def number_input_float(label, value=0.0, **kwargs):
    return st.number_input(label, value=value, step=1.0, format="%.6f", **kwargs)

def parse_float_list(text):
    return [float(s) for s in text.replace("\n", ",").replace(";", ",").split(",") if s.strip()]

# ============ SIDEBAR ============
st.sidebar.header("📚 Navigation")
level = st.sidebar.selectbox("Select Level", ["Junior Secondary (JSS)", "Senior Secondary (SSS)", "Calculator"], index=0)

# Topics
JSS_TOPICS = [
    "Arithmetic", "Fractions & Decimals", "GCD & LCM", "Simple Interest & Percentage",
    "Ratio & Proportion", "Pythagoras", "Algebra", "Simultaneous Equations (2×2)",
    "Geometry (2D & 3D)", "Mensuration", "Statistics", "Probability", "Sets"
]
SSS_TOPICS = [
    "Trigonometry", "Quadratic Equations", "Calculus", "Matrices", "Vectors",
    "Complex Numbers", "Sequences & Series", "Logarithms & Indices", "Graphs"
]

if level == "Junior Secondary (JSS)":
    topic = st.sidebar.radio("Choose a topic:", JSS_TOPICS, index=0)
elif level == "Senior Secondary (SSS)":
    topic = st.sidebar.radio("Choose a topic:", SSS_TOPICS, index=0)
else:
    topic = "Calculator"

# ============ TOPICS IMPLEMENTATION ============

# ----- JSS -----
if topic == "Arithmetic":
    st.subheader("🧮 Arithmetic")
    expr = st.text_input("Enter expression (supports implicit multiplication like 5(2+3), 2x with x value below)")
    xv = number_input_float("If expression has x, provide x =", value=1.0)
    if st.button("Compute", key="arith"):
        try:
            s = implicit_mul(expr)
            expr_sym = sp.sympify(s, locals=ALLOWED)
            res = expr_sym.subs({x: xv}).evalf()
            st.success(f"Result: {pretty_number(res)}")
        except Exception as e:
            st.error(f"Error: {e}")

elif topic == "Fractions & Decimals":
    st.subheader("➗ Fractions & Decimals")
    c1, c2 = st.columns(2)
    with c1:
        dec = st.text_input("Decimal → Fraction (e.g. 0.75)", "")
        if st.button("To Fraction"):
            try:
                r = sp.Rational(dec).limit_denominator()
                st.success(f"{dec} = {r} (≈ {float(r)})")
            except Exception as e:
                st.error(e)
    with c2:
        frac = st.text_input("Fraction → Decimal (e.g. 5/8)", "")
        if st.button("To Decimal"):
            try:
                r = sp.nsimplify(frac)
                st.success(f"{frac} ≈ {float(r)}")
            except Exception as e:
                st.error(e)

elif topic == "GCD & LCM":
    st.subheader("📏 GCD (HCF) & LCM")
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
    st.subheader("💰 Simple Interest & Percentage")
    P = number_input_float("Principal (₦)", value=10000.0)
    R = number_input_float("Rate (% per annum)", value=10.0)
    T = number_input_float("Time (years)", value=2.0)
    if st.button("Compute Simple Interest"):
        SI = (P*R*T)/100
        A = P + SI
        st.success(f"Simple Interest = ₦{pretty_number(SI)}, Amount = ₦{pretty_number(A)}")
    st.divider()
    base = number_input_float("Base value", value=200.0)
    pcent = number_input_float("Percentage %", value=15.0)
    if st.button("% of base"):
        st.success(f"{pcent}% of {base} = {pretty_number((pcent/100)*base)}")

elif topic == "Ratio & Proportion":
    st.subheader("⚖️ Ratio & Proportion")
    a = number_input_float("a", value=2.0)
    b = number_input_float("b", value=3.0)
    total = number_input_float("Total to share", value=100.0)
    if st.button("Share by a:b"):
        s = a + b
        st.success(f"Portion A = {pretty_number(total*(a/s))}, Portion B = {pretty_number(total*(b/s))}")

elif topic == "Pythagoras":
    st.subheader("📐 Pythagoras (Right Triangle)")
    tab1, tab2 = st.tabs(["Find hypotenuse", "Find a leg"])
    with tab1:
        A = number_input_float("Leg a", value=3.0)
        B = number_input_float("Leg b", value=4.0)
        if st.button("Hypotenuse"):
            st.success(f"c = √(a² + b²) = {pretty_number(float(np.hypot(A,B)))}")
    with tab2:
        C = number_input_float("Hypotenuse c", value=13.0)
        known = number_input_float("Known leg", value=5.0)
        if st.button("Other leg"):
            val = max(C**2 - known**2, 0)
            st.success(f"Other leg = {pretty_number(float(np.sqrt(val)))}")

elif topic == "Algebra":
    st.subheader("📘 Algebra (Simplify / Factor / Solve)")
    expr = st.text_input("Expression or equation in x (e.g., 2x+2x, 2*x**2-5*x-3, or 2x+3=11)")
    method = st.radio("Action", ["Simplify", "Factor", "Solve for x"], horizontal=True)
    if st.button("Go", key="alg_go"):
        try:
            obj = parse_equation(expr)
            if isinstance(obj, sp.Equality):
                # Force solving when an equality is typed
                sol = sp.solve(obj, x)
                st.success(f"Solutions: {sol}")
            else:
                if method == "Simplify":
                    st.success(f"Simplified: {sp.simplify(obj)}")
                elif method == "Factor":
                    st.success(f"Factored: {sp.factor(obj)}")
                else:
                    sol = sp.solve(sp.Eq(obj, 0), x)
                    st.success(f"Solutions: {sol}")
        except Exception as e:
            st.error(e)

elif topic == "Simultaneous Equations (2×2)":
    st.subheader("🔗 Simultaneous Equations (2×2)")
    st.caption("Form: a1*x + b1*y = c1  and  a2*x + b2*y = c2")
    c1, c2 = st.columns(2)
    with c1:
        a1 = number_input_float("a₁", value=1.0)
        b1 = number_input_float("b₁", value=2.0)
        c1v = number_input_float("c₁", value=5.0)
    with c2:
        a2 = number_input_float("a₂", value=3.0)
        b2 = number_input_float("b₂", value=-1.0)
        c2v = number_input_float("c₂", value=4.0)
    if st.button("Solve 2×2"):
        try:
            sol = sp.solve([sp.Eq(a1*x + b1*y, c1v), sp.Eq(a2*x + b2*y, c2v)], (x, y), dict=True)
            if sol:
                st.success(f"x = {sp.N(sol[0][x])}, y = {sp.N(sol[0][y])}")
            else:
                st.warning("No unique solution (parallel or coincident lines).")
        except Exception as e:
            st.error(e)

elif topic == "Geometry (2D & 3D)":
    st.subheader("📏 Geometry")
    cat = st.selectbox("Category", ["2D (Plane Shapes)", "3D (Solids)"])
    if cat == "2D (Plane Shapes)":
        shape = st.selectbox("Shape", ["Rectangle", "Triangle", "Parallelogram", "Trapezium", "Circle"])
        if shape == "Rectangle":
            L = number_input_float("Length", value=8.0)
            W = number_input_float("Width", value=5.0)
            if st.button("Compute Rectangle"):
                st.success(f"Perimeter = {pretty_number(2*(L+W))}, Area = {pretty_number(L*W)}")
        elif shape == "Triangle":
            B = number_input_float("Base", value=10.0)
            H = number_input_float("Height", value=6.0)
            if st.button("Compute Triangle"):
                st.success(f"Area = 1/2 * b * h = {pretty_number(0.5*B*H)}")
        elif shape == "Parallelogram":
            B = number_input_float("Base", value=10.0, key="pb")
            H = number_input_float("Height", value=6.0, key="ph")
            if st.button("Compute Parallelogram"):
                st.success(f"Area = b*h = {pretty_number(B*H)}")
        elif shape == "Trapezium":
            A_ = number_input_float("a (top)", value=8.0)
            Bt = number_input_float("b (bottom)", value=12.0)
            H = number_input_float("height", value=5.0)
            if st.button("Compute Trapezium"):
                st.success(f"Area = 1/2*(a+b)*h = {pretty_number(0.5*(A_+Bt)*H)}")
        else:
            r_ = number_input_float("Radius r", value=7.0)
            if st.button("Compute Circle"):
                st.success(f"Diameter = {pretty_number(2*r_)}, Circumference ≈ {pretty_number(2*math.pi*r_)}, Area ≈ {pretty_number(math.pi*r_*r_)}")
    else:
        solid = st.selectbox("Solid", ["Cuboid", "Cylinder", "Sphere", "Cone"])
        if solid == "Cuboid":
            l = number_input_float("Length", value=4.0)
            w = number_input_float("Width", value=3.0)
            h = number_input_float("Height", value=2.0)
            if st.button("Compute Cuboid"):
                st.success(f"Volume = {pretty_number(l*w*h)}; Surface Area = {pretty_number(2*(l*w + l*h + w*h))}")
        elif solid == "Cylinder":
            r_ = number_input_float("Radius", value=3.0, key="cr")
            h = number_input_float("Height", value=5.0, key="ch")
            if st.button("Compute Cylinder"):
                st.success(f"Volume ≈ {pretty_number(math.pi*r_*r_*h)}; Curved Surface Area ≈ {pretty_number(2*math.pi*r_*h)}")
        elif solid == "Sphere":
            r_ = number_input_float("Radius", value=3.0, key="sr")
            if st.button("Compute Sphere"):
                st.success(f"Volume ≈ {pretty_number((4*math.pi*r_**3)/3)}; Surface Area ≈ {pretty_number(4*math.pi*r_**2)}")
        else:
            r_ = number_input_float("Radius", value=3.0, key="cor")
            h = number_input_float("Height", value=5.0, key="coh")
            if st.button("Compute Cone"):
                st.success(f"Volume ≈ {pretty_number((math.pi*r_*r_*h)/3)}")

elif topic == "Mensuration":
    st.subheader("📐 Mensuration (Perimeter/Area/Volume quick tools)")
    kind = st.selectbox("Type", ["Perimeter", "Area", "Volume"])
    if kind == "Perimeter":
        st.write("Rectangle perimeter")
        L = number_input_float("Length", value=10.0)
        W = number_input_float("Width", value=6.0)
        if st.button("Perimeter"):
            st.success(f"P = {pretty_number(2*(L+W))}")
    elif kind == "Area":
        st.write("Circle area")
        r_ = number_input_float("Radius", value=7.0)
        if st.button("Area"):
            st.success(f"A = πr² ≈ {pretty_number(math.pi*r_**2)}")
    else:
        st.write("Cylinder volume")
        r_ = number_input_float("Radius", value=3.0)
        h_ = number_input_float("Height", value=10.0)
        if st.button("Volume"):
            st.success(f"V = πr²h ≈ {pretty_number(math.pi*r_**2*h_)}")

elif topic == "Statistics":
    st.subheader("📊 Statistics")
    raw = st.text_input("Enter numbers (comma-separated)", "2, 3, 5, 7, 11, 13, 13")
    if st.button("Compute Stats"):
        try:
            data = parse_float_list(raw)
            arr = np.array(data)
            mean = float(np.mean(arr)); median = float(np.median(arr))
            srs = pd.Series(arr).value_counts()
            modes = srs[srs == srs.max()].index.tolist()
            st.write({"Mean": pretty_number(mean), "Median": pretty_number(median), "Mode(s)": [pretty_number(m) for m in modes]})
        except Exception as e:
            st.error(e)

elif topic == "Probability":
    st.subheader("🎲 Probability (Equally-likely)")
    experiment = st.selectbox("Experiment", ["Coin", "Die (1)", "Cards: Ace from 52-card deck", "Custom (favourable/total)"])
    if experiment == "Coin":
        if st.button("Head or Tail probability"):
            st.success("P = 1/2 = 0.5")
    elif experiment == "Die (1)":
        ev = st.selectbox("Event", ["even", ">4", "prime"])
        if st.button("Probability"):
            outcomes = {1,2,3,4,5,6}
            fav = {"even": {2,4,6}, ">4": {5,6}, "prime": {2,3,5}}[ev]
            st.success(f"P = {len(fav)}/6 = {len(fav)/6}")
    elif experiment == "Cards: Ace from 52-card deck":
        if st.button("Probability of Ace"):
            st.success("P = 4/52 = 1/13 ≈ 0.076923")
    else:
        fav = number_input_int("Favourable outcomes", value=1)
        tot = number_input_int("Total outcomes", value=6)
        if st.button("Compute Probability"):
            if tot <= 0 or fav < 0 or fav > tot:
                st.error("Check values.")
            else:
                st.success(f"P = {fav}/{tot} = {fav/tot}")

elif topic == "Sets":
    st.subheader("🟦 Sets (Basic operations)")
    A_str = st.text_input("Set A elements (comma-separated)", "1,2,3,4")
    B_str = st.text_input("Set B elements (comma-separated)", "3,4,5,6")
    op = st.selectbox("Operation", ["Union A∪B", "Intersection A∩B", "A\\B (Difference)", "B\\A (Difference)"])
    if st.button("Compute Sets"):
        try:
            A = set([s.strip() for s in A_str.split(",") if s.strip()!=""])
            B = set([s.strip() for s in B_str.split(",") if s.strip()!=""])
            if op == "Union A∪B": res = A.union(B)
            elif op == "Intersection A∩B": res = A.intersection(B)
            elif op == "A\\B (Difference)": res = A.difference(B)
            else: res = B.difference(A)
            st.success(f"Result: {sorted(list(res), key=lambda v: (str(type(v)), str(v)))}")
        except Exception as e:
            st.error(e)

# ----- SSS -----
elif topic == "Trigonometry":
    st.subheader("📐 Trigonometry (Degrees by default)")
    expr = st.text_input("Enter trig expression (e.g. sin(30), cos(pi/3) — pi cases kept as radians)", "")
    angle_mode = st.radio("Angle Mode", ["Degrees", "Radians"], horizontal=True, index=0)
    if st.button("Evaluate trig"):
        try:
            parsed = sp.sympify(implicit_mul(expr), locals=ALLOWED)
            if angle_mode == "Degrees":
                parsed = convert_trig_degrees(parsed)
            st.success(f"Result: {sp.N(parsed)}")
        except Exception as e:
            st.error(e)

elif topic == "Quadratic Equations":
    st.subheader("🟩 Quadratic: ax² + bx + c = 0")
    a = number_input_float("a (≠0)", value=1.0)
    b_ = number_input_float("b", value=-3.0)
    c_ = number_input_float("c", value=2.0)
    if st.button("Solve Quadratic"):
        try:
            D = b_**2 - 4*a*c_
            r1 = (-b_ + sp.sqrt(D)) / (2*a)
            r2 = (-b_ - sp.sqrt(D)) / (2*a)
            st.write({"Discriminant": pretty_number(D), "Roots": [sp.N(r1), sp.N(r2)]})
        except Exception as e:
            st.error(e)

elif topic == "Calculus":
    st.subheader("🧭 Calculus")
    expr = st.text_input("f(x) =", "3*x**4 - 5*x**2 + 7*x - 9")
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("Differentiate"):
            try:
                f = sp.sympify(implicit_mul(expr), locals=ALLOWED)
                st.success(f"f'(x) = {sp.diff(f, x)}")
            except Exception as e:
                st.error(e)
    with c2:
        if st.button("Integrate"):
            try:
                f = sp.sympify(implicit_mul(expr), locals=ALLOWED)
                st.success(f"∫ f(x) dx = {sp.integrate(f, x)} + C")
            except Exception as e:
                st.error(e)
    with c3:
        a_val = number_input_float("Limit as x → a", value=1.0)
        if st.button("Limit"):
            try:
                f = sp.sympify(implicit_mul(expr), locals=ALLOWED)
                st.success(f"limₓ→{a_val} f(x) = {sp.limit(f, x, a_val)}")
            except Exception as e:
                st.error(e)

elif topic == "Matrices":
    st.subheader("🧮 Matrices")
    A_str = st.text_area("Matrix A (rows by ';', elements by space)", "1 2; 3 4")
    B_str = st.text_area("Matrix B (optional, same format)", "5 6; 7 8")
    op = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Determinant A", "Inverse A"])
    if st.button("Compute Matrix"):
        try:
            A = sp.Matrix([[float(n) for n in row.split()] for row in A_str.split(';')])
            B = sp.Matrix([[float(n) for n in row.split()] for row in B_str.split(';')]) if B_str.strip() else None
            if op == "Add":
                st.success(f"A + B =\n{A + B}")
            elif op == "Subtract":
                st.success(f"A - B =\n{A - B}")
            elif op == "Multiply":
                st.success(f"A * B =\n{A * B}")
            elif op == "Determinant A":
                st.success(f"det(A) = {A.det()}")
            elif op == "Inverse A":
                st.success(f"A⁻¹ =\n{A.inv()}")
        except Exception as e:
            st.error(e)

elif topic == "Vectors":
    st.subheader("🧭 Vectors (3D)")
    A_str = st.text_input("Vector A (comma-separated)", "1,2,3")
    B_str = st.text_input("Vector B (comma-separated)", "4,5,6")
    op = st.selectbox("Operation", ["Dot", "Cross", "Magnitude A", "Magnitude B", "A + B", "A - B"])
    if st.button("Compute Vector"):
        try:
            A = sp.Matrix([float(s) for s in A_str.split(",")])
            B = sp.Matrix([float(s) for s in B_str.split(",")]) if B_str.strip() else None
            if op == "Dot": st.success(f"A·B = {A.dot(B)}")
            elif op == "Cross": st.success(f"A×B = {A.cross(B)}")
            elif op == "Magnitude A": st.success(f"|A| = {A.norm()}")
            elif op == "Magnitude B": st.success(f"|B| = {B.norm()}")
            elif op == "A + B": st.success(f"A+B = {A + B}")
            elif op == "A - B": st.success(f"A-B = {A - B}")
        except Exception as e:
            st.error(e)

elif topic == "Complex Numbers":
    st.subheader("🔢 Complex Numbers")
    z_str = st.text_input("Enter complex number (e.g., 3+4*i)", "3+4*i")
    action = st.selectbox("Action", ["Simplify", "Modulus", "Argument (rad)", "Conjugate"])
    if st.button("Compute Complex"):
        try:
            zi = sp.sympify(z_str.replace("i","I"), locals=ALLOWED)
            if action == "Simplify": st.success(f"{sp.simplify(zi)}")
            elif action == "Modulus": st.success(f"|z| = {sp.Abs(zi)}")
            elif action == "Argument (rad)": st.success(f"arg(z) = {sp.arg(zi)}")
            else: st.success(f"conj(z) = {sp.conjugate(zi)}")
        except Exception as e:
            st.error(e)

elif topic == "Sequences & Series":
    st.subheader("🔗 Sequences & Series")
    kind = st.selectbox("Type", ["AP (Arithmetic Progression)", "GP (Geometric Progression)"])
    if kind == "AP (Arithmetic Progression)":
        a1 = number_input_float("First term (a₁)", value=2.0)
        d_ = number_input_float("Common difference (d)", value=3.0)
        n_ = number_input_int("n (terms)", value=5)
        if st.button("AP nth term & sum"):
            an = a1 + (n_-1)*d_
            S = (n_/2)*(2*a1 + (n_-1)*d_)
            st.success(f"aₙ = {pretty_number(an)},  Sₙ = {pretty_number(S)}")
    else:
        a1 = number_input_float("First term (a₁)", value=2.0)
        r_ = number_input_float("Common ratio (r)", value=3.0)
        n_ = number_input_int("n (terms)", value=5)
        if st.button("GP nth term & sum"):
            an = a1*(r_**(n_-1))
            if abs(r_-1) < 1e-12:
                S = a1*n_
            else:
                S = a1*((r_**n_ - 1)/(r_ - 1))
            st.success(f"aₙ = {pretty_number(an)},  Sₙ = {pretty_number(S)}")

elif topic == "Logarithms & Indices":
    st.subheader("📙 Logarithms & Indices")
    ex = st.text_input("Enter expression (e.g., log(100,10), 2**5, sqrt(49))", "log(100,10)")
    if st.button("Evaluate"):
        try:
            st.success(f"Result: {sp.sympify(implicit_mul(ex), locals=ALLOWED).evalf()}")
        except Exception as e:
            st.error(e)

elif topic == "Graphs":
    st.subheader("📈 Graph y = f(x)")
    fx = st.text_input("f(x) =", "x**2 - 3*x + 2")
    xmin, xmax = number_input_float("x min", value=-5.0), number_input_float("x max", value=5.0)
    npts = st.slider("Number of points", 20, 500, 101)
    if st.button("Plot f(x)"):
        try:
            f = sp.lambdify(x, sp.sympify(implicit_mul(fx), locals=ALLOWED), 'numpy')
            X = np.linspace(xmin, xmax, npts)
            Y = f(X)
            df = pd.DataFrame({"x": X, "f(x)": Y})
            st.line_chart(df.set_index("x"))
        except Exception as e:
            st.error(e)

# ----- CALCULATOR -----
elif topic == "Calculator":
    st.subheader("🧮 General Calculator (degrees for trig by default)")
    expr = st.text_input("Enter any expression: e.g. 2+3*5, 5(2+3), 2x with x value, sin(30), sqrt(25), log(100,10)")
    xv = number_input_float("x =", value=1.0)
    angle_mode = st.radio("Angle Mode (for trig)", ["Degrees", "Radians"], horizontal=True, index=0)
    if st.button("Calculate", key="calc"):
        try:
            parsed = sp.sympify(implicit_mul(expr), locals=ALLOWED).subs({x: xv})
            if angle_mode == "Degrees":
                parsed = convert_trig_degrees(parsed)
            st.success(f"Result: {sp.N(parsed)}")
        except Exception as e:
            st.error(e)
