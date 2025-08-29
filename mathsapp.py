import streamlit as st
import sympy as sp
import numpy as np
import pandas as pd
import math
import re
import statistics as stats

# ================== PAGE & THEME ==================
st.set_page_config(page_title="MathCore – All-in-One Maths App", layout="wide", page_icon="📖")

st.markdown(
    """
    <style>
      /* Main app background (mature dark blue) */
      .stApp { background-color:#0A1A2F; color:#FFFFFF; }

      /* Sidebar - a slightly different mature blue */
      section[data-testid="stSidebar"] { background-color:#102B57 !important; }
      section[data-testid="stSidebar"] * { color:#FFFFFF !important; }

      /* Buttons */
      .stButton>button {
        background:#1B263B !important;
        color:#FFFFFF !important;
        border:1px solid #415A77;
        border-radius:10px;
        padding:6px 12px;
      }
      .stButton>button:hover { background:#2E3F66 !important; }

      /* Text inputs / textareas / number inputs (black with white text) */
      .stTextInput>div>div>input,
      .stTextArea>div>div>textarea,
      .stNumberInput > div > input {
        background:#000000 !important;
        color:#FFFFFF !important;
        border-radius:8px;
        padding:6px;
      }

      /* Selectboxes */
      .stSelectbox>div>div { background:#102544 !important; color:#FFFFFF !important; border-radius:8px; padding:3px; }

      /* Headers */
      h1, h2, h3, h4 { color:#FFFFFF !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧮 MathCore – All-in-One Maths App (JSS & SSS)")

# ================== HELPERS ==================
ALLOWED = {
    'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
    'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
    'sinh': sp.sinh, 'cosh': sp.cosh, 'tanh': sp.tanh,
    'sqrt': sp.sqrt, 'log': sp.log, 'ln': sp.log, 'exp': sp.exp,
    'pi': sp.pi, 'E': sp.E, 'Abs': sp.Abs, 'floor': sp.floor, 'ceiling': sp.ceiling
}

# implicit multiplication helpers
_num = re.compile(r"(\d)\s*(?=\()")   # 2( -> 2*(
_alpha = re.compile(r"(\d)([a-zA-Z])") # 2x -> 2*x
_paren_num = re.compile(r"\)\s*(\d)")  # )(2 -> )*2

def implicit_mul(expr: str) -> str:
    if not expr:
        return expr
    expr = _num.sub(r"\1*", expr)
    expr = _alpha.sub(r"\1*\2", expr)
    expr = _paren_num.sub(r")*\1", expr)
    return expr

from sympy import Number, Integer, Rational, Float
def convert_trig_degrees(sym_expr: sp.Expr) -> sp.Expr:
    """
    Convert numeric trig arguments interpreted as degrees into radians.
    Only converts trig nodes whose argument is a plain numeric value (no pi).
    """
    def is_trig_numeric(node):
        return (node.func in (sp.sin, sp.cos, sp.tan)
                and len(node.args) == 1
                and isinstance(node.args[0], (Number, Integer, Rational, Float))
                and not node.args[0].has(sp.pi))
    return sym_expr.replace(is_trig_numeric, lambda e: e.func(e.args[0]*sp.pi/180))

def evaluate_sympy_expression(expr: str):
    """
    Safely evaluate an expression using sympy with ALLOWED functions,
    converting numeric trig args from degrees to radians first.
    Returns numeric result (int if whole), or raises.
    """
    expr = implicit_mul(expr)
    sym = sp.sympify(expr, locals=ALLOWED)
    sym_deg = convert_trig_degrees(sym)
    val = sp.N(sym_deg)
    # try to return whole integer when possible
    try:
        f = float(val)
        if abs(f - round(f)) < 1e-12:
            return int(round(f))
        return round(f, 10)  # keep precision
    except Exception:
        return val

# small safe evaluator fallback for simple numeric-only cases
def evaluate_numeric_fallback(expr: str):
    expr = implicit_mul(expr)
    # convert sin(x) -> math.sin(math.radians(x)) etc.
    expr = re.sub(r"\bsin\(", r"math.sin(math.radians(", expr)
    expr = re.sub(r"\bcos\(", r"math.cos(math.radians(", expr)
    expr = re.sub(r"\btan\(", r"math.tan(math.radians(", expr)
    result = eval(expr, {"math": math, "np": np, "__builtins__": {}})
    if isinstance(result, float) and result.is_integer():
        return int(result)
    if isinstance(result, float):
        return round(result, 10)
    return result

def safe_eval(expr: str):
    # try sympy path first (supports symbolic & nested parentheses)
    try:
        return evaluate_sympy_expression(expr)
    except Exception:
        # fallback to numeric eval (for simple numeric trig)
        try:
            return evaluate_numeric_fallback(expr)
        except Exception as e:
            raise e

def parse_equation(expr: str, allowed_locals: dict) -> sp.Expr:
    """
    Parse an equation string into a sympy expression or equation object.
    Handles both expressions and equations with '=' sign.
    """
    expr = implicit_mul(expr)
    
    # Check if it's an equation (contains '=')
    if '=' in expr:
        parts = expr.split('=', 1)
        left = sp.sympify(parts[0].strip(), locals=allowed_locals)
        right = sp.sympify(parts[1].strip(), locals=allowed_locals)
        return sp.Eq(left, right)
    else:
        # It's just an expression
        return sp.sympify(expr, locals=allowed_locals)

# ================== SIDEBAR ==================
st.sidebar.title("📘 MathCore")
level = st.sidebar.selectbox("Select Level", ["Junior Secondary (JSS)", "Senior Secondary (SSS)", "Calculator"], index=0)

# Add expanded topic lists + 5 extras each
jss_topics = [
    "Arithmetic", "Fractions & Decimals", "GCD & LCM", "Simple Interest & Percentage",
    "Ratio & Proportion", "Pythagoras", "Algebra (Simplify/Solve)", "Simultaneous Equations (2×2)",
    "Geometry", "Statistics", "Trigonometry"
]
jss_extras = ["Number Patterns", "Exponents & Powers", "Coordinate Geometry", "Mensuration", "Probability"]
jss_topics.extend(jss_extras)

sss_topics = [
    "Algebra (Factor/Solve)", "Quadratic Equations", "Trigonometry",
    "Calculus", "Probability", "Matrices", "Logarithms & Indices", "Graphs"
]
sss_extras = ["Complex Numbers", "Vectors", "Determinants", "Statistics & Data", "Conic Sections"]
sss_topics.extend(sss_extras)

if level.startswith("Junior"):
    topic = st.sidebar.radio("Choose a JSS topic:", jss_topics, index=0)
elif level.startswith("Senior"):
    topic = st.sidebar.radio("Choose an SSS topic:", sss_topics, index=0)
else:
    topic = "Calculator"

# ================== TOPICS ==================

# ---------- JSS ----------
if level.startswith("Junior"):
    # Arithmetic
    if topic == "Arithmetic":
        st.subheader("Arithmetic")
        expr = st.text_input("Enter arithmetic expression (supports implicit multiplication, e.g. 5(2+3))")
        if st.button("Calculate"):
            try:
                res = safe_eval(expr)
                st.success(f"Result: {res}")
            except Exception as e:
                st.error(f"Error: {e}")

    # Fractions & Decimals
    elif topic == "Fractions & Decimals":
        st.subheader("Fractions & Decimals")
        with st.expander("Decimal → Fraction"):
            dec = st.text_input("Decimal (e.g. 0.75)", key="dec2frac")
            if st.button("To Fraction"):
                try:
                    r = sp.Rational(float(dec)).limit_denominator()
                    st.success(f"{dec} = {r} (≈ {float(r)})")
                except Exception as e:
                    st.error(e)
        with st.expander("Fraction → Decimal"):
            frac = st.text_input("Fraction (e.g. 3/4)", key="frac2dec")
            if st.button("To Decimal", key="to_dec"):
                try:
                    v = sp.nsimplify(frac)
                    st.success(f"{frac} ≈ {float(v)}")
                except Exception as e:
                    st.error(e)

    # GCD & LCM
    elif topic == "GCD & LCM":
        st.subheader("GCD & LCM")
        nums = st.text_input("Enter integers separated by commas", "12,18,30")
        if st.button("Compute"):
            try:
                arr = [int(s) for s in nums.replace(';',',').split(',') if s.strip()]
                g = int(sp.igcd(*arr))
                l = int(sp.ilcm(*arr))
                st.success(f"GCD/HCF = {g}, LCM = {l}")
            except Exception as e:
                st.error(e)

    # Simple Interest & Percentage
    elif topic == "Simple Interest & Percentage":
        st.subheader("Simple Interest & Percentage")
        P = st.number_input("Principal (P)", value=10000.0)
        R = st.number_input("Rate % per annum", value=10.0)
        T = st.number_input("Time (years)", value=2.0)
        if st.button("Compute Simple Interest"):
            SI = (P * R * T) / 100
            A = P + SI
            st.success(f"Simple Interest = ₦{SI}, Amount = ₦{A}")
        st.divider()
        base = st.number_input("Base value for percentage", value=200.0, key="base_pct")
        p = st.number_input("Percentage %", value=15.0, key="p_pct")
        if st.button("Compute %"):
            st.success(f"{p}% of {base} = {(p/100)*base}")

    # Ratio & Proportion
    elif topic == "Ratio & Proportion":
        st.subheader("Ratio & Proportion")
        a = st.number_input("Ratio a", value=2.0)
        b = st.number_input("Ratio b", value=3.0)
        total = st.number_input("Total to share", value=100.0)
        if st.button("Share by ratio"):
            s = a + b
            st.success(f"Portion A = {total*(a/s)}, Portion B = {total*(b/s)}")

    # Pythagoras
    elif topic == "Pythagoras":
        st.subheader("Pythagoras (Right Triangle)")
        mode_p = st.radio("Find:", ["Hypotenuse", "Missing leg"])
        if mode_p == "Hypotenuse":
            a = st.number_input("Leg a", value=3.0)
            b_ = st.number_input("Leg b", value=4.0)
            if st.button("Compute"):
                st.success(f"Hypotenuse = {math.hypot(a,b_)}")
        else:
            c = st.number_input("Hypotenuse", value=13.0)
            known = st.number_input("Known leg", value=5.0)
            if st.button("Compute"):
                val = math.sqrt(max(c**2 - known**2, 0))
                st.success(f"Other leg = {val}")

    # Algebra (Simplify/Solve)
    elif topic == "Algebra (Simplify/Solve)":
        st.subheader("Algebra (Simplify / Solve)")
        expr = st.text_input("Expression or equation in x (e.g., 2*x + 3 = 11 or x**2 -5*x +6)")
        if st.button("Process"):
            try:
                obj = parse_equation(expr, ALLOWED)
                if isinstance(obj, sp.Equality):
                    sol = sp.solve(obj, dict=True)
                    st.success(f"Solutions: {sol}")
                else:
                    st.write("Simplified:", sp.simplify(obj))
                    st.write("Factored:", sp.factor(obj))
            except Exception as e:
                st.error(e)

    # Simultaneous Equations (2x2)
    elif topic == "Simultaneous Equations (2×2)":
        st.subheader("Simultaneous Equations (2×2)")
        c1, c2 = st.columns(2)
        with c1:
            a1 = st.number_input("a1", value=1.0)
            b1 = st.number_input("b1", value=2.0)
            c1v = st.number_input("c1", value=5.0)
        with c2:
            a2 = st.number_input("a2", value=3.0)
            b2 = st.number_input("b2", value=-1.0)
            c2v = st.number_input("c2", value=4.0)
        if st.button("Solve"):
            try:
                x, y = sp.symbols('x y')
                sol = sp.solve([sp.Eq(a1*x + b1*y, c1v), sp.Eq(a2*x + b2*y, c2v)], (x, y), dict=True)
                if sol:
                    st.success(f"x = {sp.N(sol[0][x])}, y = {sp.N(sol[0][y])}")
                else:
                    st.warning("No unique solution.")
            except Exception as e:
                st.error(e)

    # Geometry (Plane + 3D)
    elif topic == "Geometry":
        st.subheader("Geometry")
        shape = st.selectbox("Plane shapes / 3D solids", ["Plane Shapes", "Cuboid", "Cylinder", "Sphere", "Cone"])
        if shape == "Plane Shapes":
            shp = st.selectbox("Shape", ["Rectangle", "Triangle", "Parallelogram", "Trapezium"])
            if shp == "Rectangle":
                L = st.number_input("Length", value=8.0, key="rectL")
                W = st.number_input("Width", value=5.0, key="rectW")
                if st.button("Compute Rectangle"):
                    st.success(f"Perimeter = {2*(L+W)}, Area = {L*W}")
            elif shp == "Triangle":
                b_ = st.number_input("Base", value=10.0, key="triB")
                h_ = st.number_input("Height", value=6.0, key="triH")
                if st.button("Compute Triangle"):
                    st.success(f"Area = {0.5*b_*h_}")
            elif shp == "Parallelogram":
                b_ = st.number_input("Base", value=10.0, key="paraB")
                h_ = st.number_input("Height", value=6.0, key="paraH")
                if st.button("Compute Parallelogram"):
                    st.success(f"Area = {b_*h_}")
            else:
                a = st.number_input("a (top)", value=8.0, key="trapA")
                btm = st.number_input("b (bottom)", value=12.0, key="trapB")
                h = st.number_input("height", value=5.0, key="trapH")
                if st.button("Compute Trapezium"):
                    st.success(f"Area = {0.5*(a+btm)*h}")
        elif shape == "Cuboid":
            l = st.number_input("Length", value=4.0, key="cubL")
            w = st.number_input("Width", value=3.0, key="cubW")
            h = st.number_input("Height", value=2.0, key="cubH")
            if st.button("Compute Cuboid"):
                st.success(f"Volume = {l*w*h}; Surface Area = {2*(l*w + l*h + w*h)}")
        elif shape == "Cylinder":
            r = st.number_input("Radius", value=3.0, key="cylR")
            h = st.number_input("Height", value=5.0, key="cylH")
            if st.button("Compute Cylinder"):
                st.success(f"Volume ≈ {math.pi*r*r*h:.5f}; Curved Surface Area ≈ {2*math.pi*r*h:.5f}")
        elif shape == "Sphere":
            r = st.number_input("Radius", value=3.0, key="sphR")
            if st.button("Compute Sphere"):
                st.success(f"Volume ≈ {(4*math.pi*r**3)/3:.5f}; Surface Area ≈ {4*math.pi*r**2:.5f}")
        else:
            r = st.number_input("Radius", value=3.0, key="coneR")
            h = st.number_input("Height", value=5.0, key="coneH")
            if st.button("Compute Cone"):
                st.success(f"Volume ≈ {(math.pi*r*r*h)/3:.5f}")

    # Statistics
    elif topic == "Statistics":
        st.subheader("Statistics (Ungrouped)")
        nums = st.text_input("Enter numbers separated by commas", "2,3,5,7,11,13,13")
        if st.button("Compute"):
            try:
                data = [float(s) for s in nums.replace('\n',',').replace(';',',').split(',') if s.strip()]
                if not data:
                    st.warning("Enter data.")
                else:
                    arr = np.array(data)
                    mean = float(np.mean(arr))
                    median = float(np.median(arr))
                    srs = pd.Series(arr).value_counts()
                    modes = srs[srs == srs.max()].index.tolist()
                    st.success({"Mean": mean, "Median": median, "Mode(s)": modes})
            except Exception as e:
                st.error(e)

    # Trigonometry (degrees)
    elif topic == "Trigonometry":
        st.subheader("Trigonometry (degrees)")
        st.info("All trigonometric functions use degrees")
        trig_expr = st.text_input("Enter trig expression (e.g., sin(30), cos(45) + tan(30))")
        if st.button("Evaluate"):
            try:
                res = safe_eval(trig_expr)
                st.success(f"Result: {res}")
            except Exception as e:
                st.error(e)

    # Extra JSS topics
    elif topic == "Number Patterns":
        st.subheader("Number Patterns")
        seq = st.text_input("Enter sequence (comma-separated, e.g. 2,4,6,8)")
        if st.button("Analyze"):
            try:
                nums = [int(x.strip()) for x in seq.split(',')]
                diffs = [nums[i+1]-nums[i] for i in range(len(nums)-1)]
                arith = all(d==diffs[0] for d in diffs)
                st.success({"Sequence": nums, "Differences": diffs, "Arithmetic?": arith})
            except Exception as e:
                st.error(e)

    elif topic == "Exponents & Powers":
        st.subheader("Exponents & Powers")
        base = st.number_input("Base", value=2.0)
        exp = st.number_input("Exponent", value=3.0)
        if st.button("Compute"):
            st.success(f"{base}^{exp} = {base**exp}")

    elif topic == "Coordinate Geometry":
        st.subheader("Coordinate Geometry")
        x1 = st.number_input("x1", value=0.0, key="x1")
        y1 = st.number_input("y1", value=0.0, key="y1")
        x2 = st.number_input("x2", value=1.0, key="x2")
        y2 = st.number_input("y2", value=1.0, key="y2")
        if st.button("Compute"):
            distance = np.hypot(x2-x1, y2-y1)
            midpoint = ((x1+x2)/2, (y1+y2)/2)
            st.success({"Distance": distance, "Midpoint": midpoint})

    elif topic == "Mensuration":
        st.subheader("Mensuration (Cuboid example)")
        l = st.number_input("Length", value=5.0)
        b = st.number_input("Breadth", value=3.0)
        h = st.number_input("Height", value=2.0)
        if st.button("Compute"):
            vol = l*b*h
            sa = 2*(l*b + b*h + l*h)
            st.success({"Volume": vol, "Surface Area": sa})

    elif topic == "Probability":
        st.subheader("Probability (basic)")
        fav = st.number_input("Favourable outcomes", value=1)
        total = st.number_input("Total outcomes", value=6)
        if st.button("Compute"):
            if total <= 0:
                st.error("Total must be > 0")
            else:
                st.success(f"P = {fav}/{total} = {fav/total}")

# ---------- SSS ----------
elif level.startswith("Senior"):
    # Algebra (factor / solve)
    if topic == "Algebra (Factor/Solve)":
        st.subheader("Algebra (Factor / Solve)")
        expr = st.text_input("Enter expression or equation in x (e.g. 2*x**2 - 5*x - 3 or 2*x + 3 = 11)")
        if st.button("Process"):
            try:
                obj = parse_equation(expr, ALLOWED)
                if isinstance(obj, sp.Equality):
                    sol = sp.solve(obj, dict=True)
                    st.success(f"Solutions: {sol}")
                else:
                    st.write("Simplified:", sp.simplify(obj))
                    st.write("Factored:", sp.factor(obj))
            except Exception as e:
                st.error(e)

    # Quadratic Equations
    elif topic == "Quadratic Equations":
        st.subheader("Quadratic Solver")
        a = st.number_input("a (≠0)", value=1.0)
        b = st.number_input("b", value=-3.0)
        c = st.number_input("c", value=2.0)
        if st.button("Solve"):
            try:
                D = b**2 - 4*a*c
                r1 = (-b + math.sqrt(abs(D))) / (2*a) if D>=0 else complex(-b, math.sqrt(-D))/(2*a)
                r2 = (-b - math.sqrt(abs(D))) / (2*a) if D>=0 else complex(-b, -math.sqrt(-D))/(2*a)
                st.success({"Discriminant": D, "Roots": [r1, r2]})
            except Exception as e:
                st.error(e)

    # Trigonometry (degrees)
    elif topic == "Trigonometry":
        st.subheader("Trigonometry (degrees)")
        st.info("All trigonometric functions use degrees")
        trig_expr = st.text_input("Enter trig expression (e.g. sin(30)+cos(60))")
        if st.button("Evaluate"):
            try:
                res = safe_eval(trig_expr)
                st.success(f"Result: {res}")
            except Exception as e:
                st.error(e)

    # Calculus
    elif topic == "Calculus":
        st.subheader("Calculus")
        calc_expr = st.text_input("Enter f(x) (e.g., 3*x**2 - 5*x + 2)")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Differentiate"):
                try:
                    x = sp.symbols('x')
                    f = sp.sympify(calc_expr, locals=ALLOWED)
                    st.success(f"f'(x) = {sp.diff(f, x)}")
                except Exception as e:
                    st.error(e)
        with col2:
            if st.button("Integrate"):
                try:
                    x = sp.symbols('x')
                    f = sp.sympify(calc_expr, locals=ALLOWED)
                    st.success(f"∫ f(x) dx = {sp.integrate(f, x)} + C")
                except Exception as e:
                    st.error(e)
        with col3:
            a_val = st.number_input("Limit as x → a", value=1.0)
            if st.button("Limit"):
                try:
                    x = sp.symbols('x')
                    f = sp.sympify(calc_expr, locals=ALLOWED)
                    st.success(f"lim x→{a_val} f(x) = {sp.limit(f, x, a_val)}")
                except Exception as e:
                    st.error(e)

    # Probability
    elif topic == "Probability":
        st.subheader("Probability (general)")
        fav = st.number_input("Favourable outcomes", value=1)
        tot = st.number_input("Total outcomes", value=6)
        if st.button("Compute"):
            if tot <= 0:
                st.error("Total must be > 0")
            else:
                st.success(f"P = {fav}/{tot} = {fav/tot}")

    # Matrices
    elif topic == "Matrices":
        st.subheader("Matrices")
        A_str = st.text_area("Matrix A (rows separated by ';', elements by space)", "1 2; 3 4")
        op = st.selectbox("Operation", ["Add (with B)", "Subtract (with B)", "Multiply (with B)", "Determinant A", "Inverse A"])
        B_str = st.text_area("Matrix B (optional)", "5 6; 7 8")
        if st.button("Compute"):
            try:
                A = sp.Matrix([[float(n) for n in row.split()] for row in A_str.split(';')])
                B = sp.Matrix([[float(n) for n in row.split()] for row in B_str.split(';')]) if B_str.strip() else None
                if op == "Add (with B)":
                    st.success(f"A + B =\n{A + B}")
                elif op == "Subtract (with B)":
                    st.success(f"A - B =\n{A - B}")
                elif op == "Multiply (with B)":
                    st.success(f"A * B =\n{A * B}")
                elif op == "Determinant A":
                    st.success(f"det(A) = {A.det()}")
                elif op == "Inverse A":
                    st.success(f"A⁻¹ =\n{A.inv()}")
            except Exception as e:
                st.error(e)

    # Logarithms & Indices
    elif topic == "Logarithms & Indices":
        st.subheader("Logarithms & Indices")
        ex = st.text_input("Enter expression (e.g., log(100,10), 2**5, sqrt(49))", "log(100,10)")
        if st.button("Evaluate"):
            try:
                v = safe_eval(ex)
                st.success(f"Result: {v}")
            except Exception as e:
                st.error(e)

    # Graphs (function plot quick)
    elif topic == "Graphs":
        st.subheader("Graphs (function)")
        fx = st.text_input("f(x) =", "x**2 - 3*x + 2")
        xmin = st.number_input("x min", value=-5.0)
        xmax = st.number_input("x max", value=5.0)
        npts = st.slider("Number of points", 20, 500, 101)
        if st.button("Plot f(x)"):
            try:
                x = sp.symbols('x')
                f = sp.lambdify(x, sp.sympify(fx, locals=ALLOWED), 'numpy')
                X = np.linspace(xmin, xmax, npts)
                Y = f(X)
                df = pd.DataFrame({"x": X, "f(x)": Y})
                st.line_chart(df.set_index("x"))
            except Exception as e:
                st.error(e)

    # Extra SSS topics placeholders
    elif topic == "Complex Numbers":
        st.subheader("Complex Numbers")
        expr = st.text_input("Enter complex expression (e.g. 2+3j)")
        if st.button("Compute"):
            try:
                c = complex(expr)
                st.success({"Absolute": abs(c), "Conjugate": c.conjugate()})
            except Exception as e:
                st.error(e)

    elif topic == "Vectors":
        st.subheader("Vectors")
        v1 = st.text_input("Vector 1 (comma-separated)", "1,2,3")
        v2 = st.text_input("Vector 2 (comma-separated)", "4,5,6")
        if st.button("Compute"):
            try:
                a = np.array([float(n) for n in v1.split(',')])
                b = np.array([float(n) for n in v2.split(',')])
                st.success({"Addition": list(a+b), "Dot": float(np.dot(a,b)), "Cross": list(np.cross(a,b))})
            except Exception as e:
                st.error(e)

    elif topic == "Determinants":
        st.subheader("Determinants")
        mat = st.text_area("Enter matrix rows separated by ';' (e.g. '1 2;3'4')")
        if st.button("Compute"):
            try:
                M = sp.Matrix([[float(n) for n in row.split()] for row in mat.split(';')])
                st.success(f"Determinant = {M.det()}")
            except Exception as e:
                st.error(e)

    elif topic == "Statistics & Data":
        st.subheader("Statistics & Data")
        raw = st.text_input("Enter numbers (comma-separated)", "2,3,5,7,11")
        if st.button("Compute"):
            try:
                data = [float(s) for s in raw.replace('\n',',').replace(';',',').split(',') if s.strip()]
                arr = np.array(data)
                mean = float(np.mean(arr)); median = float(np.median(arr))
                srs = pd.Series(arr).value_counts()
                modes = srs[srs == srs.max()].index.tolist()
                st.success({"Mean": mean, "Median": median, "Mode(s)": modes})
            except Exception as e:
                st.error(e)

    elif topic == "Conic Sections":
        st.subheader("Conic Sections")
        eq = st.text_input("Enter conic equation (e.g. x**2/4 + y**2/9 = 1)")
        if st.button("Analyze"):
            st.info("Graphical analysis not implemented yet. Equation saved.")

# ----------------- CALCULATOR -----------------
elif topic == "Calculator":
    st.subheader("🧮 Calculator")
    expr = st.text_input("Enter any expression (e.g. 2+3*5, sin(30), sqrt(25), log(100,10))")
    st.info("Note: All trigonometric functions use degrees")
    if st.button("Calculate"):
        try:
            val = safe_eval(expr)
            st.success(f"Result: {val}")
        except Exception as e:
            st.error(e)
