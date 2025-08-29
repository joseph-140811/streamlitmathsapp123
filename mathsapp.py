import streamlit as st
import sympy as sp
import numpy as np
import statistics as stats
import math
from authlib.integrations.requests_client import OAuth2Session

# =========================
# AUTH CONFIG (Google & Microsoft)
# =========================
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]
MICROSOFT_CLIENT_ID = st.secrets["MICROSOFT_CLIENT_ID"]
MICROSOFT_CLIENT_SECRET = st.secrets["MICROSOFT_CLIENT_SECRET"]

REDIRECT_URI = "https://mathsapp123.streamlit.app/"

# =========================
# SESSION INIT
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# =========================
# QUERY PARAM HANDLING
# =========================
def set_page(page: str):
    st.query_params["page"] = page

def get_page():
    return st.query_params.get("page", "signup")

page = get_page()

# =========================
# STREAMLIT PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Maths App 123",
    page_icon="📘",
    layout="centered",
)

# =========================
# SIGNUP PAGE
# =========================
if page == "signup":
    st.title("📝 Sign Up for MathsApp123")

    with st.form("signup_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        submit = st.form_submit_button("Sign Up")

        if submit:
            if name and email:
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.success("✅ Sign up successful! Proceed to login.")
                set_page("login")
            else:
                st.error("Please enter both name and email.")

# =========================
# LOGIN PAGE
# =========================
elif page == "login":
    st.title("🔐 Login to MathsApp123")

    if st.button("Login with Google"):
        google = OAuth2Session(
            GOOGLE_CLIENT_ID,
            GOOGLE_CLIENT_SECRET,
            scope="openid email profile",
            redirect_uri=REDIRECT_URI,
        )
        uri, state = google.create_authorization_url(
            "https://accounts.google.com/o/oauth2/auth"
        )
        set_page("auth")
        st.write(f"[Click here to authorize Google]({uri})")

    if st.button("Login with Microsoft"):
        microsoft = OAuth2Session(
            MICROSOFT_CLIENT_ID,
            MICROSOFT_CLIENT_SECRET,
            scope="openid email profile",
            redirect_uri=REDIRECT_URI,
        )
        uri, state = microsoft.create_authorization_url(
            "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
        )
        set_page("auth")
        st.write(f"[Click here to authorize Microsoft]({uri})")

# =========================
# AUTH CALLBACK PAGE (placeholder)
# =========================
elif page == "auth":
    st.title("✅ Authentication Success (Placeholder)")
    st.session_state.logged_in = True
    if st.button("Go to App"):
        set_page("app")

# =========================
# MAIN APP (JSS, SSS, Calculator)
# =========================
elif page == "app":
    # force login check
    if not st.session_state.logged_in:
        st.warning("⚠️ You must log in first.")
        set_page("login")
        st.stop()

    st.title(f"📘 Welcome {st.session_state.user_name or 'Student'}!")
    st.sidebar.title("📚 Topics")

    level = st.sidebar.radio("Select Level", ["JSS", "SSS", "Calculator"])

    # =========================
    # JSS TOPICS
    # =========================
    if level == "JSS":
        topic = st.sidebar.selectbox("Choose a JSS Topic", [
            "Algebra",
            "Trigonometry",
            "Geometry",
            "Statistics",
            "Simultaneous Equations"
        ])

        if topic == "Algebra":
            st.subheader("Algebra")
            expr = st.text_input("Enter an algebraic expression (e.g., 2*x + 3*x - 4)")
            if st.button("Calculate"):
                try:
                    x = sp.symbols("x")
                    result = sp.simplify(expr)
                    st.success(f"Result: {int(result) if result.is_number else result}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif topic == "Trigonometry":
            st.subheader("Trigonometry")
            trig_expr = st.text_input("Enter a trigonometric expression (e.g., sin(30), cos(60))")
            if st.button("Calculate"):
                try:
                    result = eval(trig_expr, {"__builtins__": None}, {
                        "sin": lambda x: round(math.sin(math.radians(x))),
                        "cos": lambda x: round(math.cos(math.radians(x))),
                        "tan": lambda x: round(math.tan(math.radians(x))),
                        "sqrt": math.sqrt
                    })
                    st.success(f"Result: {result}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif topic == "Geometry":
            st.subheader("Geometry")
            shape = st.selectbox("Select Shape", ["Circle", "Rectangle", "Triangle"])
            if shape == "Circle":
                r = st.number_input("Enter radius", min_value=0.0)
                if st.button("Calculate Area"):
                    st.success(f"Area = {round(math.pi * r**2)}")
            elif shape == "Rectangle":
                l = st.number_input("Enter length", min_value=0.0)
                w = st.number_input("Enter width", min_value=0.0)
                if st.button("Calculate Area"):
                    st.success(f"Area = {round(l * w)}")
            elif shape == "Triangle":
                b = st.number_input("Enter base", min_value=0.0)
                h = st.number_input("Enter height", min_value=0.0)
                if st.button("Calculate Area"):
                    st.success(f"Area = {round(0.5 * b * h)}")

        elif topic == "Statistics":
            st.subheader("Statistics")
            nums = st.text_area("Enter numbers separated by commas", "1,2,3,4,5")
            if st.button("Calculate"):
                try:
                    data = [int(x) for x in nums.split(",")]
                    st.write(f"Mean = {stats.mean(data)}")
                    st.write(f"Median = {stats.median(data)}")
                    st.write(f"Mode = {stats.mode(data)}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif topic == "Simultaneous Equations":
            st.subheader("Simultaneous Equations")
            eq1 = st.text_input("Enter first equation (e.g., 2*x + y - 3)")
            eq2 = st.text_input("Enter second equation (e.g., x - y - 1)")
            if st.button("Solve"):
                try:
                    x, y = sp.symbols("x y")
                    sol = sp.solve([sp.sympify(eq1), sp.sympify(eq2)], (x, y))
                    st.success(f"Solution: {sol}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # =========================
    # SSS TOPICS
    # =========================
    elif level == "SSS":
        topic = st.sidebar.selectbox("Choose a SSS Topic", [
            "Differentiation",
            "Integration",
            "Complex Numbers",
            "Matrices"
        ])

        if topic == "Differentiation":
            st.subheader("Differentiation")
            expr = st.text_input("Enter expression to differentiate (e.g., x**2 + 3*x)")
            if st.button("Differentiate"):
                x = sp.symbols("x")
                result = sp.diff(expr, x)
                st.success(f"Result: {result}")

        elif topic == "Integration":
            st.subheader("Integration")
            expr = st.text_input("Enter expression to integrate (e.g., x**2)")
            if st.button("Integrate"):
                x = sp.symbols("x")
                result = sp.integrate(expr, x)
                st.success(f"Result: {result}")

        elif topic == "Complex Numbers":
            st.subheader("Complex Numbers")
            expr = st.text_input("Enter complex expression (e.g., (2+3j)*(1-2j))")
            if st.button("Calculate"):
                try:
                    result = eval(expr)
                    st.success(f"Result: {result}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif topic == "Matrices":
            st.subheader("Matrices")
            st.write("Enter rows separated by semicolon, numbers by space (e.g., '1 2; 3 4')")
            mat_input = st.text_input("Matrix")
            if st.button("Calculate Determinant"):
                try:
                    mat = sp.Matrix([[int(num) for num in row.split()] for row in mat_input.split(";")])
                    det = mat.det()
                    st.success(f"Determinant = {det}")
                except Exception as e:
                    st.error(f"Error: {e}")

    # =========================
    # CALCULATOR
    # =========================
    elif level == "Calculator":
        st.subheader("Calculator")
        expr = st.text_input("Enter expression (e.g., 2+3*4)")
        if st.button("Calculate"):
            try:
                result = eval(expr, {"__builtins__": None}, {"sqrt": math.sqrt})
                st.success(f"Result: {round(result)}")
            except Exception as e:
                st.error(f"Error: {e}")
