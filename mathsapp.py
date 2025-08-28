import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import statistics as stats
import re

# ================== PAGE & THEME ==================
st.set_page_config(page_title="MathCore – All-in-One Maths App", layout="wide", page_icon="📘")

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

st.title("🧮 MathCore – All-in-One Maths App (JSS & SSS)")
st.caption("No API keys. SymPy + NumPy + Pandas under the hood. Mature dark-blue theme + black sidebar.")

# ================== HELPERS ==================
ALLOWED = {
    'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
    'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
    'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
    'sqrt': sp.sqrt, 'log': sp.log, 'ln': sp.log, 'exp': sp.exp,
    'pi': sp.pi, 'E': sp.E, 'Abs': sp.Abs, 'floor': sp.floor, 'ceiling': sp.ceiling
}

_num = re.compile(r"(\d)\s*(?=\()")
_alpha = re.compile(r"(\d)([a-zA-Z])")
_paren_num = re.compile(r"\)\s*(\d)")

def implicit_mul(expr: str) -> str:
    if not expr:
        return expr
    expr = _num.sub(r"\1*", expr)
    expr = _alpha.sub(r"\1*\2", expr)
    expr = _paren_num.sub(r")*\1", expr)
    return expr

# --- Format results ---
def format_result(val):
    try:
        if isinstance(val, (int, float, sp.Float)):
            if float(val).is_integer():
                return int(val)
        elif isinstance(val, (list, tuple)):
            return [format_result(x) for x in val]
        return val
    except:
        return val

# --- Trig degree conversion ---
from sympy import Number
def convert_trig_degrees(sym_expr: sp.Expr) -> sp.Expr:
    def is_trig_numeric(node):
        return (node.func in (sp.sin, sp.cos, sp.tan)
                and len(node.args) == 1
                and isinstance(node.args[0], (Number, sp.Integer, sp.Rational, sp.Float))
                and not node.args[0].has(sp.pi))
    return sym_expr.replace(is_trig_numeric, lambda e: e.func(e.args[0]*sp.pi/180))

# --- Parse equations ---
def parse_equation(text: str, locals=None):
    locals = locals or ALLOWED
    text = implicit_mul(text)
    if '=' in text:
        L, R = text.split('=', 1)
        return sp.Eq(sp.sympify(L, locals=locals), sp.sympify(R, locals=locals))
    return sp.sympify(text, locals=locals)

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
# ----------------- JSS -----------------
if topic == "Arithmetic":
    st.subheader("Arithmetic")
    expr = st.text_input("Enter expression (supports implicit multiplication like 5(2+3))")
    if st.button("Compute", key="arith"):
        try:
            val = sp.sympify(implicit_mul(expr), locals=ALLOWED).evalf()
            st.success(f"Result: {format_result(val)}")
        except Exception as e:
            st.error(e)

elif topic == "Fractions & Decimals":
    st.subheader("Fractions & Decimals")
    col1, col2 = st.columns(2)
    with col1:
        dec = st.text_input("Decimal → Fraction (e.g. 0.75)")
        if st.button("To Fraction"):
            try:
                r = sp.Rational(dec).limit_denominator()
                st.success(f"{dec} = {r} (≈ {format_result(float(r))})")
            except Exception as e:
                st.error(e)
    with col2:
        frac = st.text_input("Fraction → Decimal (e.g. 5/8)")
        if st.button("To Decimal"):
            try:
                r = sp.nsimplify(frac)
                st.success(f"{frac} ≈ {format_result(float(r))}")
            except Exception as e:
                st.error(e)

elif topic == "GCD & LCM":
    st.subheader("GCD & LCM")
    nums = st.text_input("Enter integers separated by commas", "12,18,30")
    if st.button("Compute GCD/LCM"):
        try:
            arr = [int(s) for s in nums.replace(';', ',').split(',') if s.strip()]
            g = int(sp.igcd(*arr))
            l = int(sp.ilcm(*arr))
            st.success(f"GCD/HCF = {format_result(g)}, LCM = {format_result(l)}")
        except Exception as e:
            st.error(e)

