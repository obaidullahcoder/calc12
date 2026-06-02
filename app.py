import streamlit as st

# 1. Page Configuration & Custom CSS to match Screenshot (1).png
st.set_page_config(page_title="Online Calculator", page_icon="🧮", layout="centered")

# Custom styling to color buttons and style the calculator frame
st.markdown("""
<style>
    /* Main wrapper to mimic real physical frame */
    div.stMainBlockContainer {
        max-width: 380px !important;
        padding: 20px !important;
        border: 4px solid #0056b3 !important;
        border-radius: 6px !important;
        background-color: #f8f9fa !important;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.15);
    }
    /* Brand header */
    .brand-title {
        text-align: center;
        color: #0056b3;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 10px;
        font-family: Arial, sans-serif;
    }
    /* Display screen container styling */
    .screen-box {
        border: 3px solid #a0a0a0;
        border-radius: 4px;
        background-color: #ffffff;
        padding: 10px;
        text-align: right;
        font-family: monospace;
        margin-bottom: 15px;
    }
    /* Button color overrides */
    div.stButton > button {
        width: 100% !important;
        height: 50px !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    /* Label text formatting */
    .calc-label {
        font-size: 12px;
        color: #888;
        margin-bottom: 5px;
        font-family: Arial, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# 2. Initialize Session State variables to remember numbers across clicks
if "display" not in st.session_state:
    st.session_state.display = "0"
if "equation" not in st.session_state:
    st.session_state.equation = ""
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "reset_next" not in st.session_state:
    st.session_state.reset_next = False

# Helper function to process button inputs
def press(key):
    # Number inputs
    if key in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "00", "."]:
        if st.session_state.display == "0" or st.session_state.reset_next:
            st.session_state.display = "0." if key == "." else key
            st.session_state.reset_next = False
        else:
            if key == "." and "." in st.session_state.display:
                return
            st.session_state.display += key

    # Mathematical operations
    elif key in ["+", "-", "×", "÷"]:
        # Standardize operators for Python's eval engine
        py_op = "*" if key == "×" else "/" if key == "÷" else key
        st.session_state.equation = f"{st.session_state.display} {py_op} "
        st.session_state.reset_next = True

    # Calculate Total
    elif key == "=":
        if st.session_state.equation:
            try:
                full_eq = st.session_state.equation + st.session_state.display
                res = eval(full_eq)
                # Format integer results elegantly
                if isinstance(res, float) and res.is_integer():
                    res = int(res)
                st.session_state.display = str(res)
                st.session_state.equation = ""
                st.session_state.reset_next = True
            except:
                st.session_state.display = "Error"

    # Utility operations
    elif key == "AC":
        st.session_state.display = "0"
        st.session_state.equation = ""
    elif key == "C":
        st.session_state.display = "0"
    elif key == "→":
        if len(st.session_state.display) > 1:
            st.session_state.display = st.session_state.display[:-1]
        else:
            st.session_state.display = "0"
    elif key == "+/-":
        st.session_state.display = str(float(st.session_state.display) * -1)
    elif key == "%":
        st.session_state.display = str(float(st.session_state.display) / 100)
        st.session_state.reset_next = True

    # Memory modules
    elif key == "M+":
        st.session_state.memory += float(st.session_state.display)
        st.session_state.reset_next = True
    elif key == "M-":
        st.session_state.memory -= float(st.session_state.display)
        st.session_state.reset_next = True
    elif key == "MR":
        st.session_state.display = str(st.session_state.memory)
    elif key == "MC":
        st.session_state.memory = 0.0

# 3. Render Calculator Screen Layout
st.markdown('<div class="brand-title">Calculator-1.com</div>', unsafe_allow_html=True)

# Simulated LCD screen
disp_eq = st.session_state.equation if st.session_state.equation else "0"
st.markdown(f"""
<div class="screen-box">
    <div style="font-size: 12px; color: #888;">M1: {st.session_state.memory}</div>
    <div style="font-size: 40px; font-weight: bold; margin: 5px 0; color: #000;">{st.session_state.display}</div>
    <div style="font-size: 12px; color: #aaa;">{disp_eq}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-label">Accounting</div>', unsafe_allow_html=True)

# 4. Building the Layout Grid matching Screenshot (1).png
# Row 1
r1_1, r1_2, r1_3, r1_4, r1_5, r1_6 = st.columns(6)
r1_1.button("MC", on_click=press, args=("MC",))
r1_2.button("MR", on_click=press, args=("MR",))
r1_3.button("M-", on_click=press, args=("M-",))
r1_4.button("M+", on_click=press, args=("M+",))
r1_5.button("√", on_click=press, args=("√",))
r1_6.button("MU", on_click=press, args=("MU",))

# Row 2
r2_1, r2_2, r2_3, r2_4, r2_5, r2_6 = st.columns(6)
r2_1.button("+/-", on_click=press, args=("+/-",))
r2_2.button("7", on_click=press, args=("7",))
r2_3.button("8", on_click=press, args=("8",))
r2_4.button("9", on_click=press, args=("9",))
r2_5.button("÷", on_click=press, args=("÷",))
r2_6.button("%", on_click=press, args=("%",))

# Row 3
r3_1, r3_2, r3_3, r3_4, r3_5, r3_6 = st.columns(6)
r3_1.button("→", on_click=press, args=("→",))
r3_2.button("4", on_click=press, args=("4",))
r3_3.button("5", on_click=press, args=("5",))
r3_4.button("6", on_click=press, args=("6",))
r3_5.button("×", on_click=press, args=("×",))
r3_6.button("-", on_click=press, args=("-",))

# Row 4 & 5 Combined structure
r4_1, r4_2, r4_3, r4_4, r4_5, r4_6 = st.columns(6)
r4_1.button("AC", on_click=press, args=("AC",))
r4_2.button("1", on_click=press, args=("1",))
r4_3.button("2", on_click=press, args=("2",))
r4_4.button("3", on_click=press, args=("3",))

# Notice how the plus and equals occupy vertical slots natively now
r4_5.button("+", on_click=press, args=("+",))
r4_6.button("=", on_click=press, args=("=",))

# Row 5 
r5_1, r5_2, r5_3, r5_4, _, _ = st.columns(6)
r5_1.button("C", on_click=press, args=("C",))
r5_2.button("0", on_click=press, args=("0",))
r5_3.button("00", on_click=press, args=("00",))
r5_4.button(".", on_click=press, args=(".",))

# Footer
st.markdown("""
<div style="display: flex; justify-content: space-between; margin-top: 15px; font-size: 11px; color: #888; font-family: sans-serif;">
    <div>Decimal places - F (<a href="#" style="color:#0056b3; text-decoration:none;">change</a>)</div>
    <div>PC/Mobile</div>
</div>
""", unsafe_allow_html=True)
