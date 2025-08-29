import streamlit as st
import sympy as sp
import numpy as np
import re
from authlib.integrations.requests_client import OAuth2Session

# ===================== CONFIG ======================
GOOGLE_CLIENT_ID = st.secrets["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = st.secrets["GOOGLE_CLIENT_SECRET"]

MICROSOFT_CLIENT_ID = st.secrets["MICROSOFT_CLIENT_ID"]
MICROSOFT_CLIENT_SECRET = st.secrets["MICROSOFT_CLIENT_SECRET"]

REDIRECT_URI = "https://mathsapp123.streamlit.app/"

# ===================== OAUTH PROVIDERS ======================
OAUTH_PROVIDERS = {
    "Google": {
        "authorize_url": "https://accounts.google.com/o/oauth2/auth",
        "token_url": "https://oauth2.googleapis.com/token",
        "scope": "openid email profile"
    },
    "Microsoft": {
        "authorize_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
        "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        "scope": "openid email profile"
    }
}

def get_oauth_client(provider):
    conf = OAUTH_PROVIDERS[provider]
    if provider == "Google":
        client_id, client_secret = GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
    else:
        client_id, client_secret = MICROSOFT_CLIENT_ID, MICROSOFT_CLIENT_SECRET

    return OAuth2Session(
        client_id, client_secret,
        scope=conf["scope"],
        redirect_uri=REDIRECT_URI
    ), conf

# ===================== LOGIN HANDLER ======================
def login_page():
    st.title("🔑 Login to MathsApp123")
    st.write("Please login with Google or Microsoft to continue.")

    provider = st.selectbox("Choose login method:", ["Google", "Microsoft"])
    if st.button(f"Login with {provider}"):
        client, conf = get_oauth_client(provider)
        uri, _ = client.create_authorization_url(conf["authorize_url"])
        st.experimental_set_query_params(auth=provider)
        st.markdown(f"[👉 Continue login here]({uri})")

# ===================== MATHS APP ======================
def maths_app():
    st.sidebar.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #001F3F; /* Mature dark blue */
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.title("📘 MathsApp123")
    level = st.sidebar.radio("Choose Level:", ["Junior Secondary (JSS)", "Senior Secondary (SSS)", "Calculator"])

    if level == "Junior Secondary (JSS)":
        topic = st.sidebar.selectbox("Select Topic:", [
            "Algebra", "Trigonometry", "Geometry", "Statistics", "Simultaneous Equations"
        ])

        if topic == "Algebra":
            expr = st.text_input("Enter an algebraic expression:")
            if st.button("Calculate"):
                try:
                    result = sp.simplify(expr)
                    st.success(f"Result: {result}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif topic == "Trigonometry":
            expr = st.text_input("Enter trig expression (e.g. sin(30), cos(45)):")
            if st.button("Calculate"):
                try:
                    result = sp.sympify(expr, convert_xor=True).evalf()
                    st.success(f"Result: {round(float(result))}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif topic == "Geometry":
            st.write("Geometry tools coming soon...")

        elif topic == "Statistics":
            numbers = st.text_area("Enter numbers separated by commas:")
            if st.button("Calculate"):
                try:
                    nums = [float(x) for x in numbers.split(",")]
                    mean_val = np.mean(nums)
                    st.success(f"Mean: {round(mean_val)}")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif topic == "Simultaneous Equations":
            st.write("Solve system of equations: ax + by = c")
            a = st.number_input("a:", value=1)
            b = st.number_input("b:", value=1)
            c = st.number_input("c:", value=1)
            d = st.number_input("d:", value=1)
            e = st.number_input("e:", value=1)
            f = st.number_input("f:", value=1)

            if st.button("Solve"):
                try:
                    x, y = sp.symbols("x y")
                    sol = sp.solve([a*x+b*y-c, d*x+e*y-f], (x, y))
                    st.success(f"Solution: {sol}")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif level == "Senior Secondary (SSS)":
        topic = st.sidebar.selectbox("Select Topic:", [
            "Algebra", "Trigonometry", "Geometry", "Statistics", "Calculus"
        ])

        if topic == "Calculus":
            expr = st.text_input("Enter function (e.g. x**2):")
            if st.button("Differentiate"):
                try:
                    x = sp.symbols("x")
                    diff_expr = sp.diff(expr, x)
                    st.success(f"Derivative: {diff_expr}")
                except Exception as e:
                    st.error(f"Error: {e}")

    elif level == "Calculator":
        expr = st.text_input("Enter expression:")
        if st.button("Calculate"):
            try:
                result = sp.sympify(expr).evalf()
                st.success(f"Result: {round(float(result))}")
            except Exception as e:
                st.error(f"Error: {e}")

# ===================== MAIN ======================
query_params = st.experimental_get_query_params()

if "auth" not in query_params:
    login_page()
else:
    maths_app()
