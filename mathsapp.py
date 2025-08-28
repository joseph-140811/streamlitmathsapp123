import streamlit as st
import sympy as sp
import re

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Maths App", layout="wide")

# Dark theme for sidebar + main page
st.markdown(
    """
    <style>
        body {
            background-color: #0D1117;
            color: #FFFFFF;
        }
        .css-1d391kg, .css-1v0mbdj, .st-af {
            background-color: #0D1117 !important;
            color: #FFFFFF !important;
        }
        .css-1lcbmhc, .css-1q8dd3e, .st-bf, .st-ci {
            color: #FFFFFF !important;
        }
        section[data-testid="stSidebar"] {
            background-color: #0A0A0A !important;
        }
        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📘 Maths Learning  App")

# -------------------- MAIN SELECTION --------------------
level = st.sidebar.selectbox("Choose Level", ["Junior Secondary", "Senior Secondary"])

# -------------------- JUNIOR SECONDARY --------------------
if level == "Junior Secondary":
    topic = st.sidebar.selectbox("Choose a Topic", [
        "Arithmetic", "Algebra", "Simultaneous Equations", "Geometry", "Calculator"
    ])

    if topic == "Arithmetic":
        st.subheader("Arithmetic Evaluator")
        expr = st.text_input("Enter arithmetic expression (e.g., 5*(2+3)):")
        if st.button("Evaluate Arithmetic"):
            try:
                expr_fixed = re.sub(r'(\d)(\()', r'\1*\2', expr)
                result = sp.sympify(expr_fixed, evaluate=True)
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Algebra":
        st.subheader("Solve Linear Equation in x")
        expr = st.text_input("Enter equation (e.g., 2*x + 3 - 7):")
        if st.button("Solve Equation"):
            try:
                x = sp.symbols('x')
                eq = sp.sympify(expr)
                sol = sp.solve(eq, x)
                st.success(f"Solution: {sol}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Simultaneous Equations":
        st.subheader("Solve Simultaneous Equations")
        eq1 = st.text_input("Enter 1st equation (e.g., 2*x + y - 5):")
        eq2 = st.text_input("Enter 2nd equation (e.g., x - y - 1):")
        if st.button("Solve Simultaneous"):
            try:
                x, y = sp.symbols('x y')
                sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
                st.success(f"Solutions: {sol}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Geometry":
        st.subheader("Geometry Calculator (2D & 3D)")
        shape = st.selectbox("Choose a shape", ["Rectangle", "Circle", "Triangle", "Cube", "Cuboid", "Sphere", "Cylinder", "Cone"])

        if shape == "Rectangle":
            l = st.number_input("Length", value=1.0)
            b = st.number_input("Breadth", value=1.0)
            st.info(f"Area = {l*b}, Perimeter = {2*(l+b)}")

        elif shape == "Circle":
            r = st.number_input("Radius", value=1.0)
            st.info(f"Area = {sp.pi*r**2}, Circumference = {2*sp.pi*r}")

        elif shape == "Triangle":
            b = st.number_input("Base", value=1.0)
            h = st.number_input("Height", value=1.0)
            st.info(f"Area = {0.5*b*h}")

        elif shape == "Cube":
            a = st.number_input("Side", value=1.0)
            st.info(f"Surface Area = {6*a**2}, Volume = {a**3}")

        elif shape == "Cuboid":
            l = st.number_input("Length", value=1.0)
            w = st.number_input("Width", value=1.0)
            h = st.number_input("Height", value=1.0)
            st.info(f"Surface Area = {2*(l*w + l*h + w*h)}, Volume = {l*w*h}")

        elif shape == "Sphere":
            r = st.number_input("Radius", value=1.0)
            st.info(f"Surface Area = {4*sp.pi*r**2}, Volume = {(4/3)*sp.pi*r**3}")

        elif shape == "Cylinder":
            r = st.number_input("Radius", value=1.0)
            h = st.number_input("Height", value=1.0)
            st.info(f"Surface Area = {2*sp.pi*r*(r+h)}, Volume = {sp.pi*r**2*h}")

        elif shape == "Cone":
            r = st.number_input("Radius", value=1.0)
            h = st.number_input("Height", value=1.0)
            l = sp.sqrt(r**2 + h**2)
            st.info(f"Surface Area = {sp.pi*r*(r+l)}, Volume = {(1/3)*sp.pi*r**2*h}")

    elif topic == "Calculator":
        st.subheader("Universal Calculator")
        expr = st.text_input("Enter expression:")
        if st.button("Calculate"):
            try:
                expr_fixed = re.sub(r'(\d)(\()', r'\1*\2', expr)
                result = sp.sympify(expr_fixed, evaluate=True)
                st.success(f"Result = {result}")
            except Exception as e:
                st.error(f"Error: {e}")


# -------------------- SENIOR SECONDARY --------------------
if level == "Senior Secondary":
    topic = st.sidebar.selectbox("Choose a Topic", [
        "Quadratic Equations", "Trigonometry", "Calculus",
        "Logarithms & Indices", "Probability", "Matrices", "Geometry", "Calculator"
    ])

    if topic == "Quadratic Equations":
        st.subheader("Quadratic Equation Solver")
        a = st.number_input("Coefficient a", value=1)
        b = st.number_input("Coefficient b", value=0)
        c = st.number_input("Coefficient c", value=0)
        if st.button("Solve Quadratic"):
            x = sp.symbols('x')
            eq = a*x**2 + b*x + c
            solutions = sp.solve(eq, x)
            st.success(f"Solutions: {solutions}")

    elif topic == "Trigonometry":
        st.subheader("Trigonometry Evaluator")
        expr = st.text_input("Enter trig expression (e.g., sin(pi/6) + cos(pi/3)):")
        if st.button("Evaluate Trig"):
            try:
                result = sp.simplify(sp.sympify(expr, evaluate=True))
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Calculus":
        st.subheader("Calculus")
        expr = st.text_input("Enter function in x (e.g., x**3 + 2*x):")
        x = sp.symbols('x')
        if st.button("Differentiate"):
            try:
                diff = sp.diff(sp.sympify(expr), x)
                st.success(f"Derivative: {diff}")
            except Exception as e:
                st.error(f"Error: {e}")
        if st.button("Integrate"):
            try:
                integ = sp.integrate(sp.sympify(expr), x)
                st.success(f"Integral: {integ}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Logarithms & Indices":
        st.subheader("Logarithms & Indices")
        expr = st.text_input("Enter expression (e.g., log(100,10) or 2**5):")
        if st.button("Evaluate Log/Index"):
            try:
                result = sp.simplify(sp.sympify(expr))
                st.success(f"Result: {result}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Probability":
        st.subheader("Probability Calculator")
        favorable = st.number_input("Favorable Outcomes", value=1)
        total = st.number_input("Total Outcomes", value=6)
        if st.button("Calculate Probability"):
            try:
                prob = favorable/total
                st.success(f"Probability = {prob}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Matrices":
        st.subheader("Matrix Calculator")
        matA = st.text_area("Enter Matrix A (rows separated by ;, elements by space) e.g. 1 2;3 4")
        matB = st.text_area("Enter Matrix B (same format)")
        operation = st.selectbox("Choose Operation", ["Add", "Subtract", "Multiply", "Determinant A", "Inverse A"])
        if st.button("Calculate Matrix"):
            try:
                A = sp.Matrix([[int(num) for num in row.split()] for row in matA.split(";")])
                if matB:
                    B = sp.Matrix([[int(num) for num in row.split()] for row in matB.split(";")])
                if operation == "Add":
                    st.success(f"A + B = {A+B}")
                elif operation == "Subtract":
                    st.success(f"A - B = {A-B}")
                elif operation == "Multiply":
                    st.success(f"A * B = {A*B}")
                elif operation == "Determinant A":
                    st.success(f"det(A) = {A.det()}")
                elif operation == "Inverse A":
                    st.success(f"A^(-1) = {A.inv()}")
            except Exception as e:
                st.error(f"Error: {e}")

    elif topic == "Geometry":
        st.subheader("Geometry Calculator")
        shape = st.selectbox("Choose a shape", ["Rectangle", "Circle", "Triangle", "Cube", "Cuboid", "Sphere", "Cylinder", "Cone"])
        # Same 2D & 3D shape handling as JSS Geometry
        if shape == "Rectangle":
            l = st.number_input("Length", value=1.0)
            b = st.number_input("Breadth", value=1.0)
            st.info(f"Area = {l*b}, Perimeter = {2*(l+b)}")

        elif shape == "Circle":
            r = st.number_input("Radius", value=1.0)
            st.info(f"Area = {sp.pi*r**2}, Circumference = {2*sp.pi*r}")

        elif shape == "Triangle":
            b = st.number_input("Base", value=1.0)
            h = st.number_input("Height", value=1.0)
            st.info(f"Area = {0.5*b*h}")

        elif shape == "Cube":
            a = st.number_input("Side", value=1.0)
            st.info(f"Surface Area = {6*a**2}, Volume = {a**3}")

        elif shape == "Cuboid":
            l = st.number_input("Length", value=1.0)
            w = st.number_input("Width", value=1.0)
            h = st.number_input("Height", value=1.0)
            st.info(f"Surface Area = {2*(l*w + l*h + w*h)}, Volume = {l*w*h}")

        elif shape == "Sphere":
            r = st.number_input("Radius", value=1.0)
            st.info(f"Surface Area = {4*sp.pi*r**2}, Volume = {(4/3)*sp.pi*r**3}")

        elif shape == "Cylinder":
            r = st.number_input("Radius", value=1.0)
            h = st.number_input("Height", value=1.0)
            st.info(f"Surface Area = {2*sp.pi*r*(r+h)}, Volume = {sp.pi*r**2*h}")

        elif shape == "Cone":
            r = st.number_input("Radius", value=1.0)
            h = st.number_input("Height", value=1.0)
            l = sp.sqrt(r**2 + h**2)
            st.info(f"Surface Area = {sp.pi*r*(r+l)}, Volume = {(1/3)*sp.pi*r**2*h}")

    elif topic == "Calculator":
        st.subheader("Universal Calculator")
        expr = st.text_input("Enter any expression (e.g., 5*(2+3)/sin(pi/4)):")
        if st.button("Calculate"):
            try:
                expr_fixed = re.sub(r'(\d)(\()', r'\1*\2', expr)
                result = sp.sympify(expr_fixed, evaluate=True)
                st.success(f"Result = {result}")
            except Exception as e:
                st.error(f"Error: {e}")