elif topic == "Simple Interest & Percentage":
    st.subheader("Simple Interest & Percentage")
    P = st.number_input("Principal (₦)", value=10000.0, step=100.0)
    R = st.number_input("Rate (%)", value=10.0)
    T = st.number_input("Time (years)", value=2.0)
    if st.button("Compute Simple Interest"):
        SI = (P*R*T)/100
        A = P + SI
        st.success(f"Simple Interest = ₦{format_result(SI)}, Amount = ₦{format_result(A)}")
    st.divider()
    base = st.number_input("Base value", value=200.0)
    p = st.number_input("Percentage %", value=15.0)
    if st.button("% of base"):
        st.success(f"{p}% of {base} = {format_result((p/100)*base)}")

# --- Pythagoras ---
elif topic == "Pythagoras":
    st.subheader("Pythagoras")
    tab1, tab2 = st.tabs(["Find hypotenuse", "Find a leg"])
    with tab1:
        A = st.number_input("Leg a", value=3.0)
        B = st.number_input("Leg b", value=4.0)
        if st.button("Hypotenuse"):
            st.success(f"c = {format_result(np.hypot(A,B))}")
    with tab2:
        C = st.number_input("Hypotenuse c", value=13.0)
        known = st.number_input("Known leg", value=5.0)
        if st.button("Other leg"):
            val = max(C**2 - known**2, 0)
            st.success(f"Other leg = {format_result(np.sqrt(val))}")

# --- Algebra ---
elif topic == "Algebra":
    st.subheader("Algebra (JSS)")
    eq = st.text_input("Enter equation or expression in x (e.g. 2*x+3=11 or x^2-5*x+6)")
    if st.button("Solve/Factor"):
        try:
            obj = parse_equation(eq, ALLOWED)
            x = sp.Symbol('x')
            if isinstance(obj, sp.Equality):
                sol = sp.solve(obj, x)
                st.success(f"Solutions: {format_result(sol)}")
            else:
                st.write(f"Simplified: {sp.simplify(obj)}")
                st.write(f"Factored: {sp.factor(obj)}")
        except Exception as e:
            st.error(e)

# --- Simultaneous Equations (2x2) ---
elif topic == "Simultaneous Equations (2×2)":
    st.subheader("Simultaneous Equations")
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
                st.success(f"x = {format_result(sol[0][x])}, y = {format_result(sol[0][y])}")
            else:
                st.warning("No unique solution.")
        except Exception as e:
            st.error(e)

# --- Geometry ---
elif topic == "Geometry":
    st.subheader("Geometry")
    shape = st.selectbox("Shape", ["Rectangle", "Triangle", "Parallelogram", "Trapezium", "Circle"])
    if shape == "Rectangle":
        L = st.number_input("Length", value=8.0)
        W = st.number_input("Width", value=5.0)
        if st.button("Compute Rectangle"):
            st.success(f"Perimeter = {format_result(2*(L+W))}, Area = {format_result(L*W)}")
    elif shape == "Triangle":
        B = st.number_input("Base", value=10.0)
        H = st.number_input("Height", value=6.0)
        if st.button("Compute Triangle"):
            st.success(f"Area = {format_result(0.5*B*H)}")

# --- Statistics ---
elif topic == "Statistics":
    st.subheader("Statistics")
    raw = st.text_input("Enter numbers (comma-separated)", "2,3,5,7,11,13,13")
    if st.button("Compute Stats"):
        try:
            data = [float(s) for s in raw.replace('\n', ',').replace(';', ',').split(',') if s.strip()]
            arr = np.array(data)
            mean = format_result(float(np.mean(arr)))
            median = format_result(float(np.median(arr)))
            srs = pd.Series(arr).value_counts()
            modes = [format_result(x) for x in srs[srs == srs.max()].index.tolist()]
            st.write({"Mean": mean, "Median": median, "Mode(s)": modes})
        except Exception as e:
            st.error(e)

# --- Trigonometry ---
elif topic == "Trigonometry":
    st.subheader("Trigonometry Evaluator")
    expr = st.text_input("Enter trig expression (e.g. sin(30), cos(pi/3), tan(45))")
    angle_mode = st.radio("Angle Mode", ["Degrees", "Radians"], horizontal=True)
    if st.button("Evaluate trig"):
        try:
            parsed = sp.sympify(implicit_mul(expr), locals=ALLOWED)
            if angle_mode == "Degrees":
                parsed = convert_trig_degrees(parsed)
            st.success(f"Result: {format_result(parsed)}")
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
            st.success(f"Result: {format_result(parsed)}")
        except Exception as e:
            st.error(e)
